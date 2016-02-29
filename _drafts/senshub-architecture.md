---
title: The Evolving SensHub Architecture
category: senshub
---
When working on a project it's always a good idea to keep an eye on similar systems that are in development or already available - if you spot something that looks like a poor design decision you can avoid it and, more importantly, if you see someone approaching the problem in a different way that can lead to improvements in your own design. I keep a Google alert set up that flags any similar projects mentioned on blogs or any of the big 'Maker' sites which is how I spotted a series of posts about the [JeeLabs JET](http://jeelabs.org/2016/01/whats-in-a-hub/) system.

The JET server serves a very similar function to what I hope to achieve with [SensHub](TODO: Link) and, from a birds eye view, seems to have a very similar architecture - a hub server providing the main connectivity and additional functionality provided by plugins (JET Packs in this case). It also seems to be at a similar level of development - some very basic functionality working but no user interface and a limited set of extensions.

The big difference is that JET uses the underlying MQTT transport for all interactions between the various components. This is one of those 'Why didn't I think of that?' ideas - in hindsight it's an obvious solution that would greatly simplify the implementation of the hub and extensions as well as massivly improve flexibility. I have spent the last month or so prototyping a version of SensHub in Python that uses the same mechanism and results have been impressive.

In the original design for SensHub ([described here](TODO: Link)) the *MessageBus* (a pub/sub message queue with similar semantics to MQTT) was only used for data - measurements from sensors, commands to actuators, etc - and all communication between the extension components and the hub itself was done through direct method calls. This means that extended the functionality required writing a plugin in C# (or some other .NET compatible language) and having the hub run it in the same process.

![TODO: Original SensHub Architecture]()

The JET design is far more flexible - components communicate with the hub (and with each other) over MQTT which means as long as they have access to the MQTT server they can run anywhere (in-process, as a separate process or even on a separate physical machine) and be written in any language. This makes extending the system and adding additional functionality far easier and avoids imposing arbitrary limits on the technology used (just because I decided to write the core in C# doesn't mean you should be limited to using that language for your extensions).

![TODO: New SensHub Architecture]()

In the new design there is no real 'hub' anymore, SensHub is more of a framework that allows components to interact and the hub is simply the machine that provides MQTT and HTTP access to control it. The framework becomes some (relatively) simple code that implements some core design patterns and conventions - that is all that is needed to become a participant in the system.

TODO: Rewrite this

The remainder of this post describes those core elements and how they build on each other to allow a complex distributed system to be built up. The descriptions provided here are brief, I will explore each of them in more detail in future posts as I clean up the Python prototype and refactory the existing C# code to match the new design.
