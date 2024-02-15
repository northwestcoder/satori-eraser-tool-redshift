import json
import requests

def satori_auth(satori_serviceaccount_id, satori_serviceaccount_key, apihost):
    auth_headers = {'content-type': 'application/json','accept': 'application/json'}
    auth_url = "https://{}/api/authentication/token".format(apihost)
    auth_body = json.dumps(
    {
        "serviceAccountId": satori_serviceaccount_id,
        "serviceAccountKey": satori_serviceaccount_key
    })
    try:
        r = requests.post(auth_url, headers=auth_headers, data=auth_body)
        response = r.json()
        satori_token = response["token"]
    except Exception as err:
        print("Bearer Token Failure: :", err)
        print("Exception TYPE:", type(err))
    else:
        return satori_token