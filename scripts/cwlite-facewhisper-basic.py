#!/usr/bin/env python

from chipwhisperer.common.api.CWCoreAPI import CWCoreAPI
from chipwhisperer.common.scripts.base import UserScriptBase
from chipwhisperer.capture.api.programmers import XMEGAProgrammer
import os


def getFirmwarePath(name):
    return os.path.join(os.path.dirname(__file__), '../firmware/%s/%s.hex' % (name, name))


class UserScript(UserScriptBase):
    _name = "ChipWhisperer-Lite: Facewhisperer basic test"
    _description = "Getting the Facewhisperer going"

    def run(self):
        for cmd in [
            ['Generic Settings', 'Scope Module', 'ChipWhisperer/OpenADC'],
            ['Generic Settings', 'Target Module', 'Simple Serial'],
            ['Generic Settings', 'Trace Format', 'ChipWhisperer/Native'],
            ['Simple Serial', 'Connection', 'NewAE USB (CWLite/CW1200)'],
            ['ChipWhisperer/OpenADC', 'Connection', 'NewAE USB (CWLite/CW1200)'],
            ]:
            self.api.setParameter(cmd)

        self.api.connect()

        # Flash the firmware
        xmega = XMEGAProgrammer()
        xmega.setUSBInterface(self.api.getScope().scopetype.dev.xmega)
        xmega.find()
        xmega.erase()
        xmega.program(getFirmwarePath('usb-descriptor-simple'), memtype='flash', verify=True)
        xmega.close()

        # Capture parameters
        for cmd in [
            ['Simple Serial', 'Load Key Command', u''],
            ['Simple Serial', 'Go Command', u'\n'],
            ['Simple Serial', 'Output Format', u'$GLITCH$8000'],
            ['Simple Serial', 'NewAE USB (CWLite/CW1200)', 'baud', 115200],

            ['CW Extra Settings', 'Trigger Pins', 'Target IO4 (Trigger Line)', True],
            ['CW Extra Settings', 'Target IOn Pins', 'Target IO1', 'Serial RXD'],
            ['CW Extra Settings', 'Target IOn Pins', 'Target IO2', 'Serial TXD'],
            ['CW Extra Settings', 'Target HS IO-Out', 'CLKGEN'],

            ['OpenADC', 'Clock Setup', 'CLKGEN Settings', 'Desired Frequency', 12e6],
            ['OpenADC', 'Clock Setup', 'ADC Clock', 'Source', 'CLKGEN x4 via DCM'],
            ['OpenADC', 'Trigger Setup', 'Total Samples', 24400],
            ['OpenADC', 'Trigger Setup', 'Pre-Trigger Samples', 0],
            ['OpenADC', 'Trigger Setup', 'Offset', 14100],
            ['OpenADC', 'Gain Setting', 'Setting', 38],
            ['OpenADC', 'Trigger Setup', 'Mode', 'rising edge'],
            ['OpenADC', 'Clock Setup', 'ADC Clock', 'Reset ADC DCM', None],

            ['Generic Settings', 'Acquisition Settings', 'Number of Traces', 500],

            ['CW Extra Settings', 'HS-Glitch Out Enable (Low Power)', True],
            ['CW Extra Settings', 'HS-Glitch Out Enable (High Power)', True],
            ['Glitch Module', 'Clock Source', 'CLKGEN'],
            ['Glitch Module', 'Single-Shot Arm', 'Before Scope Arm'],
            ['Glitch Module', 'Glitch Trigger', 'Ext Trigger:Single-Shot'],
            ['Glitch Module', 'Output Mode', 'Glitch Only'],

            ['Glitch Module', 'Glitch Width (as % of period)', 44.4],
            ['Glitch Module', 'Glitch Offset (as % of period)', 5.3],
            ['Glitch Module', 'Repeat', 2],
            ['Glitch Module', 'Ext Trigger Offset', 7218],

            # Fixme: these are specific to the target device I'm experimenting on
            ['Glitch Explorer', 'Normal Response', u's.find("rcode 5 total 34") >= 0'],
            ['Glitch Explorer', 'Successful Response', u"(lambda n: n.isdigit() and int(n))((s+' x').split('total ')[-1].split()[0]) > 34"],
            ]:
            self.api.setParameter(cmd)

        self.api.capture1()
        self.api.capture1()


if __name__ == '__main__':
    import chipwhisperer.capture.ui.CWCaptureGUI as cwc
    from chipwhisperer.common.utils.parameter import Parameter
    Parameter.usePyQtGraph = True
    api = CWCoreAPI()
    app = cwc.makeApplication("Capture")
    gui = cwc.CWCaptureGUI(api)
    api.runScriptClass(UserScript)
    app.exec_()
