from scapy.all import IP, TCP, sr, sr1

target_ip = "192.168.211.172"  # Замените на целевой IP адрес
port_range = [22,80,443,8080]  # Указать необходимые порты

for port in port_range:
    # Создаем TCP пакет с флагом SYN для сканирования порта
    ip_packet = IP(dst=target_ip)
    tcp_packet = TCP(dport=port, flags="S")
    
    # Отправляем пакет и получаем ответ
    response = sr1(ip_packet / tcp_packet, timeout=0.5, verbose=0)
    
    # Обрабатываем полученный ответ
    if response:
        if response.haslayer(TCP) and response[TCP].flags == 18:  # TCP SYN-ACK
            print(f"{port} open")
