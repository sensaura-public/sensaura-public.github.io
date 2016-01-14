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

Mesh vs Star topology

# Hardware

ATmega vs ARM Cortex-M0. With ATmega they can easily take advantage of the Arduino code libraries.

Both use Nordic Semiconductor 2.4GHz wireless. Riots seem to integrate the NRF chip
directly on to the PCB while I still use the module.

TODO: Image of one of the sensor boards and the core board

Riots boards are a lot smaller and look like they would be difficult to build by
hand. Although photos of the prototypes show different form factors the 3D renders
of what will presumably be the final released boards have a common form factor. 

TODO: Riots core image showing pin outs

Similar amounts of GPIO exposed.

# Software

Where SensNode depends on a hub device running on the local network (a [SensHub](/pages/senshub/index.html)
running on a Raspberry Pi or other server) the Riots system is very dependent on
the cloud for device management and archiving. The [Mama Riots](TODO) seems to
be little more than an Ethernet shield attached to the ATmega core so there is
not a lot of capability for local network processing.

The Sensaura approach is to keep everything in the local network and give the
end user complete control over what (if anything) is sent to the internet. This
means more processing power is required locally but does ensure privacy and
ensures operation even when the internet connection goes down or one is not
available.

# Conclusion

It's interesting to see that someone else has come up with a very similar approach
to the problem that I did. The differences are mainly a matter of focus, familarity
and available resources.

SensNode is being developed in public under an open source license and all the
technical details are available on this site as they are developed. The Riots
system has very little in the way of technical details published to date, the
KickStarter page indicates that hardware designs and source code will be published
in the future.

Depending on a cloud based management interface is not unusual for IoT projects
but I don't believe it is required, it's a little dissapointing to see that Riots
won't work without it. Using the cloud means that the same ATmega core can be
used for the Mama component which simplifies the hardware design. With the cost
of small Linux capable ARM boards dropping rapidly though including a local
hub that can handle data management and configuration locally isn't a huge step
to take.

The amount of money they are trying to raise is a lot lower
than I would have expected - $US 30K doesn't seem like enough to get the
necessary certifications and prepare the product for mass production in 3 months.
I estimated around $AU 750K ($US 520K) and 12 months with a team of 4 people
to make a commercial version of SensNode. Unless they have external funding
and have progressed a lot further preparing for production than is apparent from
their site I don't see how they can have it ready in time with that budget.

There are still 16 days left on the KickStarter as I write this so it will be
interesting to see if they hit the fund raising goal.

Although I'm not contributing to the KickStarter myself I wish them the best of
luck - the more easy to use IoT systems that are available the better as far as
I'm concerned. The first hardware is scheduled for delivery in May 2016, if it
does become generally available I would be interested to see if I can add support
for it in SensHub.
