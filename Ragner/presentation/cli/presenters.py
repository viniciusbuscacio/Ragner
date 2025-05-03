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
        print(f"{Cores.CINZA}{mensagem}{Cores.RESET}")
    
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
    
    def exibir_pergunta(self, texto_pergunta):
        """
        Exibe a pergunta do usuário formatada.
        
        Args:
            texto_pergunta: Texto da pergunta
        """
    
    def exibir_resposta(self, resposta, mostrar_fontes=True):
        """
        Exibe a resposta formatada.
        
        Args:
            resposta: Objeto Resposta
            mostrar_fontes: Se True, exibe as fontes da resposta
        """
        print(f"\n{Cores.VERDE}Resposta:{Cores.RESET}")
        
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
        print(f"\n{Cores.MAGENTA}Contexto Encontrado:{Cores.RESET}")
        
        for i, item in enumerate(chunks_relevantes):
            chunk = item["chunk"]
            documento = item["documento"]
            
            print(f"\n{Cores.MAGENTA}[Trecho {i+1} - Fonte: {documento.arquivo_nome}]{Cores.RESET}")
            
            # Quebra o texto em linhas com largura adequada
            linhas = textwrap.wrap(chunk.chunk_texto[:200] + "...", width=self.largura_terminal)
            for linha in linhas:
                print(linha)
    
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
        print("  recarregar_arquivos_da_pasta - Recarrega todos os arquivos da pasta 'documentos'")
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
    
    def exibir_tutorial(self):
        """Exibe um tutorial sobre como usar o Ragner."""
        print(f"\n{Cores.AZUL}Tutorial do Ragner{Cores.RESET}")
        print("\nComo usar o Ragner em 4 passos simples:")
        print("\n1. Adicione documentos")
        print("   Coloque seus arquivos (PDF, DOCX, TXT) na pasta 'documentos'")
        print("   Você pode usar o comando 'recarregar_arquivos_da_pasta' para indexá-los")
        print("\n2. Verifique o status")
        print("   Use o comando 'status' para ver quantos documentos foram indexados")
        print("   ou 'status_tabela_arquivos' para ver a lista de arquivos")
        print("\n3. Faça perguntas")
        print("   Simplesmente digite sua pergunta e pressione Enter")
        print("   O Ragner mostrará o processo de busca por informações relevantes")
        print("   e a geração da resposta baseada no contexto encontrado")
        print("\n4. Explore comandos adicionais")
        print("   Digite 'menu' para ver todos os comandos disponíveis")
        print("   Experimente diferentes perguntas para entender como a RAG funciona")
    
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
        print(f"{Cores.MAGENTA}[{etapa}]{Cores.RESET} {desc}")
        time.sleep(0.5)  # Pequena pausa para visualização do processo
    
    def limpar_tela(self):
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')