import re
import socket
import time
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA256
from Crypto.Signature import DSS

def test(a):
    if a == 1:
        current = 1100
    else:
        current = 0

    if a == 1:
        newv = 1101
    else:
        newv = 1

    if current == newv:
        raise Exception("... error")
    print(current, "..current")
    print(newv, "...newv")





# Consumes 1% life by printing pages with proper ISO coverage to achieve 1% life reduction
def consumeFormatterPixelCountingLife(self, supply):
    twoK = 2000
    pageCount = 0
    auth_state = self.sps.CanonAuthStateVariable(
        self.sps.sps_get_var(self.printerIP, "AuthState{0}".format(supply.name)))
    colorSupported = True if 'Cyan' in self.psi.getSupplyNames() else False
    page_yield = self.sps.sps_get_var(self.printerIP, 'PageYield{}'.format(supply.name))
    isoCoverageNeeded = int(
        page_yield * 0.99)  # HACK!!! Use 1% less than the yield so we don't barely consume more than 1%
    out_reached_value = self.sps.sps_get_var(self.printerIP, 'OutReached{0}'.format(supply.name))
    # Out reached value should be 1 after reaching very low
    if out_reached_value == 1:
        current_life = int(self.sps.sps_get_var(self.printerIP, 'PageCount{0}'.format(supply.name)))
    else:
        current_life = int(self.sps.sps_get_var(self.printerIP, 'TonerLevelRemaining{0}'.format(supply.name)))
    (full_pages, remainder_iso) = divmod(isoCoverageNeeded, twoK)
    if full_pages > 0:
        # We are using formatter pixel counting so simulate printing several full coverage pages
        self.printJob(full_pages, str(twoK), isColor=colorSupported)
        self.setLifeChange(supply.name)
        pageCount += full_pages
        time.sleep(3)
    if remainder_iso > 0:
        self.printJob(1, str(remainder_iso), isColor=colorSupported)
        self.setLifeChange(supply.name)
        pageCount += 1
        time.sleep(3)
    if auth_state != self.sps.CanonAuthStateVariable.eAuthUsedMoved:  # Don't expect TonerLevelRemaining to decrement for used supplies
        if out_reached_value == 1:
            new_life = int(self.sps.sps_get_var(self.printerIP, 'PageCount{0}'.format(supply.name)))
        else:
            new_life = int(self.sps.sps_get_var(self.printerIP, 'TonerLevelRemaining{0}'.format(supply.name)))
        if new_life == current_life:
            raise Exception("Life didn't get consumed")
    return pageCount

def divmodetest(isoCoverageNeeded, twoK=2000):
    (full_pages, remainder_iso) = divmod(isoCoverageNeeded, twoK)
    print(full_pages)
    print(remainder_iso)


def create_signature(hex_cleartext):
    cleartext = bytearray.fromhex(hex_cleartext)
    # key_pair = get_key_pair()
    key_pair = '11223345'
    signer = DSS.new(key_pair, mode='fips-186-3', encoding='binary')
    signature = signer.sign(SHA256.new(cleartext))
    return signature


def send_command(sock, command, wait_time=1):
    sock.sendall((command.strip() + '\n').encode())
    time.sleep(wait_time)
    result = ""
    while True:
        response = sock.recv(4096).decode()
        time.sleep(wait_time)
        if response == "":
            break
        else:
            result += response
    print(result, '**************')
    return result


def getWifiDirectPassword(self):
    result = telnetDebug.TelnetDebug("io/get DIRECT_PRINT_PASSPHRASE", self.printerIP, True)
    password = re.search("DIRECT_PRINT_PASSPHRASE = (.*)", result)
    return password.group(1)


def main():
    host = '15.26.251.100'  # Replace with your printer's IP address
    port = 23000  # Telnet default port
    username = 'admin'  # Replace with your Telnet username
    password = 'adminpassword'  # Replace with your Telnet password
    mdns_name = 'HP LaserJet MFP M237sdne (9973B0)'

    # Create a socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        # Receive initial response
        response = sock.recv(4096).decode()
        print(response)

        # # Send username
        # if 'login:' in response:
        #     send_command(sock, username)
        #
        # # Send password
        # response = sock.recv(4096).decode('ascii')
        # if 'Password:' in response:
        #     send_command(sock, password)

        # Send MDNS_NAME command
        # mdns_command = f'io/set MDNS_NAME "{mdns_name}"'
        # mdns_command = f'io/set MDNS_NAME {mdns_name}'
        # send_command(sock, mdns_command)

        # Optionally save the configuration
        # send_command(sock, 'save')

        # Exit the session
        # send_command(sock, 'exit')

        create_signature()



if __name__ == '__main__':
    # main()
    # divmodetest(2400)
    test(1)
    test(2)
    test(3)





