# Script PowerShell para remover a variável de ambiente OPENAI_API_KEY
# Este script é executado durante a desinstalação do Ragner

Write-Host "Removendo variável de ambiente OPENAI_API_KEY..."

# Remover da variável de usuário
try {
    [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $null, [System.EnvironmentVariableTarget]::User)
    Write-Host "Variável de usuário OPENAI_API_KEY removida com sucesso."
}
catch {
    Write-Host "Erro ao remover variável de usuário: $($_.Exception.Message)"
}

# Remover da variável de sistema (se executando como administrador)
try {
    $isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
    
    if ($isAdmin) {
        [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $null, [System.EnvironmentVariableTarget]::Machine)
        Write-Host "Variável de sistema OPENAI_API_KEY removida com sucesso."
    }
    else {
        Write-Host "Não executando como administrador - variável de sistema não removida."
    }
}
catch {
    Write-Host "Erro ao remover variável de sistema: $($_.Exception.Message)"
}

# Verificar se a variável foi removida
$userVar = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", [System.EnvironmentVariableTarget]::User)
$machineVar = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", [System.EnvironmentVariableTarget]::Machine)

if ($null -eq $userVar -and $null -eq $machineVar) {
    Write-Host "Variável OPENAI_API_KEY removida com sucesso de todos os contextos."
    exit 0
}
else {
    Write-Host "AVISO: Variável OPENAI_API_KEY ainda existe em alguns contextos."
    if ($userVar) { Write-Host "  - Variável de usuário ainda existe: $userVar" }
    if ($machineVar) { Write-Host "  - Variável de sistema ainda existe: $machineVar" }
    exit 1
}
