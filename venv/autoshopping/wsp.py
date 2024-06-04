# def building_multipart_xml(printerIp, partial_sendjob_response, print_file):
import base64
# class A:



def building_multipart_xml(print_file):
    # if (partial_sendjob_response == None):
    #     logging.info("ERROR:Unable to create Multipart xml")
    #     return False
    ############Creating multipart xml headers(Don't allign)##############################
    Create_Multipart_xml = b""
    boundaryline_start = b"""--==/M14b4Q+AaLKDhTt1KMYtzg3B01HEVADh279uL7umG4pnLXcVj0CWV6YJvfN==\r"""
    boundaryline_end = b"""--==/M14b4Q+AaLKDhTt1KMYtzg3B01HEVADh279uL7umG4pnLXcVj0CWV6YJvfN==--\r"""

    header1 = b"""POST / HTTP/1.1\r
User-Agent: gSOAP/2.7\r
Content-Type: multipart/related; boundary="==/M14b4Q+AaLKDhTt1KMYtzg3B01HEVADh279uL7umG4pnLXcVj0CWV6YJvfN==";\
type="application/xop+xml"; start="<SOAP-ENV:Envelope>"; start-info="application/soap+xml; charset=utf-8"\r
Connection: close\r
SOAPAction: "http://schemas.microsoft.com/windows/2006/08/wdp/print/SendDocument"\r
\r
"""
    header2 = b"""Content-Type: application/xop+xml; charset=utf-8; type=application/soap+xml\r
Content-Transfer-Encoding: binary\r
Content-ID: <SOAP-ENV:Envelope>\r
\r
"""
    header3 = b"""Content-Type: text/html\r
Content-Transfer-Encoding: binary\r
Content-ID: <id26>\r
\r
"""
    header4 = b"""<?xml version="1.0" encoding="UTF-8"?>"""
    CLRF = b"""\r"""
    LF = b'\n'
    partial_sendjob_response = b'<xml></xml>'
    ####################################################################################################
    try:
        file_handle = open(print_file, "rb+")
        # file_add = file_handle.read().decode(errors='ignore')
        file_add = file_handle.read()
        # print(file_add)
        Create_Multipart_xml = header1 + boundaryline_start + LF + header2 + header4 + LF + partial_sendjob_response + CLRF + LF \
                               + boundaryline_start + LF + header3 + file_add + CLRF + LF + boundaryline_end

        # Create_Multipart_xml = header1 + boundaryline_start + "\n" + header2 + header4 + "\n" + CLRF + "\n" \
        #                        + boundaryline_start + "\n" + header3 + file_add + CLRF + "\n" + boundaryline_end

        file_handle.close()
        return Create_Multipart_xml
    except Exception as e:
        print('Exception Caught!:%s', e)


#############################################################################################################

def ws_create_printjob_processing(options):
    test_result = False
    try:
        #createprintjob xml from lib
        createprintjob_xml = wstestlib.support_xmlfile[1]
        handle_file = wstestlib.openfile(createprintjob_xml)
        #send createprintjob request
        createprintjob_response =wstestlib.createprintjob_request(options.ip,handle_file)
        #validate the create printjob response
        validate_createprintjob_response=wstestlib.validate_job_response(createprintjob_response)
        if validate_createprintjob_response == True:
            logging.info('Createprint job request is successfull')
            #get job id
            job_id =wstestlib.get_jobid(createprintjob_response)
            #set job id
            setjobidxml =wstestlib.set_jobid(job_id)
            #test input file
            print_file = wstestlib.Test_File[1]
            #building multipart xml
            create_multipart_xml_request =wstestlib.building_multipart_xml(options.ip,setjobidxml,print_file)
            #send senddocument request thru multiprocessing to get processing job status
            status = multiprocessing.Queue()
            x = multiprocessing.Process(target=send_document, args=(options.ip, create_multipart_xml_request, status))
            x.start()
            # getjob status untill jobs is in processing state
            while True:
                getactivejob_result = ws_getactive_job(options)
                if getactivejob_result == 'Processing' or getactivejob_result == 'Completed':
                    break
            if not getactivejob_result == 'Processing':
                logging.info("Job is not in processing state")
                return test_result
            # validate the send document response
            x.join()

            validate_senddocument_response  =wstestlib.validate_job_response(status.get())
            if validate_senddocument_response == True:
                logging.info('senddocument request is successfull')
                test_result = True
            else:
                logging.error('ERROR:Invalid senddocuemnt response')
                logging.info('------------------Capturing the invalid senddocument response---------------------')
                logging.error(senddocument_response)
                logging.info('----------------Canceling the original job id to reset the printer----------------')
                create_cancel_job_xml =wstestlib.set_cancel_jobid(job_id)
                cancel_job =wstestlib.cancel_jobid(options.ip,create_cancel_job_xml)
                validate_cancel_job =wstestlib.validate_job_response(cancel_job)
                if validate_cancel_job == True:
                    logging.info('Valid cancel job response')
                else:
                    logging.error('Bad cancel job response')
                    logging.info(cancel_job)
        else:
            logging.error('ERROR:Bad createprintjob response')
            logging.info('----------------Capturing the bad createprintjob response---------------------')
            logging.error(createprintjob_response)
    except Exception as e:
        logging.error('ERROR:Unable to proceed senddocument request test')
        logging.info('Exception Caught!:%s',e)
        test_result = False
        return test_result




