# Welcome to my page, where I reserve the right to ramble freely about my unfinished projects.

My name is Gabriel Campbell (<a href="https://github.com/gabecampb">GitHub</a>),
best classified as a systems programmer with interests in graphics programming,
instruction sets, kernels/OS development, game engines, and botany.

As is fairly standard for people with my interests, I am quite interested in
retrocomputing and seeing how low power devices can be pushed to their limits.

## My "Big Thing"

Instruction set architectures are a key interest of mine and I have been
developing an emulator for my own virtual RISC CPU for a while now. This
project's working title is `virt` although I _hope_ that I will eventually be
able to come up with a final title that's a little more interesting. To be able
to develop software on this architecture and really make it its own platform, I
am also developing a kernel for it, in my unoriginal C-like programming language
that I call Pier.

This operating system is attempting to be simple & clean, a good basis for
education while also being capable of being a solid target platform. In what
may otherwise be just another common hobby project, it is set apart by the fact
that it is not being made for x86 or ARM or some other pre-existing architecture.
That said, I am absolutely reinventing the wheel here, just creating my own
metal and rubber for it, too.

While it is written in a systems programming language, it does not
use C as most operating systems do. This has its downsides, and the compiler
that I wrote with the foundation of no experience in compiler design may never
be able to be considered a "decent" compiler, but as long as everything works
they way it should then I am happy. Performance improvements will come later.
As well as a probable compiler rewrite.

Like most hobby OSes, the feature set will be far from being as
sophisticated as something like Linux or Windows. Since the entire system is run
through the emulator, I'm able to easily provide features like a HW-accelerated
GPU via OpenGL on the host machine. In low memory, the CPU has static memory
mappings for accessing the disk, display, and other on-chip devices - the CPU
is really more of an "SoC". While it would be nice at some point, JIT
compilation is not on the roadmap at the moment - the interpreter is fast
enough for my liking on my 2.6 GHz CPU which according to a simple loop test
can run code at about 3 billion IPS (roughly a 300 MHz CPU).

### Naming

Here's the tricky part of the project -- naming the damn thing. There are
various names that I have considered for my virtual CPU, but I honestly have no
idea. I like short names, like Apple's M1, but simply choosing a random letter
and slapping a number on the end seems lame. TBD.

### Release Plans

The code for the emulator, assembler, compiler, and kernel will all be
open-sourced on GitHub when I decide that they are all ready. That is, unless I
can come up with some way to monetize the project and decide to do something
else with it.

## My "Small Things"

I do other things than work on that big project, just not that much. I am very
focused (read: lazy) and nothing stimulates me as much as `virt`. I pretty much
only write in C because OOP is bloat (joke... I just don't like it), although I
have some experience in some other languages including Python and JavaScript,
albeit mostly through university projects. On my GitHub, there is a "fun" little
zombie shooting FPS game that you can play in your browser, which I wrote in
JavaScript and WebGL for a computer graphics course that I took.

I've also created a few software renderers in the past, and a couple of
rudimentary 3D rendering engines in the first couple years I've been programming.
When I was in my second last year of high school, I wrote <a href="Triangles, Step by Step.pdf">this little write-up</a> on how to
render triangles. I think it's a cute little read. I also created over the
course of a few years a bytecode set which was the project which ultimately
led me to what I'm working on now, and for which I wrote a large specification
(something I wish I had for my current project) including a 3D audio API, a
modern graphics API including a custom shader bytecode to GLSL translator,
with ray tracing, compute, and other things. I also wrote a VM for it which
supported the minimum feature set and may or may not be published in the future.

That was a really fun project that I worked on throughout high school and it was the original
target platform for Pier. I eventually abandoned it due to it being poorly designed for
interpreter efficiency and I didn't like how separate it was from how computers
actually work (it didn't even have interrupts!). It would have been suitable for
software development, but not OS development, and I didn't like that. On top of
all this, I started to structure my projects better than I used to, and
refactoring code for a suboptimal project would've been a waste of time.

I have done a few smaller things on the GBA in the past, nothing really of
substance, but I loved working with memory and registers directly, as well as
pushing the slow as heck 16 MHz CPU. All low-level programmers should try
programming the GBA at some point. I hope to work on more projects on the GBA
in the future but for now I don't have much energy outside of working on my
big project, studying, and life stuff.

## End of Page

This is the end of my page. Really, that's it. I will add more here in the
future, allegedly.

<a href="cat.jpg">My old cat.</a>
