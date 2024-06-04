import base64
import re

content = b'<xml>'
if content.startswith(b'<'):
    print('right!!')

if __name__ == '__main__':
    newPassword = '12345678'
    newPassword = base64.encodebytes(newPassword.encode()).decode().replace('\n', '')
    newPassword2 = base64.encodebytes(newPassword.encode()).decode()
    print(type(newPassword))
    print(newPassword)
    print(newPassword2)
    print("-"*30)

    operator_confirmation ="\nIf Printer PIN is shown as {0} in the 'Configuration report' type YES, else NO and hit OK...\n".format('12345678')
    print(operator_confirmation)

    result = 'MDNS NAME = HP LaserJet MFP M237sdne (9973B0)'
    bounjourName = re.search("MDNS NAME = (.*)", result)
    print(bounjourName.group(1))



