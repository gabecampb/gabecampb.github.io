## Interpreters with the Efficiency IV Enchantment
#### (Because efficiency V would be JIT.)

This is a generalized description of the tricks that I used to develop a fast
interpreter loop for my emulator, using almost exclusively pure C in order to
stick to architecture-independence.

## Foundations

It is efficient to have an array of function pointers to functions implementing
the execution of each instruction that your instruction set supports. This is
written in C or whatever speedy language you like, although despite having
next-to-no knowledge on the performance of other native languages I'm inclined
to advise you to be wary of anything that doesn't compile nearly 1:1 to assembly
when writing an interpreter, for obvious reasons. Everything is LLVM these days
so it shouldn't matter too much anyway.

Now, let's see how to maximize instructions per second (IPS), relying heavily on
the almighty omnipresence of the compiler Gods.

## Tail those calls

Ideally, all functions called in sequence will take the exact same parameters.
This leaves the compiler open to not needing to resize the stack or to reuse the
stack frame of each function where it can.

The functions that will be called in the longest sequence (a theoretically
_infinite_ one!) will be your instruction functions. Here is where we make use
of TCO (tail call optimization). Calling a function with a type signature
identical to that of the caller at the end of a function, at least when compiler
optimization is enabled, will cause the caller's stack frame to be reused by the
callee (shorter prologue, baby!). And over the course of millions of calls this
adds up to A LOT of time saved. Like, a lot of fucking time. I got like 2.5x
performance boost utilizing this puppy.

At the end of each instruction function I fetch the next instruction, and then
do an indirect call to the next instruction's function by using its opcode as
index into the function pointers array. The PC is incremented during the decode
step, so at the start of each instruction function.

Sometimes compilers can miss TCO, where it shouldn't. Maybe one reason is
because we're technically doing an indirect function call indexed into the
instruction function pointers array, not a direct call (which is an obvious
optimization).

In my experience, GCC never missed the TCO, but Clang has. Which sucks because
in theory I like Clang more. There are compiler mnemonics to make sure that tail
calls are marked as such, although using them in my own emulator would be a
violation of the principles that I developed it under (as close as possible to
pure C, without sacrificing functionality). Alas.

## Pardon the interruption

The CPU has a 'paused' flag, checked after each instruction executes, just
before fetching the next instruction. When an IRQ occurs, 'paused' is set - the
tail call chain is then broken, exiting to the core loop where the reason
'paused' was set is then determined and enter_isr() will be called.

handle_int() will handle updating CPU state to correspond to having a new IRQ.
It is called every time a device wants to trigger a new IRQ, whenever the IRQ
controller config is updated, and whenever the soft IRQ ("trap") instruction is
executed.

enter_isr() will handle actually transitioning into the ISR and updating CPU
state accordingly. This involves pushing reti state, and then updating the PC
and IRQ controller config.

## Do not go into the syscall

System calls are great. Except for when you want to go fast.

Syscalls take some time. They also potentially (as happened in my case) break
the precious TCO. clock_gettime() caused my emulator to slow greatly, even when
the RTC wasn't being queried for the current time. There are also CPU timers
that I needed to implement, so this was an issue.

My code then got dirty. Really dirty. I accessed an x86 register to bypass the
need for this syscall. _I read the TSC._ I had to implement timers somehow.
This is the only place in the codebase that I use something arch-dependent and,
despite the chance of anyone wanting to run on PPC or AArch64 being slim, I
still feel disgusting about it.

## Fetch, boy

The fetch is performed in my emulator using a read_ins() function, which takes
the cpu struct and the address of the instruction to be read, and it returns a
uint32. The read_ins() ONLY reads 4 bytes (to simplify things as much as
possible), and for variable-width instructions I use multiple read_ins() calls.

## Go cache the stick

There is an "I-cache" that allows me skip table walks when reading an
instruction, most of the time. Remember, all of the code that must run
per-instruction is extremely expensive and one or two operations can make a
difference of several million IPS. Many things affect performance when you're
writing high-performance code like this, and to a large extent you are at the
mercy of pipelining and microcode-level decisions that aren't fully aware of,
but **\*generally\*** reducing the ratio of real:interpreted instructions will
get performance closer to where you want it (in _practice_, who knows).

The ins_cache_address within the cpu struct is stored in terms of virtual
address that it starts at, but the cpu.ins_cache array is a pointer to the
physical start of the I-cache, read directly from the virtual RAM (making it not
much of a "cache", more of a hack). If paging is disabled or not supported, it
would obviously be stored in terms of its physical address. An I-cache must
reside wholly on a single virtual page, which is validated at the time a miss
occurs. Anytime TLB flush occurs or the active global PD changes it must be
assumed that the PTE corresponding to the virtual page may have changed, so
doing either of those will invalidate the I-cache.

