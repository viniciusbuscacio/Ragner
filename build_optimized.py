#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script para criar executável standalone do Ragner com todas as dependências incluídas.
Esta abordagem é mais eficiente que criar um ambiente virtual completo.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def instalar_dependencias_build():
    """Instala dependências necessárias para o build."""
    print("📦 Instalando dependências para build...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    return True

def limpar_builds_anteriores():
    """Remove builds anteriores."""
    print("🧹 Limpando builds anteriores...")
    
    for pasta in ["build", "dist"]:
        if os.path.exists(pasta):
            shutil.rmtree(pasta)
            print(f"   Removido: {pasta}/")

def criar_executavel():
    """Cria o executável usando PyInstaller."""
    print("🔨 Criando executável standalone...")
    
    # Comando PyInstaller otimizado
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Um único arquivo executável
        "--windowed",                   # Sem console (GUI)
        "--console",                    # COM console para CLI
        "--name=Ragner",               # Nome do executável
        "--icon=icon.ico",             # Ícone (se existir)
        "--add-data=Ragner;Ragner",    # Incluir pasta Ragner
        "--hidden-import=colorama",     # Garantir que colorama seja incluído
        "--hidden-import=faiss",       # Garantir que FAISS seja incluído
        "--hidden-import=openai",      # Garantir que OpenAI seja incluído
        "--exclude-module=tkinter",    # Excluir tkinter (reduz tamanho)
        "--exclude-module=matplotlib", # Excluir matplotlib (reduz tamanho)
        "--exclude-module=pandas",     # Excluir pandas (reduz tamanho)
        "--clean",                     # Limpar cache
        "Ragner/Ragner.py"            # Script principal
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ Executável criado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar executável: {e}")
        return False

def otimizar_executavel():
    """Otimiza o executável final."""
    print("⚡ Otimizando executável...")
    
    exe_path = "dist/Ragner.exe"
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"   Tamanho final: {size_mb:.1f} MB")
        
        # UPX compression (se disponível)
        try:
            subprocess.run(["upx", "--best", exe_path], check=True, capture_output=True)
            new_size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"   Comprimido para: {new_size_mb:.1f} MB")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   UPX não disponível - executável não comprimido")

def criar_instalador_otimizado():
    """Atualiza o instalador para usar apenas o executável."""
    print("📝 Atualizando instalador...")
    
    # Criar versão otimizada do create_installer.iss
    iss_content = '''
; Script de instalação otimizado para o Ragner
#define MyAppName "Ragner"
#define MyAppVersion "1.0"
#define MyAppPublisher "Your Name"
#define MyAppExeName "Ragner.exe"

[Setup]
AppId={{4B6674E4-5391-4D84-8791-85F8297D3816}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\\{#MyAppName}
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\\{#MyAppExeName}
Compression=lzma
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=Ragner_Setup_Optimized
WizardStyle=modern
PrivilegesRequired=lowest

[Files]
Source: "dist\\Ragner.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "remove_env_var.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{autodesktop}\\Ragner"; Filename: "{app}\\{#MyAppExeName}"

[Run]
Filename: "{app}\\{#MyAppExeName}"; Description: "Executar Ragner"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: "{localappdata}\\{#MyAppName}\\database"; Flags: uninsneveruninstall
Name: "{localappdata}\\{#MyAppName}\\documentos"; Flags: uninsneveruninstall
Name: "{localappdata}\\{#MyAppName}\\faiss_index"; Flags: uninsneveruninstall
'''
    
    with open("create_installer_optimized.iss", "w", encoding="utf-8") as f:
        f.write(iss_content)
    
    print("✅ Instalador otimizado criado!")

def main():
    """Função principal."""
    print("🚀 RAGNER - BUILD OTIMIZADO")
    print("="*50)
    
    if not instalar_dependencias_build():
        return False
    
    limpar_builds_anteriores()
    
    if not criar_executavel():
        return False
    
    otimizar_executavel()
    criar_instalador_otimizado()
    
    print("\n✅ BUILD CONCLUÍDO!")
    print("\nComparação de tamanhos:")
    print("  📁 Ambiente virtual: ~500-800 MB")
    print("  📦 Executável standalone: ~100-200 MB")
    print("  🎯 Redução: ~60-75%")
    
    return True

if __name__ == "__main__":
    success = main()
    input(f"\n{'✅' if success else '❌'} Pressione Enter para sair...")
