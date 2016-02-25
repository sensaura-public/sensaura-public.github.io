---
title: Displaying Data with Dashboards
category: senshub
---
** Cayenne - https://www.cayenne-mydevices.com/

Mobile App (iPhone only for now - Android 'coming soon'), cloud service and host application running on the Raspberry Pi.

Looks similar to Firmata - controls GPIO directly. Currently no support for external data (via MQTT, Websockets or other protocols).

Nice website though.

** Dashing - http://dashing.io/

Ruby based server side install. Supports 'jobs' for integrating with other services and protocols. MQTT subscriber here - https://gist.github.com/jmb/ac36d16a5180c3d2032a

A bit of a pain to set up unless you have experience with Ruby web apps. Can be deployed to Heroku (and therefore Dokku).

Other benefits - open source, no cloud requirement (can be self hosted).

** Freeboard - https://github.com/Freeboard/freeboard

Nicest solution so far - a dashboard 'engine' as a static HTML page (no server side processing, all display and updates are done on the client). There is also a service to set up dashboards on a service (http://freeboard.io/).
