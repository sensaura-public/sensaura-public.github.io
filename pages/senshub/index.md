---
title: The SensHub Messaging Platform
section: senshub
---
SensHub is a server application that aggregates information from a range of sources and allows you to trigger actions based on the content of that information. Essentially it is a [Rules Engine](https://en.wikipedia.org/wiki/Business_rules_engine) that allows you to respond to external events with customised actions.

> A simple example would be a reminder to turn off lights in unoccupied rooms - using a motion sensor and a light sensor located in a room you can set up a rule that sends a notification to your phone when the following conditions are met:
> 1. The time is between sunset and sunrise.
> 2. There has been no movement in the room for more than 30 minutes.
> 3. The lights in the room are on.
> This example combines information from multiple sources to generate an action when multiple, seemingly unrelated, conditions have been met.

# No Clouds in Sight

Although the SensHub application can interact with cloud based services it does not require any internet based services to function. If you want to you can run the system on a network with no internet connection at all - you will lose access to internet data sources and will be unable to send data to the internet but all internal operations (rules processing, data storage and local notifications) will continue to function.

This was one of the major design goals of the system - it increases security as you get to control what information enters or leaves your network and increases reliability as many functions will continue to work even if your internet connection drops out.

# How It Works

SensHub treats all the data it processes as discrete messages - these messages are attached to a topic to provide categorisation and contain a set of named attributes as their content. The topic model is based on the [MQTT](https://en.wikipedia.org/wiki/MQTT) messaging protocol, SensHub integrates closely with MQTT, and the attribute model is very similar to the Bluetooth LE [GATT](https://en.wikipedia.org/wiki/List_of_Bluetooth_profiles#Generic_Attribute_Profile_.28GATT.29) profile.

![Message Format](TODO)

Message attributes consist of a name and a value where the value is one of a small set of data types - a string, a numeric value or a date and time value. How these values are interpreted is left to the consumer of the message.

Messages enter SensHub through *Sources*, these modules communicate with external services or devices and convert the information they receive into messages. Control and interaction of external services are provided by *Targets* which perform the reverse operation - when they receive a message they convert it into a format suitable for the remote service and pass it along. A basic SensHub installation includes a number of Sources and Targets to integrate with common web services such as [Slack](https://slack.com), [GitHub](https://github.com), [RSS Feeds](https://en.wikipedia.org/wiki/RSS) and generic [WebHooks](https://en.wikipedia.org/wiki/Webhook). Additional services can be added using a plugin API which allows you to write .NET assemblies that will be automatically loaded and made available when the server starts.

![Sources and Targets](TODO)

Every SensHub server also acts as a [MQTT](https://en.wikipedia.org/wiki/MQTT) server which allows messages to enter and leave the system through any MQTT compatible client such as [Node-RED](http://nodered.org/) or by using one of the many open source [MQTT client libraries](https://github.com/mqtt/mqtt.github.io/wiki/libraries).

A lot can be achieved by simply routing messages from a *Source* to a *Target* but for many applications a more versatile mechanism is required. SensHub provides this in two ways;

1. You can write a custom *Target* in the [Lua](http://www.lua.org/) scripting language directly in the web interface. These actions can perform more complex operations on the content of messages, combining values from multiple messages in the decision making process.
2. When routing messages to a *Target* you can set up simple *Filters* that provides basic decision making support. Incoming messages will only be routed to the target if they pass all the requirements specified by the filter. A combination of *Filter* and *Target* is called an *Action* - these are the design making units in the system.

![Actions](TODO)

SensHub will process *Actions* as new messages arrive, checking for any activated *Filters* and routing messages to the appropriate *Targets* as required. This allows you to build up a complex set of rules that react to changes in the environment dynamically with a high degree of customisation.

# Implementation

The SensHub server is written in C# and is designed to run on either the .NET 4.5 framework (including [Mono](http://www.mono-project.com/) on Linux based systems) as well as [Windows 10 Iot Core](https://dev.windows.com/en-us/iot) (with some limitations in functionality).

There are no working releases available at this time - the full source code for the current work in progress is available in the [GitHub Repository](https://github.com/sensaura-public/senshub) and the first external testing will begin in mid-January 2016.  The first public beta releases will be for Windows 10 IoT running on a [Raspberry Pi 2](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/) and should be available by the end of Q1 2016.

Updates and examples will be published to the [blog](/blog/index.html) as regularly as possible.
