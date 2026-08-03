# Y70 F.R.I.D.A.Y. v2 — AIDA64 SensorPanel generator (HYTE Y70 Touch, 685x2560)
# Generates: background.png (via headless Chrome), preview.png, .sensorpanel
# Usage: python gen.py        -> night (gold on black), Y70-FRIDAY-V2
#        python gen.py day    -> day   (dark gold on cream), Y70-FRIDAY-DAY
#        python gen.py blue   -> night (arc-reactor blue), Y70-FRIDAY-BLUE
import subprocess, os, sys

THEME = sys.argv[1] if len(sys.argv) > 1 else "night"
DAY = THEME == "day"
OUT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(OUT, f"out-{THEME}")
os.makedirs(OUT, exist_ok=True)
NAME = {"night": "Y70-FRIDAY-V2", "day": "Y70-FRIDAY-DAY", "blue": "Y70-FRIDAY-BLUE"}[THEME]
W, H = 685, 2560
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# ---------- palette ----------
# key names keep the night theme's vocabulary (gold = primary accent, etc.)
PAL = dict(
    gold="#FFB800", bright="#FFD76A", cream="#FFE48A", text="#F5E6C0",
    muted="#8A7340", line="#3D2C00", line2="#6B4C00", panel="#0A0703",
    warn="#FF9500", bad="#FF3B3B", dark="#1A1100",
)
if THEME == "day":
    PAL.update(
        gold="#9C7400", bright="#845F00", cream="#755808", text="#3A3018",
        muted="#857347", line="#CDBB88", line2="#B0924E", panel="#F1E4C4",
        warn="#D97700", bad="#CC2222", dark="#E0CFA4",
    )
elif THEME == "blue":
    PAL.update(
        gold="#00A8FF", bright="#6ECBFF", cream="#A5DEFF", text="#C8E4F5",
        muted="#48688A", line="#00263D", line2="#00517E", panel="#020A10",
        warn="#FFB03C", bad="#FF3B3B", dark="#001828",
    )
GLOW = {"day": "rgba(140,105,0,.20)", "night": "rgba(255,184,0,.35)",
        "blue": "rgba(0,168,255,.38)"}[THEME]
BODYBG = {"day": "#E4D5AF", "night": "#000", "blue": "#000205"}[THEME]
GLOW1 = {"day": "rgba(244,231,199,.7)", "night": "rgba(255,215,106,.10)", "blue": "rgba(110,203,255,.10)"}[THEME]
GLOW2 = {"day": "rgba(240,226,190,.5)", "night": "rgba(255,184,0,.06)", "blue": "rgba(0,168,255,.06)"}[THEME]
GLOW3 = {"day": "rgba(242,228,193,.6)", "night": "rgba(255,184,0,.08)", "blue": "rgba(0,168,255,.09)"}[THEME]
SCAN = {"day": "rgba(130,95,0,.035)", "night": "rgba(255,184,0,.02)", "blue": "rgba(0,168,255,.025)"}[THEME]
FRAMEBG = {"day": "rgba(243,230,198,.8),rgba(236,220,180,.6)",
           "night": "rgba(26,17,0,.55),rgba(10,7,3,.35)",
           "blue": "rgba(0,22,38,.60),rgba(2,8,14,.38)"}[THEME]
def cref(hexcol):  # '#RRGGBB' -> Windows COLORREF int (R + G<<8 + B<<16)
    r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
    return r + (g << 8) + (b << 16)
C = {k: cref(v) for k, v in PAL.items()}

# ---------- shared layout ----------
bake = []   # baked into background: (kind, ...)
items = []  # AIDA64 items

def btxt(x, y, size, color, text, ls=0.25, bold=False, center=False, w=None):
    bake.append(("txt", x, y, size, color, text, ls, bold, center, w))
def brule(x, y, w, grad=True):
    bake.append(("rule", x, y, w, grad))
def bframe(x, y, w, h):
    bake.append(("frame", x, y, w, h))
def bcirc(cx, cy, r):
    bake.append(("circ", cx, cy, r))

def lbl(x, y, pt, color, text, bold=False):
    b = "1" if bold else "0"
    items.append(f"<ID>LBL</ID><TXTSIZ>{pt}</TXTSIZ><FNTNAM>Consolas</FNTNAM><LBL>{text}</LBL>"
                 f"<LBLCOL>{color}</LBLCOL><LBLBIS>{b}00</LBLBIS><SHDCOL>0</SHDCOL><SHDDIS>1</SHDDIS>"
                 f"<SHDDEP>1</SHDDEP><URL></URL><ITMX>{x}</ITMX><ITMY>{y}</ITMY>")