def building_multipart_xml2(print_file):
    # with open(print_file, "rb+") as f:
    #     raw_data = f.read()
    #     result = chardet.detect(raw_data)
    #     encoding = result['encoding']
    #     # windows - 1253
    #     print("@@encoding =", encoding)

    # with open(print_file, "rb") as f:
    with open(print_file, 'r') as f:
        # content = f.read().decode(encoding=encoding)
        content = f.read()
        # temp = content.decode()
        # temp = content.decode(errors='replace')
        print("@@content%%%%%$#@@@@@@@@@@@@@@@ =", content)

    return "end"


def run_test(options):
    try:
        return_value = False
        Expected_SF_Message = wstestlib.Lastdoc_Error_list[0:3]
        testType = options.test
        if testType == "all" or testType == "senddocument_dealy_10":
            logging.info('----------------Running SendDocument request delay with 10 seconds test----------------')
            delay = 10
            # calling ws_create_printjob method
            return_value, response = ws_create_printjob(options, delay)
            if return_value == True:
                logging.info('-------------------------------------------------------------------------------')
                logging.info('Test Name:SendDocument request delay with 10 seconds test:Passed')
                logging.info('-------------------------------------------------------------------------------')
            else:
                logging.info('-------------------------------------------------------------------------------')
                logging.info('Test Name:SendDocument request delay with 10 seconds test:Failed')
                logging.info('-------------------------------------------------------------------------------')

        if testType == "all" or testType == "senddocument_dealy_61":
            logging.info('----------------Running SendDocument request delay with 61 seconds test----------------')
            delay = 65
            # calling ws_create_printjob method
            return_value, response = ws_create_printjob(options, delay)
            if return_value == False:
                get_soapfault_details = wstestlib.finding_soapfault(response)
                validate_soapfault = wstestlib.compare(Expected_SF_Message, get_soapfault_details)
                if validate_soapfault == True:
                    logging.info('Valid Soapfault message')
                    logging.info('--------------------------------------------------------------------------------')
                    logging.info('Test Name:SendDocument request delay with 61 seconds test:Passed')
                    logging.info('--------------------------------------------------------------------------------')
                    return_value = True
                else:
                    logging.info('Invalid soapfault message')
                    logging.info('--------------------------------------------------------------------------------')
                    logging.info('Test Name:SendDocument request delay with 61 seconds test:Failed')
                    logging.info('--------------------------------------------------------------------------------')
            else:
                logging.info('--------------------------------------------------------------------------------')
                logging.info('Test Name:SendDocument request delay with 61 seconds test:Failed')
                logging.info('--------------------------------------------------------------------------------')
                return_value = False
        return return_value
    except Exception as e:
        logging.error('ERROR:Unable to run test')
        logging.info('Exception Caught!:%s', e)


def ws_create_printjob_processing(options,):
    test_result = False
    try:
        #createprintjob xml from lib
        createprintjob_xml = wstestlib.support_xmlfile[1]
        handle_file = wstestlib.openfile(createprintjob_xml)
        #send createprintjob request
        createprintjob_response =wstestlib.createprintjob_request(options.ip,handle_file)
        #validate the create printjob response
        validate_createprintjob_response=wstestlib.validate_job_response(createprintjob_response)
        if validate_createprintjob_response == True:
            logging.info('Createprint job request is successfull')
            #get job id
            job_id =wstestlib.get_jobid(createprintjob_response)
            #set job id
            setjobidxml =wstestlib.set_jobid(job_id)
            #test input file
            print_file = wstestlib.Test_File[1]
            #building multipart xml
            create_multipart_xml_request =wstestlib.building_multipart_xml(options.ip,setjobidxml,print_file)
            #send senddocument request thru multiprocessing to get processing job status
            status = multiprocessing.Queue()
            x=multiprocessing.Process(target=send_document, args=(options.ip,create_multipart_xml_request,status))
            x.start()
            #getjob status untill jobs is in processing state
            while True:
                getactivejob_result = ws_getactive_job(options)
                if getactivejob_result == 'Processing' or getactivejob_result == 'Completed':
                    break
                if not getactivejob_result == 'Processing':
                    logging.info("Job is not in processing state")
                    return test_result
                # validate the send document response
            x.join()

            validate_senddocument_response  =wstestlib.validate_job_response(status.get())
            if validate_senddocument_response == True:
                logging.info('senddocument request is successfull')
                test_result = True
            else:
                logging.error('ERROR:Invalid senddocuemnt response')
                logging.info('------------------Capturing the invalid senddocument response---------------------')
                logging.error(status.get())
                logging.info('----------------Canceling the original job id to reset the printer----------------')
                create_cancel_job_xml =wstestlib.set_cancel_jobid(job_id)
                cancel_job =wstestlib.cancel_jobid(options.ip,create_cancel_job_xml)
                validate_cancel_job =wstestlib.validate_job_response(cancel_job)
                if validate_cancel_job == True:
                    logging.info('Valid cancel job response')
                else:
                    logging.error('Bad cancel job response')
                    logging.info(cancel_job)
        else:
            logging.error('ERROR:Bad createprintjob response')
            logging.info('----------------Capturing the bad createprintjob response---------------------')
            logging.error(createprintjob_response)
    except Exception as e:
        logging.error('ERROR:Unable to proceed senddocument request test')
        logging.info('Exception Caught!:%s',e)
        test_result = False
        return test_result


if __name__ == '__main__':
    Create_Multipart_xml = building_multipart_xml2("./Letter_simplex.pwg")
    print(Create_Multipart_xml)
