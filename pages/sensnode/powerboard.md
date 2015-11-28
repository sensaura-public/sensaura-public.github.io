---
title: Power Board
---
# SensNode Power Interface

To provide flexibility for different deploymet environments the SensNode [processor board](/pages/sensnode/cpuboard.html)
does not have a built in power supply or regulator - it expects external power to be provided by additional circuitry
hosted on a backpack. This allows a range of different solutions to be used depending on the environment the device
will be deployed to.

As well as providing power some power monitoring and user interface features are provided by a power adapter as well.
This includes the *ACTION* button, the *INDICATOR* LED and a battery monitoring analog input.

## Power Interface Header

The power interface uses the 6 pin *POWER* header on the SensNode board. At a minimum a power supply adapter must
provide a regulated 3.3V Vcc source and a ground connection - the simplest implementation of a power board would just
be a regulator circuit.

|Pin|Label    |Description                                     |
|---|---------|------------------------------------------------|
| 1 |Vcc      |3.3V regulated supply. Must support up to 150mA.|
| 2 |GND      |Ground.                                         |
| 3 |Vbat     |Battery level indication - 0 to 3.3V.           |
| 4 |LATCH    |Power latch output, active low.                 |
| 5 |ACTION   |Action button input, active low.                |
| 6 |INDICATOR|Indicator LED output, active high.              |

The power interface is designed to support *push on*/*push off* operation under software control. The *ACTION* button
doubles as the power switch and, when closed, provide power on the Vcc line until it is released.

![TODO: Power On Cycle]()

The firmware will pull the *LATCH* pin low early in the startup process, the power adapter must provide power on Vcc
while the *LATCH* pin remains low. The full power on sequence is shown in the diagram above.

The processor board can switch itself off by raising *LATCH* high. This will be done by the firmware if the user code
calls the [shutdown()](TODO) function, if the battery level falls below a safe value or if the *ACTION* pin is depressed
for more than two seconds.

## User Input and Feedback

The power adapter also provides a minimal user interface through the *ACTION* button and *INDICATOR* LED. This
functionality is implemented in the SensNode library, no user application code is required.

As well as providing power control the *ACTION* button is used to trigger various events;

  * A long (more than two seconds) press on power up forces a reset of any stored configuration and reverts the node
    to it's *factory default* configuration.
  * A short press (less than two seconds) while the device is powered will trigger an update of all attributes to be
    sent to the hub.
  * A long (more than two seconds) press while the device is powered will cause the device to power down.

The *INDICATOR* LED provides simple feedback on errors and network state. This is provided by different flashing cycles.
During normal operation the LED will remain unlit to conserve power.

## Implementation

In general the power supply adapter will be implemented as a separate backpack but it could be integrated with sensor
functionality to form a single board where the size of the final product is a concern.

One of the first battery powered designs consist of a CR2032 battery, a [buck-boost convert](https://en.wikipedia.org/wiki/Buck%E2%80%93boost_converter)
to generate 3.3V, a pushbutton, a LED and a FET circuit to provide latching.
