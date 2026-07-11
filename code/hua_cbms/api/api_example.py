import requests

URL = 'http://localhost:8080/api/auth/'
data = {'username': 'admin',
        'password': 'hua123##'}
res = requests.post(URL, data=data)
res_json = res.json()
token = res_json['token']
print(res.text)

URL = 'http://localhost:8080/api/staff/'
headers = {'Authorization': 'Token ' + token}
payload = {'email': 'it2022057@hua.gr'}
res = requests.get(URL, headers=headers, params=payload)
print(res.text)

URL = 'http://localhost:8080/api/subjects/'
headers = {'Authorization': 'Token ' + token}
payload = {'collective_body_id': '1'}
res = requests.get(URL, headers=headers, params=payload)
print(res.text)

URL = 'http://localhost:8080/api/meetings/'
headers = {'Authorization': 'Token ' + token}
payload = {'collective_body_id': '1'}
res = requests.get(URL, headers=headers, params=payload)
print(res.text)
