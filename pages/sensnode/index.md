---
title: The SensNode Hardware Platform
section: sensnode
---
A SensNode is a ARM based processor board with integrated NRF24L01+ wireless networking designed to make it as simple
as possible to build and deploy remote sensors. SensNode consists of a [hardware specification](/pages/sensnode/hardware.html)
and a [software API](/apidocs/sensnode/index.html) that allow a range of devices that adhere to the specific to interact
with each other.

The SensNode hardware splits the functionality into three distinct areas - a [processor board](/pages/sensnode/cpuboard.html) that contains the main CPU and networking functionality, a [power supply](/pages/sensnode/powerboard.html) and one or more [sensor backpacks](/pages/sensnode/backpack.html) to perform the actual measurements.

![Module interaction](/images/diagrams/hardware_modules.png)

Building a remote sensor is simply a matter of mixing existing designs with your own customisations. For example - if you develop a solar power power supply board you can combine that with an existing processor board and environment sensor backpack to deploy sensors for a garden. If you contribute your designs back to the project we can build up a library of modules that can be mixed and matched to suit a wide range of sensor requirements.

## Processor Boards

[Processor boards](/pages/sensnode/cpuboard.html) are the basis of the SensNode system and consist of an ARM CPU, a
NRF24L01+ 2.4GHz RF module and a well defined form factor with expansion headers. Processor boards are not tied
to any manufacturer or model of ARM chip - the current prototypes are built around an EFM32 Cortex-M0 CPU and
additional designs are being built around the XMC1100 and STM32F030 CPUs.

![Processor Board Breakout](/images/photos/sensor_and_breakout.jpg)

For testing and prototyping a simple breakout board design is available which allows the form factor to be used with
any ARM development board that has a pin header interface.

## SensNode API

A [common API](/apidocs/sensnode/index.html) is provided for all target processors which allows for portability across systems. Heavily
influenced by the [Arduino](https://www.arduino.cc/) core library this API provides functions for using GPIO (analog and digital),
SPI, I2C, timing and delays as well as more advanced features available on ARM chips such as real time clock support,
processor sleep modes and automatic wake up on pin change events.

The API is provided as a library and the build system is based on standard GNU tools. Using the template project all
you need to do is define the target processor and start creating your .C or .CPP files in the source directory. You can
use the IDE or text editor of your choice.

Special features or peripherals of the target processor can still be used alongside the library - but this will limit
the portability of your code.

## Networking

The SensNode API includes support for the [SensNet](/pages/sensnet/index.html) protocol and will handle the majority
of network operations in the background without requiring specific application support. Simple define attributes in
your main source file and update them as needed in the application loop;

```cpp
// main.cpp

BEGIN_ATTRIBUTES
  ATTRIBUTE("Temperature", NUMBER, READONLY, AUTO_UPDATE)
  ATTRIBUTE("Humidity", NUMBER, READONLY, AUTO_UPDATE)
  ATTRIBUTE("UV", NUMBER, READONLY, AUTO_UPDATE)
  ATTRIBUTE("Soil", NUMBER, READONLY, AUTO_UPDATE)
END_ATTRIBUTES

/** Application loop
 */
void loop() {
  double value = readTemperature();
  updateAttribute("Temperature", &value);
  value = readHumidity();
  updateAttribute("Humidity", &value);
  // ... etc
  // Sample again in 30 seconds
  sleep(30, SECONDS);
  }
```

The sample code above shows a very simple main loop for a garden sensor. In this case the sensor reads the values from
the hardware sensors and updates the attributes accordingly. The SensNode library will ensure the appropriate updates
are sent over [SensNet](/pages/sensnet/index.html) as well as handling other network operations such as joining the
network, responding to value requests and describing the available attributs to the network controller.
