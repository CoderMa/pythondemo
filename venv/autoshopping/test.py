# lst = ['aa', 'bb', 'cc', 'dd']
# for item in lst:
#     print(item)
#
# if item == 'aa':
#     print("************")
import argparse
import json
import logging
import requests

stackInfo = {'staging': {'environment': "stg", 'authUrl': 'https://stage.authz.wpp.api.hp.com',
                         'authKey': 'ZjczMGNhZTdmZTBlNDMwNzkzYmRlOGIyZDQ2ZmNmOTU6c3B2YXVtdHpyWFNEczZXUDY4Zkt6V1ZrbllFeFk3R00'},
             'pie': {'environment': "pie", 'authUrl': 'https://pie.authz.wpp.api.hp.com',
                     'authKey': 'ZjczMGNhZTdmZTBlNDMwNzkzYmRlOGIyZDQ2ZmNmOTU6MDlkMWZiZjBhM2Q2NDUyNWJjZDFiM2NiMDEwM2RlMmI'}}
programId = "61a65893-62c2-45cb-a0f7-c1e22108eab7"


# def getCloudID(ipAddress):
#     import phx_commonlib.ePrint.ePrintlib as ePrintlib
#     return ePrintlib.getCloudID(ipAddress)

# def isUnregisteredWithWebServices( ipAddress ):
#     import phx_commonlib.ePrint.ePrintlib as ePrintlib
#     return ePrintlib.isUnregisteredWithWebServices(ipAddress)
#
# def getTemrcCloudStack():
#     import phx_commonlib.ePrint.ePrintlib as ePrintlib
#     return ePrintlib.getTemrcCloudStack()

def getServicesEndPoint(stack):
    global endPoint
    serviceInfoUrl = "https://lookupsvc.smartcloudprint.com/v1/serviceinfos/stratus?environment={stack}&version=1.0".format(
        stack=stackInfo[stack]['environment'])
    response = requests.get(serviceInfoUrl)
    assert response.status_code == 200, "Failed to get services info, response code : {0}".format(response.status_code)
    endPoint = response.json()['endpoint']


def getAuthzToken(stack):
    global authToken
    logging.debug("Get Authorization Token")
    authHeaders = {'Content-Type': 'application/json', 'Authorization': "Basic %s" % stackInfo[stack]['authKey']}
    params = {'grant_type': 'client_credentials'}
    authorizeUrl = "{baseUrl}/openid/v1/token".format(baseUrl=stackInfo[stack]['authUrl'])
    response = requests.post(authorizeUrl, params=params, headers=authHeaders)
    assert response.status_code == 200, "Failed to post request for Auth token, response code : {0}".format(
        response.status_code)
    authToken = response.json()['access_token']


def createYetiPayload(printerIP, emailAddress):
    # Create yeti payload
    global authToken
    global endPoint
    payload = {
        "startIndex": 0,
        "maxResultSetSize": -1,
        "orderList": [{
            "propertyName": "resourceId",
            "ascending": "true"
        }],
        "criterionList": [{
            "operation": "eq",
            "propertyName": "email",
            "propertyValue": emailAddress,
            "propertyDataType": "java.lang.String"
        }]
    }

    logging.debug("Get HP ID information")
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-HTTP-Method-Override': 'GET',
               'Authorization': 'Bearer %s' % authToken, 'User-Agent': 'TEM'}
    url = "{baseUrl}/v2/usermgtsvc/users".format(baseUrl=endPoint)
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    assert response.status_code == 200, "Failed to get HP ID info, response code : {0}".format(response.status_code)

    # yetiPayload = {
    #     "deviceUUID": str(systemConfig.getVariable(printerIP, "systemApp", "eSystemDeviceUUID")),
    #     "programId": programId,
    #     "tenantId": str(response.json()['resourceList'][0]['systemTenantResourceId']),
    #     "userId": str(response.json()['resourceList'][0]['resourceId']),
    #     "deviceCloudId": str(getCloudID(printerIP))
    # }
    # return yetiPayload
    return response.text


