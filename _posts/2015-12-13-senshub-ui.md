---
title: SensHub UI
category: senshub
cover: 2015/12/13/senshub_plugins.png
---
This weeks update to SensHub is starting to flesh out the UI and RPC interface.

![Plugin Management](/images/2015/12/13/senshub_plugins.png)

Managment of [SensHub]() is done through a web interface, I'm using Google [Material Design](https://www.google.com/design/spec/material-design/introduction.html) for the look and feel. The specific implementation is provided by the excellent *[materialize.css](http://materializecss.com/)* CSS framework along with *[jQuery](https://jquery.com/)* to provide the client side logic.

![Configuration on Mobile](/images/2015/12/13/senshub_config_mobile.png)

As I'm building up the UI I'm taking care to make sure it at least renders in a usable way on mobile devices as well as on the desktop, previous experience has taught me that it's a lot easier to do this at the beginning rather than after the desktop site has been completed - you are less likely to have to go back and refactor large parts of the HTML. The mobile version will not support all the features of the desktop site, the use case for it is more for monitoring and control rather than setting up new rules and actions.

# Object Model

The UI model follows the [server architecture](/senshub/2015/12/04/senshub-architecture.html) where objects in the system are loosely coupled and self describing. Server objects that are displayed to the user implement the *IUserObject* interface which specifies the text and iconography to use when rendering them on a page. If the object can be configured it implements the *IConfigurable* interface to indicate that a properties page can be generated for the object and it's properties can be changed.

The configuration and description information is read from a *metadata.xml* file stored as an embedded resource in the assembly file that implements the plugin. The metadata file also provides support for localisation, allowing display strings to be specified on a per language basis. The file looks like the following:

```xml
<class name="Mqtt.MqttPlugin">
  <!-- MQTT integration support -->
  <description>
    <icon image="mqtt.png"/>
    <displayname lang="en">Mqtt Integration</displayname>
    <shortdescription lang="en">Duplicate SensHub messages on a MQTT server.</shortdescription>
    <longdescription lang="en">
      This plugin allows messages on the SensHub message bus to be replicated on a MQTT server
      and vice-versa. Use of MQTT provides maximum flexibility.
    </longdescription>
  </description>
  <configuration>
    <value name="server" type="StringValue" default="localhost">
      <shortdescription lang="en">MQTT Server Address</shortdescription>
      <longdescription lang="en">
        Set the hostname or the IP address of the MQTT server to connect to.
      </longdescription>
    </value>
    <value name="topic" type="StringValue" default="senshub">
      <shortdescription lang="en">MQTT Topic</shortdescription>
      <longdescription lang="en">
        Any messages posted to the 'public' topic on SensHub will be passed
        to this topic on the MQTT server, incoming messages from the MQTT
        server on the topic will be likewise replicated in SensHub.
      </longdescription>
    </value>
    <value name="identity" type="StringValue" default="">
      <shortdescription lang="en">SensHub Identity</shortdescription>
      <longdescription lang="en">
        The SensHub server will add a '_senshub' field containing this value
        to all messages sent to MQTT, this allows you to identify messages
        that came from SensHub.
      </longdescription>
    </value>
  </configuration>
</class>
```

As well as manipulating existing objects the interface must allow the user to create new objects (such as rules, actions and sources) that are implemented by the plugins. These types of objects are identified by the *IUserCreatable* interface and are associated with a factory class that can create them on the users behalf. Once again the required configuration information (and suitable default values) are provided by the metadata so a suitable property page can be generated without needing to customise the Javascript whenever a new type of object is introduced.

Every user modifiable object in the system is represented by a UUID and kept in the *Master Object Table*. Any changes to the table (new objects created, existing ones updated or removed) are published as messages on the message bus so the UI can update dynamically as these changes occur.

# RPC Interface

