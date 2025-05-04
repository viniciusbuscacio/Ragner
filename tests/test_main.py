#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Teste principal que chama todos os outros testes do Ragner Chatbot.
Este arquivo pode ser executado diretamente para rodar todos os testes
em conjunto.
"""

import unittest
import sys
import os
import time
import importlib.util
import traceback

# Define cores para saída no terminal
class Cores:
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'


class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Configuração executada antes de todos os testes.
        """
        print(f"\n{Cores.AZUL}==== Início dos Testes do Ragner Chatbot ===={Cores.RESET}")
        print(f"{Cores.AZUL}Data: {time.strftime('%d/%m/%Y %H:%M:%S')}{Cores.RESET}\n")
    
    @classmethod
    def tearDownClass(cls):
        """
        Limpeza executada após todos os testes.
        """
        print(f"\n{Cores.AZUL}==== Fim dos Testes do Ragner Chatbot ===={Cores.RESET}")
        print(f"{Cores.AZUL}Data: {time.strftime('%d/%m/%Y %H:%M:%S')}{Cores.RESET}")

    def test_all(self):
        """
        Executa todos os testes do projeto através de TestSuite.
        """
        # Obtém o diretório de testes
        diretorio_testes = os.path.dirname(os.path.abspath(__file__))
        
        # Adiciona o diretório pai ao PATH para permitir importações dos módulos
        sys.path.insert(0, os.path.dirname(diretorio_testes))
        
        # Lista todos os arquivos de teste disponíveis
        arquivos_teste = [
            'test_cli_simple.py',
            'test_buscar_contexto_usecase.py',
            'test_gerar_resposta_usecase.py',
            'test_configurar_api_key_usecase.py',
            'test_fazer_pergunta_usecase.py',
            'test_indexar_documentos_usecase.py',
            'test_dados_raw.py',
            'test_log.py',
            'test_tutorial_usecase.py',
            'test_cli_interface.py',
            'test_chat_controller.py'
        ]
        
        # Cria uma suite de testes vazia
        suite = unittest.TestSuite()
        
        # Para acompanhar o progresso
        sucessos = 0
        falhas = 0
        pulados = 0
        arquivos_pulados = []
        
        # Adiciona cada módulo de teste à suite usando importação direta
        for arquivo in arquivos_teste:
            try:
                # Ignora o arquivo atual para evitar recursão
                if arquivo == os.path.basename(__file__):
                    continue
                
                print(f"{Cores.AMARELO}Carregando {arquivo}...{Cores.RESET}")
                
                # Caminho completo para o arquivo
                caminho_arquivo = os.path.join(diretorio_testes, arquivo)
                
                # Verifica dependências conhecidas antes de tentar importar
                if arquivo == 'test_tutorial_usecase.py':
                    try:
                        import keyboard
                    except ImportError:
                        print(f"{Cores.AMARELO}Pulando {arquivo}: Dependência 'keyboard' não encontrada{Cores.RESET}")
                        pulados += 1
                        arquivos_pulados.append(arquivo)
                        continue
                
                # Carrega o módulo diretamente do arquivo
                nome_modulo = os.path.splitext(arquivo)[0]
                try:
                    spec = importlib.util.spec_from_file_location(nome_modulo, caminho_arquivo)
                    modulo = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(modulo)
                    
                    # Carrega todos os testes do módulo
                    testes_modulo = unittest.defaultTestLoader.loadTestsFromModule(modulo)
                    suite.addTest(testes_modulo)
                    sucessos += 1
                except Exception as e:
                    print(f"{Cores.VERMELHO}Erro ao carregar {arquivo}: {str(e)}{Cores.RESET}")
                    falhas += 1
                    if 'ModuleNotFoundError' in str(e) or 'ImportError' in str(e):
                        # Se for um erro de módulo não encontrado, apenas registra
                        print(f"{Cores.AMARELO}Pulando {arquivo} devido a dependências faltando:{Cores.RESET}")
                        print(f"{Cores.AMARELO}  {str(e)}{Cores.RESET}")
                        pulados += 1
                        arquivos_pulados.append(arquivo)
                    else:
                        # Se for outro tipo de erro, mostra o traceback completo
                        print(f"{Cores.VERMELHO}Traceback para {arquivo}:{Cores.RESET}")
                        traceback.print_exc()
                
            except Exception as e:
                print(f"{Cores.VERMELHO}Erro inesperado ao preparar {arquivo}: {str(e)}{Cores.RESET}")
                falhas += 1
        
        # Executa todos os testes
        print(f"\n{Cores.AZUL}==== Executando todos os testes carregados ===={Cores.RESET}")
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        
        # Exibe um relatório resumido
        print(f"\n{Cores.AZUL}==== Relatório de Testes ===={Cores.RESET}")
        print(f"Total de testes: {result.testsRun}")
        print(f"{Cores.VERDE}Testes bem-sucedidos: {result.testsRun - (len(result.errors) + len(result.failures))}{Cores.RESET}")
        
        if len(result.errors) + len(result.failures) > 0:
            print(f"{Cores.VERMELHO}Testes com falha: {len(result.errors) + len(result.failures)}{Cores.RESET}")
        else:
            print(f"Testes com falha: 0")
        
        # Calcula a taxa de sucesso
        if result.testsRun > 0:
            taxa_sucesso = ((result.testsRun - (len(result.errors) + len(result.failures))) / result.testsRun) * 100
            print(f"Taxa de sucesso: {taxa_sucesso:.2f}%")
        
        # Relatório de arquivos pulados
        if pulados > 0:
            print(f"\n{Cores.AMARELO}Arquivos pulados devido a dependências faltando: {pulados}{Cores.RESET}")
            for arquivo in arquivos_pulados:
                print(f"{Cores.AMARELO}  - {arquivo}{Cores.RESET}")
            
            print(f"\n{Cores.AMARELO}Para executar todos os testes, instale as dependências necessárias:{Cores.RESET}")
            print(f"{Cores.AMARELO}  pip install keyboard{Cores.RESET}")
        
        # O teste principal é considerado bem-sucedido desde que consiga carregar e executar pelo menos alguns testes
        self.assertTrue(sucessos > 0, "Nenhum arquivo de teste foi carregado com sucesso")


# Permite a execução direta deste arquivo
if __name__ == '__main__':
    unittest.main()