def simple(x, y, pt, color, sensor, unit="", bold=False):
    b = "1" if bold else "0"
    shwunt = "1" if unit else "0"
    items.append(f"<ID>[SIMPLE]{sensor}</ID><TXTSIZ>{pt}</TXTSIZ><FNTNAM>Consolas</FNTNAM>"
                 f"<TXTCOL>{color}</TXTCOL><TXTBIR>{b}00</TXTBIR><SHWLBL>0</SHWLBL><LBL></LBL>"
                 f"<SHWUNT>{shwunt}</SHWUNT><UNT>{unit}</UNT><ITMX>{x}</ITMX><ITMY>{y}</ITMY>")
pv_bars = []  # (x, y, w, h) preview-only
def bar(x, y, w, h, sensor, fg="gold"):
    pv_bars.append((x, y, w, h))
    items.append(f"<ID>{sensor}</ID><WID>60</WID><TXTSIZ>10</TXTSIZ><FNTNAM>Consolas</FNTNAM>"
                 f"<SHDCOL>0</SHDCOL><SHDDIS>1</SHDDIS><SHDDEP>1</SHDDEP><SHWLBL>0</SHWLBL><LBL></LBL>"
                 f"<LBLCOL>{C['muted']}</LBLCOL><LBLBIS>000</LBLBIS><SHWVAL>0</SHWVAL>"
                 f"<VALCOL>{C['bright']}</VALCOL><VALBIS>000</VALBIS><SHWUNT>0</SHWUNT><UNT></UNT>"
                 f"<UNTCOL>{C['text']}</UNTCOL><UNTBIS>000</UNTBIS><UNTWID>10</UNTWID>"
                 f"<SHWBAR>1</SHWBAR><BARWID>{w}</BARWID><BARHEI>{h}</BARHEI><BARIND>0</BARIND>"
                 f"<BARPLC>SEP</BARPLC><BARFS>0010</BARFS><BARFRMCOL>{C['line2']}</BARFRMCOL>"
                 f"<BARMIN></BARMIN><BARLIM1>60</BARLIM1><BARLIM2>80</BARLIM2><BARLIM3>92</BARLIM3><BARMAX></BARMAX>"
                 f"<BARMINFGC>{C[fg]}</BARMINFGC><BARMINBGC>{C['dark']}</BARMINBGC>"
                 f"<BARLIM1FGC>{C[fg]}</BARLIM1FGC><BARLIM1BGC>{C['dark']}</BARLIM1BGC>"
                 f"<BARLIM2FGC>{C['warn']}</BARLIM2FGC><BARLIM2BGC>{C['dark']}</BARLIM2BGC>"
                 f"<BARLIM3FGC>{C['bad']}</BARLIM3FGC><BARLIM3BGC>{C['dark']}</BARLIM3BGC>"
                 f"<ITMX>{x}</ITMX><ITMY>{y}</ITMY>")
def graph(x, y, w, h, sensor, col="gold"):
    items.append(f"<ID>[GRAPH]{sensor}</ID><LBL></LBL><TYP>LG</TYP><WID>{w}</WID><HEI>{h}</HEI>"
                 f"<GPHSTP>1</GPHSTP><GPHTCK>1</GPHTCK><GRDDNS>10</GRDDNS><MINVAL>0</MINVAL>"
                 f"<MAXVAL>100</MAXVAL><AUTSCL>0</AUTSCL><GRDCOL>{C['line']}</GRDCOL>"
                 f"<GPHCOL>{C[col]}</GPHCOL><BGCOL>{C['panel']}</BGCOL><FRMCOL>{C['line2']}</FRMCOL>"
                 f"<GPHBFG>111</GPHBFG><SHWSCL>0</SHWSCL><TXTSIZ>8</TXTSIZ><FNTNAM>Consolas</FNTNAM>"
                 f"<SCLCOL>{C['muted']}</SCLCOL><SCLBI>000</SCLBI><ITMX>{x}</ITMX><ITMY>{y}</ITMY>")

preview = []  # (x, y, px, colorhex, text) sample values for preview.png only
pv_graphs = []  # (x, y, w, h, colorhex) fake graph traces for preview.png only
def pv(x, y, pt, colorkey, text):
    preview.append((x, y, round(pt * 1.33), PAL[colorkey], text))

