import socket
import argparse
import threading
from queue import Queue

# Версия с использованием многопоточности и очередей, чтобы не сканировать один и тот же порт по несолько раз
#
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
# Создадим очередь, куда положим номера портов для проверки
queue = Queue()
# И список куда будем складывать открытые порты
open_ports = []

# Функция которая сканирует переданный порт, если удалось подключиться, то успех
def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаем сокет
        sock.connect((ip, port))  # Пытаемся подключиться
        return True
    except:
        return False


# Метод который положит выбранные порты в очередь
def ports_to_queue(start, end):
    for p in range(start, end + 1):
        queue.put(p)


# Пишем метод, с помощью которого поток будет выполнять необходимую функцию
def worker():
    # Пока очередь не пуста берём из неё порт
    while not queue.empty():
        port = queue.get()
        if scan_port(port):
            open_ports.append(port)


# Заполним очередь
ports_to_queue(start_port, end_port)

# Создадим список потоков
thread_list = []

# Создадим потоки
for t in range(500):
    thread = threading.Thread(target=worker)
    thread_list.append(thread)

# Запускаем потоки работать
for t in thread_list:
    t.start()

# Ждём завершения работы всех потоков из списка
for t in thread_list:
    t.join()

# Выводим информацию об открытых портах
for i in sorted(open_ports):
    print(f'Порт {i} открыт')

# Запишем её в файл
with open('result.txt', 'w') as res:
    res.write(f'У хоста {hostname} открыты следующие порты: ' + str(sorted(open_ports))[1:-1])
