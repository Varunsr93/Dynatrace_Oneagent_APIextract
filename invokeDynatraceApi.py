#import requests
import urllib3
import json

http = urllib3.PoolManager()

def get_with_headers(api_url, Auth):
    response = ""
    headers = {"Authorization": "Api-Token " + Auth.strip()}
    try:

        response = http.request('GET', api_url, headers=headers)

        if response.status == 200:
            print("----success response from api call----")
            return json.loads(response.data.decode('utf-8'))
    except:
        raise Exception("***An exception occurred while calling the API endpoint!****")
    # except requests.exceptions.RequestException as err:
    #     return "oops: " + str(err)


def dt_get_requests(URL, token,type,input):
    api_dict = {}
    api_dict["HostList"] = URL + "api/v1/oneagents?relativeTime=10mins&availabilityState=MONITORED"
    api_dict["nextPage"] = URL + "api/v1/oneagents?relativeTime=10mins&availabilityState=MONITORED&nextPageKey=" + input

    response = get_with_headers(api_dict[type], token)

    return response

