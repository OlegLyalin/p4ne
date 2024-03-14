# Импорт класса IPv4Network для работы с IPv4 адресами
from ipaddress import IPv4Network
# Импорт модуля random для генерации случайных чисел
import random

# Определение нового класса IPv4RandomNetwork, наследующего IPv4Network
class IPv4RandomNetwork(IPv4Network):
    # Конструктор класса с параметрами начала и конца диапазона префиксов
    def __init__(self, p_start=0, p_end=32):
        # Инициализация базового класса с случайным адресом и префиксом, отключение строгой проверки
        IPv4Network.__init__(self,
                             (random.randint(0x0B000000, 0xDF000000),  # Случайный адрес из заданного диапазона
                              random.randint(p_start, p_end)),        # Случайный префикс из заданного диапазона
                             strict=False
                             )

    # Метод для проверки, является ли сеть "обычной" (не зарезервированной, не локальной и т.д.)
    def regular(self):
        return self.is_global and not \
            (self.is_multicast or self.is_link_local or \
             self.is_loopback or self.is_private or self.is_reserved or self.is_unspecified)

    # Метод для получения ключа сети, используемого для сортировки
    def key_value(self):
        # Возвращается сумма адреса сети и маски, сдвинутой на 32 бита влево
        return int(self.network_address) + (int(self.netmask) << 32)

# Функция для сортировки, использующая key_value как ключ
def sortfunc(x):
    return x.key_value()

# Инициализация генератора случайных чисел
random.seed()

# Список для хранения уникальных сетей
rnlist = []

# Цикл для генерации 50 уникальных "обычных" сетей
while len(rnlist) < 50:
    # Создание случайной сети с префиксом от 8 до 24
    random_network = IPv4RandomNetwork(8, 24)
    # Проверка, что сеть "обычная" и не содержится в списке
    if random_network.regular() and random_network not in rnlist:
        # Добавление сети в список
        rnlist.append(random_network)

# Цикл печати отсортированного списка сетей по ключу
for n in sorted(rnlist, key=sortfunc):
    # Вывод информации о сети
    print(n)