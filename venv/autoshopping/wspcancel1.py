from six.moves import input

def set_cancel_jobid(Jobid):
    try:
        if Jobid != None:
            #################Setting the Job Id into Cancel job request xml alone############
            Send_JobId_request = open(path + '/phx_test/io/wsp/helper_file/canceljobid.xml', 'rb')
            partial_send_request_xml = Send_JobId_request.read()
            ########Setting Job Id using updatevale method from xmlUtill lib ###################
            setvalue = xmlUtil.updateValue(partial_send_request_xml, '/SOAP-ENV:Envelope/SOAP-ENV:Body/ \
            wprt:CancelJobRequest/wprt:JobId', Jobid)
            logging.info("Cancel Job id set successfully")
            Send_JobId_request.close()
            return setvalue
        else:
            logging.error("Invalid cancel Job id")
    except Exception as e:
        logging.error("ERROR:Unable to set Job Id request")
        logging.info('Exception Caught!:%s', e)


def updateValue(xml, xpaths, values, ns=namespaces.ALL_NAMESPACES):
    if isinstance(xml, bytes):
        xml = xml.decode()

    if isinstance(xpaths, str):
        xpaths = [xpaths]
    elif isinstance(xpaths, tuple):
        xpaths = list(xpaths)

    if isinstance(values, str):
        values = [values]
    elif isinstance(values, tuple):
        values = list(values)

    element = []

    xmlTree = etree.parse(StringIO(xml))

    for i in range(len(xpaths)):
        element = xmlTree.xpath(xpaths[i], namespaces=ns)

        if len(element) > 0:
            element[0].text = values[i]

    return etree.tostring(xmlTree)


# Helps to cancel the Job request
def cancel_jobid(printerIp, cancel_job_xml):
    host = printerIp
    port = 3910
    request = cancel_job_xml
    data = " ".join(sys.argv[1:])
    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response_str = ""
    try:
        sock.connect((host, port))
        sock.sendall(request)
        # Receive data from the server and shut down
        while True:
            response = sock.recv(2048).decode()
            time.sleep(2)
            if response == "":
                break
            else:
                response_str = response_str + response
        logging.info("cancel job request captured successfully")
        sock.close()
        return response_str
    except  Exception as e:
        logging.error("ERROR:Unable to proceed the Cancel job request")
        logging.info('Exception Caught!:%s', e)


if __name__ == '__main__':
    LF = '/n'
