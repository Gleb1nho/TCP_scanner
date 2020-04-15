import socket
import argparse

# Парсим аргументы
# Первым идёт имя хоста, потом порты с и до какого проверять
# Если ограничение до какого проверять не передано, то будет проверен только начальный порт
parser = argparse.ArgumentParser('TCP port scanner')
parser.add_argument('hostname', help='enter hostname')
parser.add_argument('start_port', help='port to start from')
parser.add_argument('end_port', help='last port to check')

arguments = parser.parse_args()
hostname = arguments.hostname
start_port = int(arguments.start_port)
end_port = int(arguments.end_port)

# Получаем ip адрес хоста
ip = socket.gethostbyname(hostname)

# Сканируем порты из выбранного диапазона, это может занять некоторое время
opened_port_list = []  # Сюда сложим открытые порты, чтобы записать в результирующий файл
try:
    for port in range(start_port, end_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем сокет
        sock.settimeout(5)
        res = sock.connect_ex((ip,port))
        if res == 0:  # Если сокет слушает, то пишем что этот порт открыт
            opened_port_list.append(port)
            print(f'Порт {port} открыт')
    if not opened_port_list:
        print('Нет открытых портов в заданном диапазоне.')
except Exception:
    pass


# Запишем в результирующий файл
if opened_port_list:
    with open('result.txt', 'w') as result:
        print('Результат записан')
        result.write(f'У {hostname} открытые порты: ' + str(sorted(set(opened_port_list)))[1:-1])
