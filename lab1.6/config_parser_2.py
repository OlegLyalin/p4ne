import ipaddress
import re
import glob

def parse_ip_address(s):
    # Регулярное выражение для поиска строки, соответствующей формату "ip address x.x.x.x x.x.x.x"
    ip_regex = r'^ip address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$'
    match = re.match(ip_regex, s)
    if match:
        ip_address, netmask = match.groups()
        # Преобразуем маску в префикс
        netmask = ipaddress.IPv4Network(f"0.0.0.0/{netmask}").prefixlen
        try:
            # Создаем объект IPv4Interface из IP-адреса и маски
            return ipaddress.IPv4Interface(f"{ip_address}/{netmask}")
        except ValueError as ve:
            print(f"Ошибка при обработке строки '{s}': {ve}")
    return None

# Поиск всех .log файлов в текущей директории
log_files = glob.glob('./*.log')
ip_addresses = []

# Перебор файлов и чтение их содержимого
for filename in log_files:
    with open(filename) as file:
        for line in file:
            # Применяем функцию к каждой строке файла
            ip_interface = parse_ip_address(line.strip())
            if ip_interface:
                # Добавляем объект IPv4Interface в список, если он успешно создан
                ip_addresses.append(ip_interface)

# Вывод списка IP-адресов
for ip in ip_addresses:
    print(ip)