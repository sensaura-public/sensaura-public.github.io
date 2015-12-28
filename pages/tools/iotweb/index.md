---
title: IotWeb HTTP Server
section: tools
---
The IotWeb class library allows you to embed a simple HTTP and WebSocket server into your C# application. The library supports both the .NET 4.5 framework as well as the Universal Windows Platform allowing you to target [Mono](http://www.mono-project.com/), Windows Desktop and [Windows 10 IoT Core](https://dev.windows.com/en-us/iot).

> **TLDR Summary**
>
> Don't want to read the entire page? No problem; here are some quick links to get you started:
>
> 1. The library is released under the [Creative Commons BY-SA license](http://creativecommons.org/licenses/by-sa/4.0/) - this means you can use the library in commercial and non-commercial projects as long as you provide attribution (a link to this page will be fine) and release any changes you make under the same license.
> 2. The full source code is [available on GitHub](https://github.com/sensaura-public/iotweb), please raise any bug reports or feature requests on the [issues page](https://github.com/sensaura-public/iotweb/issues) for the project.
> 3. You can install the library [using NuGet](https://www.nuget.org/packages/IotWeb/). Be aware that the NuGet package will lag behind the source repository, only stable updates will be released.
> 4. For help, examples and discussions you can join the [Sensaura Slack Team](https://sensaura.slack.com/) (get your [invitation here](https://docs.google.com/forms/d/1PTCu0A5u7OZh136BmPCS3jx0VPoCGIwvEc2fYyVhNYQ/viewform)) and jump in to the #iotweb channel. The repository includes a simple WebSocket echo server implementation for [.NET 4.5](https://github.com/sensaura-public/iotweb/tree/master/WebHost%20Desktop) and the [Universal Windows Platform](TODO). Tutorials and examples will also be posted to the [Sensaura Blog](/blog/index.html).

# Design Goals

This server is designed for use in an IoT or embedded device without a local display. The goal was to make it easy to implement a simple remote management interface or provide a REST or RPC based API for use by a companion application running on mobile or desktop.

A common usage scenario would be as follows:

1. Serve a set of static files (HTML, CSS and Javascript) to provide the client side UI.
2. Provide a REST or RPC based interface using JSON formatted data to interact with the system.
3. Implement the API calls in Javascript on the client side and update the HTML UI accordingly.

This results in a short burst of activity as the page is loaded and the initial static assets are transferred to the browser followed by a larger number of small transactions as API calls are made or updates are sent over WebSockets.

# Features and Limitations

Many of the features you would find in a full web server implementation are not available in this library - it provides a simple framework for you to build on to implement exactly what you need for your application.

## Features

1. Supports HTTP 1.1 and WebSockets 13 ( [RFC6455](https://tools.ietf.org/html/rfc6455)).
2. Provides a simple URL routing mechanism modelled on [web.py](http://webpy.org/).
3. Provides a simple request filtering mechanism to implement middleware operations.
4. A simple HttpRequestHandler implementation is provided that will serve static files from embedded resources in an assembly.

## Limitations

1. No support for secure protocols such as HTTPS or WSS.
2. All IO is cached in memory; inbound data (POST content and WebSocket packets) is limited to 64K and the maximum size of served content is limited to the amount of available RAM.
3. Persistant connections are not supported, each request is treated as a single transaction and the connection will be closed once it has been fulfilled.

# Architecture

The library consists of two assemblies;

1. IotWeb.Common is a Portable Class Library that provides the common interfaces and implementation of the HTTP and WebSocket server. This assembly also includes some utility classes and methods to help deal with the differences in functionality across the various platform runtimes.
2. IotWeb.Server is a platform specific assembly that provides the actual interface between IotWeb.Common and the target platform. There are two versions of this assembly - one for the NET 4.5 Framework which can be used on Mono and Windows 7 or above, the other for the Universal Windows Platform that can be used on the Windows 10 IoT Core platform or in Windows Store applications.

When you install the library with NuGet the appropriate package will be installed for your target architecture, if you are building from source you will have to reference the appropriate version of IotWeb.Server in your solution.

# Installation

The simplest way to install the component is to use the [NuGet package](https://www.nuget.org/packages/IotWeb/) using the [Package Manager Console](http://docs.nuget.org/consume/package-manager-console) or through the *Manage NuGet Packages* options on your project.

![Installing With NuGet](/images/tools/iotweb/nuget_install.png)

The version available on NuGet will be slightly older than the version available in GitHub but will be more stable and include less experimental or new features.

# A Simple Example

The code snippet below shows a very simple server that provides static files from embedded resources in the application.

```C#
using System;
using System.Threading;
using IotWeb.Server;
using IotWeb.Common.Util;
using IotWeb.Common.Http;

namespace MyProgram
{
    class Program
    {
        static void Main(string[] args)
        {
            // Set up and run the server
            HttpServer server = new HttpServer();
            server.AddHttpRequestHandler(
                "/",
                new HttpResourceHandler(
                    Utilities.GetContainingAssembly(typeof(Program)),
                    "Resources.Site",
                    "index.html"
                    )
                );
            server.Start(8000);
            Console.WriteLine("Server running - press any key to stop.");
            while (!Console.KeyAvailable)
                Thread.Sleep(100);
            Console.ReadKey();
        }
    }
}
```

# More Information

All the code is available in the [GitHub repository](https://github.com/sensaura-public/iotweb), that is the best place to look for more details. If you come across any bugs or would like new features added please [raise an issue](https://github.com/sensaura-public/iotweb/issues) there.

The [Sensaura Slack Team](https://sensaura.slack.com/) has a #iotweb channel devoted to discussion of the library. You will need an invitation to join the team, simply [fill out this form](https://docs.google.com/forms/d/1PTCu0A5u7OZh136BmPCS3jx0VPoCGIwvEc2fYyVhNYQ/viewform) and one will automatically be sent to you.

If you use the library in your projects please let everyone know on Slack or in the comments section below.

