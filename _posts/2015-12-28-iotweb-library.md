---
title: IotWeb - An Embedded HTTP/WebSocket Server for Windows 10 IoT
category: tools
cover: 2015/12/28/win10iot.png
---
[Windows 10 IoT Core](https://dev.windows.com/en-us/iot) uses the new *Universal Windows* application model which limits what functionality in the .NET library is available. One of the major missing pieces is [HttpListener](https://msdn.microsoft.com/en-us/library/system.net.httplistener(v=vs.110).aspx), commonly used to provide simple web services in an application. To work around this, and to have something that I can use to target Mono and the *standard* .NET framework as well, I developed the [IotWeb](/pages/tools/iotweb/index.html) library.

![NuGet Installation](/images/tools/iotweb/nuget_install.png)

The library is [available in NuGet](https://www.nuget.org/packages/IotWeb/) and the full source is [on GitHub](https://github.com/sensaura-public/iotweb). The library is released under a [Creative Commons BY-SA](http://creativecommons.org/licenses/by-sa/4.0/) license so you are free to use it in commercial projects as well.

The [project page](/pages/tools/iotweb/index.html) has more information about the library as well as some sample code to get you started, the GitHub repository contains some simple host applications for .NET 4.5 and a Universal Windows application that serve static pages from embedded resources and implement a simple *echo* server over WebSockets.

I am in the process of refactoring the [SensHub server](/pages/senshub/index.html) so I can build a version that targets Windows 10 IoT Core on the Raspberry Pi 2 - the IotWeb library will provide HTTP and WebSocket support for both platforms in a consistant way (as a bonus it provides WebSocket support on Windows 7, something that HttpListener doesn't on that platform). There will be additional libraries needed to complete the process, I will add them to the [tools page](/pages/tools/index.html) as they are done as well.

Hopefully these tools will help speed up your own IoT Core development as well.
