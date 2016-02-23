---
title: The Evolving SensHub Architecture
category: senshub
---
TODO: Lede

When working on a project it's always a good idea to keep an eye on similar systems that are in development or already available - if you spot something that looks like a poor design decision you can avoid it and, more importantly, if you see someone approaching the problem in a different way that can lead to improvements in your own design. I keep a Google alert set up that flags any similar projects mentioned on blogs or any of the big 'Maker' sites which is how I spotted a series of posts about the [JeeLabs JET](TODO: link) system.

The JET server serves a very similar function to what I hope to achieve with [SensHub](TODO: Link) and, from a birds eye view, seems to have a very smiilar architecture - a hub server providing the main connectivity and additional functionality provided by plugins (JET Packs in this case). It also seems to be at a similar level of development - some very basic functionality working but no user interface and a limited set of extensions.

The big difference is that JET uses the underlying MQTT transport for all interactions between the various components. This is one of those 'Why didn't I think of that?' ideas - in hindsight it's an obvious solution that would greatly simplify the implementation of the hub and extensions as well as massivly improve flexibility. I have spent the last month or so prototyping a version of SensHub in Python that uses the same mechanism and results have been impressive.

In the original design for SensHub ([described here](TODO: Link)) the *MessageBus* (a pub/sub message queue with similar semantics to MQTT) was only used for data - measurements from sensors, commands to actuators, etc - and all communication between the extension components and the hub itself was done through direct method calls. This means that extended the functionality required writing a plugin in C# (or some other .NET compatible language) and having the hub run it in the same process.

![TODO: Old vs New]()

The JET design is far more flexible - components can communicate with the hub (and with each other) over MQTT which means as long as they have access to the MQTT server they can run anywhere (in-process, as a separate process or even on a separate physical machine) and be written in any language. This makes extending the system and adding additional functionality far easier and avoids imposing arbitrary limits on the technology used (just because I decided to write the core in C# doesn't mean you should be limited to using that language for your extensions).

In the new design there is no real 'hub' anymore, SensHub is more of a framework that allows components to interact and the hub is simply the machine that provides MQTT and HTTP access to control it. The framework becomes some (relatively) simple code that implements some core design patterns and conventions - that is all that is needed to become a participant in the system. The remainder of this post describes those core elements and how they build on each other to allow a complex distributed system to be built up. The descriptions provided here are brief, I will explore each of them in more detail in future posts as I clean up the Python prototype and refactory the existing C# code to match the new design.

## MQTT Messaging

Overview of [PubSub](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) messaging (MQTT in particular)

Message is a combination of a topic and a payload.
Consumers subscribe to a topic and receive messages sent to it (supports wildcards)
Consumers don't know who sent the message
Multiple consumers can subscribe to the same topic (each gets a copy of the message)
Producers publish messages
Producers don't know how many (if any) subscribers are listening.
Multiple producers can publish to the same topic.

## Topic Naming and Data Format Conventions

Topic Naming
There are two ways to encode context - in the name of the topic or in the payload itself. I refer to these as 'deep' and 'shallow' topics respectively. In the deep topic model the context is encoded in the topic name. Sending a 'stop' message to the datastore service would look like this:

```
{ "action": "stop" } -> senshub/services/control/datastore
```

In the shallow topic model the topic is more generic and the context information is encoded in the message. The equivalent operation would look like this:

```
{ "action": "stop", "data": { "service": "datastore" }} -> senshub/services/control
```

In most cases the deep topic model is a better solution:
In the samples above the datastore service simply has to subscribe to senshub/services/control/datastore and knows that every message it receives is directed at it. In the shallow topic model the payload would have to be inspected to determine if it was the target of the message or not.
Message payloads are smaller and less complex. It also allows custom message content to be passed without having to worry if it will break other receivers.
The SensHub implementation favours the 'deep' topic naming scheme unless there is a specific reason not to.


Every packet in the system is a dictionary structure and is represented as UTF-8 encoded JSON data. The SensHub implementation enforces this and will ignore any messages that are not encoded in this way.
For 'system' messages (that control the interactions between the various components of the SensHub implementation) we use common names at the top level of the dictionary to ensure consistency across packets.

Field
Type
Description
status	boolean	Used to report the status of a requested operation. True for success (or active), False for failure (or inactive)
message	string	Optional additional information for the status. Recommended for negative status reports.
topic	string	If a response is expected for message this field indicates the name of the topic that response should be posted to.
action	string	The action or operation to perform. A service supports 'start' and 'stop' actions for example.
data	any	Context specific data for the request or response. This may be arguments to the action, data to store or query constraints for example

## Status and Acknowledgment

The MQTT messaging model is one way - when a message is published the sender has no idea how many (if any) subscribers received it. It is possible to use Quality of Service (QOS) levels to ensure delivery of messages but this still does not allow for additional status information - eg: the request to perform an action may have been delivered but did the action execute correctly? The obvious solution is to have status information reported back to the sender on a specific topic. In the SensHub implementation if a message on the system topic contains a 'topic' field then a status message must be published to that topic when the operation is complete.

## Remote Procedure Calls

The status reporting pattern can be extended to support an RPC model. In this case we use the 'action' field to indicate the action which should be performed, the 'topic' field to indicate where the status and results should be published and the 'data' field to provide any arguments for the procedure call. Using the 'deep topic' model the topic name specifies the namespace of the procedure call.
TODO: Diagram of a sample call.
In the Python implementation I have written a Mixin and a decorator to allow any Python class to be exported as an RPC namespace. Similar functionality could be implemented in any language that supports introspection such as C# or Java.

## Distributed Object Model

The RPC mechanism can be extended to support a distributed object system by imposing conventions on the actions that can be invoked. Two types of 'objects' are needed - 'instance objects' which represent a collection of actions and attributes and a 'class object' which is capable of creating instances. The SensHub implementation uses 'Plugins' (class objects) and 'Components' (instance objects) for this. A plugin to interact with Twitter would allow you to create multiple instances each of which might be associated with a different account, have different filters to select incoming tweets or a different message template to use for example.
Action
Class
Instance
Description
create	optional	 	Informs the class to create a new instance object with a provided configuration. It is functionality equivalent to a constructor.
destroy	optional	 	The equivalent of a destructor. It informs the class to destroy the a specific instance.
describe	required	required	Provides introspection capabilities, it describes the attributes and actions supported by the object and applies to both classes and instances.
config	required	required	Retrieve the current configuration (the values of all attributes) of an object.
update	required	required	Change the current configuration of an object.

## Broadcasts, Discovery and Events

Split control operations (handling actions, etc) from events (reporting state changes). This allows dynamic monitoring of state without having to explicitly request it.
If possible allow broadcast actions that will apply to all items of a particular type. Eg: Sending 'stop' to senshub/services/control will stop all services, sending 'stop' to senshub/services/control/datastore will just stop the datastore service. Implementations may chose to ignore some actions if they are broadcast rather than directed ('stop' is probably a good example of an action that should be ignored).
Discovery is implemented through broadcasts - the UI will send a 'describe' message to senshub/objects/plugins to determine all available plugins, it can then monitor senshub/objects/events to see as plugins are enabled or disabled from that point on.

## Next Steps

