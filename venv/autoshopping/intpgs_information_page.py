#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################  REQUIRED COMMENTS FOR ALL TESTSCRIPTS ####################################
'''
Check the supply status internal page notes and status of different supply state.
'''

DocString = __doc__

TestSteps = '''
Automated
'''

'''
The following file parameters will be parsed by TEM to provide more
information for metrics.  All of the parameter names must begin with
'%' and end with ':'.  No whitespace is allowed in the parameter names.
Any text after a '#' will be treated and will be ignored until the next
newline.  Blank lines will be ignored.

<tem_metrics>
# %AutoSetup: Is the setup of the script automatic or does the tester
# need to perform the setup manually.  Valid values are 'Y' or 'N'
%AutoSetup: Y
# %AutoScript: The approximate percentage that the script is automated.
# 0 = manual test (script only displays test step instructions)
# 100 = fully automated test.
%AutoScript: 90

# %AutoAnalysis: Is the analysis automated or are does the user need to
# manually analyze the results to determine a pass/fail status.
%AutoAnalysis: Y

# %TestObjective: Add one of the following Test Objectives
# Feature; Localization; Duration; Integration; Unit
# Default value is Feature.
%TestObjective: Feature

# %TestDependencies: Semi-colon separated list of equipment that must be
# set up prior to running this test (Tray 3, ADF paper loop, etc.)
%TestDependencies: Real Engine

# %SetupInstructions: How to set up the device and supporting infrastructure.
# For example, how to create the ADF paper loop.  Tray 3 doesn't need to
# be explained.
%SetupInstructions:

# %OwnerName - Test owner/contact person
%OwnerName: Sandhya Changarath

# %OwnerEmail - The owner's email address
%OwnerEmail: sandhya.changarath1@hp.com
</tem_metrics>

Creation Date: (11/14/2018)
Last Reviewed Date: (11/18/2018)
'''

###################  REQUIRED IMPORTS FOR ALL TESTSCRIPTS ############
import logging, re, temlib, time
from collections import OrderedDict
import phx_commonlib.sps.spsBase as spsBase
import phx_commonlib.sps.spsSimBase as spsSimBase
from phx_test.config.ledm_leev.LedmResources import LedmResources
import phx_commonlib.configuration.systemConfig as sc
from phx_commonlib.phx_common.common_unittest_factory import cu
AuthState = spsBase.SPSBase.AuthState
import phx_commonlib.io.telnetDebug as telnetDebug
import phx_commonlib.sps.sps_factory as sps_factory
import phx_commonlib.phx_common.printer_factory as printer_factory
import phx_commonlib.paperhandling.paperhandlinglib as phlib
import phx_commonlib.phx_common.printer as printdev
from phx_commonlib.ledm.ledmwifilib import *

# Different Notes on the Information Page.
def createInfoPageNotes(printerIP):

    physicalButtons = telnetDebug.TelnetDebug("ui/GetPhysicalButtons", printerIP, True).split('|')
    if "INFO" in physicalButtons:
        productInfoNote = 'For more information print the Configuration Report: press and hold the [Information] button for 3 seconds and then press the [Resume] button.',
    else:
        productInfoNote = 'For more information print the Configuration Report: press and hold the [Resume] button for 3 seconds',

    if "INFO" in physicalButtons and "CANCEL" in physicalButtons:
        wirelessNotConnectedNote = 'For more information, print the Wireless Network Test Report: press and hold the Information button for 3 seconds, and then press the Information button and the Resume button at the same time.',
    elif "INFO" not in physicalButtons and "CANCEL" in physicalButtons:
        wirelessNotConnectedNote = 'For more information, print the Wireless Network Test Report: Press and hold the [Resume] and [Wireless] buttons at the same time for 3 seconds.'
    elif "INFO" not in physicalButtons and "CANCEL" not in physicalButtons:
        wirelessNotConnectedNote = 'For more information, print the Wireless Network Test Report: Press and hold the [Wireless] button for 10 seconds.'

    InfoPageNotes = {
        'product_info': productInfoNote,
        'wireless_off': 'Press the [Wireless] button to turn on wireless.',
        'wireless_not_connected': wirelessNotConnectedNote,
        'ethernet_connected': 'Note: Wireless connections are unavailable when the printer is connected using Ethernet.',
        'wifi_direct_off': 'To turn on Wi-Fi Direct press and hold the [Information] button for 3 seconds and then press the [Resume] button and the [Wireless] button at the same time.',
    }
    return InfoPageNotes

