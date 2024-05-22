### assembler.mov

Hello! Welcome to my page.

My name is Gabriel Campbell, a programmer with interests in graphics
programming, instruction sets, and OS development.

## My Interests

I do hobby projects, some detailed below. These tend to involve
low-level things like CPU architectures or graphics programming in some way. Two
of my biggest projects were the Piculet platform/bytecode, and the platform I'm
currently working on. I've dabbled in many computer things over time, including
OpenGL, software renderers, game engines, GBA development, compilers, Haskell,
and Python.

Long-time Linux user, yearning for BSD.

## Current Work

I have been working on an emulator for a system that uses my own RISC
instruction set. I'm also working on an OS to run on it, which is implemented
in my own programming language. This is largely just for fun, but I intend to
make some cool software for it eventually as well.

The last feature that I still plan to design & implement for this system is an
integrated GPU, which you will be able to run via OpenGL or software rendering.
The goal for this project was to create a clean & portable SoC emulator using C.

The code for my emulator, assembler, compiler, and kernel will all be
open-sourced on GitHub when I decide that they are ready.

## Piculet

This bytecode was a project that I was working on between September 2018 to
January 2023. I started it while in high school and eventually abandoned it to
work on my current instruction set, which performs much faster and is better
designed.

The repo for the project is <a
href="https://github.com/gabecampb/piculet">here</a>. Most importantly, the
specification of the platform can be downloaded from
<a href="https://github.com/gabecampb/piculet/blob/main/piculet029.pdf">here</a>.

While you can tell some parts of it were designed by an amateur, Piculet was
quite unique (and grand) in what it aimed to do. The goal was to create a
platform that provides built-in, simple-as-possible interfaces for graphics,
audio, networking, and more, through dedicated bytecode instructions. While they
wouldn't be particularly optimized, you could absolutely develop 3D games on top
of Piculet. If Piculet's whole feature set was implemented, you could even do
ray tracing!

## Zombies Game

This was a zombie FPS game which can be played <a href="zombies/index.html">here</a>.
I developed it for a project in a university computer graphics course, and it
entertains for a few minutes.

It has some nice lighting, and basic animations on the zombie models. Tree
leaves wave/deform in the wind by vertex displacement in the vertex shader.

## FreeBuild

This was a <a href="https://github.com/gabecampb/freebuild">fun little project</a>
I did, somewhat of a Roblox clone. It was a side project at the time so I didn't
spend very long on it. Still fun to play around with, despite it being difficult
to build things without a GUI.

## Kernel

I am in the beginning stages of writing a kernel for my new ISA. As I work on
it, I am heavily referencing and copying homework from the Linux kernel. Once it
is mostly up and running, the idea is to make some kind of command-line OS for
it.

This project requires a from-scratch approach, which I find to be a very fun
challenge. There is no C in this kernel, as the only two programming languages
that target my CPU are my assembly language and my C-like programming languages.
Mostly, this language just has tiny changes that I find more pleasant to work
with.

<pre>Imagine there is a cool quote here.
<a href="cat.jpg">My old cat.</a></pre>



