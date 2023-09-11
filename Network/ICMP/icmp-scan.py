from scapy.all import IP, ICMP, sr1

target_ip = "192.168.211.172"  # Замените на целевой IP адрес

# Создаем ICMP запрос
icmp = IP(dst=target_ip)/ICMP()
# Отправляем пакет и получаем ответ
response = sr1(icmp, timeout=0.1, verbose=0)

# Обрабатываем полученный ответ
if response:
    if response.haslayer(ICMP):
        if response[ICMP].type == 0:  # ICMP Echo Reply
            print(f"IP адрес {target_ip} доступен")
        elif response[ICMP].type == 3:  # ICMP Destination Unreachable
            print(f"IP адрес {target_ip} недоступен (Destination Unreachable)")
else:
    print(f"IP адрес {target_ip} не ответил на ICMP запрос")