def subscribeToYeti(printerIP, stack, emailAddress):
    global authToken
    global endPoint
    verifyJoinedYeti = True
    logging.debug("Get AuthZ token and create payload for yeti subscription")
    getServicesEndPoint(stack)
    getAuthzToken(stack)
    yetiPayload = createYetiPayload(printerIP, emailAddress)

    logging.info("Trying to subscribe to Yeti program...")
    subscribeUrl = "{baseUrl}/v2/catalogmgtsvc/programs/{programId}/deviceprogramsubscriptions".format(baseUrl=endPoint,
                                                                                                       programId=programId)
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
               'Authorization': 'Bearer %s' % authToken, 'User-Agent': 'TEM'}
    response = requests.post(subscribeUrl, headers=headers, json=yetiPayload)

    if response.status_code != 200:
        responseErrorMsg = response.json()['errors'][0]['message']
        if "Already existed" in responseErrorMsg:

            logging.info(
                "Already subscribed to Yeti program.\nThe given tenantId: {tenantId}, userId: {userId}, deviceUUID: {uuid} and deviceCloudId: {cloudId} already exist.".format(
                    tenantId=yetiPayload['tenantId'], userId=yetiPayload['userId'], uuid=yetiPayload['deviceUUID'],
                    cloudId=yetiPayload['deviceCloudId']))
            verifyJoinedYeti = False
        else:
            raise Exception("Response Code: {0}, {1}".format(response.status_code, responseErrorMsg))
    else:
        resourceId = response.json()['resourceId']

    if verifyJoinedYeti:
        # Verify successfully joined Yeti program
        url = "{subscribeUrl}/{resourceId}".format(subscribeUrl=subscribeUrl, resourceId=resourceId)
        response = requests.get(url, headers=headers)
        assert response.status_code == 200, "Failed to verify Yeti subscription, response code : {0}".format(
            response.status_code)
        # assert getCloudID(printerIP) == response.json()['deviceCloudId'], "Failed to subscribe to yeti program!"
        logging.info("Successfully subscribed to Yeti program.")