def operator_interact(text='Yes or No?'):
    # Using temlib so the display occurs within the TEM GUI rather than just the terminal
    result = temlib.User.GetRespYesNo(text)
    logging.debug("'%s' was answered with '%s'" % (text, result))
    if result == 'No':
        return False
    else:
        return True

def printInformationPage(printerIP):
    printer = printer_factory.create_printer(printerIP)
    logging.info("Printing Info page... Wait for info page to print and operator instructions :")
    printer.print_internal_report(printdev.Internalreport.printer_information_page)

# Verify value on the information page.
def verify_info_report(valueToCheck, expectedValue, sectionName=""):
    logging.debug("Verify {valueToCheck} {expectedValue} is printed on the information page".format(valueToCheck=valueToCheck, expectedValue=expectedValue))
    operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nOn the info page {section}, is {valueToCheck}: {expectedValue} ? \nIf printed type YES, else NO and hit OK ...\n".format(valueToCheck=valueToCheck, expectedValue=expectedValue, section=sectionName))
    if not operator_confirmation:
        raise Exception("Printer information report shows different {valueToCheck}".format(valueToCheck=valueToCheck))

# Verify value not present on the information page.
def verify_absence_info_report(valueToCheck):
    logging.debug("Verify that {valueToCheck} are not printed on the information page:".format(valueToCheck=valueToCheck))
    operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIs {valueToCheck} on the info page ? \nIf printed type YES, else NO and hit OK ...\n".format(valueToCheck=valueToCheck))
    if operator_confirmation:
        raise Exception("{valueToCheck} is unexpectedly printed on the Info Page".format(valueToCheck=valueToCheck))

