---
title: IoTWeb - An Embedded Web Server
category: senshub
---
After playing with the [Windows 10 IoT Core](https://dev.windows.com/en-us/iot)
on the Raspberry Pi 2 I thought it would be a good platform for the [SensHub](/pages/senshub/about.html)
server so I decided to see what would be required.

# Features and Limitations

HTTP and WebSocket connections. No SSL.
Support for GET and POST methods.
POST content body is limited to 64K.
No Keep-Alive support - every request is served and the connection closed.
Usable on Universal Windows Platform and .NET 4.5 (including Mono).

# Installation

No NuGet packages yet.
Two assemblies - IotWeb.Common and IotWeb.Server
IotWeb.Common is a portable library.
IotWeb.Server is target specific.

Add to your source tree (or use a git submodule).

Very basic server example:

# URL Handlers

Allow you to map a URL to a handler implementation.
Uses 'longest path' mapping. Eg:

/files/ -> File Server
/files/images/ -> Image generator

/files/pdf/ will invoke file server, /files/images/graphs/ will invoke image
generator.

# WebSocket Handlers

Same style of mapping.
WebSockets are long lived - the handler will remain active until the connection
is closed by either side.

# Middleware

Very simple model - middleware gets to modify the request and response objects
before a handler is selected and invoked.

Middleware gets to build a 'context' (a collection of named objects) that gets
passed to handlers.

Uses:

Server side URL rewrites - eg: use 'User-Agent' header to redirect certain URLs
to client specific locations; /client/* becomes /client/ie6/* or /client/chrome/*

Session management. Create and maintain sessions to pass to the handlers through
the context.

