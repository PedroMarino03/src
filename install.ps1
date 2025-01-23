# Definir caminhos
$destPath = "C:\ServiceMonitor\Monitor"

# Criar diretório se não existir
if (!(Test-Path $destPath)) {
    New-Item -ItemType Directory -Path $destPath -Force
    Write-Host "Diretório criado: $destPath" -ForegroundColor Green
}

# Copiar executável
try {
    Copy-Item "monitor.exe" $destPath -Force
    Write-Host "Arquivo copiado com sucesso" -ForegroundColor Green
} catch {
    Write-Host "Erro ao copiar arquivo: $_" -ForegroundColor Red
    exit
}

# Criar tarefa de monitoramento (1 em 1 hora)
$action = New-ScheduledTaskAction -Execute "$destPath\monitor.exe"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Hours 1)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName "ServiceMonitor" -Action $action -Trigger $trigger -Settings $settings -RunLevel Highest -User "SYSTEM" -Force

# Criar tarefa de reinício programado
$action2 = New-ScheduledTaskAction -Execute "$destPath\monitor.exe" -Argument "--reinicio"
$amanha = (Get-Date).AddDays(1).Date.AddHours(5)
$trigger2 = New-ScheduledTaskTrigger -Once -At $amanha -RepetitionInterval (New-TimeSpan -Hours 12)
$settings2 = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Hours 1)
Register-ScheduledTask -TaskName "ServiceRestart" -Action $action2 -Trigger $trigger2 -Settings $settings2 -RunLevel Highest -User "SYSTEM" -Force

Write-Host "Instalação concluída com sucesso!" -ForegroundColor Green