class InfoPageSuite(cu.BaseTestSuite):
    def setUp(self):
        super(InfoPageSuite, self).setUp()
        self.printer.setCRCMode(None)
        self.maxDiff = None
        self.defaultPassword ="12345678"
        self.customPassword = "trythis"
        self.defaultPIN = self.printer.getDefaultDevicePassword()
        self.originalWifiDirectSetting = self.getWifiDirectSetting()
        self.sps = sps_factory.create(self.printer.getIP())
        # Ensure device has default password
        self.assertTrue(self.printer.securityOn())
        # self.assertTrue(self.printer.setDevicePassword(self.defaultPassword, self.defaultPIN))
        self.infoPageNotes = createInfoPageNotes(self.printerIP)

    def tearDown(self):
        if self.originalWifiDirectSetting == False:
            self.turnOffWifiDirect()
        else:
            self.turnOnWifiDirect()

    def createCPButtonsList(self, used=False, usedSupply=None):
        supportedButtons= ["Power"]
        notSupportedButtons = []
        physicalButtons = telnetDebug.TelnetDebug("ui/GetPhysicalButtons", self.printerIP, True).split('|')

        if "GO" in physicalButtons:
            if sc.DeviceIsMFP(self.printerIP):
                if "START COPY" not in physicalButtons:
                    supportedButtons.append("Document Copy | Resume")
                else:
                    supportedButtons.append("Resume")
            else:
                if "CANCEL" not in physicalButtons:
                    supportedButtons.append("Cancel | Resume")
                else:
                    supportedButtons.append("Resume")
        else:
            notSupportedButtons.append("Resume")
        if "INFO" in physicalButtons:
            supportedButtons.append("Information")
        if "WIRELESS WPS" in physicalButtons:
            supportedButtons.append("Wireless")
        else:
            notSupportedButtons.append("Wireless")
        if "CANCEL" in physicalButtons:
            supportedButtons.append("Cancel")
        else:
            notSupportedButtons.append("Cancel")
        if "START COPY" in physicalButtons:
            supportedButtons.append("Document Copy")
        else:
            notSupportedButtons.append("Document Copy")
        if "ID COPY" in physicalButtons:
            supportedButtons.append("ID Card Copy")
        else:
            notSupportedButtons.append("ID Card Copy")
        if "COPY SETTINGS" in physicalButtons:
            supportedButtons.append("Copy Options")
        else:
            notSupportedButtons.append("Copy Options")

        return supportedButtons, notSupportedButtons

    def createInfoPageSuiteDict(self):
        productInfo= {}
        productInfo = OrderedDict([("Product Name"           , self.printer.getMakeModel()),
                                   ("Formatter Number"       , self.printer.getFormatterSerialNumber()),
                                   ("Bonjour Service Name"   , self.getBounjourName()),
                                   ("Printer Claim Code"     , self.getPrinterClaimCode()),
                                   ("Serial Number"          , self.printer.getSerialNumber()),
                                   ("Firmware Datecode"      , self.printer.getFirmwareVer() + " Apollo Firmware"),
                                   ("Printer PIN"            , self.defaultPIN)])
        return productInfo

    def createWiFDirectDict(self):
        wifiDirectInfo= {}
        wifiDirectInfo = OrderedDict([("Status"                  , "Enabled" if self.getWifiDirectSetting() else "Disabled"),
                                      ("Wi-Fi Direct Name (SSID)", self.getWifiDirectSSID()),
                                      ("Wi-Fi Direct Password"   , self.getWifiDirectPassword())])
        return wifiDirectInfo


    def getWifiDirectSetting(self):
        if "Enabled" in (telnetDebug.TelnetDebug("io/get DIRECT_PRINT_ENABLED", self.printerIP, True)):
            return True
        else:
            return False

    def turnOffWifiDirect(self):
        self.assertTrue(telnetDebug.TelnetDebug("io/set DIRECT_PRINT_ENABLED false", self.printerIP, True))

    def turnOnWifiDirect(self):
        if "Enabled" in (telnetDebug.TelnetDebug("io/set DIRECT_PRINT_ENABLED true", self.printerIP, True)):
            return True
        else:
            return False

    def getWifiDirectSSID(self):
        result = telnetDebug.TelnetDebug("io/get DIRECT_PRINT_SSID", self.printerIP, True)
        ssidName = re.search("DIRECT_PRINT_SSID = (.*)", result)
        return ssidName.group(1)

    def getWifiDirectPassword(self):
        result = telnetDebug.TelnetDebug("io/get DIRECT_PRINT_PASSPHRASE", self.printerIP, True)
        password = re.search("DIRECT_PRINT_PASSPHRASE = (.*)", result)
        return password.group(1)

    def getBounjourName(self):
        result = telnetDebug.TelnetDebug("io/get MDNS_NAME", self.printerIP, True)
        bounjourName = re.search("MDNS NAME = (.*)", result)
        return bounjourName.group(1)

    def getWifiStatus(self):
        wifiConfig = telnetDebug.TelnetDebug("wifi/get config", self.printerIP, True)
        status = re.search("ssid = (.*)", wifiConfig)
        return status.group(1)

    def isNetworkingSupported(self):
        networking = True
        if (sc.DeviceHasEthernetNetwork(self.printerIP) == False) and (sc.DeviceHasWireless(self.printerIP) == False):
            networking = False
        return networking

    def getPrinterClaimCode(self):
        claimCode = telnetDebug.TelnetDebug("ePrint/cloud_utils/cloud_utils.get_printer_code", self.printerIP, True)
        # Formatting the claim code as printed on Info Page
        printerClaimCode = ' '.join(claimCode[i:i+4] for i in range(0,len(claimCode),4))
        return printerClaimCode

    # Verify that the footer portion of the information page contains 2 QR codes with icons and urls.
    def test_verify_footer_qr_codes(self):
        printInformationPage(self.printerIP)
        logging.info("\n**Verify that the footer portion of the information page contains 2 QR codes with icons and valid urls.**")
        # Verify that the footer portion of the information page contains 2 QR codes with icon and url each.
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIs there 'Learn More' on the left of the footer ?\nIs there Translator icon and QR code printed on the second line ?\nIs there support URL on the third line ?\nIf so type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Missing or incorrect icon/URL/QR Code on the left of the footer of Info page!")

        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIs there 'Set Up with HP Smart' on the right of the footer ?\nIs there SmartApp icon and QR code printed on the second line ?\nIs there 123.hp.com URL on the third line ?\nIf so type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Missing or incorrect icon/URL/QR Code on the right of the footer of Info page!")

        # Verify that the support URL is accessible and QR code scans successfully to open a page with product information in other langauges
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nAccess the support URL below Translator icon and QR code, did it take to a web page that allows to find out information about this product in other languages.?\nDoes scanning the QR code via mobile also lead to the same information?\nIf so type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "QR code scanning or accessing urls failed for language support")

        # Verify that 123.hp.com URL is accessible and QR code scans successfully to open a page in order to download software"
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nAccess the 123.hp.com URL below SmartApp icon and QR code, did it take to a web page that allows get information on downloading software.?\nDoes scanning the QR code via mobile also lead to the same information?\nIf so type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "QR code scanning or accessing urls failed to download software support!")

    # Verify general printer information on the Info page and verify the Printer PIN has default value
    def test_verify_product_info_default_password(self):
        logging.info('**Verify general printer information on the Info page and verify the Printer PIN has the default value.**')
        printInformationPage(self.printerIP)
        productInfo = self.createInfoPageSuiteDict()
        for valueToCheck, expectedValue in productInfo.items():
            if "Bonjour" in valueToCheck and not self.isNetworkingSupported():
                continue
            verify_info_report(valueToCheck, expectedValue)

    # Verify that if the user has changed the default password, then the string “Custom user password set” will be
    # displayed instead of the actual password/PIN.
    def test_verify_custom_password(self):
        logging.info("**Verify that on changing the default password, the info report will not display the actual password/pin.**")
        self.assertTrue(self.printer.setDevicePassword(self.customPassword, self.defaultPIN))
        printInformationPage(self.printerIP)
        verify_info_report("Printer PIN", "Custom user password set")

        logging.debug("Adding the clean up for setting back the default password in printer")
        self.addCleanup(self.printer.setDevicePassword, self.defaultPIN, self.customPassword)

    # Verify that when product security has been turned off the “Product Security: Off” will be displayed instead.
    def test_verify_password_security_off(self):
        logging.info("**Verify that on turning off Security, the info reports product security is Off.**")
        self.assertTrue(sc.turnOffSecurity(self.printerIP, self.defaultPIN))
        printInformationPage(self.printerIP)
        verify_info_report("Product Security", "Off")

        logging.debug("Adding the clean up for setting back the default password in printer")
        self.addCleanup(self.printer.setDevicePassword, self.defaultPIN, "")

    # Verify Wi-fi direct settings and notes when Wi-Fi Direct is disabled.
    def test_wifi_direct_disabled(self):
        logging.info("Verify Wi-fi direct settings and notes when Wi-Fi Direct is disabled.")
        self.turnOffWifiDirect()
        printInformationPage(self.printerIP)

        self.assertEqual(self.getWifiDirectSetting(), False)
        verify_info_report("Status", "Disabled", "Wi-Fi Direct section")

        # Verify note on the information page.
        logging.info("Verify that proper note is printed on the information page when Wi-Fi Direct is Disabled.")
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIs the following note printed under Wi-Fi Direct section on the Info page?\n{note}\nIf printed type YES, else NO and hit OK ...\n".format(note=self.infoPageNotes['wifi_direct_off']))
        self.assertTrue(operator_confirmation, "Incorrect note under Wi-Fi Direct section when Wi-fi Direct is off")

    # Verify Wifi and ethernet settings when Wifi is off and ethernet is connected
    def test_ethernet_connected(self):
        logging.info("Verify information under Ethernet/Wireless section")
        self.assertTrue(sc.DeviceIsConnectedToEthernet(self.printerIP))
        self.assertEqual(self.getWifiStatus(), "unconfigured")

        printInformationPage(self.printerIP)
        logging.info("Verify Ethernet settings when Ethernet is connected")
        verify_info_report("Status", "Connected", "Ethernet section")

        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nOn the info page under Ethernet section, is the Ethernet IP printed? \nIf printed type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Wrong ethernet info printed under the Ethernet section.")

        # Verify that proper note is printed on the information page when ethernet is connected.
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIs \"{note}\" note printed under Ethernet section on the info page ? \nIf printed type YES, else NO and hit OK ...\n".format(note=self.infoPageNotes['ethernet_connected']))
        self.assertTrue(operator_confirmation, "Incorrect note under ethernet section ethernet is connected")

        # Verify absence of Wireles section
        logging.info("Verify Wireless section not present when Ethernet is connected")
        verify_absence_info_report("Wireless section")

    # Verify that only supported control panel button are printed on the info page
    def test_control_panel_buttons(self):
        printInformationPage(self.printerIP)
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\n On the info page, is Control Panel Buttons displayed with a header Icon. Is button list with an icon each displayed horizontally. \nIf printed type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Printer information report shows different behavior")

        supportedButtons, unsupportedButtons = self.createCPButtonsList()

        logging.info("Verify that all the supported buttons are printed on the information page.")
        for button in supportedButtons:
            operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nOn the info page under Control Panel Buttons, is the '{button}' button printed along with appropriate icon to its left? \nIf printed type YES, else NO anOd hit OK ...\n".format(button=button))
            self.assertTrue(operator_confirmation, "The '{button}' is not printed under the Control Panel Buttons section.")

        logging.info("Verify none of the unsupported buttons are printed on the information page.")
        for button in unsupportedButtons:
            operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nOn the info page under Control Panel Buttons, is the '{button}' button printed along with appropriate icon to its left? \nIf printed type YES, else NO and hit OK ...\n".format(button=button))
            self.assertFalse(operator_confirmation, "The {button} is printed under the Control Panel Buttons section.")

        logging.info("Verify buttons are printed with correct position on the information page.")
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIf the device has information button,\nOn the info page under Control Panel Buttons,\nInformation button and Wireless button should be printed next to each other.\nIf printed type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "The button is printed incorrect position under the Control Panel Buttons section.")

        logging.info("Verify buttons are printed with correct position on the information page.")
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nOn the info page under Control Panel Buttons,\nResume button and Cancel button should be printed next to each other.\nIf it is a Kay or Gaheris device, It should be combined Resume-Cancel button and Copy-Settings button\nIf printed type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Incorrect button printed under the Control Panel Buttons section.")

    # Verify Wi-fi direct settings are displayed correctly on the info page when Wi-Fi Direct is Enabled
    def test_wifi_direct_enabled(self):
        logging.info("Verify Wi-fi direct settings are displayed correctly on the info page when Wi-Fi Direct is Enabled.")
        self.assertTrue(self.turnOnWifiDirect(), "Failed to turn Wi-Fi Direct On")

        printInformationPage(self.printerIP)
        for valueToCheck, expectedValue in self.createWiFDirectDict().items():
            verify_info_report(valueToCheck, expectedValue, "Wi-Fi Direct section")

    # Verify Wireless settings are displayed correctly on the info page when Wireless is Connected
    def test_wireless_connected(self):
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\n Test Setup:\n1. Disconnect Ethernet cable and set up PPP.\n2. Open EWS page using the PPP IP and set up Wireless connection.\
                                                  \n3. Once Wireless connection is successful, print info page from the CP.\n4. Once info page printed, Reconnect the ethernet cable and type yes then hit OK.")
        self.assertTrue(operator_confirmation)

        logging.info("Verify Wireless settings when Wireless is connected")
        verify_info_report("Status", "Connected", "Wireless section")

        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nOn the info page under Wireless section, is the Wireless IP, Network Name(SSID) and Signal Strength info printed? \nIf printed type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Wrong wireless info printed under the Wireless section.")

        # Verify that note is Not printed on the information page when Wireless is connected.
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIs the following note printed under the Wireless section on the Info Page? \n{note}\nIf printed type YES, else NO and hit OK ...\n".format(note=self.infoPageNotes['wireless_off']))
        self.assertFalse(operator_confirmation, "Incorrect note under wireless section when Wifi is connected")

        logging.info("Verify Ethernet section not present when Wireles is connected")
        # Verify absence of Ethernet section
        verify_absence_info_report("Ethernet section")


    # Verify Network settings are displayed correctly on the info page when both Wireless is Off and Ethernet not Connected
    def test_wifi_and_ethernet_off(self):
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\n Test Setup:\n1. Disconnect Ethernet cable.\n2. Disconnect Wireless connection.\n3. Set up PPP and Verify that Wireless is Off on the EWS page.\n4. Use PPP IP and print info page using telnet debug command and type yes......")

        self.assertTrue(operator_confirmation)
        logging.info("Verify Wireless settings when both Ethernet and Wifi are off")

        verify_info_report("Status", "Off", "Wireless section")

        # Verify that proper note is printed on the information page when both ethernet & wireless are Off.
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIs \"{note}\" note printed under Wireless section on the info page ? \nIf printed type YES, else NO and hit OK ...\n".format(note=self.infoPageNotes['wireless_off']))
        self.assertTrue(operator_confirmation, "Incorrect note under wireless section when wifi is not connected")

    # Verify Network settings are displayed correctly on the info page when Wireless is On but Not Connected and Ethernet is disconnected
    def test_wifi_on_but_not_connected_and_ethernet_off(self):
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\n Test Setup:\n1. Disconnect Ethernet cable and set up PPP.\n2. Open EWS page using the PPP IP. \n3. Ensure Wireless is ON but Not connected.\n4. Use PPP IP and print info page using telnet debug command \intpgs\informationPage and type yes......")

        self.assertTrue(operator_confirmation)
        logging.info("Verify Wireless settings when Wireless is On but Not Connected and Ethernet is disconnected")

        verify_info_report("Status", "Not Connected", "Wireless section")

        # Verify that proper note is printed on the information page when ethernet is off & wireless is On but not connected.
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIs \"{note}\" note printed under Wireless section on the info page ? \nIf printed type YES, else NO and hit OK ...\n".format(note=self.infoPageNotes['wireless_not_connected']))
        self.assertTrue(operator_confirmation, "Incorrect note under wireless section when wifi is not connected")

    # Verify all the Network sections are NOT printed on the info page for a USB only device
    @cu.skipIfHasDependencies(['networking'])
    def test_verify_network_info_absent(self):
        logging.info("Verify Info page on a USB only device")
        self.assertFalse(self.isNetworkingSupported())

        logging.info("Verify Wireless settings when Ethernet is connected")
        for valueToCheck in ["Ethernet section", "Wireless section", "Wi-Fi Direct section"]:
            verify_absence_info_report(valueToCheck)

    # Verify info page prints correctly on Letter paper
    def test_default_media_size_Letter(self):
        originalMediaSize = phlib.getDefaultMediaSize(self.printerIP)
        logging.debug("Set default media size {mediaSize} via LEDM".format(mediaSize="Letter"))
        phlib.setDefaultMediaSize(self.printerIP, 'na_letter_8.5x11in')
        self.assertEqual(phlib.getDefaultMediaSize(self.printerIP), 'na_letter_8.5x11in', "Expected default ledm mediasize value : {expectedVal}, Actual value : {actualVal}".format(expectedVal='na_letter_8.5x11in', actualVal=phlib.getDefaultMediaSize(self.printerIP)))

        printInformationPage(self.printerIP)
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\n Is the info page printed on Letter paper with correct info with the text fitting properly on the page and not cut off? \nIf printed type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Printer information report not correct on Letter page!")

        # Restore to default settings
        if originalMediaSize != 'na_letter_8.5x11in':
            phlib.setDefaultMediaSize(self.printerIP, originalMediaSize)

    # Verify info page prints correctly on A4 paper
    def test_default_media_size_A4(self):
        originalMediaSize = phlib.getDefaultMediaSize(self.printerIP)
        logging.debug("Set default media size {mediaSize} via LEDM".format(mediaSize="A4"))
        phlib.setDefaultMediaSize(self.printerIP, 'iso_a4_210x297mm')
        self.assertEqual(phlib.getDefaultMediaSize(self.printerIP), 'iso_a4_210x297mm', "Expected default ledm mediasize value : {expectedVal}, Actual value : {actualVal}".format(expectedVal='iso_a4_210x297mm', actualVal=phlib.getDefaultMediaSize(self.printerIP)))

        printInformationPage(self.printerIP)
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\n Is the info page printed on A4 paper with correct info with the text fitting properly on the page and not cut off? \nIf printed type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Printer information report not correct on A4 page!")

        # Restore to default settings
        if originalMediaSize != 'iso_a4_210x297mm':
            phlib.setDefaultMediaSize(self.printerIP, originalMediaSize)

    # Verify info page prints correctly on A4 paper
    def test_bonjour_name_max_length(self):
        originalBonjourName = self.getBounjourName()
        self.assertTrue(telnetDebug.TelnetDebug("io/set MDNS_NAME SETTING_BONJOUR_NAME_TO_VERY_LONG_VALUE_TO_CHECK_INFO_PAGE", self.printerIP, True))
        printInformationPage(self.printerIP)
        self.assertTrue(telnetDebug.TelnetDebug("io/set MDNS_NAME {originalBonjourName}".format(originalBonjourName=originalBonjourName), self.printerIP, True))
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\n Is long Bonjour name line wrapped correctly to the line below on the info page? \nIf printed type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Line wrapping not not correct for Bonjour name on the info page!")

    # Verify that the footer portion of the information page contains Support QR code with icon and Support url.
    def test_verify_footer_qr_codes_ctss(self):
        printInformationPage(self.printerIP)
        logging.info("\n**Verify that the footer portion of the information page contains Support QR code with icon and Support url.**")
        # Verify that the footer portion of the information page contains Support QR code with icon and Support url.
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nIs there 'Set Up with HP Smart' on the left of the footer ?\nIs there SmartApp icon and QR code printed on the second line ?\nIs there 123.hp.com URL on the third line ?\nIf so type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "Missing or incorrect icon/URL/QR Code on the left of the footer of Info page!")

        # Verify that 123.hp.com URL is accessible and QR code scans successfully to open a page in order to download software"
        operator_confirmation = operator_interact("\nOPERATOR ACTION REQUIRED\nAccess the 123.hp.com URL below SmartApp icon and QR code, did it take to a web page that allows get information on downloading software.?\nDoes scanning the QR code via mobile also lead to the same information?\nIf so type YES, else NO and hit OK ...\n")
        self.assertTrue(operator_confirmation, "QR code scanning or accessing urls failed to download software support!")

