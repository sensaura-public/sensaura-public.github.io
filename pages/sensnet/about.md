---
title: SensNet
section: sensnet
---
# SensNet Sensor Protocol

The SensNet protocol is a simple data transfer protocol built on the NRF24L01+ that allows *attributes* on a sensor
to be read from or written to through a simple API. The network uses a [star topology](https://en.wikipedia.org/wiki/Star_network)
where each network consists of a single hub and multiple nodes.

The current design allows for a theoretical maximum of 254 nodes in each network and has a range of up to 100m from
the hub. The primary design goal was ease of configuration, the protocol supports;

1. Automatic network connections. Pressing and holding the *action* button on a [SensNode](/pages/sensnode/about.html) on power up will trigger a connection to the network. This connection information will be remembered and the node will automatically join the network again after a power cycle.
2. Self describing nodes. Each node can report the attributes it provides - their name, data type and if they can be written to as well as read from.

## Attributes

Each node is represented as a set of *attributes* - named slots that hold information. In general an attribute value
will be sent by the node if it changes or on a periodic basis. Attributes may also be queried directly rather than waiting
for the next update event.

Attributes may also be marked as *writable* - values can be sent over the network to the node to change its operating
behavour or configuration.

## Implementation Details

The initial implementations of the SensNet protocol are provided as part of the [SensNode](/pages/sensnode/about.html)
firmware and as Python and .NET libraries that can be used in applications. SensNet can be used in custom applications
or integrated with the [SensHub](/pages/senshub/about.html) server.

To participate in a SensNet network a PC will require a NRF24L01 adapater module. Currently a SensNode processor board
can be used for this - providing a serial interface to network for packet transmission and reception.

### Broadcast Model

The SensNode network does not use the ShockBurst features of the NRF24L01+ (this would limit the number of nodes to 6
per network). Each node uses the same NRF24L01 address which means that every packet sent from the hub will be received
by every node on the network - the node itself determines if the packet is intended for it or not.

Nodes use a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) to identify themselves, this value is
hard coded into the firmware for the node and will not change across power cycles.

### Automatic Address Assignment

Because the NRF24L01 packet size is limited to 32 bytes it is not possible to send the 128 bit (16 byte) UUID in each
packet to provide identification. A one byte local network address is used instead - this address is assigned by the
protocol when the node joins the network. This address is transient, it may change while the node is operating or
across power cycles.

The SensNet API allows applications to simply refer to nodes by their UUID and hides the local network address details.

### Attribute Discovery

The set of attributes provided by a node are defined in it's firmware and are immutable - they do not change unless the
firmware is reloaded and a different UUID is assigned to the node. When a node joins the network it's attributes will
be queried and the initial values read. During normal operation these values will be updated by events sent from the
node or by direct query from the SensNet library.

Each attribute description consists of a name, a read/write flag and a data type. Common types such as string, flag,
number and date are supported and arbitrary data (up to 20 bytes in size) can be used. This design was heavily influenced
by the Bluetooth LE GATT protocol and has many aspects in common.
