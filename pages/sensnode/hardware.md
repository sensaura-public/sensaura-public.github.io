---
title: Hardware Specification
---
# SensNode Hardware Specification

A SensNode device must adhere to this hardware specification to provide interoperability between components. The specification
consists of a PCB form factor, pin headers and electrical characteristics.


## Form Factor

The form factor specifies the size of the PCB and the location of the headers.

![PCB Form Factor](/images/diagrams/sensnode_form_factor.png)

The size of the PCB is designed to be small enough to easily deploy but large enough that it can be built by hand with
relative ease. A SensNode (and associated back pack boards) can be etched or milled as single sided PCBs as well as
being fabricated as multiple layer boards. The design uses 0.1" (2.54mm) pitch headers which allows the PCB to be used
on a breadboard during development and debugging.

All inputs and output operate at 3.3V levels, interacting with 5V level components will require a level convertor. Analog
inputs use the 3.3V Vcc line as the reference voltage, inputs must be scaled accordingly.

![SensNode Breakout](/images/photos/breakout_board.jpg)

A final SensNode sensor will consist of two or more boards stacked together. The headers on a [processor board](/pages/sensnode/cpuboard.html)
should provide both male and female header connections to allow this stacking. The design uses 6 and 8 pin headers so
readily available Arduino style stackable headers can be used. The image above shows a SensNode breakout board, this
is designed to connect to a development kit or prototype circuit and allow the use of SensNode compatible power or sensor
boards.

### Power Header

The *POWER* header provides the primary power source for the board. A [power adapter](/pages/sensnode/powerboard.html) provides
the voltage, all other boards are consumers.

|Pin|Label    |Description                                     |
|---|---------|------------------------------------------------|
| 1 |Vcc      |3.3V regulated supply. Must support up to 150mA.|
| 2 |GND      |Ground.                                         |
| 3 |Vbat     |Battery level indication - 0 to 3.3V.           |
| 4 |LATCH    |Power latch output, active low.                 |
| 5 |ACTION   |Action button input, active low.                |
| 6 |INDICATOR|Indicator LED output, active high.              |

### Debug Header

The *DEBUG* header provides a serial interface to the processor as well as control pins to reset the device and enter
programming mode.

|Pin|Label    |Description                                     |
|---|---------|------------------------------------------------|
| 1 |Vcc      |3.3V regulated supply.                          |
| 2 |GND      |Ground.                                         |
| 3 |TX       |UART TX line (from processor)                   |
| 4 |RX       |UART RX line (to processor)                     |
| 5 |PROG     |Programming mode request, active high.          |
| 6 |RESET    |CPU reset line, active low.                     |

As different manufacturers provide different methods of entering bootloader mode on start up this interface defines
a generic interface. If the *PROG* input is held high while the processor powers up (or comes out of reset) it will
enter serial bootloader mode. Discrete circuitry on the processor board itself will trigger the processor specific
entry conditions from these inputs.

As entering bootloader mode requires the processor to reset which will unlatch the power supply the debug interface
allows for power to be provided by an alternative method. If the Vcc pin goes low when the processor is reset the
programming tool should provide a 3.3V regulated voltage on the Vcc pin to allow for programming to continue.

The serial interface pins (TX, RX and GND) may be used to interface with serial peripherals as well. When designing
these interfaces care should be taken to ensure no communication occurs while the *PROG* pin is high.

### GPIO Header

The *GPIO* header provides the primary interface for sensor boards and external peripherals. It consists of a SPI
interface and a collection of user configurable pins supporting I2C, digital IO and analog input.

|Pin|Label|Alt Function|Description                                                    |
|---|-----|------------|---------------------------------------------------------------|
| 1 |MOSI |-           |SPI Master Out/Slave In                                        |
| 2 |MISO |-           |SPI Master In/Slave Out                                        |
| 3 |SCK  |-           |SPI Clock                                                      |
| 4 |PIN0 |SCL         |Digital input, digital output or I2C clock.                    |
| 5 |PIN1 |SDA         |Digital input, digital output or I2C data.                     |
| 6 |PIN2 |Analog      |Digital input, digital output or analog input.                 |
| 7 |PIN3 |Analog      |Digital input, digital output or analog input.                 |
| 8 |PIN4 |Analog/Sleep|Digital input, digital output, analog input or sleep indicator.|

The SPI bus is used to communicate with the built in NRF24L01+ module and the function of those pins cannot be changed.
They may be used to communicate with other SPI devices from user application code.

The I2C pins do not have pull up resistors, a sensor board containing I2C devices must proide it's own pull ups.

Analog input pins use Vcc (3.3V) as the reference voltage. Any inputs must be scaled to a maximum 3.3V level when these
pins are configured for analog sampling.

The firmware allows for *PIN4* to be configured as a sleep indication pin. When this functionality is enabled the pin
will be held high while the processor is in running mode and will be pulled low when the processor enters sleep or
low power mode. Sensor boards may use this to control power to external peripherals.
