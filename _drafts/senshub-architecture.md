---
title: SensHub Architecture
category: senshub
---
I pushed a lot of [SensHub](/pages/senshub/about.html) related code to the
[public repository](https://github.com/sensaura-public/senshub) today. This
update includes a plugin framework, the internal HTTP server, MQTT integration
as well as refactoring the messaging system. It's not yet in a state where it
can be used *in the wild* but it is several steps closer to that goal.

The overall architecture is fairly settled now so this seems like a good
opportunity to describe it and cover some of the implementation details.

## Deployment Targets

I have two deployment targets in mind; in a *production* system the SensHub
server will run on a dedicated Linux system with the
[mosquitto](http://mosquitto.org/) MQTT server and [NGINX](https://www.nginx.com/)
HTTP server while a *development* environment would consist of SensHub running
on a desktop machine with the MQTT server located elsewhere on the network and
serving up the web interface itself.

![TODO: Product and Development Deployments]()

The target device for production will be a low power (in terms of processing
and energy), constrained resources device like the [Raspberry Pi](https://www.raspberrypi.org/)
or [CHIP](http://getchip.com/) single board computers.

## Software Architecture

TODO: Overview

### Message Bus

The SensHub server is based around an internal asynchronous message bus that
uses a publish/subscribe model to dispatch messages from their source to anything
that is interested in doing something with them. This internal message bus is
distinct from MQTT, messages on this bus are only visible inside the SensHub
process itself.

Messages on the internal bus are categorised by a *topic* - essentially a path
string - that you can publish to or subscribe to events from. Messages themselves
are just dictionaries - a simple name to value mapping that allows fairly
complex data structures to be transfered from one entity to another without
requiring a shared definition of their content. The interface to the message
bus is fairly simple:

```C#
public interface IMessageBus
{
  /// <summary>
  /// Subscribe to a specific topic.
  ///
  /// Once subscribed any messages sent to the topic (or any of it's
  /// child topics) will be passed to the subscriber instance.
  /// </summary>
  /// <param name="topic">The topic to listen to for messages</param>
  /// <param name="subscriber">The ISubscriber instance to receive messages</param>
  void Subscribe(ITopic topic, ISubscriber subscriber);

  /// <summary>
  /// Unsubscribe from a topic
  ///
  /// If the subscriber is attached to the topic it will be removed and
  /// messages for the topic will no longer be passed to it.
  /// </summary>
  /// <param name="topic">The topic to unsubscribe from</param>
  /// <param name="subscriber">The subscriber to remove</param>
  void Unsubscribe(ITopic topic, ISubscriber subscriber);

  /// <summary>
  /// Unsubscribe from all topics
  ///
  /// This method will remove the subscriber from all topics it is
  /// attached to.
  /// </summary>
  /// <param name="subscriber">The subscriber to remove</param>
  void Unsubscribe(ISubscriber subscriber);

  /// <summary>
  /// Publish a message to the given topic.
  ///
  /// When a message is published it is passed to the specified
  /// topic and all parent topics. Subscribers attached to any
  /// of those topics will be notified that the message has
  /// arrived.
  ///
  /// You may optionally provide a source for the message. If
  /// the source is an ISubscriber instance that would be
  /// triggered by the message the triggering will not occur,
  /// allowing you to ignore messages you send yourself.
  /// </summary>
  /// <param name="topic">The topic to publish to</param>
  /// <param name="message">The message to publish.</param>
  /// <param name="source">The (optional) source of the message.</param>
  void Publish(ITopic topic, Message message, object source = null);
}
```

Publishing a message is simply a matter of getting a reference to the topic,
building a message object and then calling publish. The logging implementation
in the server actually sends *WARN* and *ERROR* messages to the message bus
so they can be used to trigger events, the portion of the code that does
that looks like this:

```C#
MessageBuilder builder = new MessageBuilder()
m_builder.Add("logLevel", logLevel.ToString());
m_builder.Add("source", source);
m_builder.Add("message", message);
IMessageBus messageBus = Locator.Current.GetService<IMessageBus>();
ITopic topic = messageBus.Private.CreateTopic("server/notifications/errors");
messageBus.Publish(topic, builder.CreateMessage());
```

> A note about topics: there is no restriction on how you set up the topic
> topic tree or where you publish messages but SensHub does use a simple
> convention of splitting the tree into two parts - *public* and *private*.
> Any message sent to the *public* part of the tree will be replicated on
> the external MQTT server (and vice-versa, messages coming from MQTT will
> be sent to the *public* tree as well) while messages on the *private* tree
> remain internal to the server. The line in the sample above that reads
> *messageBus.Private.CreateTopic("server/notifications/errors")* creates
> the topic *private/server/notifications/errors*.

Receiving messages is just as simple, get a reference to a topic and call
*Subscribe()* to attach a *ISubscriber* instance to it. Any messages sent to
that topic (or any of it's child topics) will be passed to the subscriber
instance from that point on. The *ISubscriber* interface is also straight
forward:

```C#
public interface ISubscriber
{
  /// <summary>
  /// Invoked when a message arrives on a topic this subscriber is attached to.
  /// </summary>
  /// <param name="topic">The topic the message was sent on</param>
  /// <param name="source">The source of the message. May be null</param>
  /// <param name="message">The message itself</param>
  void MessageReceived(ITopic topic, object source, Message message);
}
```

The *source* referenced in the *MessageReceived()* method (and in the *Publish()*
method on *IMessageBus*) is optional. Internally it is used as a simple filter,
if the *source* attached to the message is equal to the *ISubscriber* the
message will not be dispatched to the subscriber. This allows you to implement
a class the publishes and subscribes to messages on the same topic and avoid
receiving the messages that you publish.

The vast majority of the components in the server implementation simply attach
to the message bus and produce or consume messages. It's really a very simple,
loosly coupled system with a lot of power.

### Plugin Architecture

Passing messages around internally is all well and good but to be useful message
consumers need to be able to interface to the outside world - interact with
web services or control physical devices over Bluetooth, ZigBee or serial port
connections. Rather than attempting to build all possible functionality into
the core server (and requiring a recompile and redeploy everytime something
new is added) I wanted a way to allow plugins to be added - simply drop the
plugin implementation into the right directory and the server will pick it
up and start using it.

Because C# has full support for dynamic loading of code and run time type
information this was not that difficult to achieve. The SensHub API defines
two interfaces to support this, *IPluginHost* provides limited access to the
server internals and *IPlugin* lets the server control the plugin life cycle.

The *IPlugin* interface looks like this:

```C#
public interface IPlugin
{
  /// <summary>
  /// The UUID that uniquely identifies this plugin. This value is used to
  /// provide a unique reference for the plugin and determines where configuration
  /// and associated data files for the plugin as stored. The UUID must remain
  /// constant across different versions of the plugin.
  /// </summary>
  Guid UUID { get; }

  /// <summary>
  /// The version of this plugin. The version information is only used
  /// for display purposes, no checking or validation is done on the value.
  /// </summary>
  Version Version { get; }

  /// <summary>
  /// Initialise the plugin.
  ///
  /// Every plugin must have a default constructor but no meaningful
  /// initialisation should be done there. This initialisation function
  /// is passed a <see cref="IPluginHost"/> instance which allows the
  /// plugin to interact with the SensHub server.
  /// </summary>
  /// <param name="host">
  /// An instance of IPluginHost that the plugin uses to interact with
  /// host services. The plugin should keep a reference to this instance
  /// for use later in it's lifetime.
  /// </param>
  /// <returns>true on success, false on failure.</returns>
  bool Initialise(IPluginHost host);

  /// <summary>
  /// Shut down the plugin.
  ///
  /// When this method is invoked the plugin must unregister all
  /// extensions, ensure any cached data is saved and revert to
  /// an inactive state.
  /// </summary>
  void Shutdown();
}
```

The *IPluginHost* is a little more complex (and still being expanded) so I
won't provide details about it here. Essentially it provides access to the
message bus and methods to manage configuration files, store and retreive
data and some user interface related functions.

All plugins are independent of each other - one plugin is not aware of any
others and can have no effect on their operation. The only possible way to for
plugins to communicate is over the message bus and even then you have no way
of knowing if anyone was listening for messages you send anyway.

TODO: Internal Plugins

TODO: External Plugins

## User Interface

## Next Steps

