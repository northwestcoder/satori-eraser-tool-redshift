import json
import requests
import io

from satori import satori_common

def get_all_datastores(headers, apihost, satori_account_id):

	url =  "https://{}/api/v1/datastore?accountId={}&pageSize=500".format(apihost, satori_account_id)
	print("trying to find all datastores: " + url)

	try:
		response = requests.get(url, headers=headers)
		response.raise_for_status()
	except requests.exceptions.RequestException as err:
		print("EXCEPTION: ", type(err))
	else:
		return [ response.json()['count'], response.json()['records']]