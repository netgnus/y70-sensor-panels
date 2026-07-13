# Y70 skin trio — Original / Snow / Ink editions (685x2560), real AIDA64 format
import subprocess, os, random

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 685, 2560
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FONT = "Segoe UI"
RAINBOW = "conic-gradient(from 210deg,#ff9a3c,#ff4e87,#a34eff,#3c8cff,#2ee6c8,#ff9a3c)"
GRAD_LINE = "linear-gradient(90deg,#3c8cff,#2ee6c8,#ffb03c,#ff4e87)"

def cref(hexcol):
    r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
    return r + (g << 8) + (b << 16)

THEMES = {
    "Original": dict(
        pagebg="linear-gradient(150deg,#1b1035 0%,#2a1550 30%,#14204a 65%,#301040 100%)",
        glows="radial-gradient(ellipse 60% 25% at 75% 12%,rgba(255,78,135,.28),transparent 70%),"
              "radial-gradient(ellipse 60% 25% at 20% 45%,rgba(60,140,255,.25),transparent 70%),"
              "radial-gradient(ellipse 60% 25% at 70% 85%,rgba(46,230,200,.18),transparent 70%)",
        cardbg="rgba(16,10,40,.72)", cardborder="rgba(255,255,255,.14)", cardshadow="none",
        text="#ffffff", muted="#b9b3d9", accent="#4da3ff",
        graphline="#4da3ff", graphbg="#120c30", graphframe="#3a3468", graphgrid="#241d50",
        barfill="#3c8cff", barmid="#ffb03c", barhigh="#ff4e87", bartrack="#241d50", barframe="#3a3468",
        ringhole="rgba(16,10,40,0)", light=False),
    "Snow": dict(
        pagebg="linear-gradient(160deg,#f2f3f7 0%,#e7e9ef 50%,#eceef3 100%)",
        glows="radial-gradient(ellipse 60% 25% at 75% 10%,rgba(60,140,255,.10),transparent 70%),"
              "radial-gradient(ellipse 60% 25% at 25% 80%,rgba(255,78,135,.08),transparent 70%)",
        cardbg="#fbfbfd", cardborder="#d8dae2", cardshadow="0 2px 14px rgba(30,40,80,.10)",
        text="#16181d", muted="#70747f", accent="#1a73e8",
        graphline="#1a73e8", graphbg="#eef0f5", graphframe="#c9ccd6", graphgrid="#dde0e8",
        barfill="#1a73e8", barmid="#f5a623", barhigh="#e8467c", bartrack="#e2e4ec", barframe="#c9ccd6",
        ringhole="#fbfbfd", light=True),
    "Ink": dict(
        pagebg="linear-gradient(180deg,#050505 0%,#0a0a0c 100%)",
        glows="none",
        cardbg="#151518", cardborder="#2c2c31", cardshadow="none",
        text="#ffffff", muted="#9a9aa4", accent="#4da3ff",
        graphline="#4da3ff", graphbg="#0e0e11", graphframe="#333338", graphgrid="#222227",
        barfill="#3c8cff", barmid="#ffb03c", barhigh="#ff4e87", bartrack="#232328", barframe="#333338",
        ringhole="#151518", light=False),
}