class SuppliesInfo(spsSimBase.SuppliesSimBaseSuite):

    def setUp(self):
        super(SuppliesInfo, self).setUp()
        self.printer.setCRCMode(None)
        self.maxDiff = None
        self.defaultPassword ="12345678"

    def tearDown(self):
        pass
    # Cartridge status of each supply state.
    cartridgeStatusDict = {AuthState.genuineHP              : 'Normal',
                            AuthState.nonHP                 : 'Normal',
                            AuthState.usedMovedBlocking     : 'Used',
                            AuthState.cartridgeLow          : 'Low',
                            AuthState.cartridgeVeryLow      : 'Very Low (Warranty expired)',
                            }

    def getCartridgeOrderInfo(self, supplyName, used=False, nonHP=False):
        usedString =""
        nonHpString =""
        if used:
            usedString = "Used "
        if nonHP:
            nonHpString = "Non-HP "
        sku = self.sps.getLEDMInstalledSKU(supplyName, self.printerIP)
        selectability_number = self.sps.getLEDMSelectibilityNumber(supplyName, self.printerIP)
        orderInfo = "\n{used}{nonHP}{supplyName} Cartridge: Order {selectability_number} ({sku})".format(used=usedString,nonHP=nonHpString, supplyName=supplyName, selectability_number=selectability_number, sku=sku)
        return orderInfo

    # Install all HP supplies with 100% Life to device and validate the supply status internal page note.
    def test_supply_status_full_life(self):
        logging.debug("Install all supplies with 100% Life")
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            tag = self.spssim.getNewTag(supply, lifeValue=100)
            self.spssim.installSupply(supply, tag, lifeValue=100)
        self.spssim.closeDoor()

        printInformationPage(self.printerIP)
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            verify_info_report('Supplies Info', self.getCartridgeOrderInfo(supply.name), 'Supplies section')
            verify_info_report('Status', self.cartridgeStatusDict[AuthState.genuineHP], 'Supplies section')

        # Install Normal supply back
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            self.spssim.installNormalSupply(supply)
        self.spssim.closeDoor()

    # Install all used supplies to device and validate the supply status internal page note.
    def test_supply_status_used_supply(self):
        logging.debug("Install all used supplies to device and press Ok on used supply prompt.")
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            tag = self.spssim.getLowTag(supply,used=True)
            self.spssim.installSupply(supply, tag, lifeValue=int(supply.default_low))
        self.spssim.closeDoor()
        self.printer.pressButton("OK")

        printInformationPage(self.printerIP)
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            verify_info_report('Supplies Info', self.getCartridgeOrderInfo(supply.name), 'Supplies section')
            verify_info_report('Status', self.cartridgeStatusDict[AuthState.usedMovedBlocking], 'Supplies section')

        # Install Normal supply back
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            self.spssim.installNormalSupply(supply)
        self.spssim.closeDoor()

    # Install Non HP supplies and validate the supply status on the info page.
    def test_supply_status_nonHP_supply(self):
        logging.debug("Install all NON HP supplies to device.")
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            self.spssim.installNonHPSupply(supply)
        self.spssim.closeDoor()

        logging.debug("Clear Non HP prompt.")
        self.printer.pressButton("OK")

        printInformationPage(self.printerIP)
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            verify_info_report('Supplies Info', self.getCartridgeOrderInfo(supply.name), 'Supplies section')
            verify_info_report('Status', self.cartridgeStatusDict[AuthState.nonHP], 'Supplies section')

        # Install Normal supply back
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            self.spssim.installNormalSupply(supply)
        self.spssim.closeDoor()

    # Install all supplies with low life and validate the supply status on the info page.
    def test_supply_status_low_life(self):
        logging.debug("Install all supplies with low life supply to device.")
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            tag = self.spssim.getLowTag(supply)
            self.spssim.installSupply(supply, tag, lifeValue=int(supply.default_low))
        self.spssim.closeDoor()

        printInformationPage(self.printerIP)
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            verify_info_report('Supplies Info', self.getCartridgeOrderInfo(supply.name), 'Supplies section')
            verify_info_report('Status', self.cartridgeStatusDict[AuthState.cartridgeLow], 'Supplies section')

        # Install Normal supply back
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            self.spssim.installNormalSupply(supply)
        self.spssim.closeDoor()

    # Install all supplies with very low life and validate the supply status on the info page .
    def test_supply_status_very_low_life(self):
        # Install supply with engine out value
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            lifeValue = supply.engine_out
            tag = self.spssim.getNewTag(supply, lifeValue=lifeValue)
            self.spssim.installSupply(supply, tag, lifeValue)
        self.spssim.closeDoor()

        # Set WTP to 1% below lifeValue
        varName = 'WarrantyTriggerPoint{0}'.format(supply.name)
        self.sps.sps_set_var(self.printerIP, varName, lifeValue-1)

        # Cause lower the supply life by 1%
        self.spssim.consumeTonerLife(supply)

        # Make sure Info internal page reports corresponding warranty message
        printInformationPage(self.printerIP)
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            verify_info_report('Supplies Info', self.getCartridgeOrderInfo(supply.name), 'Supplies section')
            verify_info_report('Status', self.cartridgeStatusDict[AuthState.cartridgeVeryLow], 'Supplies section')

        # Install Normal supply back
        self.spssim.openDoor()
        for supply in self.psi.getDefaultSetOfCompatibleSupplies():
            self.spssim.installNormalSupply(supply)
        self.spssim.closeDoor()

if __name__ == '__main__':
    cu.runTests()
