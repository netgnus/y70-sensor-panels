F.R.I.D.A.Y. DAY EDITION  -  HYTE Y70 TOUCH (685 x 2560)
=========================================================
Light daytime version of the F.R.I.D.A.Y. v2 panel: warm cream
background, dark-gold text - same layout, sensors and rings as v2,
readable in a bright room.

Install: AIDA64 -> SensorPanel Manager -> Import -> Y70-FRIDAY-DAY.sensorpanel
Swap back to the night version the same way any time.

All sensor IDs identical to friday-v2 (verified live on NETGNUSPC):
NIC3 network, VCPU vcore, TGPU1MEM VRAM temp, SRTSSFPS via RTSS.

v2.2 (2026-07-28)
-----------------
- Drive rows now C/D/E/H with live drive temps (C=THDD2 NVMe, D=THDD3
  NVMe, H=THDD1 HDD; E is USB, no temp sensor)
- Memory module shows MOBO / VRM / PCH temps (TMOBO/TVRM/TPCH1DIO,
  all verified live)

v2.3 (2026-07-28)
-----------------
- Weather next to the date (Melbourne, Open-Meteo): temp = SREGVALS1,
  condition = SREGVALS2, fed by AIDA64 registry ImportValues.
- Updater: Documents\AIDA\weather-update.ps1, scheduled task
  "AIDA64 Weather" every 15 min (schtasks /Delete /TN "AIDA64 Weather"
  to remove). Blank until the task has run once.
