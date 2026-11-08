"""Generate the topology and rack elevation diagrams.

Run:  python tools/make_diagrams.py
Output: docs/images/topology.png, docs/images/rack-elevation.png
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, Ellipse

OUT = Path(__file__).resolve().parents[1] / "images"
OUT.mkdir(parents=True, exist_ok=True)

for name in ("Inter", "DejaVu Sans"):
    if any(name in f.name for f in font_manager.fontManager.ttflist):
        plt.rcParams["font.family"] = name
        break

INK = "#1F2430"
MUTED = "#6B7280"
GRID = "#E5E7EB"
BG = "#FFFFFF"
C_SRV = "#2563EB"   # VLAN 10
C_CLI = "#0F9D76"   # VLAN 20
C_MGT = "#D97706"   # VLAN 99
C_TRK = "#7C3AED"   # trunks
C_NET = "#334155"   # network gear


def bh(n):
    return 4.4 + 2.5 * n + 1.6


def box(ax, x, y, w, h, title, lines, color, fs=10):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                                boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc="white", ec=color, lw=2, zorder=3))
    ax.add_patch(FancyBboxPatch((x - w / 2, y + h / 2 - 3.2), w, 3.2,
                                boxstyle="round,pad=0.4,rounding_size=1.2",
                                fc=color, ec=color, lw=2, zorder=4))
    ax.text(x, y + h / 2 - 1.6, title, ha="center", va="center", color="white",
            fontsize=fs, fontweight="bold", zorder=5)
    for i, ln in enumerate(lines):
        ax.text(x, y + h / 2 - 5.4 - i * 2.5, ln, ha="center", va="center",
                color=INK, fontsize=fs - 1.5, zorder=5)


def _exit(p, q, half):
    """Point just outside the box centred at p (half-sizes) on the segment p->q."""
    (x1, y1), (x2, y2) = p, q
    hw, hh = half
    dx, dy = x2 - x1, y2 - y1
    ts = []
    if dx:
        ts.append(hw / abs(dx))
    if dy:
        ts.append(hh / abs(dy))
    t = min(ts) + 0.06
    return x1 + dx * t, y1 + dy * t


def link(ax, p1, p2, color, lw=2.2, ls="-", l1=None, l2=None, h1=None, h2=None):
    (x1, y1), (x2, y2) = p1, p2
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls, zorder=1, solid_capstyle="round")
    for lab, a, b, h in ((l1, p1, p2, h1), (l2, p2, p1, h2)):
        if lab and h:
            lx, ly = _exit(a, b, h)
            ax.text(lx, ly, lab, ha="center", va="center", fontsize=8, color=color,
                    fontweight="bold", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=color, lw=0.8))


def topology():
    fig, ax = plt.subplots(figsize=(14, 9.2), dpi=160)
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 72)
    ax.axis("off")

    ax.text(2, 69.5, "DOHA-DC01  ·  Enterprise Data Center Network Lab", fontsize=17,
            fontweight="bold", color=INK, va="center")
    ax.text(2, 66.6, "Router-on-a-stick · 802.1Q trunks · LACP EtherChannel · Rapid-PVST+ · "
            "Port-security · SSH-only management · DHCP · Syslog/NTP",
            fontsize=10, color=MUTED, va="center")

    R1, SW1, SW2 = (50, 56), (28, 35), (72, 35)
    WEB, PC1, ADM = (13, 11), (36, 11), (9.5, 51)
    DB, PC2 = (63, 11), (87, 11)

    H = {"R1": (11, bh(3) / 2), "SW": (10.5, bh(2) / 2), "WEB": (9.5, bh(3) / 2),
         "PC": (8.5, bh(2) / 2), "ADM": (7, bh(2) / 2), "DB": (9.5, bh(2) / 2)}
    # links (drawn first)
    link(ax, R1, SW1, C_TRK, l1="G0/0", l2="G0/1", h1=H["R1"], h2=H["SW"])
    ax.text(35, 47.5, "802.1Q trunk\nnative 999", fontsize=8, color=C_TRK, ha="right")
    ax.plot([SW1[0] + 10.5, SW2[0] - 10.5], [SW1[1] + 0.8, SW2[1] + 0.8], color=C_TRK, lw=2.2, zorder=1)
    ax.plot([SW1[0] + 10.5, SW2[0] - 10.5], [SW1[1] - 0.8, SW2[1] - 0.8], color=C_TRK, lw=2.2, zorder=1)
    ax.add_patch(Ellipse((50, 35), 4, 5, fc="none", ec=C_TRK, lw=1.6, zorder=2))
    ax.text(50, 39.6, "Po1 · LACP (2 × 100 Mb)", ha="center", fontsize=9, color=C_TRK,
            fontweight="bold")
    ax.text(50, 30.2, "Fa0/23-24  <->  Fa0/23-24", ha="center", fontsize=8, color=C_TRK)
    link(ax, SW1, WEB, C_SRV, l1="Fa0/1", h1=H["SW"])
    link(ax, SW1, PC1, C_CLI, l1="Fa0/2", h1=H["SW"])
    link(ax, SW1, ADM, C_MGT, l1="Fa0/3", h1=H["SW"])
    link(ax, SW2, DB, C_SRV, l1="Fa0/1", h1=H["SW"])
    link(ax, SW2, PC2, C_CLI, l1="Fa0/2", h1=H["SW"])

    box(ax, *R1, 22, bh(3), "DOH-DC01-R1  (2911)",
        ["G0/0.10  192.168.10.1", "G0/0.20  192.168.20.1", "G0/0.99  192.168.99.1"], C_NET)
    box(ax, *SW1, 21, bh(2), "DOH-DC01-SW1  (2960)",
        ["STP root · VLAN 10/20/99", "MGMT 192.168.99.2"], C_NET)
    box(ax, *SW2, 21, bh(2), "DOH-DC01-SW2  (2960)",
        ["Rapid-PVST+", "MGMT 192.168.99.3"], C_NET)
    box(ax, *WEB, 19, bh(3), "SRV-WEB01",
        ["VLAN 10 · 192.168.10.10", "GW 192.168.10.1", "Syslog · NTP · DNS"], C_SRV)
    box(ax, *PC1, 17, bh(2), "CLIENT-PC1", ["VLAN 20 · DHCP", "(192.168.20.100+)"], C_CLI)
    box(ax, *ADM, 14, bh(2), "ADMIN-PC", ["VLAN 99", "192.168.99.50"], C_MGT, fs=9.5)
    box(ax, *DB, 19, bh(2), "SRV-DB01", ["VLAN 10 · 192.168.10.11", "GW 192.168.10.1"], C_SRV)
    box(ax, *PC2, 17, bh(2), "CLIENT-PC2", ["VLAN 20 · DHCP", "(192.168.20.100+)"], C_CLI)

    # legend
    lx, ly = 71, 60
    ax.add_patch(FancyBboxPatch((lx - 1, ly - 9.2), 29.5, 12.6, boxstyle="round,pad=0.3",
                                fc="#F9FAFB", ec=GRID, lw=1))
    for i, (c, t) in enumerate([(C_SRV, "VLAN 10  SERVERS  192.168.10.0/24"),
                                (C_CLI, "VLAN 20  CLIENTS  192.168.20.0/24"),
                                (C_MGT, "VLAN 99  MGMT     192.168.99.0/24"),
                                (C_TRK, "Trunk (10,20,99 · native 999)")]):
        y = ly + 1.8 - i * 2.9
        ax.plot([lx, lx + 3], [y, y], color=c, lw=3)
        ax.text(lx + 4, y, t, va="center", fontsize=8.5, color=INK, family="DejaVu Sans Mono")
    ax.text(2, 1.2, "Unused ports → VLAN 998 PARKING (shutdown)  ·  VLAN 1 SVI disabled  ·  "
            "Cable IDs CAB-0001… match port descriptions", fontsize=8.5, color=MUTED)
    fig.savefig(OUT / "topology.png", bbox_inches="tight", facecolor=BG)
    plt.close(fig)


def rack():
    fig, ax = plt.subplots(figsize=(11, 10), dpi=160)
    fig.patch.set_facecolor(BG)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 92)
    ax.axis("off")
    ax.text(2, 89, "Rack R01 Elevation & Cable Schedule (logical)", fontsize=15,
            fontweight="bold", color=INK)
    # rack frame 42U → draw 20 U visible slice (U1..U20 compressed)
    x0, w, uh = 6, 34, 3.6
    units = {20: ("PP-01  Patch panel 24p", "#94A3B8"), 18: ("DOH-DC01-R1  (1U)", C_NET),
             16: ("DOH-DC01-SW1  (1U)", C_NET), 15: ("DOH-DC01-SW2  (1U)", C_NET),
             12: ("SRV-DB01  (2U)", C_SRV), 10: ("SRV-WEB01  (2U)", C_SRV),
             4: ("PDU-A / PDU-B  (0U side)", "#B45309"), 2: ("UPS-A  (2U)", "#B45309")}
    base = 6
    ax.add_patch(plt.Rectangle((x0 - 2, base - 1), w + 4, 21 * uh + 2, fc="#111827", ec="#111827"))
    for u in range(1, 21):
        y = base + (u - 1) * uh
        ax.text(x0 - 1, y + uh / 2, f"U{u:02d}", color="#9CA3AF", fontsize=6.5, ha="center", va="center")
        lab = units.get(u)
        hgt = 2 if lab and "(2U)" in lab[0] else 1
        if lab:
            ax.add_patch(FancyBboxPatch((x0 + 1, y + 0.25), w - 2, hgt * uh - 0.5,
                                        boxstyle="round,pad=0.1,rounding_size=0.4",
                                        fc=lab[1], ec="white", lw=0.6))
            ax.text(x0 + w / 2, y + hgt * uh / 2, lab[0], color="white", fontsize=8,
                    ha="center", va="center", fontweight="bold")
    ax.text(x0 + w / 2, base + 21 * uh + 2.2, "R01 (front view, U01–U20)", ha="center", fontsize=9, color=MUTED)

    rows = [("CAB-0001", "R1 G0/0", "SW1 G0/1", "Cat6 · Trunk"),
            ("CAB-0002a", "SW1 Fa0/23", "SW2 Fa0/23", "Cat6 · Po1"),
            ("CAB-0002b", "SW1 Fa0/24", "SW2 Fa0/24", "Cat6 · Po1"),
            ("CAB-0003", "SW1 Fa0/1", "SRV-WEB01 eth0", "Cat6 · VLAN 10"),
            ("CAB-0004", "SW1 Fa0/2", "CLIENT-PC1", "Cat6 · VLAN 20"),
            ("CAB-0005", "SW1 Fa0/3", "ADMIN-PC", "Cat6 · VLAN 99"),
            ("CAB-0006", "SW2 Fa0/1", "SRV-DB01 eth0", "Cat6 · VLAN 10"),
            ("CAB-0007", "SW2 Fa0/2", "CLIENT-PC2", "Cat6 · VLAN 20")]
    tx, ty = 46, 80
    hdr = ("Cable ID", "A-end", "B-end", "Type / Use")
    colx = [tx, tx + 12, tx + 26, tx + 41]
    for cx, h in zip(colx, hdr):
        ax.text(cx, ty, h, fontsize=9, fontweight="bold", color=INK)
    ax.plot([tx, 99], [ty - 1.4, ty - 1.4], color=INK, lw=0.8)
    for i, r in enumerate(rows):
        yy = ty - 4.2 - i * 3.6
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((tx - 0.5, yy - 1.6), 53.5, 3.4, fc="#F3F4F6", ec="none"))
        for cx, v in zip(colx, r):
            ax.text(cx, yy, v, fontsize=8.3, color=INK, va="center", family="DejaVu Sans Mono")
    ax.text(tx, 42, "Label standard (both ends, 5 cm from connector):", fontsize=9.5,
            fontweight="bold", color=INK)
    ax.text(tx, 38.3, "<SITE>-<RACK>-<U>-<PORT> <-> <SITE>-<RACK>-<U>-<PORT>", fontsize=9,
            color=C_TRK, family="DejaVu Sans Mono")
    ax.text(tx, 34.8, "e.g. DOH01-R01-U16-FA01 <-> DOH01-R01-U10-ETH0", fontsize=9,
            color=MUTED, family="DejaVu Sans Mono")
    ax.text(tx, 28, "Why it matters for a DCT:", fontsize=9.5, fontweight="bold", color=INK)
    for i, t in enumerate(["Port description on the switch = cable label = CMDB record",
                           "Any tech can trace a fault without guessing",
                           "Dual PDUs (A/B) → servers survive a single power-feed loss",
                           "Network gear at top, heavy UPS at bottom (weight/stability)"]):
        ax.text(tx, 24.5 - i * 3.3, "•  " + t, fontsize=8.8, color=INK)
    fig.savefig(OUT / "rack-elevation.png", bbox_inches="tight", facecolor=BG)
    plt.close(fig)


if __name__ == "__main__":
    topology()
    rack()
    print("Diagrams written to", OUT)