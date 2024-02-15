import json
import requests

from satori import satori_common

def get_locations_by_datastore(headers, apihost, account_id, datastore_id):

    url = "https://{}/api/locations/{}/query?pageSize=10000&dataStoreId={}".format(apihost, 
                                                                                   account_id, 
                                                                                   datastore_id)
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("EXCEPTION: ", type(err))
    else:
        return [ response.json()['count'], response.json()['records'] ]