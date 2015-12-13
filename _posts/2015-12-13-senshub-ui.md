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
<TODO></TODO>
```

As well as manipulating existing objects the interface must allow the user to create new objects (such as rules, actions and sources) that are implemented by the plugins. These types of objects are identified by the *IUserCreatable* interface and are associated with a factory class that can create them on the users behalf. Once again the required configuration information (and suitable default values) are provided by the metadata so a suitable property page can be generated without needing to customise the Javascript whenever a new type of object is introduced.

Every user modifiable object in the system is represented by a UUID and kept in the *Master Object Table*. Any changes to the table (new objects created, existing ones updated or removed) are published as messages on the message bus so the UI can update dynamically as these changes occur.

# RPC Interface

