---
title: Silicon Labs Low Power Design Competition
category: sensnode
cover: photos/zero_gecko_prototype.jpg
---
A few months ago I found out about a [Low Power Contest](http://community.silabs.com/t5/Contests/Low-Power-Contest/m-p/153186#U153186)
being run by [Silicon Labs](http://www.silabs.com/Pages/default.aspx). The [SensNode](/pages/sensnode/index.html) hardware
seemed a good candidate so I submitted an outline to the first phase of the competition which was simply looking for
ideas. In return Silicon Labs sent me a [EFM32 Zero Gecko Starter Kit](https://www.silabs.com/products/mcu/lowpower/Pages/efm32zg-stk3200.aspx)
so I moved on to the next stage, prototyping a SensNode board with the starter kit acting as the processor.

![Zero Gecko Breakout](/images/photos/zero_gecko_prototype.jpg)

My [entry is now submitted](http://community.silabs.com/t5/Projects/Low-Power-Contest-2015-Wireless-Sensor-Platform/m-p/158364) but unfortunately it was not entirely complete. You can read the actual
submission for more details but it boiled down to a lot of problems maintaining reliable communications with the NRF24L01+
module on the breakout board. These modules seem very sensitive to noise on the SPI bus, when the connecting tracks are
fairly short (such as when the CPU and the module are on the same PCB) this isn't really an issue but with the jumper
cables involved to connect the breakout board to the Gecko development kit it becomes difficult to communicate with
the module.

![Garden Sensor](/images/photos/garden_sensor.jpg)

It was a good test of the hardware form factor though - the sensor board I designed was fairly easy to lay out, mill
and solder as a single sided PCB and it functions perfectly well. The sensor uses a couple of I2C sensors and a resistive
soil moisture sensor - the firmware code was fairly straight forward, the [SensNode API](/apidocs/sensnode/index.html)
seems to be complete enough to do most things now. I have identified a few extra features I would like to add and a
few extensions to existing functions (adding timing control to the software SPI functions for example).

For the competition I had to reimplement the API as a shim layer over Silicon Labs [EMLIB Library](http://devtools.silabs.com/dl/documentation/doxygen/EM_CMSIS_P1_DOC_4.0.0/emlib_zero/html/index.html)
which is not the most efficient way to do things. The final firmware image came out at a touch under 8Kb which is
larger than I would prefer not too mention the overhead of function calls passing through several abstraction layers
before something actually happens at the hardware level. Preferably I would like to use a more *bare metal* approach
to implement the SensNode API. I started down that path with the XMC1100 and STM32F030 chips using header files that
simply defined the peripheral register locations and manipulating them directly in the code. Generating those headers
is a time consuming process (thankfully [Frank Duignan](http://eleceng.dit.ie/frank/arm/index.html) has created headers
for a [range of CPUs](http://eleceng.dit.ie/frank/arm/cortex/) already).

![Breakout Board](/images/photos/breakout_board.jpg)

Another useful things that came out of the competition entry was the SensNode breakout board (shown above). This allows
the use of manufacturer development boards for prototyping while keeping the SensNode form factor for testing integration.
As I mentioned earlier, communication with the NRF24L01 on the breakout is a bit problematic but being able to test
everything except networking is still very useful.

The competition results will be announced in the next few weeks, it will be interesting to see how I go. Now I need to
figure out the best way forward to get a working, stand alone SensNode board working. Continuing with the development
kit based prototype seems a bit pointless (I was using very little of the extra functionality it provided) - without the
time constraints imposed by the competition I can devote some time to building a custom board around the
[EFM32HG108 chip](https://www.silabs.com/products/mcu/32-bit/efm32-happy-gecko/pages/EFM32HG108F64-QFN24.aspx) or move
back to the [XMC1100](http://www.infineon.com/cms/en/product/microcontroller/32-bit-industrial-microcontroller-based-on-arm-registered-cortex-registered-m/32-bit-xmc1000-industrial-microcontroller-arm-registered-cortex-registered-m0/channel.html?channel=db3a30433c1a8752013c1aa35a6a0029)
based board design I was working on prior to the competition.

In either case entering the competition was well worth it, I'm a few more steps closer to fully functional prototype. Be sure
to check the [other entries](http://community.silabs.com/t5/forums/filteredbylabelpage/board-id/9/label-name/low%20power%20design%20contest), there are some interesting designs there.
