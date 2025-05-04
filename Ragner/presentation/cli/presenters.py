#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Presenters: Classes responsáveis por formatar e apresentar dados ao usuário na CLI.
"""

import os
import textwrap
import time
from presentation.cli.cli_cores import Cores


class ChatPresenter:
    """
    Presenter para o chat CLI.
    
    Esta classe é responsável por formatar e apresentar mensagens,
    respostas e informações ao usuário na CLI.
    """
    
    def __init__(self, largura_terminal=80, db_gateway=None):
        """
        Inicializa o presenter.
        
        Args:
            largura_terminal: Largura do terminal para formatação de texto
            db_gateway: Gateway para o banco de dados (opcional)
        """
        self.largura_terminal = largura_terminal
        self.db_gateway = db_gateway  # Armazena a referência ao db_gateway
    
    def exibir_mensagem_sistema(self, mensagem):
        """
        Exibe uma mensagem de sistema.
        
        Args:
            mensagem: Mensagem a ser exibida
        """
        print(f"{mensagem}")
    
    def exibir_mensagem_erro(self, mensagem):
        """
        Exibe uma mensagem de erro.
        
        Args:
            mensagem: Mensagem de erro a ser exibida
        """
        print(f"{Cores.VERMELHO}[Erro] {mensagem}{Cores.RESET}")
    
    def exibir_mensagem_sucesso(self, mensagem):
        """
        Exibe uma mensagem de sucesso.
        
        Args:
            mensagem: Mensagem de sucesso a ser exibida
        """
        print(f"{Cores.VERDE}{mensagem}{Cores.RESET}")
    
    def exibir_mensagem_info(self, mensagem):
        """
        Exibe uma mensagem informativa.
        
        Args:
            mensagem: Mensagem informativa a ser exibida
        """
        print(f"{Cores.CINZA}{mensagem}{Cores.RESET}")

    def exibir_mensagem_amarelo(self, mensagem):
        """
        Exibe uma mensagem informativa em amarelo.
        
        Args:
            mensagem: Mensagem informativa a ser exibida
        """
        print(f"{Cores.AMARELO}{mensagem}{Cores.RESET}")
    
    def exibir_pergunta(self, texto_pergunta):
        """
        Prepara a UI para exibir o processamento da pergunta.
        
        Args:
            texto_pergunta: Texto da pergunta (não utilizado diretamente)
        """
        # Apenas adiciona uma quebra de linha para separação visual
        print()
    
    def exibir_resposta(self, resposta, mostrar_fontes=True):
        """
        Exibe a resposta formatada.
        
        Args:
            resposta: Objeto Resposta
            mostrar_fontes: Se True, exibe as fontes da resposta
        """
        print(f"\n{Cores.VERDE}Ragner: {Cores.RESET}")
        
        # Quebra o texto em linhas com largura adequada
        linhas = textwrap.wrap(resposta.texto, width=self.largura_terminal)
        for linha in linhas:
            print(linha)
        
        # Mostra as fontes utilizadas, se solicitado
        if mostrar_fontes and resposta.chunks_utilizados:
            # Lista para rastrear documentos já mencionados
            documentos_mencionados = {}
            
            # Identificar quais documentos são mencionados na resposta
            for chunk in resposta.chunks_utilizados:
                if self.db_gateway:
                    try:
                        dados_arquivo = self.db_gateway.ler_arquivo_db(chunk.arquivo_uuid)
                        if dados_arquivo and 'arquivo_nome' in dados_arquivo:
                            nome_documento = dados_arquivo['arquivo_nome']
                            
                            # Verifica se este documento é mencionado na resposta
                            # ou se é o único documento disponível
                            doc_mencionado = nome_documento.lower() in resposta.texto.lower()
                            
                            if chunk.arquivo_uuid not in documentos_mencionados:
                                documentos_mencionados[chunk.arquivo_uuid] = {
                                    'nome': nome_documento,
                                    'mencionado': doc_mencionado
                                }
                    except Exception as e:
                        # Silenciosamente ignora erros ao buscar o nome do documento
                        pass
            
            # Se há apenas um documento, sempre o mostra
            if len(documentos_mencionados) == 1:
                unico_doc = list(documentos_mencionados.values())[0]
                print(f"\n{Cores.AZUL}Fontes utilizadas:{Cores.RESET}")
                print(f"- {unico_doc['nome']}")
            else:
                # Se há mais de um documento, mostra apenas os mencionados na resposta
                docs_mencionados = [doc['nome'] for doc in documentos_mencionados.values() if doc['mencionado']]
                
                if docs_mencionados:
                    print(f"\n{Cores.AZUL}Fontes utilizadas:{Cores.RESET}")
                    for nome in docs_mencionados:
                        print(f"- {nome}")
                else:
                    # Se nenhum documento foi explicitamente mencionado, mostra todos
                    print(f"\n{Cores.AZUL}Fontes utilizadas:{Cores.RESET}")
                    for doc in documentos_mencionados.values():
                        print(f"- {doc['nome']}")
                    
            # Se não temos chunks utilizados, informamos
            if not documentos_mencionados:
                print(f"\n{Cores.AZUL}Fontes utilizadas:{Cores.RESET}")
                print("Nenhuma fonte específica utilizada.")
    
    def exibir_contexto(self, chunks_relevantes):
        """
        Exibe os chunks de contexto encontrados.
        
        Args:
            chunks_relevantes: Lista de dicionários com chunks e documentos
        """
        print(f"{Cores.CINZA}Contexto Encontrado:{Cores.RESET}")
        
        for i, item in enumerate(chunks_relevantes):
            chunk = item["chunk"]
            documento = item["documento"]
            
            print(f"{Cores.CINZA}[Trecho {i+1} - Fonte: {documento.arquivo_nome}]{Cores.RESET}")
            
            # Quebra o texto em linhas com largura adequada
            linhas = textwrap.wrap(chunk.chunk_texto[:200] + "...", width=self.largura_terminal)
            for linha in linhas:
                print(f"{Cores.CINZA}{linha}{Cores.RESET}")
    
    def exibir_menu(self):
        """Exibe o menu de comandos disponíveis."""
        print(f"\n{Cores.AMARELO}Comandos Disponíveis:{Cores.RESET}")
        print("  sobre                        - Exibe informações sobre o Ragner")
        print("  tutorial                     - Exibe um tutorial sobre como usar o Ragner")
        print("  configurar_api_key           - Configura uma nova chave de API da OpenAI")
        print("  status                       - Exibe o status geral do sistema")
        print("  status_tabela_arquivos       - Exibe os arquivos indexados")
        print("  status_tabela_chunks         - Exibe informações sobre os chunks")
        print("  status_faiss                 - Exibe informações sobre o índice FAISS")
        print("  recarregar_arquivos_da_pasta - Recarregar todos os arquivos da pasta 'documentos'")
        print("  apagar_tudo                  - Apaga todos os dados do sistema")
        print("  menu                         - Exibe este menu de comandos")
        print("  sair                         - Encerra o programa")
        print(f"\n{Cores.AMARELO}Para perguntar algo, simplesmente digite sua pergunta e pressione Enter.{Cores.RESET}")
    
    def exibir_sobre(self):
        """Exibe informações sobre o Ragner."""
        print(f"\n{Cores.AZUL}Ragner Chatbot: Desvendando o Retrieval-Augmented Generation (RAG){Cores.RESET}")
        print("\nO Ragner é um software educacional desenvolvido em Python para demonstrar")
        print("de forma clara e interativa o funcionamento interno da técnica de Geração")
        print("Aumentada por Recuperação (RAG), que combina a busca por informações")
        print("relevantes em documentos com a geração de respostas por modelos de linguagem.")
        print("\nCom o Ragner, você pode:")
        print("1. Adicionar documentos em diferentes formatos (PDF, DOCX, TXT)")
        print("2. Ver o processo de indexação e vetorização de documentos")
        print("3. Fazer perguntas e observar como o sistema busca informações relevantes")
        print("4. Entender como o contexto encontrado é usado para gerar respostas precisas")
    
    def exibir_tutorial(self, chat_controller=None):
        """
        Exibe um tutorial interativo sobre como usar o Ragner.
        
        Args:
            chat_controller: Controlador do chat para executar comandos durante o tutorial
        
        Esta função delega a execução do tutorial para a interface TutorialInterface,
        seguindo os princípios da Clean Architecture.
        """
        try:
            # Importamos aqui para evitar importação circular
            from presentation.cli.tutorial import TutorialInterface
            
            # Criamos a interface e delegamos a execução do tutorial
            tutorial_interface = TutorialInterface(
                presenter=self, 
                db_gateway=self.db_gateway,
                chat_controller=chat_controller
            )
            tutorial_interface.executar_tutorial()
        except ImportError:
            print(f"{Cores.VERMELHO}Erro: O módulo de tutorial não foi encontrado.{Cores.RESET}")
        except Exception as e:
            print(f"{Cores.VERMELHO}Erro ao executar o tutorial: {str(e)}{Cores.RESET}")
    
    def exibir_processando(self, operacao):
        """
        Exibe uma mensagem indicando que uma operação está em andamento.
        
        Args:
            operacao: Nome da operação em andamento
        """
        print(f"{Cores.CINZA}Processando {operacao}...{Cores.RESET}")
    
    def exibir_progresso(self, etapa, desc=""):
        """
        Exibe uma etapa do processamento RAG.
        
        Args:
            etapa: Nome da etapa
            desc: Descrição adicional
        """
        print(f"{Cores.CINZA}[[{etapa}]] {desc}{Cores.RESET}")
        time.sleep(0.5)  # Pequena pausa para visualização do processo
    
    def limpar_tela(self):
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')