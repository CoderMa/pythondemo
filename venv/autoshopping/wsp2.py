import requests


def building_multipart_xml2(print_file):
    # with open(print_file, "rb") as f:
    with open(print_file, 'r', encoding='cp1252') as f:
        # content = f.read().decode(encoding=encoding)
        content = f.read()
        # temp = content.decode()
        # temp = content.decode(errors='replace')
        print("@@content%%%%%$#@@@@@@@@@@@@@@@ =", content)


def wsptest():
    # 构造SOAP请求消息
    soap_request1 = """<s12:Envelope xmlns:s12="http://www.w3.org/2003/05/soap-envelope" xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:wse="http://schemas.xmlsoap.org/ws/2004/08/eventing" xmlns:ow="http://www.example.org/oceanwatch">
       <s12:Header>
         <wsa:Action>http://schemas.xmlsoap.org/ws/2004/08/eventing/GetStatus</wsa:Action>
         <wsa:MessageID>uuid:bd88b3df-5db4-4392-9621-aee9160721f6</wsa:MessageID>
         <wsa:ReplyTo>
           <wsa:Address>http://www.example.com/MyEventSink</wsa:Address>
         </wsa:ReplyTo>
         <wsa:To>http://www.example.org/oceanwatch/SubscriptionManager</wsa:To>
         <wse:Identifier>urn:uuid:2b4816a1-0457-1f0f-8cf9-bc0ff39973be</wse:Identifier>
       </s12:Header>
       <s12:Body>
         <wse:GetStatus />
       </s12:Body>
     </s12:Envelope>
    """

    soap_request = '<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:wse="http://schemas.xmlsoap.org/ws/2004/08/eventing" xmlns:ow="http://www.example.org/oceanwatch"><soap:Header><wsa:Action>http://schemas.xmlsoap.org/ws/2004/08/eventing/GetStatus</wsa:Action><wsa:MessageID>urn:uuid:bd88b3df-5db4-4392-9621-aee9160721f6</wsa:MessageID><wsa:ReplyTo><wsa:Address>http://www.example.com/MyEventSink</wsa:Address></wsa:ReplyTo><wsa:To>http://www.example.org/oceanwatch/SubscriptionManager</wsa:To><wse:Identifier>urn:uuid:2b4816a1-0457-1f0f-8cf9-bc0ff39973be</wse:Identifier></soap:Header><soap:Body><wse:GetStatus></wse:GetStatus></soap:Body></soap:Envelope>'

    # 发送SOAP请求
    response = requests.post("http://www.example.org/oceanwatch/SubscriptionManager", data=soap_request)

    # 打印响应内容
    print(response.text)






if __name__ == '__main__':
    # Create_Multipart_xml = building_multipart_xml2("./Letter_simplex.pwg")
    # print(Create_Multipart_xml)
    wsptest()