# =============== LAYOUT ===============
ML, MR = 30, 655           # module left/right
IL, IR = 50, 635           # inner left/right
VX = 400                   # value column x
LX = 250                   # row-label x in two-col modules

# ---- header ----
btxt(0, 26, 30, PAL["gold"], "F.R.I.D.A.Y.", ls=0.42, bold=True, center=True, w=W)
btxt(0, 72, 13, PAL["cream"], "NETGNUSPC  //  SYSTEM TELEMETRY", ls=0.32, center=True, w=W)
brule(ML, 100, MR - ML)

# ---- clock ----
simple(120, 128, 78, C["gold"], "STIME", bold=True)
simple(130, 268, 15, C["cream"], "SDATE")
btxt(300, 272, 11, PAL["muted"], "//", ls=0.1)
simple(340, 268, 15, C["bright"], "SREGVALS1", bold=True)   # weather temp (registry import)
simple(425, 268, 15, C["cream"], "SREGVALS2")               # weather condition
pv(130, 268, 15, "cream", "13/07/2026")
pv(340, 268, 15, "bright", "14°C"); pv(425, 268, 15, "cream", "MOSTLY CLEAR")
btxt(0, 306, 12, PAL["muted"], "SESSION UPTIME", ls=0.35, center=True, w=W)
simple(268, 326, 13, C["bright"], "SUPTIME")

# ---- module 00 : identity ----
bframe(ML, 372, MR - ML, 268)
btxt(IL, 390, 15, PAL["gold"], "SYSTEM IDENTITY  //  00", ls=0.3, bold=True)
brule(IL, 418, IR - IL, grad=False)
specs = [
    ("PROCESSOR", "AMD RYZEN 7 7800X3D · 8C/16T"),
    ("GRAPHICS",  "NVIDIA RTX 5070 Ti · 16 GB GDDR7"),
    ("MEMORY",    "64 GB DDR5-6000 · VENGEANCE"),
    ("BOARD",     "ASUS PRIME X670-P · AM5"),
    ("STORAGE",   "6 DRIVES · 8.6 TB TOTAL"),
    ("OS",        "WINDOWS 11 PRO 25H2"),
]
for i, (k, v) in enumerate(specs):
    yy = 436 + i * 33
    btxt(IL, yy, 12, PAL["muted"], k, ls=0.2)
    lbl(210, yy - 2, 11, C["text"], v)
    pv(210, yy - 2, 11, "text", v)

# ---- module helper for CPU / GPU ----
def hw_module(y0, title, sub, temp_sensor, temp_cap, rows, graph_sensor, gcol, samples):
    bframe(ML, y0, MR - ML, 470)
    btxt(IL, y0 + 18, 16, PAL["gold"], title, ls=0.3, bold=True)
    btxt(IL, y0 + 46, 11, PAL["cream"], sub, ls=0.2)
    brule(IL, y0 + 68, IR - IL, grad=False)
    bcirc(135, y0 + 152, 84)                                         # temp ring
    simple(93, y0 + 112, 54, C["bright"], temp_sensor, bold=True)    # big temp
    btxt(53, y0 + 196, 10, PAL["muted"], temp_cap, ls=0.2, center=True, w=164)
    pv(93, y0 + 112, 54, "bright", samples[0])
    for i, (cap, sensor, unit, colkey, mk_bar) in enumerate(rows):
        ry = y0 + 86 + i * 34
        btxt(LX, ry + 4, 11, PAL["muted"], cap, ls=0.2)
        simple(VX, ry, 14, C[colkey], sensor, unit=unit, bold=(i == 0))
        pv(VX, ry, 14, colkey, samples[i + 1])
        if mk_bar:
            bar(LX, ry + 24, IR - LX, 9, sensor)
    graph(IL, y0 + 260, IR - IL - 4, 140, graph_sensor, gcol)
    pv_graphs.append((IL, y0 + 260, IR - IL - 4, 140, PAL[gcol]))
    btxt(IL, y0 + 414, 10, PAL["muted"], "LOAD HISTORY // 0-100%", ls=0.25)

