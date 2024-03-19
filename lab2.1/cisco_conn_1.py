import paramiko

# Данные для подключения
host = "10.31.70.209"
username = "restapi"
password = "j0sg1280-7@"

# Создаем SSH клиент
ssh = paramiko.SSHClient()

# Автоматическое принятие ключей узлов, которых нет в known_hosts
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Подключаемся к устройству
try:
    ssh.connect(hostname=host, username=username, password=password, look_for_keys=False, allow_agent=False)

    # Запускаем shell
    shell = ssh.invoke_shell()

    # Устанавливаем длину терминала, чтобы избежать постраничного вывода
    shell.send('terminal length 0\n')
    shell.send('show interface\n')

    # Ждем, пока команда выполнится
    import time

    time.sleep(3)  # Подстройте задержку под реальные условия

    # Считываем данные из буфера
    output = shell.recv(10000).decode('utf-8')

    # Обрабатываем вывод команды
    interfaces = {}
    for line in output.splitlines():
        if line.startswith('GigabitEthernet') or line.startswith('FastEthernet'):
            interface_name = line.split()[0]
            interfaces[interface_name] = {}
        elif 'packets input' in line:
            packets_input, bytes_input = line.split(',')[0:2]
            packets_input = packets_input.split()[0]
            bytes_input = bytes_input.split()[0]
            interfaces[interface_name]['packets_input'] = packets_input
            interfaces[interface_name]['bytes_input'] = bytes_input
        elif 'packets output' in line:
            packets_output, bytes_output = line.split(',')[0:2]
            packets_output = packets_output.split()[0]
            bytes_output = bytes_output.split()[0]
            interfaces[interface_name]['packets_output'] = packets_output
            interfaces[interface_name]['bytes_output'] = bytes_output

    # Выводим результат
    for intf, stats in interfaces.items():
        print(f"Interface: {intf}")
        for key, value in stats.items():
            print(f"  {key}: {value}")

except Exception as e:
    print(f"Ошибка при подключении или выполнении команды: {e}")
finally:
    if ssh:
        ssh.close()