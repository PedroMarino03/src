import os
import sys
from datetime import datetime

def get_execution_path():
    """Obtém o caminho correto seja executando como script ou exe"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def verificar_data_log():
    """Verifica se o log é de um dia anterior e limpa se necessário"""
    log_file = os.path.join(get_execution_path(), 'service_monitor.log')
    
    if os.path.exists(log_file):
        data_atual = datetime.now().strftime('%Y-%m-%d')
        
        with open(log_file, 'r', encoding='utf-8') as f:
            primeira_linha = f.readline().strip()
            
        if not primeira_linha or data_atual not in primeira_linha:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO ] - Arquivo de log iniciado\n")
                f.write("-" * 80 + "\n")

def log_message(message, tipo="INFO"):
    """Registra mensagens no arquivo de log com formato melhorado."""
    verificar_data_log()
    
    log_file = os.path.join(get_execution_path(), 'service_monitor.log')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    log_entry = f"[{timestamp}] [{tipo:5}] - {message}\n"
    
    if "Iniciando execução" in message:
        separator = "-" * 80 + "\n"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(separator)
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def verificar_servico(nome):
    """Verifica se o serviço está ativo e existe."""
    resultado = os.popen(f'sc query "{nome}"').read()
    if "1060" in resultado:  # Código de erro quando serviço não existe
        log_message(f"Serviço {nome} não está instalado neste servidor", "INFO")
        return None
    return "RUNNING" in resultado

def reiniciar_servico(nome):
    """Reinicia o serviço."""
    log_message(f"Iniciando processo de reinício do serviço: {nome}", "WARN")
    os.system(f'sc stop "{nome}"')
    log_message(f"Serviço {nome} parado", "INFO")
    os.system('timeout /t 10')
    os.system(f'sc start "{nome}"')
    log_message(f"Serviço {nome} iniciado com sucesso", "INFO")

def monitorar_servicos():
    """Monitora os serviços instalados."""
    log_message("Iniciando ciclo de monitoramento dos serviços", "INFO")
    
    # Monitoramento do serviço principal
    if not verificar_servico("ServiceMain"):
        log_message("ServiceMain está PARADO", "ALERT")
        reiniciar_servico("ServiceMain")
    else:
        log_message("ServiceMain está em execução", "INFO")
    
    # Verifica serviço com reinício programado
    status_scheduled = verificar_servico("ServiceScheduled")
    if status_scheduled is not None:
        if not status_scheduled:
            log_message("ServiceScheduled está PARADO", "ALERT")
            reiniciar_servico("ServiceScheduled")
        else:
            log_message("ServiceScheduled está em execução", "INFO")
    
    log_message("Ciclo de monitoramento finalizado", "INFO")

def reinicio_programado():
    """Executa o reinício programado do ServiceScheduled."""
    log_message("Verificando existência do ServiceScheduled para reinício programado", "INFO")
    status = verificar_servico("ServiceScheduled")
    
    if status is not None:
        log_message("Iniciando reinício programado do ServiceScheduled", "WARN")
        reiniciar_servico("ServiceScheduled")
        log_message("Reinício programado concluído com sucesso", "INFO")
    else:
        log_message("Reinício programado ignorado - ServiceScheduled não está instalado", "INFO")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--reinicio":
            log_message("Iniciando execução com parâmetro de reinício", "INFO")
            reinicio_programado()
        else:
            log_message("Iniciando execução de monitoramento padrão", "INFO")
            monitorar_servicos()
    except Exception as e:
        log_message(f"Erro durante a execução: {str(e)}", "ERROR")
