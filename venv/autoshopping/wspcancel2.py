HTTP/1.1 400 Bad Request
Server: gSOAP/2.7
Content-Type: application/soap+xml; charset=utf-8
Content-Length: 1614
Connection: close

<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:wsa="http://schemas.xmlsoap.org/ws/2004/08/addressing" xmlns:wse="http://schemas.xmlsoap.org/ws/2004/08/eventing" xmlns:xmime="http://www.w3.org/2004/06/xmlmime" xmlns:wprt20="http://tempuri.org/wprt20.xsd" xmlns:hpprt="http://www.hp.com/schemas/imaging/con/hpprt/2014/08/22" xmlns:wprt="http://schemas.microsoft.com/windows/2006/08/wdp/print"
xmlns:wprt2="http://schemas.microsoft.com/windows/2014/04/wdp/printV20">
<SOAP-ENV:Header>
<wsa:MessageID SOAP-ENV:mustUnderstand="true">urn:uuid:28a17de2-e2ce-1f0d-945c-bc0ff39973be</wsa:MessageID>
<wsa:RelatesTo SOAP-ENV:mustUnderstand="true">urn:uuid:5332548-a3f9-11e3-87bf-f937cd6c3c</wsa:RelatesTo>
<wsa:To SOAP-ENV:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/08/addressing/role/anonymous</wsa:To>
<wsa:Action SOAP-ENV:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2004/08/addressing/fault</wsa:Action>
</SOAP-ENV:Header>

<SOAP-ENV:Body>
<SOAP-ENV:Fault>
<SOAP-ENV:Code>
<SOAP-ENV:Value>SOAP-ENV:Sender</SOAP-ENV:Value>
<SOAP-ENV:Subcode>
<SOAP-ENV:Value>wprt:ClientErrorMultipleDocumentsNotSupported</SOAP-ENV:Value>
</SOAP-ENV:Subcode>

</SOAP-ENV:Code>
<SOAP-ENV:Reason>
<SOAP-ENV:Text>Print Service does not support jobs with multiple documents.</SOAP-ENV:Text>
</SOAP-ENV:Reason>
</SOAP-ENV:Fault>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>