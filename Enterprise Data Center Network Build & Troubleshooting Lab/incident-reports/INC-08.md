# INC-08 – All clients lose connectivity and DHCP – wrong 802.1Q tag on router sub-interface


## 1. Problem description
All client PCs lost network access after a router change; new PCs get 169.254.x.x.

## 2. Symptoms observed
- PC1 and PC2 cannot ping 192.168.20.1
- PC1 → PC2 (same VLAN) **still works** → switching fine, gateway broken
- `ipconfig /renew` → APIPA 169.254.x.x

## 3. Diagnosis
**`R1# show ip interface brief`**
```
GigabitEthernet0/0.20  192.168.20.1  YES manual up  up
```
→ Looks healthy. **Up/up does not mean correct.**

**`R1# show running-config interface g0/0.20`**
```
 encapsulation dot1Q 30
```
→ Sub-interface tags VLAN 30, but clients are in VLAN 20 → frames never match.

**`SW1# show interfaces trunk`**
```
Gig0/1  10,20,99,999
```
→ Switch side is correct → fault is on the router.

## 4. Root cause
Sub-interface G0/0.20 was configured with `encapsulation dot1Q 30`. The gateway and DHCP server for VLAN 20 became unreachable.

## 5. Resolution
```
R1(config)# interface gigabitEthernet0/0.20
R1(config-subif)# encapsulation dot1Q 20
R1(config-subif)# ip address 192.168.20.1 255.255.255.0
Clients: ipconfig /renew
```

## 6. Verification
- [x] PCs receive 192.168.20.10x via DHCP
- [x] `show ip dhcp binding` lists both PCs
- [x] Full ping matrix (T1–T9) passes

## 7. Prevention / lessons learned
Configuration backups and a post-change verification checklist (ping matrix) after every router change. A sub-interface number that matches its VLAN ID makes this error obvious on review.

