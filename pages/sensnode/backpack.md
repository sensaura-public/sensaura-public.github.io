---
title: SensNode Sensor Boards
section: sensnode
---
Most customisation on a SensNode device will be done by building sensor board (or *back packs*). These boards adhere
to the [SensNode Form Factor](/pages/sensnode/hardware.html) and plug above or below a [processor board](/pages/sensnode/cpuboard.html)
to provide input for the sensor.

![Garden Sensor](/images/photos/garden_sensor.jpg)

The image above shows a typical home made sensor board, in this case one designed for use in a garden to measure light
levels, humidity, temperature and soil moisture. This particular board uses the I2C interface to communicate with the
sensor chips and analog and digital IO to measure the resistance across moisture probes.

## Design Guidelines

This section provides some guidelines to follow when designing sensor boards.

### Power Consumption

All sensor boards must draw their power from the *POWER* header, not the Vcc line on the *DEBUG* header. This pin will
provide up to 150mA of current, the processor will use 20 to 50 mA so sensor boards should limit their maximum current
draw to 100mA or less.

SensNode devices are intended to operate for long periods on a battery supply. As a result power management is an
important consideration - if possible sensors should use the *SLEEP* output on the *GPIO* header to control power to
sensor modules to reduce the amount of current being drawn during low power mode to a minimum.

### Pin Limitations

The SensNode design only provides 5 general purpose pins, 3 of which can be used as analog inputs. If possible sensors
that use I2C or SPI interfaces should be used to reduce pin count requirements. The SPI interface is permanently
available but will require a digital output for the *CS* (chip select) line to each SPI peripheral. The I2C interface
consumes two of the digital IO pins but allows for multiple devices to share the two pins.

IO exanders (such as the MCP23008 or MCP23016) can be used to extend the number of digital IO pins.

### Size Reduction

A SensNode device would normally consist of 3 boards - the [processor](/pages/sensnode/cpuboard.html), a [power adapter](/pages/sensnode/powerboard.html)
and a sensor back pack. The power adapter functionality could be combined with sensors on a single board to reduce the
overall size of the final unit. This may be suitable for specific applications but will limit overall flexibility.
