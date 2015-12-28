---
title: SensNode Processor Boards
section: sensnode
---
# Processor Boards

A SensNode processor board consists of an ARM Cortex-M0 or M0+ CPU, a NRF24L01+ wireless module and some discrete
components to implement a standardised debug and programming interface. The processor board design is deliberately
minimalistic to allow for a wide range of CPUs from different manufacturers to be used.

## CPU Selection

To provide full support for the [SensNode API](/apidocs/sensnode/index.html) and [hardware specification](/pages/sensnode/hardware.html)
the selected CPU should have the following features:

  * At least 16K of flash and 4K of RAM. These requirements are determined by the [SensNet](/pages/sensnet/index.html)
    implementation.
  * At least 14 available GPIO pins (of which at least 4 support analog input) to provide a fully functional header
    interface.
  * Real time clock (RTC) with alarm functionality.
  * Hardware support for I2C and UART.

These requirements allow for a wide range of CPUs from different manufacturers, prototypes have been (or are in development)
for devices from [Silicon Labs](http://www.silabs.com/Pages/default.aspx) (EFM32HG108), [Infineon](http://www.infineon.com/)
(XMC1100) and [STMicroelectronics](http://www.st.com/web/en/home.html) (STM32F030). In general most 20 pin or better
ARM processors can be used.

> NOTE: The SensNode reference implementation and the SensNode firmware has been designed for ARM processors but this
> does not prohibit the use of other CPU architectures. The PIC32 and some models of the MSP430 and AVR devices match
> the required functionality. Using other architectures would require rewriting the API and will not be supported as
> part of the main project.
