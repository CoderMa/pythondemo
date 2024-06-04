
from scapy.all import *


def send_llmnr_query(query_name):
    # 构造LLMNR查询数据包
    llmnr_query = Ether() / IP(dst="224.0.0.252") / UDP(dport=5355) / LLMNRQuery(qdcount=1,
                                                                                 qd=DNSQR(qname=query_name, qtype="A",
                                                                                          qclass="IN"))

    # 发送LLMNR查询并接收响应
    response = srp(llmnr_query, timeout=2, verbose=False)

    # 处理响应
    for _, packet in response:
        if packet.haslayer(DNS):
            dns_response = packet[DNS]
            if dns_response.an:
                print("LLMNR Response received for {query_name}:")
                for answer in dns_response.an:
                    if isinstance(answer, DNSRR):
                        print(f"IP Address: {answer.rdata}")
            else:
                print("No LLMNR Response received for {query_name}")


# 发送LLMNR查询
# send_llmnr_query("printer")
send_llmnr_query("15.26.248.108")
