#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para criar o instalador do Ragner Chatbot.
Este script executa o create_executable.py e depois usa o Inno Setup para criar um instalador.
"""

import os
import sys
import subprocess
import time

def main():
    """Cria um instalador para o Ragner Chatbot."""
    
    print("=" * 80)
    print(" " * 30 + "Ragner Chatbot - Criação do Instalador")
    print("=" * 80)
    
    # Define o diretório do projeto
    projeto_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Primeiro passo: Criar o executável usando o script existente
    print("\n[Passo 1/2] Executando script para gerar o executável...")
    
    try:
        # Executa o script create_executable.py
        subprocess.run([sys.executable, "create_executable.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar create_executable.py: {e}")
        return 1
    
    # Verifica se o executável foi criado com sucesso
    exe_path = os.path.join(projeto_dir, "dist", "Ragner.exe")
    if not os.path.exists(exe_path):
        print("Erro: O executável não foi gerado corretamente!")
        return 1
    
    print("\nExecutável criado com sucesso!")
    
    # Segundo passo: Criar o instalador usando o Inno Setup
    print("\n[Passo 2/2] Criando o instalador com Inno Setup...")
    
    # Cria o diretório de saída para o instalador se não existir
    installer_dir = os.path.join(projeto_dir, "installer")
    if not os.path.exists(installer_dir):
        os.makedirs(installer_dir)
    
    # Caminho do script para o Inno Setup
    # Usando o script create_installer.iss original
    inno_script = os.path.join(projeto_dir, "create_installer.iss")
    
    # Verificar se o Inno Setup está instalado
    inno_compiler_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe"
    ]
    
    inno_compiler = None
    for path in inno_compiler_paths:
        if os.path.exists(path):
            inno_compiler = path
            break
    
    if not inno_compiler:
        print("Erro: Inno Setup não encontrado! Por favor, instale o Inno Setup 6 primeiro.")
        print("Você pode baixar o Inno Setup em: https://jrsoftware.org/isdl.php")
        return 1
    
    try:
        # Executa o compilador do Inno Setup
        subprocess.run([inno_compiler, inno_script], check=True)
        
        # Verifica se o instalador foi criado
        installer_path = os.path.join(installer_dir, "Ragner_Setup.exe")
        
        if os.path.exists(installer_path):
            print(f"\nInstalador criado com sucesso em: {installer_path}")
            print(f"Tamanho do instalador: {os.path.getsize(installer_path) / (1024*1024):.2f} MB")
        else:
            print("\nErro: O instalador não foi encontrado no local esperado.")
            return 1
            
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar o instalador com Inno Setup: {e}")
        return 1
    
    print("\nProcesso concluído! O instalador do Ragner Chatbot está pronto para distribuição.")
    print("=" * 80)
    return 0

if __name__ == "__main__":
    sys.exit(main())