# ---- module 01 : CPU (y 680..1150) ----
hw_module(680, "PROCESSOR  //  01", "RYZEN 7 7800X3D — 8C/16T",
          "TCPU", "CORE TEMP °C",
          [("LOAD",  "SCPUUTI",  "%",   "bright", True),
           ("CLOCK", "SCPUCLK",  "MHz", "gold",   False),
           ("POWER", "PCPUPKG",  "W",   "text",   False),
           ("VCORE", "VCPU",     "V",   "text",   False),
           ("FAN",   "FCPU",     "RPM", "text",   False)],
          "SCPUUTI", "gold",
          ["62", "34 %", "4650 MHz", "74.2 W", "1.185 V", "1180 RPM"])

# ---- module 02 : GPU (y 1180..1650) ----
hw_module(1180, "GRAPHICS  //  02", "NVIDIA RTX 5070 Ti — 16 GB GDDR7",
          "TGPU1", "GPU TEMP °C",
          [("LOAD",    "SGPU1UTI",     "%",   "bright", True),
           ("CLOCK",   "SGPU1CLK",     "MHz", "gold",   False),
           ("POWER",   "PGPU1",        "W",   "text",   False),
           ("MEM TEMP", "TGPU1MEM", "°C", "text", False),
           ("FAN",     "FGPU1",        "RPM", "text",   False)],
          "SGPU1UTI", "bright",
          ["48", "97 %", "2917 MHz", "285.0 W", "74 °C", "1650 RPM"])

# ---- module 03 : memory (y 1690..1960) ----
y0 = 1690
bframe(ML, y0, MR - ML, 270)
btxt(IL, y0 + 18, 16, PAL["gold"], "MEMORY  //  03", ls=0.3, bold=True)
btxt(IL, y0 + 46, 11, PAL["cream"], "64 GB DDR5-6000 — CORSAIR VENGEANCE", ls=0.2)
brule(IL, y0 + 68, IR - IL, grad=False)
bcirc(135, y0 + 158, 76)                                          # RAM % ring
simple(93, y0 + 122, 46, C["bright"], "SMEMUTI", bold=True)
btxt(53, y0 + 196, 10, PAL["muted"], "RAM USED %", ls=0.2, center=True, w=164)
pv(93, y0 + 122, 46, "bright", "76")
btxt(LX, y0 + 90, 11, PAL["muted"], "USED", ls=0.2);    simple(VX, y0 + 86, 14, C["bright"], "SUSEDMEM", unit="MB", bold=True)
bar(LX, y0 + 110, IR - LX, 9, "SMEMUTI")
btxt(LX, y0 + 130, 11, PAL["muted"], "FREE", ls=0.2);   simple(VX, y0 + 126, 14, C["text"], "SFREEMEM", unit="MB")
btxt(LX, y0 + 164, 11, PAL["muted"], "VIRTUAL", ls=0.2); simple(VX, y0 + 160, 14, C["text"], "SVMEMUSAGE", unit="%")
btxt(LX, y0 + 198, 11, PAL["muted"], "MOBO", ls=0.2);    simple(LX + 52, y0 + 194, 13, C["bright"], "TMOBO", unit="°C")
btxt(392, y0 + 198, 11, PAL["muted"], "VRM", ls=0.2);    simple(434, y0 + 194, 13, C["text"], "TVRM", unit="°C")
btxt(516, y0 + 198, 11, PAL["muted"], "PCH", ls=0.2);    simple(558, y0 + 194, 13, C["text"], "TPCH1DIO", unit="°C")
pv(VX, y0 + 86, 14, "bright", "24 107 MB"); pv(VX, y0 + 126, 14, "text", "7 798 MB")
pv(VX, y0 + 160, 14, "text", "27 %")
pv(LX + 52, y0 + 194, 13, "bright", "34 °C"); pv(434, y0 + 194, 13, "text", "38 °C"); pv(558, y0 + 194, 13, "text", "52 °C")

# ---- module 04 : storage + network (y 2000..2400) ----
y0 = 2000
bframe(ML, y0, MR - ML, 400)
btxt(IL, y0 + 18, 16, PAL["gold"], "STORAGE & NETWORK  //  04", ls=0.3, bold=True)
brule(IL, y0 + 46, IR - IL, grad=False)
drives = [("C:  SYSTEM · NVME", "SDRVCUTI", "THDD2", "69", "38"),
          ("D:  DATA · NVME",   "SDRVDUTI", "THDD3", "0",  "48"),
          ("E:  MEDIA · USB",   "SDRVEUTI", None,    "29", None),
          ("H:  ARCHIVE · HDD", "SDRVHUTI", "THDD1", "62", "36")]
