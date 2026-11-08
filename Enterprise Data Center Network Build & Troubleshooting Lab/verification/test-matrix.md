# Verification test matrix – DOHA-DC01 baseline


| # | From | Command | Proves | Expected | Result | Evidence |
|---|---|---|---|---|---|---|
| T1 | CLIENT-PC1 | `ping 192.168.20.1` | Client → gateway | Reply | ☐ | |
| T2 | CLIENT-PC1 | `ping 192.168.10.10` | Inter-VLAN routing | Reply | ☐ | |
| T3 | CLIENT-PC1 | `ping 192.168.10.11` | Routing + EtherChannel | Reply | ☐ | |
| T4 | CLIENT-PC1 | `ping <PC2 DHCP IP>` | L2 across Po1 | Reply | ☐ | |
| T5 | SRV-WEB01 | `ping 192.168.10.11` | Server ⇄ server | Reply | ☐ | |
| T6 | CLIENT-PC1 | `tracert 192.168.10.11` | Path via gateway | 2 hops | ☐ | |
| T7 | ADMIN-PC | `ssh -l netadmin 192.168.99.2` | Secure mgmt SW1 | Login OK | ☐ | |
| T8 | ADMIN-PC | `telnet 192.168.99.2` | Telnet blocked | Refused | ☐ | |
| T9 | ADMIN-PC | `ssh -l netadmin 192.168.99.1` | Secure mgmt R1 | Login OK | ☐ | |
| T10 | CLIENT-PC1 | `ping web01.doha-dc01.lab` | DNS works | Resolves + reply | ☐ | |
| T11 | SW1 | `show etherchannel summary` | Redundant uplink | Po1(SU), 2×(P) | ☐ | |
| T12 | SW1 | `show spanning-tree vlan 10` | Root bridge | "This bridge is the root" | ☐ | |


# Can check results in verification --> test results

