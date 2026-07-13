Y70 SKIN TRIO  -  ORIGINAL / SNOW / INK EDITIONS  (685 x 2560)
===============================================================
Recreation of the 3-edition "AIDA64 Sensor Panel Skin" pack, rebuilt for
NETGNUSPC and the HYTE Y70 Touch. Native AIDA64 format, background art
embedded - each imports directly, no manual setup.

Folders
-------
Original\  purple/nebula gradient dark theme
Snow\      clean light theme
Ink\       pure black theme
Each contains: Y70-<EDITION>.sensorpanel, background.png, preview.png

Install
-------
AIDA64 -> right-click SensorPanel -> SensorPanel Manager -> Import ->
pick the edition's .sensorpanel. Swap editions any time the same way.

Layout (top to bottom)
----------------------
- CPU card:  temp in rainbow ring, package W, Load / Voltage / Clock /
             Fan rows, load-history graph (auto-scale)
- GPU card:  temp ring, board W, Load / Voltage / Clock / VRAM Temp /
             VRAM Used % / Fan rows, load graph
- Device card: NETGNUSPC - Status: Online
- Clock card:  time + date
- Memory card: DDR5-6000, DIMM temps in mini rings (slots 2 & 4 have
               sensors; 1 & 3 show N/A), usage bar + used/free MB
- Storage card: C / D / E used-% bars

All sensor IDs verified live on this machine 2026-07-13:
TCPU PCPUPKG SCPUUTI VCPU SCPUCLK FCPU | TGPU1 PGPU1 SGPU1UTI VGPU1
SGPU1CLK TGPU1MEM SVMEMUSAGE FGPU1 | TDIMMTS2 TDIMMTS4 SMEMUTI SUSEDMEM
SFREEMEM | SDRVCUTI SDRVDUTI SDRVEUTI | STIME SDATE
(RTX 5070 Ti GPU fans legitimately read 0 RPM when idle - semi-passive.)

Bars change colour by value: blue < 50, amber < 75, pink/red above.