for i, (cap, sensor, tsensor, upv, tpv) in enumerate(drives):
    ry = y0 + 62 + i * 56
    btxt(IL, ry, 11, PAL["muted"], cap, ls=0.2)
    simple(390, ry - 4, 13, C["text"], sensor, unit="% USED")
    pv(390, ry - 4, 13, "text", f"{upv} % USED")
    if tsensor:
        simple(560, ry - 4, 13, C["bright"], tsensor, unit="°C")
        pv(560, ry - 4, 13, "bright", f"{tpv} °C")
    bar(IL, ry + 20, IR - IL, 9, sensor)
ny = y0 + 296
btxt(IL, ny, 12, PAL["gold"], "NETWORK", ls=0.3, bold=True)
brule(IL, ny + 22, IR - IL, grad=False)
btxt(IL, ny + 38, 11, PAL["muted"], "DOWN", ls=0.2); simple(180, ny + 34, 13, C["bright"], "SNIC3DLRATE", unit="KB/s")
btxt(360, ny + 38, 11, PAL["muted"], "UP", ls=0.2);  simple(430, ny + 34, 13, C["text"], "SNIC3ULRATE", unit="KB/s")
btxt(IL, ny + 74, 11, PAL["muted"], "FPS", ls=0.2);  simple(180, ny + 70, 13, C["gold"], "SRTSSFPS", bold=True)
btxt(260, ny + 74, 10, PAL["line2"], "RTSS — IN-GAME ONLY", ls=0.15)
pv(180, ny + 34, 13, "bright", "2 340 KB/s"); pv(430, ny + 34, 13, "text", "188 KB/s"); pv(180, ny + 70, 13, "gold", "144")

# ---- footer ----
brule(ML, 2478, MR - ML)
btxt(0, 2498, 11, PAL["muted"], "AIDA64 EXTREME  //  HYTE Y70 TOUCH  //  685 x 2560", ls=0.28, center=True, w=W)
pv(120, 128, 78, "gold", "21:36:54"); pv(268, 326, 13, "bright", "3 d 04:12")

