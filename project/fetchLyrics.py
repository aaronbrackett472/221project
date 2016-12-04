import requests
import json

url = "https://api.genius.com//artists/:id/songs"
clientId = "62z5Bwa2W3zMu1AZlUUi1heqA35IZeT3_wgOccgZ4lvHa1JZ_XYKktw_OEfl_FeJ"
TOKEN = "rTNAfXuSPK2GWd6eXtmZwuHVMitzHO-iAl5CKKPNiQ-m2arGCN7eqRRRy7v1F6j8"
headers = {'Authorization': 'BEARER '+ TOKEN, "User-Agent": "CompuServe Classic/1.22", "Accept": "application/json"}
r = requests.get(url, params={'access_token' : TOKEN})
print r.json()
response = json.loads(json.dumps(r.json()))
print response["response"]
