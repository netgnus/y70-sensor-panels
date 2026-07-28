# AIDA64 weather updater - writes current Melbourne weather to AIDA64 ImportValues.
# Str1 = temperature ("22°C"), Str2 = condition ("PARTLY CLOUDY").
# Scheduled task "AIDA64 Weather" runs this every 15 minutes.
$ErrorActionPreference = "Stop"
try {
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    $url = "https://api.open-meteo.com/v1/forecast?latitude=-37.814&longitude=144.963&current=temperature_2m,weather_code&timezone=Australia%2FMelbourne"
    $w = (Invoke-RestMethod -Uri $url -TimeoutSec 20).current
    $codes = @{
        0="CLEAR"; 1="MOSTLY CLEAR"; 2="PARTLY CLOUDY"; 3="OVERCAST";
        45="FOG"; 48="RIME FOG"; 51="LIGHT DRIZZLE"; 53="DRIZZLE"; 55="HEAVY DRIZZLE";
        56="FRZ DRIZZLE"; 57="FRZ DRIZZLE"; 61="LIGHT RAIN"; 63="RAIN"; 65="HEAVY RAIN";
        66="FRZ RAIN"; 67="FRZ RAIN"; 71="LIGHT SNOW"; 73="SNOW"; 75="HEAVY SNOW"; 77="SNOW GRAINS";
        80="SHOWERS"; 81="SHOWERS"; 82="HEAVY SHOWERS"; 85="SNOW SHOWERS"; 86="SNOW SHOWERS";
        95="THUNDERSTORM"; 96="THUNDERSTORM"; 99="HAIL STORM"
    }
    $cond = $codes[[int]$w.weather_code]; if (-not $cond) { $cond = "---" }
    $temp = "{0}{1}C" -f [Math]::Round($w.temperature_2m), [char]176
    $key = "HKCU:\Software\FinalWire\AIDA64\ImportValues"
    if (-not (Test-Path $key)) { New-Item -Path $key -Force | Out-Null }
    Set-ItemProperty -Path $key -Name "Str1" -Value $temp
    Set-ItemProperty -Path $key -Name "Str2" -Value $cond
} catch {
    # leave last values in place on network failure
}
