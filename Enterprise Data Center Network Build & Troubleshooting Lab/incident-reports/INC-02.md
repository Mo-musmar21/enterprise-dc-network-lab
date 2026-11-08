# INC-02 – SRV-DB01 offline after maintenance – cable patched into wrong switch port


## 1. Problem description
After a rack-and-stack activity, SRV-DB01 is unreachable.

## 2. Symptoms observed
- Ping to 192.168.10.11 fails from every host
- CAB-0006 link light red on switch side
- SRV-DB01 NIC shows link but no traffic

## 3. Diagnosis
**`SW2# show interfaces status`**
```
Fa0/1  SRV-DB01|R01-U12  notconnect  10
Fa0/5  UNUSED             disabled    998
```
→ The port reserved for DB01 (per its description) has no cable; the cable landed on Fa0/5, a parked and shut port in VLAN 998.

**`Physical check`**
```
Cable label CAB-0006 reads SW2-FA01 ⇄ SRV-DB01-ETH0
```
→ Label says Fa0/1, cable is in Fa0/5 → patching error.

## 4. Root cause
Cable CAB-0006 was patched into SW2 Fa0/5 instead of Fa0/1 during maintenance. Fa0/5 is intentionally shut and in the PARKING VLAN, so the server was isolated (the hardening worked as designed).

## 5. Resolution
```
Move CAB-0006 from SW2 Fa0/5 to SW2 Fa0/1 (as labelled)
```

## 6. Verification
- [x] `show interfaces status` → Fa0/1 *connected* VLAN 10
- [x] `ping 192.168.10.11` from PC1 and SRV-WEB01 → success
- [x] `show port-security interface fa0/1` → Secure-up

## 7. Prevention / lessons learned
Always verify the cable label against the switch port description before closing a physical task. Take a photo of the patch panel as completion evidence.

