import requests

URL ="https://swq.jp/l/en-US/"

page = requests.get(URL)

print(page.text)