def build_theme(name, T):
    bake, items, preview, pv_graphs, pv_bars = [], [], [], [], []
    C_text, C_muted, C_acc = cref(T["text"]), cref(T["muted"]), cref(T["accent"])

    def btxt(x, y, size, color, text, bold=False, center=False, w=None):
        bake.append(("txt", x, y, size, color, text, bold, center, w))
    def bcard(x, y, w, h):
        bake.append(("card", x, y, w, h))
    def bring(cx, cy, r, th):
        bake.append(("ring", cx, cy, r, th))
    def bline(x, y, w):
        bake.append(("gline", x, y, w))
    def simple(x, y, pt, color, sensor, unit="", bold=False):
        b = "1" if bold else "0"
        items.append(f"<ID>[SIMPLE]{sensor}</ID><TXTSIZ>{pt}</TXTSIZ><FNTNAM>{FONT}</FNTNAM>"
                     f"<TXTCOL>{color}</TXTCOL><TXTBIR>{b}00</TXTBIR><SHWLBL>0</SHWLBL><LBL></LBL>"
                     f"<SHWUNT>{1 if unit else 0}</SHWUNT><UNT>{unit}</UNT><ITMX>{x}</ITMX><ITMY>{y}</ITMY>")
    def bar(x, y, w, h, sensor):
        pv_bars.append((x, y, w, h))
        items.append(f"<ID>{sensor}</ID><WID>60</WID><TXTSIZ>10</TXTSIZ><FNTNAM>{FONT}</FNTNAM>"
                     f"<SHDCOL>0</SHDCOL><SHDDIS>1</SHDDIS><SHDDEP>1</SHDDEP><SHWLBL>0</SHWLBL><LBL></LBL>"
                     f"<LBLCOL>{C_muted}</LBLCOL><LBLBIS>000</LBLBIS><SHWVAL>0</SHWVAL>"
                     f"<VALCOL>{C_text}</VALCOL><VALBIS>000</VALBIS><SHWUNT>0</SHWUNT><UNT></UNT>"
                     f"<UNTCOL>{C_text}</UNTCOL><UNTBIS>000</UNTBIS><UNTWID>10</UNTWID>"
                     f"<SHWBAR>1</SHWBAR><BARWID>{w}</BARWID><BARHEI>{h}</BARHEI><BARIND>0</BARIND>"
                     f"<BARPLC>SEP</BARPLC><BARFS>0010</BARFS><BARFRMCOL>{cref(T['barframe'])}</BARFRMCOL>"
                     f"<BARMIN></BARMIN><BARLIM1>50</BARLIM1><BARLIM2>75</BARLIM2><BARLIM3>90</BARLIM3><BARMAX></BARMAX>"
                     f"<BARMINFGC>{cref(T['barfill'])}</BARMINFGC><BARMINBGC>{cref(T['bartrack'])}</BARMINBGC>"
                     f"<BARLIM1FGC>{cref(T['barmid'])}</BARLIM1FGC><BARLIM1BGC>{cref(T['bartrack'])}</BARLIM1BGC>"
                     f"<BARLIM2FGC>{cref(T['barhigh'])}</BARLIM2FGC><BARLIM2BGC>{cref(T['bartrack'])}</BARLIM2BGC>"
                     f"<BARLIM3FGC>{cref(T['barhigh'])}</BARLIM3FGC><BARLIM3BGC>{cref(T['bartrack'])}</BARLIM3BGC>"
                     f"<ITMX>{x}</ITMX><ITMY>{y}</ITMY>")
    def graph(x, y, w, h, sensor):
        pv_graphs.append((x, y, w, h))
        items.append(f"<ID>[GRAPH]{sensor}</ID><LBL></LBL><TYP>LG</TYP><WID>{w}</WID><HEI>{h}</HEI>"
                     f"<GPHSTP>1</GPHSTP><GPHTCK>1</GPHTCK><GRDDNS>10</GRDDNS><MINVAL>0</MINVAL>"
                     f"<MAXVAL>100</MAXVAL><AUTSCL>1</AUTSCL><GRDCOL>{cref(T['graphgrid'])}</GRDCOL>"
                     f"<GPHCOL>{cref(T['graphline'])}</GPHCOL><BGCOL>{cref(T['graphbg'])}</BGCOL>"
                     f"<FRMCOL>{cref(T['graphframe'])}</FRMCOL><GPHBFG>111</GPHBFG><SHWSCL>1</SHWSCL>"
                     f"<TXTSIZ>8</TXTSIZ><FNTNAM>{FONT}</FNTNAM><SCLCOL>{C_muted}</SCLCOL><SCLBI>000</SCLBI>"
                     f"<ITMX>{x}</ITMX><ITMY>{y}</ITMY>")
    def pv(x, y, pt, colorhex, text, bold=False):
        preview.append((x, y, round(pt * 1.33), colorhex, text, bold))

    Mx, CW = 20, 645
    IL, IR = 48, 637
    RX = 300           # rows x in CPU/GPU cards
    VX2 = 480          # value x

    # ---------- hardware card helper ----------
    def hwcard(y0, hgt, title, ring_sensor, pwr_sensor, rows, graph_sensor, rows_y0, samples):
        bcard(Mx, y0, CW, hgt)
        btxt(IL, y0 + 30, 22, T["text"], title, bold=True)
        cx, cy = 160, rows_y0 + 150
        bring(cx, cy, 100, 14)
        simple(cx - 62, cy - 30, 30, C_text, ring_sensor, unit="°C", bold=True)
        pv(cx - 62, cy - 30, 30, T["text"], samples[0] + "°C", bold=True)
        simple(cx - 60, cy + 128, 20, C_text, pwr_sensor, unit="W", bold=True)
        pv(cx - 60, cy + 128, 20, T["text"], samples[1] + " W", bold=True)
        for i, (cap, sensor, unit, sv) in enumerate(rows):
            ry = rows_y0 + i * 62
            btxt(RX, ry, 15, T["muted"], cap)
            simple(VX2, ry - 2, 15, C_text, sensor, unit=unit)
            pv(VX2, ry - 2, 15, T["text"], sv)
            bline(RX, ry + 30, IR - RX)
        gy = y0 + hgt - 190
        graph(IL, gy, IR - IL - 4, 150, graph_sensor)

    # CPU card: 4 rows
    hwcard(30, 660, "AMD Ryzen 7 7800X3D", "TCPU", "PCPUPKG",
           [("Load", "SCPUUTI", "%", "34 %"), ("Voltage", "VCPU", "V", "1.112 V"),
            ("CPU Clock", "SCPUCLK", "MHz", "4650 MHz"), ("CPU Fan", "FCPU", "RPM", "1262 RPM")],
           "SCPUUTI", 130, ["62", "49.33"])

    # GPU card: 6 rows
    hwcard(710, 740, "NVIDIA GeForce RTX 5070 Ti", "TGPU1", "PGPU1",
           [("Load", "SGPU1UTI", "%", "10 %"), ("Voltage", "VGPU1", "V", "0.855 V"),
            ("GPU Clock", "SGPU1CLK", "MHz", "2917 MHz"), ("VRAM Temp", "TGPU1MEM", "°C", "60 °C"),
            ("VRAM Used", "SVMEMUSAGE", "%", "27 %"), ("Fan", "FGPU1", "RPM", "0 RPM")],
           "SGPU1UTI", 810, ["48", "37.14"])

    # Device card
    bcard(Mx, 1470, CW, 130)
    btxt(IL, 1492, 14, T["muted"], "Device Name:")
    btxt(IL, 1518, 24, T["text"], "NETGNUSPC", bold=True)
    btxt(IL, 1558, 15, T["accent"], "Status: Online")

    # Clock card
    bcard(Mx, 1620, CW, 190)
    simple(150, 1646, 50, C_text, "STIME", bold=True)
    pv(150, 1646, 50, T["text"], "12:05:04 PM", bold=True)
    simple(270, 1740, 16, C_muted, "SDATE")
    pv(270, 1740, 16, T["muted"], "13/07/2026")

    # Memory card
    y0 = 1830
    bcard(Mx, y0, CW, 330)
    btxt(IL, y0 + 24, 20, T["text"], "Memory", bold=True)
    btxt(IL, y0 + 60, 14, T["muted"], "Speed")
    btxt(430, y0 + 60, 14, T["muted"], "DDR5-6000")
    btxt(IL, y0 + 88, 14, T["muted"], "Temps (°C):")
    dimms = [(100, None), (205, "TDIMMTS2"), (310, None), (415, "TDIMMTS4")]
    for cx, sensor in dimms:
        bring(cx, y0 + 160, 36, 7)
        if sensor:
            simple(cx - 18, y0 + 146, 13, C_text, sensor)
            pv(cx - 18, y0 + 146, 13, T["text"], "39")
        else:
            btxt(cx - 20, y0 + 148, 13, T["muted"], "N/A")
    btxt(IL, y0 + 218, 15, T["muted"], "Memory")
    simple(560, y0 + 216, 15, C_text, "SMEMUTI", unit="%")
    pv(560, y0 + 216, 15, T["text"], "76%")
    bar(IL, y0 + 248, IR - IL, 12, "SMEMUTI")
    btxt(IL, y0 + 278, 14, T["muted"], "U:")
    simple(IL + 28, y0 + 276, 14, C_text, "SUSEDMEM", unit="MB")
    pv(IL + 28, y0 + 276, 14, T["text"], "24 107 MB")
    btxt(400, y0 + 278, 14, T["muted"], "F:")
    simple(430, y0 + 276, 14, C_text, "SFREEMEM", unit="MB")
    pv(430, y0 + 276, 14, T["text"], "7 798 MB")

    # Storage card
    y0 = 2180
    bcard(Mx, y0, CW, 280)
    btxt(IL, y0 + 24, 20, T["text"], "Storage", bold=True)
    for i, (cap, sensor, tag) in enumerate([("C:", "SDRVCUTI", "SYSTEM"), ("D:", "SDRVDUTI", "DATA"), ("E:", "SDRVEUTI", "MEDIA")]):
        ry = y0 + 72 + i * 66
        btxt(IL, ry, 15, T["muted"], cap)
        simple(IL + 36, ry - 2, 15, C_text, sensor, unit="%")
        pv(IL + 36, ry - 2, 15, T["text"], ("69%", "0%", "29%")[i])
        btxt(500, ry, 14, T["muted"], tag)
        bar(IL, ry + 28, IR - IL, 10, sensor)

    btxt(0, 2534, 12, T["muted"], f"NETGNUSPC  //  {name.upper()} EDITION  //  HYTE Y70 TOUCH", center=True, w=W)

    # ---------- HTML ----------
    def html(with_pv):
        el = []
        for k in bake:
            if k[0] == "txt":
                _, x, y, size, color, text, bold, center, w = k
                st = (f"position:absolute;top:{y}px;font-family:'{FONT}',sans-serif;font-size:{size}px;"
                      f"color:{color};font-weight:{700 if bold else 400};white-space:nowrap;")
                st += f"left:{x}px;width:{w}px;text-align:center;" if center else f"left:{x}px;"
                el.append(f'<div style="{st}">{text}</div>')
            elif k[0] == "card":
                _, x, y, w, h = k
                el.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                          f'background:{T["cardbg"]};border:1px solid {T["cardborder"]};border-radius:14px;'
                          f'box-shadow:{T["cardshadow"]};"></div>')
            elif k[0] == "ring":
                _, cx, cy, r, th = k
                el.append(f'<div style="position:absolute;left:{cx-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px;'
                          f'border-radius:50%;background:{RAINBOW};'
                          f'-webkit-mask:radial-gradient(closest-side,transparent calc(100% - {th+1}px),#000 calc(100% - {th}px));'
                          f'mask:radial-gradient(closest-side,transparent calc(100% - {th+1}px),#000 calc(100% - {th}px));"></div>')
            elif k[0] == "gline":
                _, x, y, w = k
                el.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:3px;'
                          f'border-radius:2px;background:{GRAD_LINE};opacity:.85;"></div>')
        pvel = ""
        if with_pv:
            random.seed(11)
            for x, y, px, col, t, *b in preview:
                bold = b and b[0]
                pvel += (f'<div style="position:absolute;left:{x}px;top:{y}px;font-family:\'{FONT}\',sans-serif;'
                         f'font-size:{px}px;color:{col};font-weight:{700 if bold else 400};white-space:nowrap;">{t}</div>')
            for gx, gy, gw, gh in pv_graphs:
                pts, v = [], 35
                for i in range(0, gw + 1, 8):
                    v = max(5, min(95, v + random.randint(-13, 13)))
                    pts.append(f"{i},{gh - gh * v / 100:.0f}")
                pvel += (f'<svg style="position:absolute;left:{gx}px;top:{gy}px;background:{T["graphbg"]};'
                         f'border:1px solid {T["graphframe"]};" width="{gw}" height="{gh}">'
                         f'<polyline points="{" ".join(pts)}" fill="none" stroke="{T["graphline"]}" stroke-width="1.6"/></svg>')
            for bx, by, bw, bh in pv_bars:
                fill = random.randint(25, 80)
                fc = T["barfill"] if fill < 50 else (T["barmid"] if fill < 75 else T["barhigh"])
                pvel += (f'<div style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px;'
                         f'background:{T["bartrack"]};border:1px solid {T["barframe"]};border-radius:{bh//2}px;">'
                         f'<div style="width:{fill}%;height:100%;background:{fc};border-radius:{bh//2}px;"></div></div>')
        return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}'
                f'html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{T["pagebg"]}}}'
                f'body::before{{content:"";position:fixed;inset:0;background:{T["glows"]}}}'
                f'</style></head><body>{"".join(el)}{pvel}</body></html>')

    tdir = os.path.join(OUT, "trio", name)
    os.makedirs(tdir, exist_ok=True)
    for fn, wp, png in [("bg.html", False, "background.png"), ("pv.html", True, "preview.png")]:
        p = os.path.join(tdir, fn)
        with open(p, "w", encoding="utf-8") as f:
            f.write(html(wp))
        subprocess.run([CHROME, "--headless=new", f"--screenshot={os.path.join(tdir, png)}",
                        f"--window-size={W},{H}", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--disable-gpu", p], capture_output=True, timeout=120)
        os.remove(p)
    with open(os.path.join(tdir, "background.png"), "rb") as f:
        imgdat = f.read().hex().upper()
    doc = (f"<SPVER>100</SPVER><SWVER>7.40.7100</SWVER>\n"
           f"<SPWIDTH>{W}</SPWIDTH><SPHEIGHT>{H}</SPHEIGHT><SPBGCOLOR>0</SPBGCOLOR>\n"
           f"<ID>IMG</ID><URL></URL><ITMX>0</ITMX><ITMY>0</ITMY><IMGFIL>background.png</IMGFIL>"
           f"<IMGDAT>{imgdat}</IMGDAT>\n" + "\n".join(items) + "\n")
    with open(os.path.join(tdir, f"Y70-{name.upper()}.sensorpanel"), "w", encoding="cp1252", errors="replace") as f:
        f.write(doc)
    print(name, "done:", len(items), "items")

for name, T in THEMES.items():
    build_theme(name, T)
