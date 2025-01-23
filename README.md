# Windows Service Monitor

Sistema automatizado para monitoramento e gestão de serviços Windows.

## 📋 Descrição
Este projeto oferece uma solução automatizada para monitoramento de serviços Windows, com capacidade de reinício automático em caso de falhas e reinícios programados.

## ⚙️ Funcionalidades
- Monitoramento automático de serviços Windows
- Reinício automático em caso de falha
- Reinícios programados configuráveis
- Sistema de logs com rotação diária
- Instalação automatizada via PowerShell

## 🔧 Requisitos
- Windows Server/Windows 10
- Python 3.x
- Permissões administrativas
- PowerShell habilitado para scripts

## 📦 Instalação

1. Clone o repositório
git clone https://github.com/PedroMarino03/windows-service-monitor.git

2. Configure os serviços a serem monitorados:
- Abra `src/monitor.py`
- Ajuste os nomes dos serviços (ServiceMain e ServiceScheduled)

3. Execute o script de instalação:
- Abra PowerShell como Administrador
- Navegue até a pasta do projeto
- Execute: `.\src\install.ps1`

## 🚀 Uso

O sistema irá:
- Monitorar os serviços configurados a cada hora
- Realizar reinícios programados (5:00 e 17:00)
- Gerar logs em `C:\ServiceMonitor\Monitor\service_monitor.log`

### Estrutura de Logs
[2025-01-22 08:00:00] [INFO ] - Iniciando monitoramento
[2025-01-22 08:00:01] [INFO ] - ServiceMain está em execução
[2025-01-22 08:00:02] [INFO ] - ServiceScheduled está em execução

## ⚠️ Configuração

Para modificar os serviços monitorados:
1. Edite `src/monitor.py`
2. Altere os nomes dos serviços
3. Ajuste os intervalos conforme necessário

## 🤝 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📫 Contato
- Pedro Marino
- LinkedIn: [https://www.linkedin.com/in/pedromarino1702/]
- Email: [pedro.marino23@gmail.com]

