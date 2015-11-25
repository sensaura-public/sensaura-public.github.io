---
title: SensNode
section: sensnode
---
# SensNode Hardware Platform

A SensNode is a ARM based processor board with integrated NRF24L01+ wireless networking designed to make it as simple
as possible to build and deploy remote sensors. SensNode consists of a [hardware specification](/pages/sensnode/hardware.html)
and a [software API](/apidocs/sensnode/index.html) that allow a range of devices that adhere to the specific to interact
with each other.

## Processor Boards

The processor boards are the basis of the SensNode system and consist of an ARM CPU, a NRF24L01+ 2.4GHz RF module and
a well defined form factor and expansion headers. Processor boards are not tied to any manufacturer or model of ARM
chip - the current prototypes are built around an EFM32 Cortex-M0 CPU and additional designs are being built around
the XMC1100 and STM32F030 CPUs.

![TODO: Processor Board Breakout]()

For testing and prototyping a simple breakout board design is available which allows the form factor to be used with
any ARM development board that has a pin header interface.

## SensNode API

A common API is provided for all target processors which allows for portability across systems. Heavily influenced by
the [Arduino](https://www.arduino.cc/) core library this API provides functions for using GPIO (analog and digital),
SPI, I2C, timing and delays as well as more advanced features available on ARM chips such as real time clock support,
processor sleep modes and automatic wake up on pin change events.

The API is provided as a library and the build system is based on standard GNU tools. Using the template project all
you need to do is define the target processor and start creating your .C or .CPP files in the source directory. You can
use the IDE or text editor of your choice.

Special features or peripherals of the target processor can still be used alongside the library - but this will limit
the portability of your code.

## Networking

The SensNode API includes support for the [SensNet](/pages/sensnet/about.html) protocol and will handle the majority
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
are sent over [SensNet](/pages/sensnet/about.html) as well as handling other network operations such as joining the
network, responding to value requests and describing the available attributs to the network controller.