def createYetiPayload_partial():
    global authToken, endPoint, data
    payload = {
        "startIndex": 0,
        "maxResultSetSize": -1,
        "orderList": [{
            "propertyName": "resourceId",
            "ascending": "true"
        }],
        "criterionList": [{
            "operation": "eq",
            "propertyName": "email",
            "propertyValue": "SMBFW-hp_plus-test-printers@hp.com",
            "propertyDataType": "java.lang.String"
        }]
    }
    authToken = "eyJraWQiOiJhdXRoei1waWUtMTY5NjkzNTg3MyIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJmcV90ZW5hbnRfaWQiOiI1YzFjMjU0N2JmOTY1ZGVlMDA0NjVhM2IvYzFhNDY5ODctY2JkMy00NWRiLWI5NGEtYTY1NDQxMTZmYzJkIiwibmJmIjoxNzA1MzkzNDQwLCJncm91cF9wb2xpY3kiOiJNYW5hZ2VQcm9ncmFtcyxSZWFkTWVzc2FnZUh1YkNyZWRlbnRpYWxzLFJlYWREZXZpY2VzLE1hbmFnZVNlbGYsTWFuYWdlVmlydHVhbFByaW50ZXIsTWFuYWdlU01DbG91ZEFzc2Vzc21lbnQsUmVhZE93blNob3J0Y3V0cyxDcmVhdGVUb2tlbnMsTWFuYWdlRGV2aWNlc1N1cHBsaWVzLEV2ZW50UHVibGlzaGVyLE1lc3NhZ2VQdWJsaXNoZXIsTG9naW4sUmVhZEZlYXR1cmVzLEdlbmVyYWxTZXJ2aWNlLE1hbmFnZU9mZmVyaW5ncyxNYW5hZ2VEZXZpY2VNZXNzYWdlcyxSZWFkU3Vic2NyaXB0aW9ucyxNYW5hZ2VEZXZpY2VTZWN1cml0eSxSZWFkQWNjb3VudERhdGEsUmVhZE1hc3RlckJ1c2luZXNzTG9naWNTdWJzY3JpcHRpb25zLE1hbmFnZURldmljZXNNaXNyLFJlbWFuU3VwcGx5U2lnbixNYW5hZ2VJZGVudGl0eVNlcnZlckNvbmZpZyxTdXBwbHlBc3Nlc3NtZW50V3JpdGUsUmVhZFZpcnR1YWxQcmludGVyLFJlYWRJZGVudGl0eVNlcnZlckNvbmZpZyxSZWFkU29mdFJUUCxBdXRoWk1pZ3JhdGlvbixSZWFkTWFuaWZlc3QsSXBwSm9iQ2FwYWJpbGl0aWVzLE1hbmFnZU1hbmlmZXN0LEVkaXRVc2VyTWVzc2FnZXMsUmVhZERldmljZXNTdXBwbGllcyxNYW5hZ2VSdHBEZWxpdmVyeSxNYW5hZ2VCZW5lZml0cyxNYW5hZ2VDYXRhbG9nLE1hbnVmYWN0dXJpbmdFdmVudFN1YnNjcmliZXIsUmVhZFJlZ2lzdHJhdGlvbixSZWFkT3duTWFya3MsRmxlZXRFeGVjdXRpb24sUmVhZFByb3ZpZGVyLE1hbmFnZU93blNob3J0Y3V0cyxEZXZpY2VTdXBwbGllc0V2ZW50U3Vic2NyaWJlcixEZXZpY2VNaXNyRXZlbnRTdWJzY3JpYmVyLFJlYWRVc2VycyxNYW5hZ2VQcm92aWRlcixSZWFkRGV2aWNlc1J0cCxEZXZpY2VFdmVudFN1YnNjcmliZXIsUHJpbnRPblRoZUdvUHJpbnQgLFRlbGVtZXRyeVB1Ymxpc2hlcixNYW5hZ2VEZXZpY2VzTWVzc2FnaW5nLE1hbmFnZU93bk1hcmtzLFNlY3VyaXR5QXNzZXNzbWVudFJlYWQsUmVhZENvbGxlY3Rpb25Qcm9maWxlLFJlYWRGbGVldCxNYW5hZ2VEZXZpY2VzQml6TW9kZWwsTWFuYWdlU29mdFJUUCxSZWFkQWNjb3VudHMsUmVhZEJlbmVmaXRzLE1hbmFnZUZsZWV0LE1hbmFnZUhwcGx1c1Byb2dyYW1Pd25lcnNoaXAsUmVhZENvbm5lY3Rpb25TZXR0aW5ncyxQcmludE9uVGhlR29NYW5hZ2UsQ2xpZW50VGVsZW1ldHJ5UHVibGlzaGVyLFJlYWRNYW51ZmFjdHVyaW5nLE1hbmFnZVJlZnVuZHMsTWFuYWdlRGV2aWNlc1J0cCxNYW5hZ2VBZGRyZXNzLE1lcmdlRG9jdW1lbnRzLFJlYWRBZGRyZXNzLEFkbWluaXN0ZXJUb2tlbnMsVWNkZVN1cHBvcnQsTWFuYWdlVXNlcnMsTWFuYWdlUmVwYWlyRGV2aWNlLERldmljZVJ0cEV2ZW50U3Vic2NyaWJlcixSZWFkTWVzc2FnZUh1YkNhdGFsb2csUmVhZEhwUGx1c1Byb2dyYW0sTWFuYWdlUmVwYWlyLE1hbmFnZU1lc3NhZ2VzLFJlYWRSUEwsTWFuYWdlQ29sbGVjdGlvblByb2ZpbGUsTWFuYWdlQml6TW9kZWxSZXBhaXIsTWFuYWdlU3Vic2NyaXB0aW9ucyxSZWFkUnRwRGVsaXZlcnksTWFuYWdlQWNjb3VudHMsTWFuYWdlVG9rZW5zLERldmljZVNlY3VyaXR5RXZlbnRTdWJzY3JpYmVyLE1hbmFnZVNlcnZpY2UsUHJpbnRPblRoZUdvUmVhZCxTZWN1cml0eUFzc2Vzc21lbnRNYW5hZ2UgLFdyaXRlTWVzc2FnZUhpc3RvcnksSU9USW50ZXJuYWwsUmVhZFNNQ2xvdWRBc3Nlc3NtZW50LE1hbmFnZU1hbnVmYWN0dXJpbmcsUmVhZFVzZXJNZXNzYWdlcyxSZWFkSHBwbHVzUHJvZ3JhbU93bmVyc2hpcCxSZWFkQ2F0YWxvZyxNYW5hZ2VEZXZpY2VzLFJlYWRTdXBwbGllc09wZXJhdGlvbmFsRGF0YSxTdXBwbHlBc3Nlc3NtZW50UmVhZCxEZXZpY2VNZXNzYWdpbmdFdmVudFN1YnNjcmliZXIiLCJwb2xpY3lfaWQiOiJmNzMwY2FlN2ZlMGU0MzA3OTNiZGU4YjJkNDZmY2Y5NSIsInNjb3BlIjoiamVlcy5ocC5jb20vam9icyBzdG9yYWdlc2VydmljZS53cHAuYXBpLmhwLmNvbS9maWxlLmNyZWF0ZSBhdmRscy53cHAuYXBpLmhwLmNvbS90ZW5hbmN5LmluZm8udXBkYXRlIHdwcC5hcGkuaHAuY29tL2Jhc2ljIGRhdGFicmlkZ2UuYXBpLmhwLmNvbS9wcmludGVyLmNvbW11bmljYXRlLmFsbCBvdHAucHJpbnRlci5hcGkuaHAuY29tL2tleS53cml0ZSBvZmZsaW5lX2FjY2VzcyBhdmRscy53cHAuYXBpLmhwLmNvbS9wcmludGVyLmNsYWltLmNvbmZpZ3VyZSBhdnJlZy53cHAuYXBpLmhwLmNvbS9wcmludGVyLmluZm8ucmVhZCB3bnMud3BwLmFwaS5ocC5jb20vZXZlbnQubm90aWZ5IHdzLWhwLmNvbS9jbGllbnRtZ250L2NsaWVudC5SRUFEIHdzLWhwLmNvbS9kZXZpY2VzL2RldmljZXMuY2xhaW0uV1JJVEUgZGNzLndwcC5hcGkuaHAuY29tL293bmVyc2hpcC5yZWFkIGRjcy53cHAuYXBpLmhwLmNvbS9vd25lcnNoaXAuZGV0YWlsIGRjcy53cHAuYXBpLmhwLmNvbS9kZXZpY2UuaWRlbnRpdHkgYW1zLndwcC5hcGkuaHAuY29tL2F1dGhvcml6ZSBlbWFpbGNvbmZpZy53cHAuYXBpLmhwLmNvbS9lbWFpbC5yZWFkIG9wZW5pZCB3cHAuYXBpLmhwLmNvbS9kZXZpY2UubG9va3VwIGF2Y21udC53cHAuYXBpLmhwLmNvbS9jb25uLnByb2ZpbGUgc2VydmljZWRpc2NvdmVyeS5ocC5jb20vc2VydmljZS5kaXNjb3ZlciBhdXRoei5hcGkuaHAuY29tL2NsaWVudC5yZWFkIHNpZXJyYS53cHAuYXBpLmhwLmNvbS9yZW5kZXIgYW1zLndwcC5hcGkuaHAuY29tL2RldmljZS5jb25maWd1cmUgYXZkc3Qud3BwLmFwaS5ocC5jb20vc3RhdHVzIHdzLWhwLmNvbS9hdXRoei9jbGllbnQucHJvZHVjdGluZm8uUkVBRCBqZWVzLmhwLmNvbS9jb25zZW50IGRjcy53cHAuYXBpLmhwLmNvbS9vd25lcnNoaXAgYXZyZWcud3BwLmFwaS5ocC5jb20vcHJpbnRlci52YWxpZGF0ZSB3bnMud3BwLmFwaS5ocC5jb20vc3Vic2NyaWJlIGF2ZGxzLndwcC5hcGkuaHAuY29tL3ByaW50ZXIuY2xhaW0uaW5mby5yZWFkIiwiaXNzIjoiaHR0cHM6Ly9waWUuYXV0aHoud3BwLmFwaS5ocC5jb20vIiwiYWNjZXNzX3BvbGljaWVzIjp7IjVjMWMyNTQ3YmY5NjVkZWUwMDQ2NWEzYi9jMWE0Njk4Ny1jYmQzLTQ1ZGItYjk0YS1hNjU0NDExNmZjMmQvKioiOiJmNGU4OTlhZTgzM2YwZjM2ZDE1NDVkZTczYmZjM2EzNTY1MjA0NGU5IiwiNWMxYzI1NDdiZjk2NWRlZTAwNDY1YTNiL2MxYTQ2OTg3LWNiZDMtNDVkYi1iOTRhLWE2NTQ0MTE2ZmMyZCI6ImY0ZTg5OWFlODMzZjBmMzZkMTU0NWRlNzNiZmMzYTM1NjUyMDQ0ZTkifSwiZXhwIjoxNzA1Mzk3MDQwLCJpYXQiOjE3MDUzOTM0NDAsImp0aSI6ImEwYzBkODRhLWYyNjEtNGFlNC05YzZkLWE2MDRlYmI4MTRlYV9BVCIsImNsaWVudF9pZCI6ImY3MzBjYWU3ZmUwZTQzMDc5M2JkZThiMmQ0NmZjZjk1In0.I-fta1rIA_LVq2FAkrArK0haUzKXffvPkDCxNTB_W9wEUDw-pAp3FIJjSNNqu0SyC_F0JXGqDoRFiNc-O17iMjlDaq7efdCLwHEhoc9-ey76UbkqHSvDPWDTTdzyVSGQNPLs3WwxnvA-qoSg2l2aKH6D2EbQo1f4rGK9jRqEfAvgRHTOllR0vuosXtViy84aBWRfI11ks0bMBzQJpCvV04HuyMfTzzs3Fg6X04nH6DPk586M16Rs6MIAdjobDFNgLu4LEQUngvJsyGK21JEnI_wqtGKETcUEDs_IGKgqX91Os18_17xcsppMyQpc__6yl0Notp3MUUszMB15oBiZOw"
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'X-HTTP-Method-Override': 'GET',
               'Authorization': 'Bearer %s' % authToken, 'User-Agent': 'TEM'}
    endPoint = "https://stratus-pie.tropos-rnd.com"
    url = "{baseUrl}/v2/usermgtsvc/users".format(baseUrl=endPoint)
    # data = json.dumps(payload)
    # print(1, data, type(data))
    # print(2, payload, type(payload))
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.status_code)
    print(response.text)
    # assert response.status_code == 200, "Failed to get HP ID info, response code : {0}".format(response.status_code)


# createYetiPayload_partial()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", dest="ip", help="the ip address (or friendly name) of the printer")
    parser.add_argument("-s", "--stack", dest="stack", default=None,
                        help="Stack name to patch the printer to, e.g: Pie or Staging. Production stack is not supported. Default is read from temrc.")
    parser.add_argument("-e", "--email", dest="email", help="Email address for your HP smart account.")
    args = parser.parse_args()

    # stack = getTemrcCloudStack().lower() if not args.stack else args.stack.lower()
    # stack = "pie"
    stack = "staging"
    printerIP = "15.26.248.107"
    # emailAddress = "SMBFW-hp_plus-test-printers@hp.com" if not args.email else args.email
    emailAddress = "iiqa_mjl+2610us2@outlook.com" if not args.email else args.email
    if stack not in ["pie", "staging"]:
        raise Exception("Unsupported stack {0} for patching".format(stack))
    # if isUnregisteredWithWebServices(printerIP):
    #     raise Exception("Device not registered with Web services, please register!")

    subscribeToYeti(printerIP, stack, emailAddress)
