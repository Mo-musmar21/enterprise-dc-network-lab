# INC-03 – CLIENT-PC2 gets APIPA address – port assigned to wrong VLAN

## 1. Problem description
User on DESK-02 has no network access.

## 2. Symptoms observed
- `ipconfig` on PC2 shows 169.254.x.x (APIPA): DHCP failed
- Link is green → layer 1 is fine

## 3. Diagnosis
**`SW2# show vlan brief`**
```
10   SERVERS   active   Fa0/1, Fa0/2
```
→ Fa0/2 (a client port) is in VLAN 10 (SERVERS) instead of 20.

**`SW2# show interfaces fa0/2 switchport`**
```
Access Mode VLAN: 10 (SERVERS)
```
→ Confirms. There is no DHCP pool for VLAN 10, so the PC fell back to APIPA.

## 4. Root cause
Access VLAN on SW2 Fa0/2 was set to 10 instead of 20. This also put an untrusted client into the server VLAN, a **security** issue as well as an outage.

## 5. Resolution
```
SW2(config)# interface fastEthernet0/2
SW2(config-if)# switchport access vlan 20
CLIENT-PC2> ipconfig /renew
```

## 6. Verification
- [x] `show vlan brief` → Fa0/2 in VLAN 20
- [x] PC2 receives 192.168.20.10x via DHCP
- [x] PC2 pings 192.168.20.1 and 192.168.10.10

## 7. Prevention / lessons learned
VLAN assignments are checked against the port description/CMDB.

