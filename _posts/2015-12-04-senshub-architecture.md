---
title: SensHub Architecture
category: senshub
cover: covers/coding.png
---
I pushed a lot of [SensHub](/pages/senshub/index.html) related code to the
[public repository](https://github.com/sensaura-public/senshub) today. This
update includes a plugin framework, the internal HTTP server, MQTT integration
as well as refactoring the messaging system. It's not yet in a state where it
can be used *in the wild* but it is several steps closer to that goal. The
overall architecture is fairly settled now so this seems like a good
opportunity to describe it and cover some of the implementation details.

## Deployment Targets

I have two deployment targets in mind; in a *production* system the SensHub
server will run on a dedicated Linux system with the
[mosquitto](http://mosquitto.org/) MQTT server and [NGINX](https://www.nginx.com/)
HTTP server while a *development* environment would consist of SensHub running
on a desktop machine with the MQTT server located elsewhere on the network and
serving up the web interface itself.

The target device for production will be a low power (in terms of processing
and energy), constrained resources device like the [Raspberry Pi](https://www.raspberrypi.org/)
or [CHIP](http://getchip.com/) single board computers. This means that some
care has to be taken to reduce the amount of memory and processing power the server
requires. As a result I've tried to keep the implementation as simple as possible
and have been careful about external dependencies.

## Software Architecture

There are two core parts to the SensHub server - the message bus that is used
to distribute messages and events between the components and the plugin system
that allows external components to add additional sources and actions for those
messages.

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

The server doesn't impose any restriction on how you set up the topic
topic tree or where you publish messages to but it does use a simple
convention of splitting the tree into two parts - *public* and *private*.
Any message sent to the *public* part of the tree will be replicated on
the external MQTT server (and vice-versa, messages coming from MQTT will
be sent to the *public* tree as well) while messages on the *private* tree
remain internal to the server. The line in the sample above that reads
*messageBus.Private.CreateTopic("server/notifications/errors")* creates
the topic *private/server/notifications/errors*.

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

External plugins are simply .NET assemblies compiled to a DLL and placed in
the servers *plugins* directory. On start up the server simply inspects each
DLL searching for any classes that implement *IPlugin*; any that are found
are instantiated, the assembly queried for some additional metadata about the
plugin and then they are added to the list of available plugins.

The plugin loading code is shown below, this snippet is part of a loop which
inspects each DLL file in turn:

```C#
// Load the assembly
Assembly asm = null;
try
{
  this.Log().Debug("Attempting to load '{0}'", pluginDLL);
  asm = Assembly.LoadFile(pluginDLL);
}
catch (Exception ex)
{
    this.Log().Error("Failed to load assembly from file '{0}' - {1}", pluginDLL, ex.ToString());
    continue;
}
// Get the plugins defined in the file (it can have more than one)
Type[] types = null;
try
{
  types = asm.GetTypes();
}
catch (Exception ex)
{
    // TODO: an exception here indicates a plugin built against a different version
    //       of the API. Should report it as such.
    this.Log().Error("Failed to load assembly from file '{0}' - {1}", pluginDLL, ex.ToString());
    continue;
}
// Load metadata from the assembly
metadata.LoadFromAssembly(asm);
// Look for plugins
foreach (var candidate in types)
{
  if (typeof(IPlugin).IsAssignableFrom(candidate))
  {
    // Make sure we have metadata available
    if (metadata.GetDescription(candidate) == null)
    {
      this.Log().Warn("Plugin '{0}.{1}' does not provide a description.", candidate.Namespace, candidate.Name);
      continue;
    }
    if (typeof(IConfigurable).IsAssignableFrom(candidate) && (metadata.GetConfiguration(candidate) == null))
    {
      this.Log().Warn("Plugin '{0}.{1}' is marked as configurable but does not provide a configuration description.", candidate.Namespace, candidate.Name);
      continue;
    }
    // Go ahead and try to load it
    try
    {
      this.Log().Debug("Creating plugin '{0}.{1}'", candidate.Namespace, candidate.Name);
      Object instance = Activator.CreateInstance(candidate);
      AddPlugin((IPlugin)instance);
    }
    catch (Exception ex)
    {
      this.Log().Error("Unable to create plugin with class '{0}' in extension '{1}' - {2}",
        candidate.Name,
        pluginDLL,
        ex.ToString()
        );
      continue;
    }
  }
}
```

The metadata mentioned in the code above is some additional information about
the plugin - mainly localised strings for its description and configuration
information. This is just an XML file stored as an embedded resource in the
DLL with a standard name.

A lot of the core functionality, such as the MQTT integration, is implemented
using the plugin system as well - these are simply added to the list of available
plugins manually rather than being automatically discovered. The only difference
between these built-in plugins and the external ones is that they have access
to more of the server internals because they are part of the same assembly.

The plugin system makes it easier to add extra functionality to SensHub without
having to modify the server source code directly. The plugin API is separated
out into it's own assembly (you can [see the source here](https://github.com/sensaura-public/senshub/tree/master/SensHub%20API)); a plugin
project simply needs to reference that assembly and the [Splat](https://github.com/paulcbetts/splat)
library (used for logging, service discovery and some other cross platform
functionality) to be able to work with the server.

## Next Steps

I'm pretty happy with the progress made in the past week, I'm hoping to have
some basic rules and actions working soon. I'm using a simple [Slack](https://slack.com/)
integration as the first external plugin, it just takes messages arriving on the
topic it's attached to and sends it to a specified channel in your Slack team.
Getting that to work will be a good test of the overall architecture.

Now that it's the weekend again though it's time to switch focus to hardware
while I have access to my equipment. Hopefully I will have an update related
to that in the next few days.