My I-cache is 256 bytes long, so it's 256-byte aligned. If it's not aligned,
calculations around instruction fetches extending past the end of cache become
significantly more complicated and slow (think: split-page reads), without any
real benefit. Whether you allow misaligned fetches or not, it is just better to
assume that instructions are usually 4-byte aligned. Those that aren't and
extend past the end of I-cache have negligible performance impact and are rather
few and far between.

Originally, my cache miss code was the below, which was really fast.

<pre>if((v_addr >> 8) == (cpu->ins_cache_addr >> 8))
    read from ins_cache at (v_addr & 0xFF)</pre>

However, it had two shortcomings; one is that it didn't check that the I-cache
was validated, and that it didn't handle reading past the end of the 256-byte
long I-cache! Reluctant to add another check, I figured safety is better than
performance and corrected it:

<pre>if(cpu->ins_cache_addr != UINT64_MAX && ((v_addr + 3) >> 8) == (cpu->ins_cache_addr >> 8))
    read from ins_cache at (v_addr & 0xFF)</pre>

I then figured that I could probably find a way to do it with less operations,
so I did like so:

<pre>if(cpu->ins_cache_addr != UINT64_MAX && (v_addr - cpu->ins_cache_addr) < 253)
    read from ins_cache at (v_addr & 0xFF)</pre>

Comparing visually, this is 2 less instructions (2 less bitshifts).

According to Godbolt, this change from the initial corrected code resulted in
several less instructions (14 instead of 17). After compiling with gcc's -O3 I
opened it in Ghidra and was happy to see that it gets reduced to only 8. Oh wow,
so fast.

## If devices had a memory address...

The device registers are mapped at "lowmem" (address 0-4FFFF). When the MMU
write function is called and the virtual address range is < 0x50000, then, an
update_device_regs() function is called which then calls each device's
update-registers function, which checks if there is a new request or information
to process and does work accordingly. This means that having device register
mappings costs us 1 less-than check for writes, and nothing for reads.
Considering reads are much more common than writes, this is not bad at all.

## Ready thready?

Obviously, to be very very fast, we need to make use of multithreading. Each
core is run on its own thread executing the infinite interpreter loop. The main
thread is responsible for handling GLFW stuff and for spawning the` CPU threads.

Without multithreading, every 1000 instructions or so the single do-everything
interpreter loop needs to run an exit check and check for expiry of any set
timers. With multithreading, each CPU thread ONLY runs the interpreter loop. MMU
writes to lowmem will cause device code to run only when requested to do work,
while set CPU timers and the emulator's event polling are run in separate
threads.

## Timing

Each (virtual) CPU has 16 timers. When you start a timer, the CPU thread spawns
a timer thread, which simply calls pthread_cond_timedwait - the conditional
timed wait. If a timer expires (pthread_cond_timedwait returns E_TIMEDOUT), the
associated timer config register's specified IRQ is triggered. If a running
timer is set to a new duration, the condition variable is pthread_cond_signal'd
and the timer thread will exit before a new timer thread is spawned to take its
place.

Having multithreaded timers bypasses the need for the TSC read mentioned
earlier, since we rely on pthread_cond_timedwait instead of periodically
checking the current time and whether or not a set timer has expired (if any are
set). As a downside, this adds a dependence on pthreads.

## Exiting

After beginning the various spawned CPU threads, the main thread runs an
exit check and polls events using glfwPollEvents every 16 ms. The exit check
involves checking if the GLFW window was closed, and also checking the system's
shutdown bit to see whether or not a shutdown was requested. Writes to set the
shutdown bit must be captured and persist eternally in a dedicated variable, due
to the 16 ms delay on processing it possibly allowing it to be set and then
quickly unset. Emulator-specific behaviour should not deny expected behaviour of
the system.

## Results

Fast. Speed. About 250 million IPS on a 2.6 GHz Ryzen 3250U, according to a very
very crude 1-billion iteration loop. Maybe this isn't impressive in comparison
to an interpreter hand-written and tweaked in assembler, but for a pure C
interpreter I believe this is pretty good.

Take everything said in this document with a grain of salt. While everything is
close enough to accurate, none of it is completely technically accurate, which
people in high-performance interpreter development tend to care about. Finally,
if you melt your CPU, I am not to be held responsible.
