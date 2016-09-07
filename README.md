FaceWhisperer
=============

FaceWhisperer is a hardware add-on for the [ChipWhisperer](https://newae.com/tools/chipwhisperer/) side-channel analysis tool, for working with devices that primarily communicate over USB. The goal is to create a USB host controller scripted with an experiment, all running totally synchronous with the target. This should give predictable timing each time the experiment is run from a target reset.

One proven use for this is to glitch GET_DESCRIPTOR requests into returning firmware images for devices that don't otherwise have firmware available for inspection.

The experiments are scripted from an ATxmega128 processor, same as the one included on ChipWhisperer-Lite. The USB host is a MAX3241E, inspired by Travis Goodspeed's [Facedancer21](http://goodfet.sourceforge.net/hardware/facedancer21/) tool.

For keeping the target device in sync, this board provides a 12 MHz clock output, an open-collector reset output, and a trigger input with adjustable voltage threshold.

This project is a quick hack that builds on the work and inspiration of several great projects:

- [GoodFET](http://goodfet.sourceforge.net)
- [ChipWhisperer](https://newae.com/tools/chipwhisperer)
- [Xmegaduino](https://github.com/Xmegaduino/Xmegaduino)
- [Arduino USB Host Shield library](https://github.com/felis/USB_Host_Shield_2.0)

This repository includes the hardware design itself, as well as a firmware framework and scripts to integrate with ChipWhisperer.

<img alt="Prototype PCB, rev A" src="http://i.imgur.com/cdOqJJ2.jpg" width="100%" >


Hardware Errata
---------------

The current PCB design is usable, but there are some changes that still need to be made before I'd recommend anyone manufacture the design:

- Labels on the silkscreen and copper layers. I was milling the Rev A board, so I kept it simple.
- The CLK output is rather weak. I used the NC7WZ14 because I had them on hand, but they're just barely up to the task.
- I originally included the second CLK SMA jack for clock glitching via the CWLite's crowbar FET, but that's silly and this should really just have an XOR on-board for inserting glitches in the target clock without disrupting the facewhisperer itself.
- The SYNCIN didn't make it into the first board design at all, I had to rework it on.
- I didn't include headers for the spare GPIOs in the first board, for expediency's sake, but these would be an obviously handy addition.
- Connector placement is awkward. Rethink this around optimal coax routing.
- FTDI header for sniffing the serial bus. Jumper for optional transmit. I ended up using an FTDI cable to log the results while also allowing CWLite's serial port to orchestrate the glitching process.
- Maybe use a better transistor for the reset puller. The 2N7000 was just what I had handy. Also maybe take the LED off the gate, it may have been causing some 100ns-scale glitches in the reset's falling edge.
- Lots more test points and posts and things for you to grab onto with a logic analyzer.

