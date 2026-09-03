import requests

URL = 'http://localhost:8000/en/accounts/login/?next=/en/'
session = requests.session()
login_page = session.get(URL)
csrf_token = session.cookies.get('csrftoken')
headers = {'Referer': URL}
data = {
    'username': 'admin',
    'password': 'test1234',
    'csrfmiddlewaretoken': csrf_token,
    'next': '/en/'
}
res = session.post(URL, data=data, headers=headers, allow_redirects=True)
print('Login status:', res.status_code)
print('Final URL:', res.url)
print('CSRF Token:', csrf_token)
print('Session ID:', session.cookies.get('sessionid'))

URL = 'http://localhost:8000/api/subjects/next-index/'
payload = {'collective_body_id': '1'}
res = session.get(URL, params=payload)
print(res.text)

URL = 'http://localhost:8000/api/meetings/next-index/'
payload = {'collective_body_id': '1'}
res = session.get(URL, params=payload)
print(res.text)