There are two main functions of the RPC interface, interfacing with the message bus and manipulating the objects in the system. The RPC implementation uses JSON to describe messages and function calls and can either poll using HTTP POST requests or operate asynchronously over a WebSocket connection. The [HttpListener](https://msdn.microsoft.com/en-us/library/system.net.httplistener(v=vs.110).aspx) class doesn't support WebSockets on all platforms so the polling implementation is required for portability.

The object model makes the RPC interface very simple - creating, removing and manipulating objects can be done with four calls:

**GetConfiguration(objid)**

Retrieve the configuration information for the object with the specific ID. The return value contains a description of the configuration fields for the object as well as the currently applied values.

**SetConfiguration(objid, config)**

Apply the configuration values to the object with the specified ID. If the configuration is accepted this will result in a new message being sent notifying all clients of the update.

**CreateInstance(objid, config)**

Create a new object using the factory specified by the ID with the configuration information provided. The configuration description for the new object can be acquired by calling *GetConfiguration()* with the object ID of the factory.

**RemoveInstance(objid)**

Delete an existing object. Only objects that have been created by the user can be deleted, existing objects such as plugins and factory objects cannot be deleted.

These four functions are all that is needed to manipulate everything in the SensHub system - using them you can create and modify rules, actions and sources. This greatly simplifies the client side implementation as the same techniques can be used for every object with very few special cases.

# User Interface

The user interface uses a lot of template nodes, hidden DIV nodes that describe the layout of various elements in the UI that are cloned, populated with information specific to their use and then inserted into DOM where needed. The function will also replace any text in the format *${name}* with the value of the *name* entry in the passed object.

```javascript
// Create a copy of the node with the given ID
//
// The copy will be given the ID 'newID' and any instances of ${oldID} in the
// content will be renamed as well.
//
// Strings with the format ${name} will be replaced with the value of 'name'
// in the 'vals' object.
function copyTemplate(oldID, newID, vals) {
  var copy = $("#" + oldID).clone();
  copy.attr("id", newID);
  var html = copy.html();
  // Replace variables
  foreach(vals, function(key, value) {
    var re = new RegExp("\\${" + key + "}", "g");
    html = html.replace(re, value);
    });
  // Also replace the ID
  var re = new RegExp("\\${" + oldID + "}", "g");
  html = html.replace(re, newID);
  // Update the copy and return it
  copy.html(html);
  return copy;
  }
```
When displaying a property page for example the configuration description is used to dynamically create a form by inserting the appropriate layout for each field type.

```html
<!-- PaswordValue input -->
<div id="template-PasswordValue" class="col s12 row padding-horizontal-none margin-none">
  <div id="${template-PasswordValue}-current" class="col s12 input-field">
    <i class="material-icons prefix">lock_outline</i>
    <input id="${template-PasswordValue}-current-field" type="password" class="validate">
    <label for="${template-PasswordValue}-current-field">Current password</label>
  </div>
  <div id="${template-PasswordValue}-new" class="col s12 input-field">
    <i class="material-icons prefix">blank</i>
    <input id="${template-PasswordValue}-new-field" type="password" class="validate">
    <label for="${template-PasswordValue}-new-field">New password</label>
  </div>
  <div id="${template-PasswordValue}-verify" class="col s12 input-field">
    <i class="material-icons prefix">blank</i>
    <input id="${template-PasswordValue}-verify-field" type="password" class="validate">
    <label for="${template-PasswordValue}-verify-field">New password (again)</label>
  </div>
  <div id="${template-PasswordValue}-description" class="col s12 italic padding-large">
      ${DetailedDescription}
  </div>
</div>
```
The code above describes the password entry field. As you can see the template allows for descriptive text as well as values to be inserted into relatively complex layouts. The end result can be seen below.

![SensHub Configuration](/images/2015/12/13/senshub_config.png)

Getting the framework in place will make building the rest of the interface relatively simple.

# Next Steps

The user interface and RPC API is progressing nicely, I'm hoping to have basic configuration and object configuration debugged and working smoothly by the end of the coming week with the first simple sources and actions working the week after. I am aiming for a downloadable beta version with enough functionality to be useful to be available in January - so far I'm on track and there are no obvious obstacles in view.
