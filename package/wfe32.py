import requests
import json


def get_token(username="jtao", password="verint1!"):

    url = "https://wfe32.verint.live/wfo/rest/core-api/auth/token"

    payload = json.dumps({
    "user": username,
    "password": password
    })
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'JSESSIONID=dUzOs0JX5rMQp6yeQS8VoOm1Pvwv-O_wdHyx9VV92ZJFNZ6ukSWT!-2101935040; _WL_AUTHCOOKIE_JSESSIONID=nYJyxMNhjT3wsPd2Vp93'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    token = response.json()["AuthToken"]["token"]

    return token

def get_org_id(token, org_name):

    url = "https://wfe32.verint.live/wfo/user-mgmt-api/v1/organizations"

    payload = {}
    headers = {
        'Impact360AuthToken': token,
        'Cookie': 'JSESSIONID=dUzOs0JX5rMQp6yeQS8VoOm1Pvwv-O_wdHyx9VV92ZJFNZ6ukSWT!-2101935040; _WL_AUTHCOOKIE_JSESSIONID=nYJyxMNhjT3wsPd2Vp93'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    for org in response.json()["data"]:
        if org["attributes"]["name"] == org_name:
            org_id = org["id"]
            break
    else:
        org_id = None

    return org_id

def get_timeoff(
        token, 
        org_id, 
        start_time="2013-10-01T07:00:00Z", 
        end_time="2033-10-01T07:00:00Z",
        status=2047):

    url = f"https://wfe32.verint.live/wfo/rest/rm-api/timeoff/get?organizationId={org_id}&startTime={start_time}&endTime={end_time}&status={status}"

    payload = {}
    headers = {
        'Impact360AuthToken': token,
        'Cookie': 'JSESSIONID=qOHPdjGxkhNuZYTbGSojHIh3HBsZ8LKN0YLgl3I4SKsgOmCC3CN4!-2101935040; _WL_AUTHCOOKIE_JSESSIONID=CCcRUbUVtmCvRY141Z1C'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def get_an_employee(token, id):

    url = f"https://wfe32.verint.live/wfo/user-mgmt-api/v1/employees/{id}"

    payload = {}
    headers = {
    'Impact360AuthToken': token,
    'Cookie': 'JSESSIONID=2-rP381liI6CpwqHMmfpnw4To-f1e5de7f9tiPH5zc3ip0mdGjr2!-2101935040; _WL_AUTHCOOKIE_JSESSIONID=7WBLrZsVrX.e56EhyCxA'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

def process_timeoff_request(token, request_id, action_code):

    url = "https://wfe32.verint.live/wfo/rest/rm-api/timeoff/processTimeoffRequest"

    payload = json.dumps({
        "timeoffRequestId": request_id,
        "actionCode": action_code
    })
    headers = {
    'Impact360AuthToken': token,
    'Content-Type': 'application/json',
    'Cookie': 'JSESSIONID=BgzQHfJ24RF9mQdz1bHfoUluzG72E3MqyifXAmQS572RgP-JULTW!-2101935040; _WL_AUTHCOOKIE_JSESSIONID=JVc8uARmYufGWGG7zk4l'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()

    
if __name__ == "__main__":
    pass
