---
title: About Sensaura
---
# About Sensaura

The Sensaura platform consists of three inter-related projects - the [SensNode](/pages/sensnode/about.html) hardware
platform, the [SensNet](/pages/sensnet/about.html) NRF24L01+ based networking protocol and [SensHub](/pages/senshub/about.html)
message bus service and rules engine. The components are intended to be used together to provide a customisable remote sensing
implementation for home, office and manufacturing environments.

> The project is currently in the pre-alpha stage of development. at this stage there are some sample circuit designs,
> specifications for the hardware interfaces and very early prototype implementations of the software components. As an
> [open source](http://creativecommons.org/licenses/by-sa/3.0/) project being developed by one person it seemed better
> to start releasing at this early stage to allow people to provide feedback and, hopefully, contribute to the development.

## Design Goals

All elements of the framework are intended to be easily built, modified and extended by makers and hobbyists who may
not have access to professional level or commercial resources. The framework adopts a very modular approach for both
hardware and software components allowing you to concentrate on a single aspect to achieve the desired end result.

### Hardware

The [SensNode](/pages/sensnode/about.html) hardware splits the functionality into three distinct areas - the
[processor board](/pages/sensnode/cpuboard.html) which contains the main CPU and networking functionality, a
[power supply](/pages/sensnode/powerboard.html) and one or more [sensor backpacks](/pages/sensnode/backpack.html) to
perform the actual measurements.

![Module interaction](/images/diagrams/hardware_modules.png)

Building a remote sensor is simply a matter of mixing existing designs with your own customisations. For example -
if you develop a solar power power supply board you can combine that with an existing processor board and environment
sensor backpack to deploy sensors for a garden. If you contribute your designs back to the project we can build up a
library of modules that can be mixed and matched to suit a wide range of sensor requirements.

The SensNode footprint is designed in such a way that the boards can be milled or etched on single sided PCBs at home
and hand soldered with minimal effort (all of the prototypes to date have been built this way). You can also send off
the designs for fabrication if needed.

### Software

Developing software for the SensNode hardware requires the [GCC ARM Embedded Toolchain](https://launchpad.net/gcc-arm-embedded)
(available for Windows, Linux and OS/X) and a sensor project template sets things up for command line compilation using
GNU Make. This allows you to use the editor or IDE of your choice rather than forcing you to use a vendor or platform
specific environment. If you are a big fan of [Eclipse](https://eclipse.org/) there is nothing stopping you from using it, on the other
hand if [vi](http://www.vim.org/) is more to your taste you can use that too.

The [SensNet](/pages/sensnet/about.html) implementation is provided as a [Python](https://www.python.org/) module and
as a .NET Portable Class Library for integration into applications. The [SensHub](/pages/senshub/about.html) server is
implemented in C# and runs on both the official Microsoft .NET framework and [Mono](http://www.mono-project.com/) for
Linux and OS/X systems. The .NET components can be compiled with [Visual Studio 2015 Community Edition](https://www.visualstudio.com/products/visual-studio-community-vs)
or [MonoDevelop](http://www.monodevelop.com/).

## Current State

The project is in the very early stages of development - there are no completed libraries or hardware designs available
at this stage and much of the code base is still being imported from older repositories.
