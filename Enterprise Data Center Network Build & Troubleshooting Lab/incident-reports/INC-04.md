# INC-04 – SRV-DB01 reachable only inside its subnet – wrong default gateway


## 1. Problem description
Web server can talk to the database, but client PCs cannot.

## 2. Symptoms observed
- SRV-WEB01 → `ping 192.168.10.11` ✅
- CLIENT-PC1 → `ping 192.168.10.11` ❌
- Pattern: same-subnet OK, cross-subnet fails → layer-3 / gateway problem

## 3. Diagnosis (runbook steps)
**`SRV-DB01> ipconfig`**
```
Default Gateway......: 192.168.10.254
```
→ Gateway should be 192.168.10.1 (R1 G0/0.10).

**`SRV-DB01> ping 192.168.10.254`**
```
Request timed out.
```
→ Configured gateway does not exist.

## 4. Root cause
Static default gateway on SRV-DB01 mis-typed as 192.168.10.254. Replies to other subnets were sent to a non-existent router.

## 5. Resolution
```
SRV-DB01 → Desktop → IP Configuration → Default Gateway = 192.168.10.1
```

## 6. Verification
- [x] CLIENT-PC1 `ping 192.168.10.11` → success
- [x] `tracert 192.168.10.11` → 192.168.20.1 → 192.168.10.11

## 7. Prevention / lessons learned
Server build checklist includes a cross-subnet ping test, not only a same-subnet test.


