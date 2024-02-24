Get-WmiObject -Class Win32_LogicalDisk | Select-Object size, deviceid, drivetype | ConvertTo-Json