# =============== HTML background ===============
def build_html(with_preview):
    el = []
    for k in bake:
        if k[0] == "txt":
            _, x, y, size, color, text, ls, bold, center, w = k
            style = (f"position:absolute;top:{y}px;font-family:Consolas,monospace;"
                     f"font-size:{size}px;color:{color};letter-spacing:{ls}em;"
                     f"font-weight:{700 if bold else 400};white-space:nowrap;")
            style += f"left:{x}px;width:{w or W}px;text-align:center;" if center else f"left:{x}px;"
            if bold: style += f"text-shadow:0 0 14px {color}88;"
            el.append(f'<div style="{style}">{text}</div>')
        elif k[0] == "rule":
            _, x, y, w, grad = k
            bgcss = (f"linear-gradient(90deg,transparent,{PAL['gold']} 18%,{PAL['bright']} 50%,{PAL['gold']} 82%,transparent)"
                     if grad else f"linear-gradient(90deg,{PAL['line2']},{PAL['line']} 85%,transparent)")
            el.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:2px;background:{bgcss};"></div>')
        elif k[0] == "circ":
            _, cx, cy, r = k
            el.append(
                # outer gold ring with glow
                f'<div style="position:absolute;left:{cx-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px;'
                f'border-radius:50%;border:2px solid {PAL["gold"]};opacity:.85;'
                f'box-shadow:0 0 18px {GLOW}, inset 0 0 18px {GLOW};"></div>'
                # inner faint ring
                f'<div style="position:absolute;left:{cx-r+8}px;top:{cy-r+8}px;width:{2*(r-8)}px;height:{2*(r-8)}px;'
                f'border-radius:50%;border:1px solid {PAL["line2"]};"></div>'
                # top tick
                f'<div style="position:absolute;left:{cx-1}px;top:{cy-r-6}px;width:3px;height:12px;'
                f'background:{PAL["bright"]};box-shadow:0 0 8px {PAL["gold"]};"></div>')
        elif k[0] == "frame":
            _, x, y, w, h = k
            el.append(
                f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
                f'background:linear-gradient(180deg,{FRAMEBG});'
                f'border:1px solid {PAL["line2"]};'
                f'clip-path:polygon(0 14px,14px 0,calc(100% - 14px) 0,100% 14px,100% calc(100% - 14px),'
                f'calc(100% - 14px) 100%,14px 100%,0 calc(100% - 14px));"></div>'
                f'<div style="position:absolute;left:{x+14}px;top:{y}px;width:{w-28}px;height:2px;'
                f'background:linear-gradient(90deg,transparent,{PAL["gold"]} 30%,{PAL["gold"]} 70%,transparent);opacity:.65;"></div>')
    corners = "".join(
        f'<div style="position:absolute;{pos}width:26px;height:26px;border:2px solid {PAL["gold"]};{cut}opacity:.9;"></div>'
        for pos, cut in [("left:10px;top:10px;", "border-right:none;border-bottom:none;"),
                         ("right:10px;top:10px;", "border-left:none;border-bottom:none;"),
                         ("left:10px;bottom:10px;", "border-right:none;border-top:none;"),
                         ("right:10px;bottom:10px;", "border-left:none;border-top:none;")])
    pvel = ""
    if with_preview:
        pvel = "".join(
            f'<div style="position:absolute;left:{x}px;top:{y}px;font-family:Consolas,monospace;'
            f'font-size:{px}px;color:{col};white-space:nowrap;text-shadow:0 0 12px {col}66;">{t}</div>'
            for x, y, px, col, t in preview)
        import random
        random.seed(7)
        for gx, gy, gw, gh, gcol in pv_graphs:
            pts, v = [], 35
            for i in range(0, gw + 1, 8):
                v = max(5, min(95, v + random.randint(-14, 14)))
                pts.append(f"{i},{gh - gh * v / 100:.0f}")
            pvel += (f'<svg style="position:absolute;left:{gx}px;top:{gy}px;background:{PAL["panel"]};'
                     f'border:1px solid {PAL["line2"]};" width="{gw}" height="{gh}">'
                     f'<polyline points="{" ".join(pts)}" fill="none" stroke="{gcol}" stroke-width="1.6"/></svg>')
        for bx, by, bw, bh in pv_bars:
            fill = random.randint(30, 75)
            pvel += (f'<div style="position:absolute;left:{bx}px;top:{by}px;width:{bw}px;height:{bh}px;'
                     f'background:{PAL["dark"]};border:1px solid {PAL["line2"]};">'
                     f'<div style="width:{fill}%;height:100%;background:{PAL["gold"]};"></div></div>')
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:{W}px;height:{H}px;overflow:hidden;background:{BODYBG}}}
body::before{{content:"";position:fixed;inset:0;background:
 radial-gradient(ellipse 90% 40% at 50% 8%,{GLOW1},transparent 70%),
 radial-gradient(ellipse 90% 30% at 50% 55%,{GLOW2},transparent 70%),
 radial-gradient(ellipse 90% 30% at 50% 95%,{GLOW3},transparent 70%),
 repeating-linear-gradient(0deg,{SCAN} 0 1px,transparent 1px 3px);}}
</style></head><body>{corners}{"".join(el)}{pvel}</body></html>"""

for name, wp in [("bg.html", False), ("preview.html", True)]:
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(build_html(wp))

for html, png in [("bg.html", "background.png"), ("preview.html", "preview.png")]:
    subprocess.run([CHROME, "--headless=new", f"--screenshot={os.path.join(OUT, png)}",
                    f"--window-size={W},{H}", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--disable-gpu", os.path.join(OUT, html)], capture_output=True, timeout=120)

# =============== .sensorpanel ===============
with open(os.path.join(OUT, "background.png"), "rb") as f:
    imgdat = f.read().hex().upper()
img_item = f"<ID>IMG</ID><URL></URL><ITMX>0</ITMX><ITMY>0</ITMY><IMGFIL>background.png</IMGFIL><IMGDAT>{imgdat}</IMGDAT>"
doc = (f"<SPVER>100</SPVER><SWVER>7.40.7100</SWVER>\n"
       f"<SPWIDTH>{W}</SPWIDTH><SPHEIGHT>{H}</SPHEIGHT><SPBGCOLOR>0</SPBGCOLOR>\n"
       + img_item + "\n" + "\n".join(items) + "\n")
with open(os.path.join(OUT, NAME + ".sensorpanel"), "w", encoding="cp1252", errors="replace") as f:
    f.write(doc)
print(NAME, "| items:", len(items), "| png:", os.path.getsize(os.path.join(OUT, 'background.png')),
      "| panel:", os.path.getsize(os.path.join(OUT, NAME + '.sensorpanel')))
