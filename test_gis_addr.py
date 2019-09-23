import requests
import json
 
url = "http://localhost:5000/addr"

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {'addr': '1600 Amphitheatre Parkway, Mountain View, CA'}
response = requests.post(url, data=json.dumps(data), headers=headers)
if response.ok:
    print((response.text))

data = {'addr': '94-139 Polani St, Waipahu, Hawaii(HI), 96797'}  
response = requests.post(url, data=json.dumps(data), headers=headers)
if response.ok:
    print((response.text))
    
data = {'addr': '820 Del Rio Way, Merritt Island, Florida(FL), 32953'}  
response = requests.post(url, data=json.dumps(data), headers=headers)
if response.ok:
    print((response.text))

data = {'addr': '1281 E 19th Ave #APT A101, Anchorage, Alaska(AK), 99501'}  
response = requests.post(url, data=json.dumps(data), headers=headers)
if response.ok:
    print((response.text))
    
data = {'addr': '321 14th Pl NE, Washington, District of Columbia(DC), 20002'}  
response = requests.post(url, data=json.dumps(data), headers=headers)
if response.ok:
    print((response.text))
   
data = {'addr': '36 W 138th St, New York, New York(NY), 10037'}  
response = requests.post(url, data=json.dumps(data), headers=headers)
if response.ok:
    print((response.text))


data = {'addr': '2171 Saint Claire Rd, Louisville, Georgia(GA), 30434'}  
response = requests.post(url, data=json.dumps(data), headers=headers)
if response.ok:
    print((response.text))