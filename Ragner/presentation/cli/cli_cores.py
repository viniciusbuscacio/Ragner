"""
Cores - Sistema inteligente de cores para terminal Windows sem dependências externas.
"""

import os
import sys
import platform

def configurar_terminal_windows():
    """
    Configura o terminal Windows para suportar cores ANSI nativamente.
    Usa apenas APIs padrão do Windows - sem dependências externas.
    """
    if platform.system() != 'Windows':
        return True
    
    try:
        # Método 1: Habilitar VIRTUAL_TERMINAL_PROCESSING via ctypes
        import ctypes
        from ctypes import wintypes
        
        # Constantes do Windows
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE = -12
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        
        kernel32 = ctypes.windll.kernel32
        
        # Configurar stdout
        handle_out = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        if handle_out != -1:
            mode_out = wintypes.DWORD()
            if kernel32.GetConsoleMode(handle_out, ctypes.byref(mode_out)):
                mode_out.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
                kernel32.SetConsoleMode(handle_out, mode_out)
        
        # Configurar stderr
        handle_err = kernel32.GetStdHandle(STD_ERROR_HANDLE)
        if handle_err != -1:
            mode_err = wintypes.DWORD()
            if kernel32.GetConsoleMode(handle_err, ctypes.byref(mode_err)):
                mode_err.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
                kernel32.SetConsoleMode(handle_err, mode_err)
        
        return True
        
    except Exception:
        # Se falhar, tentar método alternativo
        try:
            # Método 2: Usar comando do sistema
            os.system('')  # Força inicialização do console
            return True
        except Exception:
            return False

def detectar_suporte_cores():
    """
    Detecta se o terminal atual suporta cores ANSI.
    """
    # Variáveis de ambiente que indicam suporte a cores
    if os.getenv('COLORTERM'):
        return True
    
    if os.getenv('TERM') in ['xterm-256color', 'screen-256color']:
        return True
    
    # Windows Terminal e PowerShell moderno
    if platform.system() == 'Windows':
        if os.getenv('WT_SESSION'):  # Windows Terminal
            return True
        if 'WindowsTerminal' in os.getenv('TERM_PROGRAM', ''):
            return True
    
    # Testar enviando uma sequência ANSI simples
    try:
        # Salvar posição do cursor, mover e restaurar
        sys.stdout.write('\033[s\033[1;1H\033[u')
        sys.stdout.flush()
        return True
    except Exception:
        return False

# Configurar terminal Windows automaticamente
_CORES_HABILITADAS = configurar_terminal_windows() and detectar_suporte_cores()

class Cores:
    """
    Sistema inteligente de cores que se adapta ao terminal.
    """
    
    # Definir cores baseado na capacidade do terminal
    if _CORES_HABILITADAS:
        AMARELO = "\033[93m"
        AZUL = "\033[94m"
        VERDE = "\033[92m"
        VERMELHO = "\033[91m"
        MAGENTA = "\033[95m"
        CINZA = "\033[90m"
        BRANCO = "\033[97m"
        CIANO = "\033[96m"
        RESET = "\033[0m"
        NEGRITO = "\033[1m"
        SUBLINHADO = "\033[4m"
    else:
        # Fallback sem cores
        AMARELO = ""
        AZUL = ""
        VERDE = ""
        VERMELHO = ""
        MAGENTA = ""
        CINZA = ""
        BRANCO = ""
        CIANO = ""
        RESET = ""
        NEGRITO = ""
        SUBLINHADO = ""
    
    @staticmethod
    def aplicar_cor(texto, cor):
        """Aplica cor a um texto."""
        if _CORES_HABILITADAS:
            return f"{cor}{texto}{Cores.RESET}"
        return texto
    
    @staticmethod
    def amarelo(texto):
        return Cores.aplicar_cor(texto, Cores.AMARELO)
    
    @staticmethod
    def azul(texto):
        return Cores.aplicar_cor(texto, Cores.AZUL)
    
    @staticmethod
    def verde(texto):
        return Cores.aplicar_cor(texto, Cores.VERDE)
    
    @staticmethod
    def vermelho(texto):
        return Cores.aplicar_cor(texto, Cores.VERMELHO)
    
    @staticmethod
    def magenta(texto):
        return Cores.aplicar_cor(texto, Cores.MAGENTA)
    
    @staticmethod
    def cinza(texto):
        return Cores.aplicar_cor(texto, Cores.CINZA)
    
    @staticmethod
    def branco(texto):
        return Cores.aplicar_cor(texto, Cores.BRANCO)
    
    @staticmethod
    def suporte_ativo():
        """Retorna True se as cores estão ativas."""
        return _CORES_HABILITADAS

def testar_cores():
    """Testa as cores no terminal atual."""
    print("🎨 Teste do sistema de cores:")
    print(f"Terminal: {platform.system()}")
    print(f"Suporte ANSI: {'✅ Ativo' if _CORES_HABILITADAS else '❌ Desabilitado'}")
    print()
    
    if _CORES_HABILITADAS:
        print(f"{Cores.VERMELHO}● Vermelho{Cores.RESET}")
        print(f"{Cores.VERDE}● Verde{Cores.RESET}")
        print(f"{Cores.AZUL}● Azul{Cores.RESET}")
        print(f"{Cores.AMARELO}● Amarelo{Cores.RESET}")
        print(f"{Cores.MAGENTA}● Magenta{Cores.RESET}")
        print(f"{Cores.CINZA}● Cinza{Cores.RESET}")
    else:
        print("● Vermelho (sem cor)")
        print("● Verde (sem cor)")
        print("● Azul (sem cor)")
        print("● Amarelo (sem cor)")
        print("● Magenta (sem cor)")
        print("● Cinza (sem cor)")
    
    return _CORES_HABILITADAS

if __name__ == "__main__":
    testar_cores()

