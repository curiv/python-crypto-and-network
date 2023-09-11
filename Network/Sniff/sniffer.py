from scapy.all import *

# Укажите имя сетевого интерфейса
pkts = sniff(iface='wlp58s0', filter='' , prn=lambda x:x.summary())
