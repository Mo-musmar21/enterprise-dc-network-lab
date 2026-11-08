# INC-01 – SRV-WEB01 unreachable – switch port administratively down


## 1. Problem description
Clients in VLAN 20 report the web application is unreachable. Monitoring shows SRV-WEB01 down.

## 2. Symptoms observed
- `ping 192.168.10.10` from CLIENT-PC1 → *Request timed out* (100% loss)
- Link indicator for CAB-0003 is red at both ends
- SRV-DB01 and other hosts are reachable → fault is isolated to one host

## 3. Diagnosis
**`SW1# show interfaces status`**
```
Fa0/1  SRV-WEB01|R01-U10  disabled  10  auto  auto  10/100BaseTX
```
→ Port is **disabled** = administratively shut, not a cable fault (that would be *notconnect*).

**`SW1# show running-config interface fa0/1`**
```
 shutdown
```
→ Confirms a `shutdown` command on the port.

## 4. Root cause
Port Fa0/1 on DOH-DC01-SW1 was administratively shut down (simulated unauthorised/erroneous change).

## 5. Resolution
```
SW1(config)# interface fastEthernet0/1
SW1(config-if)# no shutdown
```

## 6. Verification
- [x] `show interfaces status` → Fa0/1 *connected*
- [x] CLIENT-PC1 `ping 192.168.10.10` → 4/4 replies
- [x] Syslog server shows `%LINK-3-UPDOWN: Interface FastEthernet0/1, changed state to up`


