#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para criar executável do Ragner Chatbot.
Este script usa o PyInstaller para criar um executável Windows standalone.
"""

import os
import sys
import shutil
import subprocess

def main():
    """Cria um executável para o Ragner Chatbot."""
    
    print("=" * 80)
    print(" " * 30 + "Ragner Chatbot - Criação do Executável")
    print("=" * 80)
    
    # Define o diretório do projeto e os caminhos relevantes
    projeto_dir = os.path.abspath(os.path.dirname(__file__))
    ragner_dir = os.path.join(projeto_dir, 'Ragner')
    documentos_dir = os.path.join(projeto_dir, 'documentos')
    saida_dir = os.path.join(projeto_dir, 'dist')
    faiss_index_dir = os.path.join(projeto_dir, 'faiss_index')
    
    # Verifica se o diretório principal Ragner existe
    if not os.path.exists(ragner_dir):
        print("Erro: O diretório Ragner não foi encontrado!")
        return 1
    
    # Executa o PyInstaller para criar o executável
    print("\nIniciando o processo de criação do executável com PyInstaller...\n")
    
    # Comando para o PyInstaller - Remoção da flag --windowed e adicionando --console
    comando = [
        'pyinstaller',
        '--name=Ragner',
        '--onefile',                   # Cria um único arquivo executável
        '--console',                   # Mantém o console aberto para ver logs/erros
        '--add-data=Ragner;Ragner',    # Inclui o diretório Ragner
        '--add-data=documentos;documentos',  # Inclui o diretório documentos
        '--add-data=faiss_index;faiss_index',  # Inclui o diretório faiss_index
        '--clean',                     # Limpa cache do PyInstaller antes da compilação
        # Exclusões para reduzir o tamanho
        '--exclude-module=matplotlib',
        '--exclude-module=PyQt5',
        '--exclude-module=scipy',
        '--exclude-module=pandas',
        '--exclude-module=PIL',
        '--exclude-module=notebook',
        '--exclude-module=IPython',
        '--exclude-module=tkinter',
        '--exclude-module=PySide2',
        # Adiciona um diretório de banco de dados vazio para ser incluído na distribuição
        '--add-data=database;database',  # Inclui o diretório database (se existir)
        'Ragner/Ragner.py'             # Script principal
    ]
    
    # Cria um diretório database vazio para ser incluído (se ainda não existir)
    database_dir = os.path.join(projeto_dir, 'database')
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
        print(f"Diretório de banco de dados criado em: {database_dir}")
    
    # Executa o comando do PyInstaller
    try:
        subprocess.run(comando, check=True)
        print("\nExecutável criado com sucesso!")
        
        # Caminho para o executável criado
        exe_path = os.path.join(saida_dir, 'Ragner.exe')
        
        if os.path.exists(exe_path):
            print(f"\nO executável está disponível em: {exe_path}")
            print(f"Tamanho do executável: {os.path.getsize(exe_path) / (1024*1024):.2f} MB")
        else:
            print("\nAviso: O executável não foi encontrado no local esperado.")
        
    except subprocess.CalledProcessError as e:
        print(f"Erro ao criar o executável: {e}")
        return 1
    
    # Copia o README.md para o diretório dist
    try:
        readme_path = os.path.join(projeto_dir, 'README.md')
        if os.path.exists(readme_path):
            shutil.copy(readme_path, os.path.join(saida_dir, 'README.md'))
            print("README.md copiado para o diretório de saída.")
    except Exception as e:
        print(f"Aviso: Não foi possível copiar o README.md: {e}")
    
    # Cria um arquivo .bat para facilitar a execução
    try:
        bat_path = os.path.join(saida_dir, 'Executar_Ragner.bat')
        with open(bat_path, 'w') as f:
            f.write('@echo off\n')
            f.write('echo Iniciando Ragner Chatbot...\n')
            f.write('start Ragner.exe\n')
            f.write('pause\n')
        print("Arquivo batch criado para facilitar a execução.")
    except Exception as e:
        print(f"Aviso: Não foi possível criar o arquivo batch: {e}")
    
    print("\nProcesso concluído! O Ragner Chatbot agora está pronto para ser distribuído.")
    print("=" * 80)
    return 0

if __name__ == "__main__":
    sys.exit(main())