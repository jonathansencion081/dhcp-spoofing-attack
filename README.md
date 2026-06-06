# DHCP Spoofing Attack Script
**Autor:** Jonathan Sención  
**Matrícula:** 20250851  
**Institución:** ITLA - Instituto Tecnológico de las Américas  

---

## Objetivo del Laboratorio
Demostrar cómo un atacante puede configurar un servidor DHCP falso en la red para 
responder a las solicitudes DHCP de los clientes antes que el servidor legítimo, 
asignando configuraciones de red maliciosas como gateway o DNS falsos.

---

## Objetivo del Script
Escuchar solicitudes DHCP Discover en la red y responder con DHCP Offers falsos, 
proporcionando al cliente una IP, gateway y DNS controlados por el atacante.

### Parámetros Usados
| Parámetro | Valor | Descripción |
|---|---|---|
| `src` | `192.168.85.254` | IP falsa del servidor DHCP |
| `yiaddr` | `192.168.85.100` | IP ofrecida al cliente |
| `router` | `192.168.85.254` | Gateway falso (Kali) |
| `name_server` | `8.8.8.8` | DNS asignado |
| `lease_time` | `3600` | Tiempo de arrendamiento |
| `iface` | `eth0` | Interfaz de red atacante |

### Requisitos
- Kali Linux
- Python 3
- Scapy (`sudo apt install python3-scapy`)
- Ejecutar como root (`sudo`)

---

## Funcionamiento del Script
1. El script escucha paquetes UDP en puertos 67 y 68 (DHCP)
2. Al detectar un DHCP Discover, extrae la MAC del cliente
3. Construye un DHCP Offer con configuración falsa
4. Envía el Offer al cliente antes que el servidor legítimo
5. El cliente acepta la configuración maliciosa del atacante

---

## Topología de Red
[Kali Atacante] eth0 ──── e0/2 [SW1] e0/0 ──── e0/0 [SW2] e0/1 ──── eth0 [VPC1]
192.168.85.10                10.20.25.1              10.20.25.2         192.168.85.20
│
e0/1 └──── e0/0 [SW3] e0/1 ──── eth0 [VPC2]
10.20.25.3         192.168.51.20

### VLANs
| VLAN | Nombre | Red |
|---|---|---|
| VLAN 10 | VLAN10-20250851 | 192.168.85.0/24 |
| VLAN 20 | VLAN20-20250851 | 192.168.51.0/24 |
| Management | MGMT | 10.20.25.0/24 |

---

## Ejecución
```bash
sudo python3 dhcp_spoofing.py
```

### Verificación del Ataque
En VPC1 ejecutar:
dhcp
show ip
La IP asignada debe ser `192.168.85.100` con gateway `192.168.85.254`.

---

## Capturas de Pantalla
<img width="641" height="599" alt="image" src="https://github.com/user-attachments/assets/40ae509e-8781-4e77-be86-4e22fdec9435" />


<img width="763" height="256" alt="image" src="https://github.com/user-attachments/assets/296c33fe-3881-4f72-9e3f-7e8370181e5d" />

<img width="719" height="556" alt="image" src="https://github.com/user-attachments/assets/55f7dba6-aafc-43d5-9ab1-e52e8b46ff99" />

---

## Contramedidas
### 1. DHCP Snooping
ip dhcp snooping
ip dhcp snooping vlan 10
no ip dhcp snooping information option
interface e0/2
ip dhcp snooping limit rate 15
interface e0/0
ip dhcp snooping trust
### 2. Port Security
interface e0/2
switchport port-security
switchport port-security maximum 1
switchport port-security violation restrict
### 3. Monitoreo
Revisar regularmente:
show ip dhcp snooping binding
show ip dhcp snooping statistics
