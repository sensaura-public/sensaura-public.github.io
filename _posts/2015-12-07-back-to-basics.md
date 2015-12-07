---
title: Back to Basics, An ATMega SensNode
category: sensnode
cover: 2015/12/07/atmega_sensnode_sensor.jpg
---
The NRF24L01 modules are still giving me a lot of grief unfortunately, getting
reliable communications with them over the SPI bus is proving far more difficult
than anticipated. As they are a key component of the [SensNode](/pages/sensnode/about.html)
hardware platform I really need to prove that they can be used as designed. It's
time to step back to a *known working* configuration and move forward from there.

![Swim Timer Modules](/images/2015/12/07/swimtimer.jpg)

Some time ago I designed a race timing system for a friends project based
around an ATmega CPU and using the NRF24L01 modules for communication. They
worked well and were regularly used for nearly two years. It was this project
that inspired my choice of the NRF24L01 as the wireless communications module
for SensNode in the first place. I still had a few of the prototypes stored
away so they can be repurposed to test the [SensNet](/pages/sensnet/about.html)
protocol.

I still need a SensNode form factor module to do a complete test of the network
though and that leaves me with a few choices:

1. Continue with the SensNode breakout connected to a development board. I have
   a suspicion that the jumper wire connection between the processor and the
   NRF module is causing most of my problems so I would prefer to eliminate
   those wires to be certain.
2. Build up a ARM based processor board using an EFM32 or XMC110 ARM chip. This
   would be the preferable solution but I don't have the infrastructure in place
   to program either of those chips over a serial bootloader yet - implementing
   this would introduce additional unknowns to the problem.
3. Build up a processor board around a CPU I do have all the infrastructure in
   place to use - the ATmega. Although it feels like a step backwards this is
   most likely the fastest way forward.

Although I've chosen the ARM platform for SensNode hardware designs there is
no reason the API can't be implemented on other CPUs, the minimum requirements
would be at least 16K of flash (the SensNode API and networking stack will
take up about 8K) and a touch under 2K of RAM. The ATmega328p just fits into
these requirements, the biggest risk factor is the amount of RAM available.

The AVR family uses the [Harvard Architecture](https://en.wikipedia.org/wiki/Harvard_architecture)
which has separate address spaces for code (flash memory) and data (RAM). In
practical terms this means constants defined in code (strings or lookup
tables for example) are copied from flash to RAM by the startup code. The
SensNode library implementation does use a number of fairly large (more than
128 bytes) lookup tables. On the ARM chip these stay in flash so they don't
have an impact of the amount of RAM available - on the AVR it's a different
story, the base RAM requirements will be larger.

To cut a long story short this means that although it might be possible to run
a very simple SensNode implementation on the ATmega it may be too limited for
practical purposes. As a prototype for basic testing though it should be sufficient.

![SensNode ATmega PCB](/images/2015/12/07/atmega_sensnode.jpg)

The design I came up with is based around the DIP version of the ATmega328p,
simply because I have some of them available to use immediately. The board
layout is very tight and I simply wasn't able to fit it in the standard
SensNode form factor - it's slightly longer and the NRF module is positioned
differently but it is still pin compatible so sensor and power boards can
be used. Using the TQFP version of the ATmega would simplify the routing
significantly and allow the board to be brought back down to the correct
dimensions. If the ATmega proves to be a reasonable core I will do a redesign
and make it one of the reference implementations - it doesn't hurt to have a
good range of options.

![ATmega Form Factor](/images/2015/12/07/atmega_sensnode_sensor.jpg)

I'm using [Optiboot](https://github.com/Optiboot/optiboot) as the bootloader
on the AVR which means I can simply use [avrdude](http://www.nongnu.org/avrdude/)
to send new firmware to the node. I've configured optiboot to provide a window
of opportunity to enter bootloader mode on every reset avoiding having to route
the *PROG* line from the debug header. A more complete solution would jump
straight to user code if the *PROG* line isn't asserted.

Now I have the hardware in place to verify the NRF communications in general
and the [SensNet](/pages/sensnet/about.html) in particular. Unfortunately
building up and testing hardware takes a lot more time (and requires far more
physical resources) than writing the software does - this part of the project
is progressing at a much slower rate than I would have preferred. With luck
I will have some more positive news to report after next weekends hardware
session.

