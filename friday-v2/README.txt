F.R.I.D.A.Y. v2 SENSORPANEL  -  HYTE Y70 TOUCH (685 x 2560)
============================================================

Files
-----
- Y70-FRIDAY-V2.sensorpanel   AIDA64 panel (native format, background image
                              EMBEDDED inside the file - imports directly)
- background.png              the backdrop on its own (reference / re-editing)
- preview.png                 what the finished panel looks like with live data

What's new vs v1
----------------
- Written in AIDA64's REAL export format (reverse-engineered from working
  community panels), so File > Preferences > SensorPanel > Manage > Import
  just works - no manual rebuild needed.
- Background art is embedded in the .sensorpanel file itself.
- Corrected sensor IDs (v1 used SGPU1 for GPU load; the real ID is SGPU1UTI).
- Threshold-coloured bars: gold normally, orange above 80, red above 92.
- Live load-history graphs for CPU and GPU, drive usage bars, network rates,
  RTSS FPS readout.

Install
-------
1. AIDA64 Extreme or Engineer (SensorPanel needs a paid edition / 30-day trial).
2. AIDA64 -> File -> Preferences -> Hardware Monitoring -> SensorPanel:
   - Tick "Show SensorPanel"
   - Click "Manage" (or right-click the panel -> SensorPanel Manager)
   - Import... -> pick Y70-FRIDAY-V2.sensorpanel
3. Drag the panel onto the Y70 Touch display. Right-click -> lock position.
4. If your Y70 screen runs a different logical resolution, right-click the
   panel -> SensorPanel Manager and adjust, or tell Claude to regenerate at
   the exact size.

Sensor IDs used
---------------
ALL sensors verified live on NETGNUSPC via AIDA64 shared memory (2026-07-13):
  STIME / SDATE / SUPTIME         time, date, uptime
  TCPU / TMOBO / TGPU1 / TGPU1MEM CPU, motherboard, GPU core & VRAM temps
  SCPUUTI / SGPU1UTI / SMEMUTI    CPU, GPU, RAM utilisation
  SCPUCLK / SGPU1CLK              CPU / GPU clocks
  PCPUPKG / PGPU1                 CPU package / GPU power
  VCPU                            CPU vcore  (this board does NOT expose VCPUCORE)
  FCPU / FGPU1                    CPU / GPU fan RPM (GPU fans read 0 when idle)
  SUSEDMEM / SFREEMEM             RAM used / free MB
  SVMEMUSAGE                      VRAM utilisation %
  SDRVCUTI / SDRVDUTI / SDRVEUTI  drive C/D/E used-space %
  SNIC3DLRATE / SNIC3ULRATE       network down / up - NIC3 is the Intel
                                  Wi-Fi 6 AX200 on this machine
  SRTSSFPS                        FPS - RivaTuner Statistics Server must be
                                  running; reads 0 on desktop, live in games

Notes:
- The RTX 5070 Ti has no hotspot sensor (NVIDIA removed it on 50-series),
  so the panel shows GPU memory temp instead.
- If Windows re-orders adapters after hardware changes, rebind the two
  network items to whichever NICx shows traffic.

Editing
-------
Every value is a normal SensorPanel item - right-click any element ->
SensorPanel Manager to change sensor, font, colour or position. The static
gold frames, titles and labels are baked into the background image.

Enjoy, Boss.
