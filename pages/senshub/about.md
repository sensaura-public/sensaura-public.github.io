---
title: SensHub
section: senshub
---
# SensHub Messaging Platform

The SensHub application is the glue that combines information from sensors and data from external sources.

## Message Bus

The core of SensHub is an internal message bus on which all incoming information and events are published. The bus is
structured around a heirarchial topic tree, similar to a directory structure. A message is published to a topic (such
as *public/sensnet/sensors/garden*) and any *subscribers* to the topic will be notified when the message is sent.

![TODO: Topic Tree]()

The tree is split into two main sections - the *public* tree and the *private* tree. Messages sent to the *public*
tree will be echoed on an external [MQTT](https://en.wikipedia.org/wiki/MQTT) broker - messages received on the MQTT
server will also be reflected on the internal message bus as well.

![TODO: Message Format]()

Messages are represented as dictionaries mapping key names to arbitrary values - internally a [IReadOnlyDictionary](https://msdn.microsoft.com/en-us/library/hh136548(v=vs.110).aspx)
is passed to subscribers. When messages are passed outside the application - to the MQTT broker or through the web interface
for example - they are converted to [JSON](http://www.json.org/) format.

To provide more flexibility
[MQTT](https://en.wikipedia.org/wiki/MQTT)

## Rules Engine

The rules engine allows incoming events and information to be reacted to. A *rule* can be implemented as a plugin or as
a script and can be triggered by messages appearing on one or more topics. Rules may also be triggered on a user specified
schedule.

## Implementation

The current version of the SensHub server is implemented in C# and will run on the .NET runtime on Windows or under
Mono on a Linux or OS/X platform. SensHub is a server application - the host machine is expected to be always on.

The anticipated target hardware is a single board computer with similar capabilities to a [Raspberry Pi](https://www.raspberrypi.org/)
combined with WiFi (802.11g/n) support and an adapter to communicate with the [SensNet](/pages/sensnet/about.html)
network.

Internal testing is being done on a [Raspberry Pi 2](https://www.raspberrypi.org/products/raspberry-pi-2-model-b/)
with the [mosquitto](http://mosquitto.org/) MQTT broker.
