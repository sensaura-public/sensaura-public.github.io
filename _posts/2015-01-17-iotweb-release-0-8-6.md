---
title: IotWeb 0.8.6 Released
category: tools
---
A new version (0.8.6) of the [IotWeb Library](http://sensaura.org/pages/tools/iotweb/index.html) has been pushed to [NuGet](https://www.nuget.org/packages/IotWeb/). If you are using a previous version please upgrade.

The changes in this version are minimal:

* Changed IServer/ISocket server interface to take the port number as a parameter in the constructor rather than on the *Start()* method. This makes it more generic (and simplifies the integration with [SensHub](http://sensaura.org/pages/senshub/index.html)).
* Added support for sending binary WebSocket frames (requested on Slack).
* Changed filter interface to support before and after filter hooks. This makes it easy to do things like time request handling and perform logging. Also allows for custom HTTP error pages.

There will be some changes required to hosting code. The port number is now specified when the socket server is constructed rather than when it is started, a simple sample of a server hosting embedded content would look like this:

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
            HttpServer server = new HttpServer(8000);
            server.AddHttpRequestHandler(
                "/",
                new HttpResourceHandler(
                    Utilities.GetContainingAssembly(typeof(Program)),
                    "Resources.Site",
                    "index.html"
                    )
                );
            server.Start();
            Console.WriteLine("Server running - press any key to stop.");
            while (!Console.KeyAvailable)
                Thread.Sleep(100);
            Console.ReadKey();
        }
    }
}
```

The filter interface has been extended to support *pre* and *post* handling features.

```C#
public interface IHttpFilter
{
  bool Before(HttpRequest request, HttpResponse response, HttpContext context);

  void After(HttpRequest request, HttpResponse response, HttpContext context);
}
```
The *Before()* method is invoked prior to the request being dispatched to the mapped handler. This will be invoked even if there is no handler associated with the URL. The *After()* method is invoked once the handler has generated the response (in the case of a Websocket upgrade request this is just prior to the upgrade handshake being sent). This allows you to modify the headers both before and after the request handler has been invoked. This can be used to manage sessions, perform request logging and generate custom error pages.

I am working on a set of tutorials for the library, unfortunately it is consuming more time than I originally anticipated so it will be a little while yet before I can post it to the site. I have also replaced the [SensHub](https://github.com/sensaura-public/senshub) internal HTTP server with IotWeb and it is performing nicely with no major bugs discovered yet. A few issues have been raised on the [GitHub project](https://github.com/sensaura-public/iotweb/issues), these will be fixed in the next point release.
