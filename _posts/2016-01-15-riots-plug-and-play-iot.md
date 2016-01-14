---
title: Riots - A Plug and Play IoT System
category: sensnode
cover: 2016/01/15/riots_core.png
---
I recently came across the [Riots](http://www.riots.fi/) plug and play IoT system that has a lot of similarities to the [SensNode](/pages/sensnode/index.html) design I've been working on. They have recently launched a [KickStarter campaign](https://www.kickstarter.com/projects/riotsinstruments/riots-aware-for-you) and the hardware and software seem to be a lot closer to production ready than SensNode is. Given that the two systems are trying to solve the same problem it seems worthwhile to do a comparison between the two.

# Architecture

The overall architecture of the Riots system is very similar to Sensaura although they use different terminology. Where Sensuara consists of a network of *SensNode* devices connected to a *SensHub* Riots has a set of *Babies* talking to a *Mama*.

![Mama and Babies](/images/2016/01/15/mama_and_babies.png)

Riots uses a [mesh network](https://en.wikipedia.org/wiki/Mesh_network) for communication between the nodes while SensNode is a [star network](https://en.wikipedia.org/wiki/Star_network). This would give the Riots system better communication range at the expense of a more complex network stack implementation.

Like SensNet the configuration of the nodes is automatic and handled by the hub so there is no manual intervention required by the user. I couldn't find any details on the maximum number of nodes that can coexist in the same network or how the devices uniquely identify themselves.

Riots also separates the roles of the hardware components in a similar way to SensNode - there is a core board containing the processor (similar to the SensNode [CPU Board](/pages/sensnode/cpuboard.html)) which is then attached to a sensor board (the SensNode equivalent is a [Backpack](/pages/sensnode/backpack.html)). SensNode goes a step further and puts the power supply on [a separate board](/pages/sensnode/powerboard.html) while Riots uses a coin cell battery for all the sensor boards.

# Hardware

Both SensNode and Riots use a [Nordic Semiconductor 2.4GHz](http://www.nordicsemi.com/eng/Products/2.4GHz-RF) wireless chip to provide network communications. Where SensNode makes use of a premade module the Riots system seems to integrate the chip directly on to the PCB. There are advantages to this but it would make product certification more difficult.

![Riots Core Board](/images/2016/01/15/riots_core.png)

The Riots boards are smaller than the SensNode - 30.8 x 19 mm for the core board and 30.8 x 30.8 mm for the sensors (The [SensNode hardware](/pages/sensnode/hardware.html) is 26 x 45 mm). This makes for more compact sensors but would be more difficult to solder up at home. Photographs of the prototypes show the sensors with different board sizes while the 3D renderings show a consistant size - I assume the final product will match the renderings making it easier to create casings for them.

![Riots Core Pinout](/images/2016/01/15/riots_core_pinout.jpg)

Riots have chosen the ATmega328p as the primary processor and indicate they are using the Arduino library on the system so the exposed GPIO pins closely match the Arduino model. The image above (from the Riots site) shows how they are exposed. I chose to use an ARM chip in the SensNode design (although some prototypes use the same ATmega328p that Riots uses) mainly for cost and availability reasons. Having access to the Arduino tools and libraries would be a benefit though (with the new [boards manager](http://playground.arduino.cc/Main/BoardsManagerSupport) in the Arduino IDE support is no longer restricted to AVR chips so it is still a possibility).

# Software

Where SensNode depends on a hub device running on the local network (a [SensHub](/pages/senshub/index.html) running on a Raspberry Pi or other server) the Riots system is managed using a cloud based service. The [Mama Riots](http://www.riots.fi/p/mama-riots.html) seems to be little more than an Ethernet shield attached to the ATmega core so there is not a lot of capability for local data processing, I assume it would mostly pass data to a REST API running on their servers and do very little actual processing itself.

The Sensaura approach is to keep everything in the local network and give the end user complete control over what (if anything) is sent to the internet. This means more processing power is required locally but does ensure privacy and allows continued operation even when the internet connection goes down or one is not available.

# Conclusion

It's interesting to see that someone else has come up with a very similar approach to the problem that I did. The differences are mainly a matter of focus, familarity and available resources.

SensNode is being developed in public under an open source license and all the technical details are available on this site as they are developed. The Riots system has very little in the way of technical details published to date, the KickStarter page indicates that hardware designs and source code will be published in the future.

Depending on a cloud based management interface is not unusual for IoT projects but I don't believe it is required, it's a little dissapointing to see that Riots won't work without it. I understand the decision though, using the cloud means that the same ATmega core can be used for the Mama component which simplifies the hardware design. With the cost of small Linux capable ARM boards dropping rapidly though including a local hub that can handle data management and configuration locally isn't a huge step to take.

![Core and Base](/images/2016/01/15/core_and_base.png)

The amount of money they are trying to raise is a lot lower than I would have expected - $US 30K doesn't seem like enough to get the necessary certifications and prepare the product for mass production in 3 months. I estimated around $AU 750K ($US 520K) and 12 months with a team of 4 people to make a commercial (mass produced) version of SensNode. Unless they have external funding and have progressed a lot further preparing for production than is apparent from their site I don't see how they can have it ready in time with that budget.

There are still 16 days left on the KickStarter as I write this so it will be interesting to see if they hit the fund raising goal. Although I won't be contributing myself I wish them the best of luck - the more easy to use IoT systems that are available the better as far as I'm concerned. The first hardware is scheduled for delivery in May 2016, if it does become generally available I would be interested to see if I can add support for it in SensHub.
