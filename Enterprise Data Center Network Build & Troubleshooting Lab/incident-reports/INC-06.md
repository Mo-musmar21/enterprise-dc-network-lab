# INC-06 – Port err-disabled – port-security violation (unauthorised device)


## 1. Problem description
A contractor connected a laptop at DESK-01; the port died and CLIENT-PC1 cannot reconnect.

## 2. Symptoms observed
- Link on SW1 Fa0/2 goes red immediately after the unknown device sends traffic
- Reconnecting the original PC1 does not restore service

## 3. Diagnosis
**`SW1# show interfaces status`**
```
Fa0/2  CLIENT-PC1|DESK-01  err-disabled  20
```
→ Port shut by the switch, not by an admin.

**`SW1# show port-security interface fa0/2`**
```
Port Status : Secure-shutdown
Violation Mode : Shutdown
Last Source Address:Vlan : 00XX.XXXX.XXXX:20
Security Violation Count : 1
```
→ An unknown MAC (not the sticky PC1 MAC) triggered the violation.

## 4. Root cause
Unauthorised device connected to a secured access port. Port-security (max 1, sticky, violation shutdown) correctly blocked it. **The control worked**.

## 5. Resolution
```
Remove the rogue device; reconnect CLIENT-PC1
SW1(config)# interface fastEthernet0/2
SW1(config-if)# shutdown
SW1(config-if)# no shutdown
```

## 6. Verification
- [x] `show port-security interface fa0/2` → Secure-up, count 0
- [x] PC1 pings gateway successfully

## 7. Prevention / lessons learned
Policy reminder: no personal devices on DC/office ports. Optionally enable `errdisable recovery` only after review.

