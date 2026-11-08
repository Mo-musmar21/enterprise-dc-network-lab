# INC-05 – SRV-DB01 isolated – VLAN 10 pruned from EtherChannel trunk


## 1. Problem description
Database unreachable, but the PC on the same switch (PC2) works fine.

## 2. Symptoms observed
- SRV-DB01 unreachable from all hosts, including SRV-WEB01 (same VLAN)
- CLIENT-PC2 on the same switch works → switch and uplink are up
- Only one VLAN on one switch is affected → trunk VLAN problem

## 3. Diagnosis
**`SW2# show interfaces trunk`**
```
Port  Vlans allowed on trunk
Po1   20,99,999
```
→ VLAN 10 is missing from the allowed list on SW2.

**`SW1# show interfaces trunk`**
```
Po1   10,20,99,999
```
→ SW1 still allows it → mismatch on SW2 only.

## 4. Root cause
`switchport trunk allowed vlan remove 10` was applied to Port-channel 1 on SW2, so VLAN 10 frames were dropped between switches.

## 5. Resolution
```
SW2(config)# interface port-channel 1
SW2(config-if)# switchport trunk allowed vlan add 10
```

## 6. Verification
- [x] `show interfaces trunk` on SW2 → 10,20,99,999
- [x] SRV-WEB01 ⇄ SRV-DB01 ping OK; PC1 → DB01 OK

## 7. Prevention / lessons learned
Always use `allowed vlan add/remove`, never `allowed vlan <list>` (which overwrites). Peer review for trunk changes.


