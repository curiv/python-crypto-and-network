from scapy.all import ARP, Ether, srp

target_ip = "192.168.211.0/24"  # Замените на вашу подсеть

# Создаем ARP запрос
arp = ARP(pdst=target_ip)
# Создаем Ethernet кадр
ether = Ether(dst="ff:ff:ff:ff:ff:ff")
# Комбинируем Ethernet и ARP
packet = ether/arp

# Отправляем пакет и получаем ответы
# SRP - Send and Receive Packets
result = srp(packet, timeout=3, verbose=0)[0]

# Обрабатываем полученные ответы
for sent, received in result:
    print(f"IP адрес: {received.psrc} - MAC адрес: {received.hwsrc}")

