# Hello!

Welcome to my page. My name is Gabriel Campbell, a programmer with interests in
web development, graphics programming, instruction sets, and OS development.

## My Interests

I do various hobby projects, some detailed below. These tend to involve
low-level things like CPU architectures or graphics programming in some way. Two
of my biggest projects were the Piculet platform/bytecode, and the platform I'm
currently working on. I've dabbled in many things over time, including OpenGL,
software renderers, game engines, GBA development, compilers, Haskell, and
Python.

## virt

This is a project that I've been working on to create clean & portable virtual
SoC running a new RISC instruction set, with the long-term goal of making an
operating system for it in my own programming language. This is not released yet
but I plan to release it under MIT license when finished.

The last feature that I still plan to design & implement for this system is an
integrated GPU, which you will be able to run via OpenGL or software rendering.
Outside of this last feature, the emulator and assembler are complete. The
compiler for my language is mostly complete but still being improved.

## Piculet

This bytecode was a project that I worked on for several years. I eventually
abandoned it to work on my current instruction set, which performs much faster
and is better designed.

The repo for the project is <a
href="https://github.com/gabecampb/piculet">here</a>. Most importantly, the
platform spec can be downloaded from
<a href="https://github.com/gabecampb/piculet/blob/main/piculet029.pdf">here</a>.

While you can tell some parts of it were designed by an amateur, Piculet was
quite unique (and grand) in what it aimed to do. The goal was to create a
platform that provides built-in, simple-as-possible interfaces for graphics,
audio, networking, and more, through dedicated bytecode instructions. While they
wouldn't be particularly optimized, you could absolutely develop 3D games on top
of Piculet. If Piculet's whole feature set was implemented, you could even do
ray tracing!

## Other Projects

**Kernel** - A WIP kernel for my new ISA. Quite Unix-like so far - eventually I
want to make a simple OS. Written entirely in my own C-like language.

**Zombies Game** - A <a href="zombies">zombie FPS game</a> that I made in
JavaScript and WebGL.

**FreeBuild** - A <a href="https://github.com/gabecampb/freebuild">small 3D game</a>
I made. Didn't spend long on it but still fun to play around with.

<pre style="text-align: center">Make it work, make it right, make it fast.
<a href="cat.jpg">My old cat.</a></pre>
