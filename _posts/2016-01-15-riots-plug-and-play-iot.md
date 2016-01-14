---
title: Riots - A Plug and Play IoT System
category: sensnode
cover: 2016/01/15/riots_core.png
---
I recently came across the [Riots](http://www.riots.fi/) plug and play IoT system
that has a lot of similarities to the [SensNode](/pages/sensnode/index.html) design
I've been working on. They have recently launched a [KickStarter campaign](https://www.kickstarter.com/projects/riotsinstruments/riots-aware-for-you?ref=discovery)
and the hardware and software seems to be a lot closer to production ready than
SensNode. Given that the two systems are trying to solve the same problem it
seems worthwhile to do a comparison between the two.

# Architecture

mama + babies vs Hub + Nodes

Separating the core from the sensor.
SensNode also separates the power supply, all Riots devices seem to use a coin cell.

Automatic discovery and addressing.

# Hardware

ATmega vs ARM Cortex-M0

Both use Nordic Semiconductor 2.4GHz wireless. Riots seem to integrate the NRF chip
directly on to the PCB while I still use the module.

Riots boards are a lot smaller and look like they would be difficult to build by
hand. The SensNode boards have more GPIO exposed (? verify).




