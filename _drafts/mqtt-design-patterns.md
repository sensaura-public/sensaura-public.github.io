---
title: MQTT Design Patterns
category: senshub
---
## MQTT Messaging

[MQTT](https://en.wikipedia.org/wiki/MQTT) is an implementation of the [Publish/Subscribe pattern](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) with topic based filtering. In essence each message is a combination of a topic and a payload, producers *publish* a topic/payload combination and consumers *subscribe* to a topic to filter the payloads they will receive.

![TODO: Message Transport]()

MQTT uses string based topics in a tree like heirarchy, very similar to a directory structure, that are expressed as a set of names separated by the '/' character (for example - '*senshub/services/datastore*' or '*data/sensors/garage*'). Subscribers may listen to multiple topics either by using wildcards for topic names or by subscribing to multiple individual topics.

The system is very decoupled - when a publisher sends a message it doesn't know how many (if any) subscribers received it, similarly a subscriber doesn't know if anyone is publishing on a topic until it actually receives a message.

## Data Format

Every packet in the system is a dictionary structure and is represented as UTF-8 encoded JSON data. The SensHub implementation enforces this and will ignore any messages that are not encoded in this way.
For 'system' messages (that control the interactions between the various components of the SensHub implementation) we use common names at the top level of the dictionary to ensure consistency across packets.

|Field  |Type   |Description|
|-------|-------|-----------|
|event  |string |Used to report state change events. One of "available", "unavailable" or "updated".|
|status |boolean|Used to report the status of a requested operation. True for success (or active), False for failure (or inactive)|
|message|string |Optional additional information for the status. Recommended for negative status reports.|
|topic  |string |If a response is expected for message this field indicates the name of the topic that response should be posted to.|
|action |string |The action or operation to perform. A service supports 'start' and 'stop' actions for example.|
|data   |any    |Context specific data for the request or response. This may be arguments to the action, data to store or query constraints for example|

## Topic Naming

This section only applies to topics used for component interactions, not the topics used to send or receive sensor (or other) data. The SensHub system uses a single root topic for all system related messages called, rather unimaginatively, 'senshub'. No sensor data should be published to any topic under this root but may be published to any other topic.

There are two ways to encode context - in the name of the topic or in the payload itself. I refer to these as 'deep' and 'shallow' topics respectively. In the deep topic model the context is encoded in the topic name. Sending a 'stop' message to the datastore service would look like this:

```
{ "action": "stop" } -> senshub/services/datastore
```

In the shallow topic model the topic is more generic and the context information is encoded in the message. The equivalent operation would look like this:

```
{ "action": "stop", "data": { "service": "datastore" }} -> senshub/services
```

In most cases the deep topic model is a better solution; a service can subscribe to a single topic and be sure than any message it receives is intended for it, with shallow topics the payload of each message would have to be inspected to determine if it was the target of the message or not. Message payloads are smaller and less complex and allow for custom message content to be passed without having to worry if it will break other subscribers. The SensHub implementation favours the 'deep' topic naming scheme.

### Broadcasting

There are a number of situations where a message should be processed by more than one subscriber while still maintaining separate topics for each implementation. Consider a collection of services that add functionality to the system - each service must be able to be communicated with directly but at the same time we would like to be able to send a query to all services simultaneously to determine which ones are currently running.

To do this the SensHub implementation uses a parent topic broadcast - similar items are grouped under a common parent topic and listen on a unique child topic for direct requests, at the same time they are subscribed to the parent topic and treat requests sent there as applying to them as well. In the services example the topic tree would look like this:

|Topic             |Description|
|------------------|-----------|
|services          |This is the category topic, any messages sent here should be processed by all implementations of the category.|
|services/datastore|This is a specific implementation of the category, it should process messages sent directly to this topic as well as any messages sent to the parent topic.|
|services/zigbee   |Another implementation of the category, it should process messages sent directly to this topic as well as any messages sent to the parent topic.

An implementation is not required to respond to every event sent to the parent topic, the category will define what types of request should be accepted when sent as broadcasts, any others may be ignored.

The main use for broadcast messages is for discovery - it provides an easy mechanism to determine what subscribers are currently available and willing to respond to requests.

### Events

Because new functionality may become available (or become unavailable) after the initial discovery process you would have to either rerun the discovery process periodically or provide a mechanism to changes in state to be announced. In SensHub I use an event reporting model - implementations announce significant events to a commonly named topic that can be monitored to keep the list of available resources up to date.

This model extends the broadcasting model above by adding an 'events' child topic under the category parent and each implementation is required to publish a message when it becomes available, unavailable or it's state has changed. Each event message must contain an 'event' key set to one of "available", "unavailable" or "updated" and an optional 'message' key containing a human readable description of the event.

The topic tree would now look like this:

|Topic                    |Description|
|-------------------------|-----------|
|services                 |The root topic for the category.|
|services/datastore       |A specific implementation of the category.|
|services/events          |Each implementation must publish events to a child topic under this.|
|services/events/datastore|Events for a specific implementation of the category.|

A client may subscribe to the events topic and all it's children ('services/events/#') to monitor all implementations of the category or just a single child topic to monitor a single implementation.

> It will not always be possible for an implementation to report unavailability (due to a server shutdown or network problem for example) so the "available" event should be published periodically even if the implementations state has not changed. This allows clients to infer unavailability if an event has not been received after a certain period of time.

## Message Acknowledgment

When a message is published over MQTT the publisher does not know how many (if any) subscribers received the message. In situations where the message is expected to have side effects we need to know if it was received and acted on so the subscriber needs to publish a status or acknowledgement message that the initial publisher can check for.

There are two ways to do this - the subscriber can publish all acknowledgments to a well known topic or the publisher can specify a unique topic that the subscriber should publish the acknowledgment to. In the first method third parties to the exchange can monitor the acknowledgment topic to determine status changes and react to them as needed but it would require more complex filtering to determine which acknowledgment matches the original request.

In the SensHub implementation I have opted for the later implementation. If an acknowledgment is required the original publisher is required to specify the topic it should be sent to. For each request a unique child topic name is generated under the 'senshub/callback' root and specified in the 'topic' field of the source message. Subscribers that receive the message must publish an acknowledgment containing a 'status' field and may optionally include a 'message' field (containing additional human readable information about the status of the request) and a 'data' field containing additional information resulting from the request.

The procedure for sending a message with an acknowledgment becomes:

1. Generate a unique callback topic name.
2. Subscribe to the callback topic.
3. Publish the request with the 'topic' field set to the callback topic.
4. Wait (with a suitable timeout) for one or more messages to be received on the callback topic.
5. Unsubscribe from the callback topic.

This is a very simple pattern that can be used in a range of different interactions.

## Remote Procedure Calls

A simple RPC (Remote Procedure Call) interface can be built on top of the acknowledgment pattern by imposing some additional naming conventions. By using the topic name as the namespace of the RPC library and requiring that request messages must include an 'action' field that specifies the name of the procedure to invoke we can make a library available to any other participant on the network.

TODO: Diagram of a sample call.

mathLib.calculateAverage(7, 8, 12, 10)

```
{ "action": "calculateAverage", "topic": "senshub/callback/mycallback", "data": [ 7, 8, 12, 10 ] } -> senshub/libraries/mathLib

{ "status": true, "data": 9.25 } -> senshub/callback/mycallback
```

To support basic introspection each library must support a 'describe' action that returns a mapping of the supported procedures along with a simple human readable description of each.

```
{ "action": "describe", "topic": "senshub/callback/mycallback" } -> senshub/services/control/datastore

{ "status": true, "data": { "start": "Start the service", "stop": "Stop the service", "backup": "Back up the database" } }
```

In the Python implementation I have written a Mixin and a decorator to allow any Python class to be exported as an RPC namespace. Similar functionality could be implemented in any language that supports introspection such as C# or Java.

## Distributed Object Model

The RPC mechanism can be extended to support a distributed object system by imposing conventions on the actions that can be invoked. Two types of 'objects' are needed - 'instance objects' which represent a collection of actions and attributes and a 'class object' which is capable of creating instances. The SensHub implementation uses 'Plugins' (class objects) and 'Components' (instance objects) for this.

The are only a handful of defined actions required to implement a simple object model - 3 are mandatory for both classes and instances and two may be optionally implemented by classes.

|Action  |Class   |Instance|Description|
|create  |optional|        |Informs the class to create a new instance object with a provided configuration. It is functionality equivalent to a constructor.|
|destroy |optional|        |The equivalent of a destructor. It informs the class to destroy the a specific instance.|
|describe|required|required|Provides introspection capabilities, it describes the attributes and actions supported by the object.|
|config  |required|required|Retrieve the current configuration (the values of all attributes) of an object.|
|update  |required|required|Change the current configuration of an object.|

If a class does not implement the 'create' and 'destroy' actions it behaves like a static singleton - it may have an associated class level configuration but it cannot be used to create new instances.

The object model must support discovery and state change events - as a result it uses the topic naming model for this functionality that I described earlier in the post.

|Topic           |Description|
|----------------|-----------|
|classes         |The category topic for class implementations.|
|classes/events  |The events topic for class implementations.|
|classes/clsid   |The class specific topic. The CLSID is unique for the class and should be a string representation of a UUID|
|instances       |The category topic for instance implementations.|
|instances/events|The events topic for instance implementations.|
|instances/OBJID |The instance specific topic. The OBJID is unique for the instance and should be a string representation of a UUID|

Both classes and instances must respond to a 'describe' action sent to the category topic, all other actions sent to the category topic must be ignored.

## Next Steps

So far I have prototyped a lot of the functionality described above as a set of Python scripts and managed to build up a minimal hub implementation - that prototype help me codify the patterns and naming conventions but there is still a lot more work to do. I am in the process of cleaning up the prototype and developing it into a cleaner Python library that can be used to build up more complex functionality and I expect that to take a while as the finer details are sorted out.

Although this was a fairly large post it only glossed over the basic details of the patterns, as each piece of functionality is finalised I will cover it in more detailed posts with sample code in C# and Python - hopefully enough for you to be able to start implementing the prototype SensHub server on your own system.
