#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Presenters: Classes responsáveis por formatar e apresentar dados ao usuário na CLI.
"""

import os
import textwrap
import time
from presentation.cli.cli_cores import Cores
from presentation.cli.cli_logger import CLILogger

# Inicializa o logger para a interface CLI
cli_logger = CLILogger()


class ChatPresenter:
    """
    Presenter para o chat CLI.
    
    Esta classe é responsável por formatar e apresentar mensagens,
    respostas e informações ao usuário na CLI.
    """
    
    def __init__(self, largura_terminal=120, db_gateway=None):
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
        cli_logger.registrar_info(f"{mensagem}")
    
    def exibir_mensagem_erro(self, mensagem):
        """
        Exibe uma mensagem de erro.
        
        Args:
            mensagem: Mensagem de erro a ser exibida
        """
        cli_logger.registrar_info(f"{Cores.VERMELHO}[Erro] {mensagem}{Cores.RESET}")
    
    def exibir_mensagem_sucesso(self, mensagem):
        """
        Exibe uma mensagem de sucesso.
        
        Args:
            mensagem: Mensagem de sucesso a ser exibida
        """
        cli_logger.registrar_info(f"{Cores.VERDE}{mensagem}{Cores.RESET}")
    
    def exibir_mensagem_info(self, mensagem):
        """
        Exibe uma mensagem informativa.
        
        Args:
            mensagem: Mensagem informativa a ser exibida
        """
        cli_logger.registrar_info(f"{Cores.CINZA}{mensagem}{Cores.RESET}")

    def exibir_mensagem_amarelo(self, mensagem):
        """
        Exibe uma mensagem informativa em amarelo.
        
        Args:
            mensagem: Mensagem informativa a ser exibida
        """
        cli_logger.registrar_info(f"{Cores.AMARELO}{mensagem}{Cores.RESET}")
    
    def exibir_pergunta(self, texto_pergunta):
        """
        Prepara a UI para exibir o processamento da pergunta.
        
        Args:
            texto_pergunta: Texto da pergunta (não utilizado diretamente)
        """
        # Apenas adiciona uma quebra de linha para separação visual
        cli_logger.registrar_info()
    
    def exibir_resposta(self, resposta, mostrar_fontes=True):
        """
        Exibe a resposta formatada.
        
        Args:
            resposta: Objeto Resposta
            mostrar_fontes: Se True, exibe as fontes da resposta
        """
        # Abordagem mais simples e confiável para formatação
        texto = resposta.texto.strip()
        
        # Se o texto contém blocos de código (```), preserva a formatação original
        if '```' in texto:
            # Para texto com código, mantém quebras naturais e preserva blocos
            linhas = []
            dentro_codigo = False
            
            for linha in texto.split('\n'):
                if '```' in linha:
                    dentro_codigo = not dentro_codigo
                    linhas.append(linha)
                elif dentro_codigo:
                    # Dentro de bloco de código - preserva formatação exata
                    linhas.append(linha)
                else:
                    # Fora de bloco de código - pode quebrar se muito longa
                    if len(linha) > self.largura_terminal:
                        linhas_quebradas = textwrap.wrap(
                            linha, 
                            width=self.largura_terminal,
                            break_long_words=False,
                            break_on_hyphens=False
                        )
                        linhas.extend(linhas_quebradas)
                    else:
                        linhas.append(linha)
        else:
            # Para texto sem código, usa quebra inteligente por parágrafos
            paragrafos = texto.split('\n\n')
            linhas = []
            
            for i, paragrafo in enumerate(paragrafos):
                if paragrafo.strip():
                    linhas_paragrafo = textwrap.wrap(
                        paragrafo.strip(), 
                        width=self.largura_terminal,
                        break_long_words=False,
                        break_on_hyphens=False
                    )
                    linhas.extend(linhas_paragrafo)
                    # Adiciona linha em branco entre parágrafos (exceto no último)
                    if i < len(paragrafos) - 1:
                        linhas.append("")
        
        # Exibe as linhas formatadas
        for i, linha in enumerate(linhas):
            if i == 0:
                # Primeira linha com o prefixo "Ragner:"
                cli_logger.registrar_info(f"\n{Cores.VERDE}Ragner:{Cores.RESET} {linha}")
            else:
                # Linhas subsequentes
                cli_logger.registrar_info(f"{Cores.RESET}{linha}")
        
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
                cli_logger.registrar_info(f"\n{Cores.AZUL}Fontes utilizadas:{Cores.RESET}")
                cli_logger.registrar_info(f"- {unico_doc['nome']}")
            else:
                # Se há mais de um documento, mostra apenas os mencionados na resposta
                docs_mencionados = [doc['nome'] for doc in documentos_mencionados.values() if doc['mencionado']]
                
                if docs_mencionados:
                    cli_logger.registrar_info(f"\n{Cores.AZUL}Fontes utilizadas:{Cores.RESET}")
                    for nome in docs_mencionados:
                        cli_logger.registrar_info(f"- {nome}")
                else:
                    # Se nenhum documento foi explicitamente mencionado, mostra todos
                    cli_logger.registrar_info(f"\n{Cores.AZUL}Fontes utilizadas:{Cores.RESET}")
                    for doc in documentos_mencionados.values():
                        cli_logger.registrar_info(f"- {doc['nome']}")
                    
            # Se não temos chunks utilizados, informamos
            if not documentos_mencionados:
                cli_logger.registrar_info(f"\n{Cores.AZUL}Fontes utilizadas:{Cores.RESET}")
                cli_logger.registrar_info("Nenhuma fonte específica utilizada.")
    
    def exibir_contexto(self, chunks_relevantes):
        """
        Exibe os chunks de contexto encontrados.
        
        Args:
            chunks_relevantes: Lista de dicionários com chunks e documentos
        """
        cli_logger.registrar_info(f"{Cores.CINZA}Contexto Encontrado:{Cores.RESET}")
        
        for i, item in enumerate(chunks_relevantes):
            chunk = item["chunk"]
            documento = item["documento"]
            
            cli_logger.registrar_info(f"{Cores.CINZA}[Trecho {i+1} - Fonte: {documento.arquivo_nome}]{Cores.RESET}")
            
            # Quebra o texto em linhas com largura adequada
            linhas = textwrap.wrap(chunk.chunk_texto[:200] + "...", width=self.largura_terminal)
            for linha in linhas:
                cli_logger.registrar_info(f"{Cores.CINZA}{linha}{Cores.RESET}")
    
    def exibir_menu(self):
        """Exibe o menu de comandos disponíveis."""
        cli_logger.registrar_info(f"\n{Cores.AMARELO}Comandos Disponíveis:{Cores.RESET}")
        cli_logger.registrar_info("  sobre                        - Exibe informações sobre o Ragner")
        cli_logger.registrar_info("  tutorial                     - Exibe um tutorial sobre como usar o Ragner")
        cli_logger.registrar_info("  configurar_api_key           - Configura uma nova chave de API da OpenAI")
        cli_logger.registrar_info("  status                       - Exibe o status geral do sistema")
        cli_logger.registrar_info("  status_tabela_arquivos       - Exibe os arquivos indexados")
        cli_logger.registrar_info("  status_tabela_chunks         - Exibe informações sobre os chunks")
        cli_logger.registrar_info("  status_faiss                 - Exibe informações sobre o índice FAISS")
        cli_logger.registrar_info("  recarregar_arquivos_da_pasta - Recarregar todos os arquivos da pasta 'documentos'")
        cli_logger.registrar_info("  teste_vetor                  - Transforma um texto em vetor para executar um teste")
        cli_logger.registrar_info("  apagar_tudo                  - Apaga todos os dados do sistema")
        cli_logger.registrar_info("  menu                         - Exibe este menu de comandos")
        cli_logger.registrar_info("  sair                         - Encerra o programa")
        cli_logger.registrar_info(f"\n{Cores.AMARELO}Para perguntar algo, simplesmente digite sua pergunta e pressione Enter.{Cores.RESET}")
    
    def exibir_sobre(self):
        """Exibe informações sobre o Ragner."""
        cli_logger.registrar_info(f"\n{Cores.AZUL}Ragner Chatbot: Desvendando o Retrieval-Augmented Generation (RAG){Cores.RESET}")
        cli_logger.registrar_info("\nO Ragner é um software educacional desenvolvido em Python para demonstrar")
        cli_logger.registrar_info("de forma clara e interativa o funcionamento interno da técnica de Geração")
        cli_logger.registrar_info("Aumentada por Recuperação (RAG), que combina a busca por informações")
        cli_logger.registrar_info("relevantes em documentos com a geração de respostas por modelos de linguagem.")
        cli_logger.registrar_info("\nCom o Ragner, você pode:")
        cli_logger.registrar_info("1. Adicionar documentos em diferentes formatos (PDF, DOCX, TXT)")
        cli_logger.registrar_info("2. Ver o processo de indexação e vetorização de documentos")
        cli_logger.registrar_info("3. Fazer perguntas e observar como o sistema busca informações relevantes")
        cli_logger.registrar_info("4. Entender como o contexto encontrado é usado para gerar respostas precisas")
    
    def exibir_tutorial(self, chat_controller=None):
        """
        Exibe um tutorial interativo sobre como usar o Ragner.
        
        Args:
            chat_controller: Controlador do chat para executar comandos durante o tutorial
        
        Esta função delega a execução do tutorial para a interface TutorialInterface,
        seguindo os princípios da Clean Architecture.
        """
        try:
            # Importamos usando caminho absoluto para evitar problemas de importação circular
            import sys
            import os
            
            # Adiciona o diretório atual ao path se necessário
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            try:
                from .tutorial import TutorialInterface
            except ImportError:
                # Fallback para import absoluto
                from tutorial import TutorialInterface
            
            # Criamos a interface e delegamos a execução do tutorial
            tutorial_interface = TutorialInterface(
                presenter=self, 
                db_gateway=self.db_gateway,
                chat_controller=chat_controller
            )
            tutorial_interface.executar_tutorial()
        except ImportError as ie:
            self.exibir_mensagem_erro(f"Erro: O módulo de tutorial não foi encontrado: {str(ie)}")
        except Exception as e:
            self.exibir_mensagem_erro(f"Erro ao executar o tutorial: {str(e)}")
    
    def exibir_processando(self, operacao):
        """
        Exibe uma mensagem indicando que uma operação está em andamento.
        
        Args:
            operacao: Nome da operação em andamento
        """
        cli_logger.registrar_info(f"{Cores.CINZA}Processando {operacao}...{Cores.RESET}")
    
    def exibir_progresso(self, Passo, desc=""):
        """
        Exibe uma Passo do processamento RAG.
        
        Args:
            Passo: Nome da Passo
            desc: Descrição adicional
        """
        cli_logger.registrar_info(f"{Cores.CINZA}* {Passo}: {desc}{Cores.RESET}")
        time.sleep(0.5)  # Pequena pausa para visualização do processo
    
    def limpar_tela(self):
        """Limpa a tela do terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_titulo_tutorial(self, texto):
        """
        Exibe um título de seção do tutorial com formatação especial.
        
        Args:
            texto: O texto do título a ser exibido
        """
        cli_logger.registrar_info(f"\n{Cores.AMARELO}======= {texto} ======={Cores.RESET}")
    
    def exibir_saudacao(self, texto):
        """
        Exibe uma saudação do tutorial em branco.
        
        Args:
            texto: O texto da saudação a ser exibido
        """
        cli_logger.registrar_info(f"\n{Cores.BRANCO}{texto}{Cores.RESET}")
    
    def exibir_texto_tutorial(self, texto, destacar=None):
        """
        Exibe texto do tutorial em branco com possibilidade de destacar partes em verde.
        
        Args:
            texto: Texto completo a ser exibido
            destacar: Lista opcional de strings a serem destacadas em verde
        """
        if not destacar:
            cli_logger.registrar_info(f"\n{Cores.BRANCO}{texto}{Cores.RESET}")
            return
            
        # Se temos trechos para destacar, substituímos cada um deles
        texto_formatado = f"{Cores.BRANCO}{texto}{Cores.RESET}"
        for trecho in destacar:
            texto_formatado = texto_formatado.replace(trecho, f"{Cores.VERDE}{trecho}{Cores.RESET}{Cores.BRANCO}")
        
        cli_logger.registrar_info(f"\n{texto_formatado}{Cores.RESET}")
    
    def exibir_passo_tutorial(self, numero, texto, destacar=None):
        """
        Exibe um passo numerado do tutorial com possibilidade de destacar partes.
        
        Args:
            numero: Número do passo
            texto: Texto do passo a ser exibido
            destacar: Lista opcional de strings a serem destacadas em verde
        """
        if not destacar:
            cli_logger.registrar_info(f"\n{Cores.VERDE}{numero}) {Cores.RESET}{texto}")
            return
            
        # Se temos trechos para destacar, substituímos cada um deles
        texto_formatado = texto
        for trecho in destacar:
            texto_formatado = texto_formatado.replace(trecho, f"{Cores.VERDE}{trecho}{Cores.RESET}")
        
        cli_logger.registrar_info(f"\n{Cores.VERDE}{numero}) {Cores.RESET}{texto_formatado}")
    
    def exibir_secao_numerada(self, prefixo, titulo, texto, destacar=None):
        """
        Exibe uma seção numerada do tutorial com possibilidade de destacar partes.
        
        Args:
            prefixo: Numeração da seção (ex: "2.1")
            titulo: Título da seção
            texto: Texto da seção
            destacar: Lista opcional de strings a serem destacadas em verde
        """
        if not destacar:
            cli_logger.registrar_info(f"\n{prefixo}) {titulo}: {texto}")
            return
            
        # Se temos trechos para destacar, substituímos cada um deles
        texto_formatado = texto
        for trecho in destacar:
            texto_formatado = texto_formatado.replace(trecho, f"{Cores.VERDE}{trecho}{Cores.RESET}")
        
        cli_logger.registrar_info(f"\n{prefixo}) {titulo}: {texto_formatado}")
    
    def exibir_texto_aguardar(self, texto):
        """
        Exibe texto de instrução para aguardar em cor cinza.
        
        Args:
            texto: Texto de instrução para aguardar
        """
        cli_logger.registrar_info(f"\n{Cores.CINZA}{texto}{Cores.RESET}")