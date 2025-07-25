"""
Utilitários para detecção de capacidades do terminal.
"""

import os
import sys
import platform

def terminal_suporta_cores():
    """
    Detecta se o terminal atual suporta códigos de escape ANSI para cores.
    
    Returns:
        bool: True se o terminal suporta cores, False caso contrário
    """
    # Verificar variáveis de ambiente comuns
    if os.getenv('TERM') in ['dumb', 'unknown']:
        return False
    
    # Windows: verificar se está no PowerShell moderno ou Windows Terminal
    if platform.system() == 'Windows':
        # Verificar se está no Windows Terminal
        if os.getenv('WT_SESSION'):
            return True
        
        # Verificar se está no PowerShell Core (7+)
        if 'pwsh' in os.getenv('PSModulePath', '').lower():
            return True
        
        # Verificar se colorama está disponível
        try:
            import colorama
            return True
        except ImportError:
            pass
        
        # Windows CMD tradicional geralmente não suporta cores bem
        return False
    
    # Unix/Linux: a maioria dos terminais modernos suporta cores
    return True

def configurar_terminal_para_cores():
    """
    Configura o terminal para suporte a cores quando possível.
    """
    if platform.system() == 'Windows':
        try:
            # Tentar habilitar suporte ANSI no Windows
            import colorama
            colorama.init(autoreset=True)
            return True
        except ImportError:
            return False
    return True

def obter_info_terminal():
    """
    Retorna informações sobre o terminal atual.
    
    Returns:
        dict: Informações sobre o terminal
    """
    return {
        'plataforma': platform.system(),
        'terminal': os.getenv('TERM', 'desconhecido'),
        'colorterm': os.getenv('COLORTERM', 'não definido'),
        'wt_session': bool(os.getenv('WT_SESSION')),
        'suporta_cores': terminal_suporta_cores(),
        'encoding': sys.stdout.encoding or 'desconhecido'
    }
