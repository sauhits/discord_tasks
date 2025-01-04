import requests

url = "https://teams.microsoft.com/v2/"
session = requests.session()
response = session.get(url)

cookie = response.cookies
print(cookie)
