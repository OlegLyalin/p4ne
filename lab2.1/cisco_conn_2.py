import requests
from requests.auth import HTTPBasicAuth
import json

# Отключаем предупреждения о непроверенных SSL сертификатах
requests.packages.urllib3.disable_warnings()

# Данные для подключения
url = "https://10.31.70.209/restconf/data/ietf-interfaces:interfaces"
username = "restapi"
password = "j0sg1280-7@"

# Заголовки для запроса
headers = {
    'Accept': 'application/yang-data+json',
    'Content-Type': 'application/yang-data+json'
}

# Отправка запроса
response = requests.get(url, auth=HTTPBasicAuth(username, password), headers=headers, verify=False)

# Проверка успешности запроса
if response.status_code == 200:
    # Разбор ответа и вывод информации об интерфейсах
    interfaces_data = response.json()
    for interface in interfaces_data['ietf-interfaces:interfaces']['interface']:
        print(f"Interface: {interface['name']}")
        print(f"  Type: {interface.get('type', 'N/A')}")
        print(f"  Enabled: {interface.get('enabled', 'N/A')}")
        if 'statistics' in interface:
            stats = interface['statistics']
            print(f"  Packets Received: {stats.get('in-unicast-pkts', 'N/A')}")
            print(f"  Packets Sent: {stats.get('out-unicast-pkts', 'N/A')}")
            print(f"  Bytes Received: {stats.get('in-octets', 'N/A')}")
            print(f"  Bytes Sent: {stats.get('out-octets', 'N/A')}")
        print("-" * 20)
else:
    print("Failed to retrieve data:", response.status_code)