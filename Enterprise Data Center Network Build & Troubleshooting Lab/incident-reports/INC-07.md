# INC-07 – Redundancy degraded – EtherChannel member link down (no outage)


## 1. Problem description
Monitoring alert: interface Fa0/24 down on SW1/SW2. No user complaints.

## 2. Symptoms observed
- All ping tests still pass (continuous `ping -t` from PC1 to DB01 lost ≤ 1 packet)
- Syslog: `%LINK-5-CHANGED: Interface FastEthernet0/24, changed state to down`

## 3. Diagnosis
**`SW1# show etherchannel summary`**
```
1  Po1(SU)  LACP  Fa0/23(P) Fa0/24(D)
```
→ Bundle still up via Fa0/23; Fa0/24 is down.

**`SW1# show interfaces fa0/24`**
```
FastEthernet0/24 is down, line protocol is down
```
→ Physical-layer fault on cable CAB-0002b.

## 4. Root cause
Cable CAB-0002b failed/removed. LACP automatically moved traffic onto the remaining member. Service unaffected, but **a second failure would isolate SW2**.

## 5. Resolution
```
Replace CAB-0002b (SW1 Fa0/24 ⇄ SW2 Fa0/24, cross-over)
```

## 6. Verification
- [x] `show etherchannel summary` → Fa0/23(P) Fa0/24(P)
- [x] Bandwidth: Po1 back to 200 Mb (`show interfaces po1`)

## 7. Prevention / lessons learned
Treat loss of redundancy as a real incident with an SLA. Spare patch cables stocked per row.

