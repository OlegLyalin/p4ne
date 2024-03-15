import glob
import re

# Создаем пустое множество для хранения уникальных IP-адресов и масок.
set_of_ip = set()

# Регулярное выражение для поиска строк с IP-адресами и масками.
ip_pattern = re.compile(r'ip address (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')

# Перебор всех файлов с расширением .log в текущей директории.
for current_file_name in glob.glob("*.log"):
    try:
        with open(current_file_name, 'r') as f:  # Открываем текущий файл для чтения.
            # Перебираем каждую строку в файле.
            for current_line in f:
                # Используем регулярные выражения для поиска соответствующих строк.
                match = ip_pattern.search(current_line)
                if match:
                    # Если найдено соответствие, формируем строку с IP-адресом и маской и добавляем в множество.
                    ip_and_mask = f"{match.group(1)} -- {match.group(2)}"
                    set_of_ip.add(ip_and_mask)
    except IOError as e:
        print(f"Не удалось открыть файл {current_file_name}: {e}")

# Выводим количество уникальных IP-адресов и масок.
print(f"Найдено уникальных IP-адресов и масок: {len(set_of_ip)}")

# Вывод уникальных IP-адресов и масок.
for ip in set_of_ip:
    print(ip)