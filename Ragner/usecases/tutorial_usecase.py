#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use Case de Tutorial: Implementa a lógica de negócio do tutorial interativo do Ragner.
"""

import os
import time
import keyboard


class TutorialUseCase:
    """
    Caso de uso para executar o tutorial interativo do Ragner.
    
    Esta classe implementa a lógica de negócio para o tutorial, seguindo
    os princípios da Clean Architecture.
    """
    
    def __init__(self, presenter, db_gateway=None, doc_indexador=None, chat_controller=None):
        """
        Inicializa o caso de uso do tutorial.
        
        Args:
            presenter: Objeto presenter para exibir informações ao usuário
            db_gateway: Gateway de acesso ao banco de dados
            doc_indexador: Serviço de indexação de documentos
            chat_controller: Controlador do chat, usado para comandos como recarregar_arquivos_da_pasta
        """
        self.presenter = presenter
        self.db_gateway = db_gateway
        self.doc_indexador = doc_indexador
        self.chat_controller = chat_controller
    
    def executar_tutorial(self):
        """
        Executa o tutorial interativo completo do Ragner.
        
        Esta é a função principal que orquestra todos os passos do tutorial.
        """
        try:
            # Passo 1: Boas-vindas e introdução
            if self._tutorial_passo1():
                
                # Passo 2: Adicionar novos documentos
                if self._tutorial_passo2():
                    
                    # Passo 3: Verificar novos documentos
                    if self._tutorial_passo3():
                        
                        # Passo 4: Indexação dos documentos
                        if self._tutorial_passo4():
                            
                            # Passo 5: Visualizar resultados da indexação
                            if self._tutorial_passo5():
                                
                                # Passo 6: Fazendo uma pergunta (Retrieval)
                                if self._tutorial_passo6():
                                    
                                    # Passo 7: Visualizando a resposta (Generation)
                                    if self._tutorial_passo7():
                                        
                                        # Passo 8: Explorando outros comandos
                                        if self._tutorial_passo8():
                                            
                                            # Passo 9: Encerramento do tutorial
                                            self._tutorial_passo9()
        
        except Exception as e:
            self.presenter.exibir_mensagem_erro(f"Erro durante o tutorial: {str(e)}")
            self.presenter.exibir_mensagem_sistema("Pressione qualquer tecla para voltar ao programa principal...")
            keyboard.read_event()
    
    def _aguardar_tecla(self, mensagem="Pressione qualquer tecla para continuar ou ESC para sair..."):
        """
        Aguarda que o usuário pressione uma tecla.
        
        Args:
            mensagem: Mensagem a ser exibida antes de aguardar a tecla
            
        Returns:
            bool: True se o usuário quer continuar, False se quer sair (tecla ESC)
        """
        self.presenter.exibir_mensagem_sistema(f"\n{mensagem}")
        
        # Limpar qualquer evento de tecla pendente
        keyboard.read_event(suppress=True)
        
        # Aguardar a próxima tecla
        evento = keyboard.read_event(suppress=True)
        
        # Adiciona um atraso para evitar múltiplos eventos de tecla
        #time.sleep(1)
        
        # Limpar o buffer de eventos de teclado
        while keyboard.is_pressed(evento.name):
            pass
            
        if evento.name == 'esc':
            return False
        return True
    
    def _tutorial_passo1(self):
        """
        Tutorial Passo 1: Boas-vindas e introdução
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Limpa a tela na primeira etapa do tutorial
        self.presenter.limpar_tela()
        
        # Exibe cabeçalho e instruções
        self.presenter.exibir_mensagem_sistema("\n======= PASSO 1: BOAS-VINDAS AO TUTORIAL DO RAGNER =======")
        self.presenter.exibir_mensagem_sucesso("\nBem-vindo ao tutorial do Ragner!")
        self.presenter.exibir_mensagem_sistema("\nO Ragner é uma ferramenta educacional que usa tecnologia RAG (Retrieval-Augmented Generation)")
        self.presenter.exibir_mensagem_sistema("para responder perguntas com base nos seus documentos.")
        self.presenter.exibir_mensagem_sistema("\nNeste tutorial, você aprenderá como:")
        self.presenter.exibir_mensagem_sistema("1. Adicionar documentos ao Ragner")
        self.presenter.exibir_mensagem_sistema("2. Indexar e processar esses documentos")
        self.presenter.exibir_mensagem_sistema("3. Fazer perguntas sobre o conteúdo dos documentos")
        self.presenter.exibir_mensagem_sistema("4. Entender como o Ragner busca informações e gera respostas")
        
        # Aguarda que o usuário pressione uma tecla para continuar
        return self._aguardar_tecla("Pressione qualquer tecla para começar o tutorial ou ESC para sair...")
    
    def _tutorial_passo2(self):
        """
        Tutorial Passo 2: Adicionar novos documentos
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Adiciona apenas separação visual em vez de limpar a tela
        self.presenter.exibir_mensagem_sistema("\n\n" + "=" * 50)
        
        # Exibe cabeçalho e instruções para adicionar documentos
        self.presenter.exibir_mensagem_sistema("\n======= PASSO 2: ADICIONAR NOVOS DOCUMENTOS =======")
        self.presenter.exibir_mensagem_sistema("\nPara que o Ragner funcione, precisamos adicionar documentos para ele processar.")
        
        # Obtém o caminho da pasta de documentos
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        diretorio_raiz = os.path.dirname(os.path.dirname(diretorio_atual))
        pasta_documentos = os.path.join(diretorio_raiz, "documentos")
        
        self.presenter.exibir_mensagem_amarelo(f"\nPor favor, adicione um novo documento na pasta:")
        self.presenter.exibir_mensagem_sistema(f"{pasta_documentos}")
        self.presenter.exibir_mensagem_info(f"\nTipos de arquivos suportados: PDF, DOCX, TXT")
        self.presenter.exibir_mensagem_sistema("\nO processo de indexação que veremos a seguir será aplicado a este novo documento")
        self.presenter.exibir_mensagem_sistema("(ou aos documentos já existentes na pasta, caso prefira).")
        
        # Aguarda que o usuário pressione uma tecla para continuar
        return self._aguardar_tecla("Pressione qualquer tecla quando tiver adicionado documentos, ou ESC para sair...")
    
    def _tutorial_passo3(self):
        """
        Tutorial Passo 3: Verificar novos documentos
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Adiciona apenas separação visual em vez de limpar a tela
        self.presenter.exibir_mensagem_sistema("\n\n" + "=" * 50)
        
        # Exibe cabeçalho e inicia a verificação de documentos
        self.presenter.exibir_mensagem_sistema("\n======= PASSO 3: VERIFICAÇÃO DE NOVOS DOCUMENTOS =======")
        self.presenter.exibir_mensagem_sistema("\nVerificando a pasta de documentos...")
        
        # Obtém o caminho da pasta de documentos
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        diretorio_raiz = os.path.dirname(os.path.dirname(diretorio_atual))
        pasta_documentos = os.path.join(diretorio_raiz, "documentos")
        
        # Lista os arquivos na pasta
        arquivos = []
        extensoes_validas = ['.pdf', '.docx', '.txt']
        
        try:
            for arquivo in os.listdir(pasta_documentos):
                caminho_completo = os.path.join(pasta_documentos, arquivo)
                if os.path.isfile(caminho_completo):
                    _, ext = os.path.splitext(arquivo)
                    if ext.lower() in extensoes_validas:
                        arquivos.append(arquivo)
        except Exception as e:
            self.presenter.exibir_mensagem_erro(f"Erro ao listar arquivos: {str(e)}")
        
        # Verificar no banco de dados se os documentos já estão indexados
        documentos_indexados = []
        if self.db_gateway:
            try:
                # Tentar obter a lista de documentos já indexados
                documentos_db = self.db_gateway.listar_arquivos_db()
                for doc_db in documentos_db:
                    if 'arquivo_nome' in doc_db:
                        documentos_indexados.append(doc_db['arquivo_nome'])
            except Exception as e:
                # Se ocorrer algum erro, assumimos que não há documentos indexados
                documentos_indexados = []
        
        # Verificar quais arquivos encontrados já estão indexados
        arquivos_indexados = []
        arquivos_nao_indexados = []
        
        for arquivo in arquivos:
            if arquivo in documentos_indexados:
                arquivos_indexados.append(arquivo)
            else:
                arquivos_nao_indexados.append(arquivo)
        
        # Exibe o resultado da verificação
        if arquivos:
            self.presenter.exibir_mensagem_sucesso(f"\nEncontrado(s) {len(arquivos)} arquivo(s) na pasta:")
            for i, arquivo in enumerate(arquivos, 1):
                self.presenter.exibir_mensagem_sistema(f"{i}. {arquivo}")
            
            if arquivos_indexados and not arquivos_nao_indexados:
                # Todos os documentos já estão indexados
                self.presenter.exibir_mensagem_info(f"\nTodos os documentos já estão indexados!")
                self.presenter.exibir_mensagem_sistema("Você pode visualizar os detalhes desses documentos no próximo passo.")
                
                # Oferecer a opção de reindexar durante o tutorial
                self.presenter.exibir_mensagem_sistema("\nDeseja reindexar todos os documentos agora?")
                self.presenter.exibir_mensagem_sistema("R - Reindexar todos os documentos")
                self.presenter.exibir_mensagem_sistema("C - Continuar sem reindexar")
                self.presenter.exibir_mensagem_sistema("ESC - Sair do tutorial")
                
                # Aguardar a entrada do usuário (R, C ou ESC)
                keyboard.read_event(suppress=True)  # Limpar o buffer
                evento = keyboard.read_event(suppress=True)
                
                # Adiciona um atraso para evitar múltiplos eventos de tecla
                time.sleep(1)
                
                # Processar a escolha do usuário
                if evento.name.lower() == 'r':
                    # Reindexar documentos
                    self.presenter.exibir_mensagem_sistema("\nReindexando documentos...")
                    if self.chat_controller and self.db_gateway:
                        try:
                            # 1. Primeiro apagar todos os dados do banco de dados
                            self.presenter.exibir_mensagem_sistema("Limpando dados existentes...")
                            self.db_gateway.apagar_tudo_db()
                            
                            # 2. Depois reindexar todos os documentos usando o controlador
                            self.presenter.exibir_mensagem_sistema("Iniciando o processo de reindexação...")
                            self.chat_controller.recarregar_arquivos_da_pasta()
                            self.presenter.exibir_mensagem_sucesso("\nReindexação concluída com sucesso!")
                        except Exception as e:
                            self.presenter.exibir_mensagem_erro(f"Erro durante a reindexação: {str(e)}")
                    else: 
                        # Se não houver controlador de chat disponível, informar que não pode reindexar
                        self.presenter.exibir_mensagem_erro("\nNão foi possível reindexar os documentos.")
                        self.presenter.exibir_mensagem_sistema("O controlador de chat ou o gateway de banco de dados não está disponível durante o tutorial.")
                        self.presenter.exibir_mensagem_sistema("Use o comando 'recarregar_arquivos_da_pasta' no programa principal.")
                    
                    # Aguardar a tecla para continuar após reindexação
                    return self._aguardar_tecla("Pressione qualquer tecla para continuar ou ESC para sair...")
                
                elif evento.name.lower() == 'c':
                    # Continuar sem reindexar
                    self.presenter.exibir_mensagem_sistema("\nContinuando sem reindexar os documentos.")
                    return True
                
                elif evento.name == 'esc':
                    # Sair do tutorial
                    return False
                
                # Se for qualquer outra tecla, continuamos sem reindexar
                self.presenter.exibir_mensagem_sistema("\nContinuando sem reindexar os documentos.")
                return True
            
            elif arquivos_indexados:
                # Alguns documentos já estão indexados
                self.presenter.exibir_mensagem_info(f"\nNota: {len(arquivos_indexados)} documento(s) já está(ão) indexado(s):")
                for arquivo in arquivos_indexados:
                    self.presenter.exibir_mensagem_sistema(f"- {arquivo}")
                
                if arquivos_nao_indexados:
                    self.presenter.exibir_mensagem_sucesso(f"\n{len(arquivos_nao_indexados)} novo(s) documento(s) para indexar:")
                    for arquivo in arquivos_nao_indexados:
                        self.presenter.exibir_mensagem_sistema(f"- {arquivo}")
            
            self.presenter.exibir_mensagem_sistema("\nPressione a tecla ESPAÇO para prosseguir para o próximo passo.")
            
            # Aguardar a entrada de ESPAÇO
            keyboard.read_event(suppress=True)
            evento = keyboard.read_event(suppress=True)
            
            # Adiciona um atraso para evitar múltiplos eventos de tecla
            time.sleep(1)
            
            # Se a tecla for ESC, encerra o tutorial
            if evento.name == 'esc':
                return False
            
            # Se a tecla for ESPAÇO ou qualquer outra, continua
            return True
        else:
            self.presenter.exibir_mensagem_info("\nNenhum arquivo encontrado na pasta de documentos.")
            self.presenter.exibir_mensagem_sistema("\nVocê precisa adicionar pelo menos um arquivo para continuar o tutorial.")
            self.presenter.exibir_mensagem_sistema("Tipos de arquivos aceitos: PDF, DOCX, TXT")
            
            # Pergunta se o usuário quer tentar novamente ou sair
            self.presenter.exibir_mensagem_sistema("\nDeseja tentar novamente?")
            return self._aguardar_tecla("Pressione qualquer tecla para verificar novamente ou ESC para sair...")
    
    def _tutorial_passo4(self):
        """
        Tutorial Passo 4: Indexação dos documentos
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Adiciona apenas separação visual em vez de limpar a tela
        self.presenter.exibir_mensagem_sistema("\n\n" + "=" * 50)
        
        # Exibe cabeçalho e instruções de indexação
        self.presenter.exibir_mensagem_sistema("\n======= PASSO 4: INDEXAÇÃO DOS DOCUMENTOS =======")
        
        # Verificar se temos documentos indexados
        documentos_indexados = []
        if self.db_gateway:
            try:
                # Tentar obter a lista de documentos já indexados
                documentos_db = self.db_gateway.listar_arquivos_db()
                for doc_db in documentos_db:
                    if 'arquivo_nome' in doc_db:
                        documentos_indexados.append(doc_db['arquivo_nome'])
            except Exception as e:
                # Se ocorrer algum erro, assumimos que não há documentos indexados
                documentos_indexados = []

        # Se documentos já estão indexados
        if documentos_indexados:
            self.presenter.exibir_mensagem_info("\nSeus documentos já estão indexados!")
            self.presenter.exibir_mensagem_sistema(f"\nO Ragner já processou {len(documentos_indexados)} documento(s):")
            for doc in documentos_indexados:
                self.presenter.exibir_mensagem_sistema(f"- {doc}")
            
            # Tentar obter o número de chunks
            num_chunks = 0
            try:
                if self.db_gateway:
                    chunks = self.db_gateway.listar_chunks_db()
                    num_chunks = len(chunks)
            except:
                pass
            
            if num_chunks > 0:
                self.presenter.exibir_mensagem_sistema(f"\nForam gerados {num_chunks} chunks a partir desses documentos.")
            
            self.presenter.exibir_mensagem_sistema("\nPara reindexar os documentos a qualquer momento, você pode usar o comando:")
            self.presenter.exibir_mensagem_info("recarregar_arquivos_da_pasta")
        else:
            # Se não há documentos indexados, mostrar o processo normal
            self.presenter.exibir_mensagem_sistema("\nIniciando o processo de indexação dos documentos...")
            self.presenter.exibir_mensagem_sistema("\nDurante a indexação, o Ragner realiza as seguintes etapas:")
            self.presenter.exibir_mensagem_sistema("1. Lê o conteúdo de cada documento")
            self.presenter.exibir_mensagem_sistema("2. Divide o texto em pequenos trechos (chunks)")
            self.presenter.exibir_mensagem_sistema("3. Cria representações vetoriais (embeddings) para cada trecho")
            self.presenter.exibir_mensagem_sistema("4. Armazena esses vetores em um índice FAISS para busca rápida")
            
            self.presenter.exibir_mensagem_sistema("\nNo programa principal, esse processo é iniciado com o comando:")
            self.presenter.exibir_mensagem_info("recarregar_arquivos_da_pasta")
            
            # Aqui simulamos ou indicamos que o processo de indexação está ocorrendo
            self.presenter.exibir_mensagem_sistema("\nObserve as mensagens de processamento que seriam exibidas:")
            self.presenter.exibir_mensagem_sistema("Verificando arquivos na pasta 'documentos'...")
            self.presenter.exibir_mensagem_sistema("Processando documento: exemplo.pdf")
            self.presenter.exibir_mensagem_sistema("Dividindo documento em chunks...")
            self.presenter.exibir_mensagem_sistema("Gerando embeddings para os chunks...")
            self.presenter.exibir_mensagem_sistema("Adicionando vetores ao índice FAISS...")
            self.presenter.exibir_mensagem_sucesso("\nIndexação concluída com sucesso!")
            self.presenter.exibir_mensagem_sistema("3 documentos processados")
            self.presenter.exibir_mensagem_sistema("42 chunks gerados")
        
        # Aguarda que o usuário pressione uma tecla para continuar
        return self._aguardar_tecla()
    
    def _tutorial_passo5(self):
        """
        Tutorial Passo 5: Visualizar resultados da indexação
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Adiciona apenas separação visual em vez de limpar a tela
        self.presenter.exibir_mensagem_sistema("\n\n" + "=" * 50)
        
        # Exibe cabeçalho e instruções de visualização de resultados
        self.presenter.exibir_mensagem_sistema("\n======= PASSO 5: VISUALIZAR RESULTADOS DA INDEXAÇÃO =======")
        self.presenter.exibir_mensagem_sistema("\nAgora que os documentos foram indexados, você pode verificar os resultados")
        self.presenter.exibir_mensagem_sistema("utilizando os seguintes comandos no programa principal:")
        
        self.presenter.exibir_mensagem_info("\nstatus_tabela_arquivos")
        self.presenter.exibir_mensagem_sistema("Este comando mostra uma lista dos arquivos processados com detalhes como:")
        self.presenter.exibir_mensagem_sistema("- Nome do arquivo")
        self.presenter.exibir_mensagem_sistema("- Tipo de arquivo")
        self.presenter.exibir_mensagem_sistema("- Tamanho em bytes")
        self.presenter.exibir_mensagem_sistema("- Quantidade de chunks gerados")
        
        self.presenter.exibir_mensagem_info("\nstatus_tabela_chunks")
        self.presenter.exibir_mensagem_sistema("Este comando exibe informações sobre os chunks (trechos) criados:")
        self.presenter.exibir_mensagem_sistema("- ID do chunk")
        self.presenter.exibir_mensagem_sistema("- Arquivo de origem")
        self.presenter.exibir_mensagem_sistema("- Primeiras palavras do texto")
        self.presenter.exibir_mensagem_sistema("- Tamanho do texto")
        
        self.presenter.exibir_mensagem_info("\nstatus_faiss")
        self.presenter.exibir_mensagem_sistema("Este comando mostra informações técnicas sobre o índice vetorial FAISS:")
        self.presenter.exibir_mensagem_sistema("- Dimensão dos vetores")
        self.presenter.exibir_mensagem_sistema("- Quantidade de vetores armazenados")
        self.presenter.exibir_mensagem_sistema("- Tipo de índice")
        
        # Aguarda que o usuário pressione uma tecla para continuar
        return self._aguardar_tecla()
    
    def _tutorial_passo6(self):
        """
        Tutorial Passo 6: Fazendo uma pergunta (Retrieval)
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Adiciona apenas separação visual em vez de limpar a tela
        self.presenter.exibir_mensagem_sistema("\n\n" + "=" * 50)
        
        # Exibe cabeçalho e instruções para fazer perguntas
        self.presenter.exibir_mensagem_sistema("\n======= PASSO 6: FAZENDO UMA PERGUNTA (RETRIEVAL) =======")
        self.presenter.exibir_mensagem_sistema("\nAgora você pode fazer perguntas sobre o conteúdo dos documentos indexados!")
        self.presenter.exibir_mensagem_sistema("\nPara fazer uma pergunta, simplesmente:")
        self.presenter.exibir_mensagem_sistema("1. Digite sua pergunta diretamente no programa principal")
        self.presenter.exibir_mensagem_sistema("2. Pressione Enter")
        
        self.presenter.exibir_mensagem_sistema("\nProcesso de Retrieval (Recuperação):")
        self.presenter.exibir_mensagem_sistema("1. Sua pergunta é convertida em um vetor numérico (embedding)")
        self.presenter.exibir_mensagem_sistema("2. O sistema busca no índice FAISS os trechos mais similares à sua pergunta")
        self.presenter.exibir_mensagem_sistema("3. Os trechos encontrados formam o contexto para gerar a resposta")
        
        self.presenter.exibir_mensagem_info("\nExemplo de pergunta: \"Quais são os principais conceitos abordados no documento?\"")
        self.presenter.exibir_mensagem_sistema("\nObserve as mensagens que mostram o processo de busca:")
        self.presenter.exibir_mensagem_sistema("Processando pergunta...")
        self.presenter.exibir_mensagem_sistema("Gerando embedding para a pergunta...")
        self.presenter.exibir_mensagem_sistema("Buscando chunks relevantes...")
        self.presenter.exibir_mensagem_sistema("Encontrados 3 chunks relevantes para a pergunta.")
        
        # Aguarda que o usuário pressione uma tecla para continuar
        return self._aguardar_tecla()
    
    def _tutorial_passo7(self):
        """
        Tutorial Passo 7: Visualizando a resposta (Generation)
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Adiciona apenas separação visual em vez de limpar a tela
        self.presenter.exibir_mensagem_sistema("\n\n" + "=" * 50)
        
        # Exibe cabeçalho e instruções para analisar respostas
        self.presenter.exibir_mensagem_sistema("\n======= PASSO 7: VISUALIZANDO A RESPOSTA (GENERATION) =======")
        self.presenter.exibir_mensagem_sistema("\nDepois que o Ragner encontra os trechos relevantes (Retrieval),")
        self.presenter.exibir_mensagem_sistema("ele usa um modelo de linguagem para gerar uma resposta (Generation).")
        
        self.presenter.exibir_mensagem_sistema("\nProcesso de Generation (Geração):")
        self.presenter.exibir_mensagem_sistema("1. Os trechos relevantes são enviados ao modelo de linguagem junto com a pergunta")
        self.presenter.exibir_mensagem_sistema("2. O modelo gera uma resposta baseada apenas no contexto fornecido")
        self.presenter.exibir_mensagem_sistema("3. A resposta é apresentada ao usuário com as fontes utilizadas")
        
        self.presenter.exibir_mensagem_sucesso("\nExemplo de resposta:")
        self.presenter.exibir_mensagem_sistema("Os principais conceitos abordados no documento são: Retrieval-Augmented")
        self.presenter.exibir_mensagem_sistema("Generation (RAG), embeddings vetoriais, busca semântica e geração de")
        self.presenter.exibir_mensagem_sistema("texto baseada em contexto. O documento explica como esses elementos")
        self.presenter.exibir_mensagem_sistema("se combinam para criar sistemas de IA capazes de responder perguntas")
        self.presenter.exibir_mensagem_sistema("com base em conhecimento específico contido em documentos.")
        
        self.presenter.exibir_mensagem_sistema("\nFontes utilizadas:")
        self.presenter.exibir_mensagem_sistema("- exemplo.pdf")
        
        # Aguarda que o usuário pressione uma tecla para continuar
        return self._aguardar_tecla()
    
    def _tutorial_passo8(self):
        """
        Tutorial Passo 8: Explorando outros comandos
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Adiciona apenas separação visual em vez de limpar a tela
        self.presenter.exibir_mensagem_sistema("\n\n" + "=" * 50)
        
        # Exibe cabeçalho e instruções sobre comandos adicionais
        self.presenter.exibir_mensagem_sistema("\n======= PASSO 8: EXPLORANDO OUTROS COMANDOS =======")
        self.presenter.exibir_mensagem_sistema("\nO Ragner possui outros comandos úteis que você pode explorar:")
        
        self.presenter.exibir_mensagem_info("\nmenu")
        self.presenter.exibir_mensagem_sistema("Exibe todos os comandos disponíveis no sistema")
        
        self.presenter.exibir_mensagem_info("\nstatus")
        self.presenter.exibir_mensagem_sistema("Mostra um resumo geral do sistema, incluindo quantidade de documentos e chunks")
        
        self.presenter.exibir_mensagem_info("\nsobre")
        self.presenter.exibir_mensagem_sistema("Exibe informações gerais sobre o Ragner e a tecnologia RAG")
        
        self.presenter.exibir_mensagem_erro("\nCUIDADO: apagar_tudo")
        self.presenter.exibir_mensagem_sistema("Este comando apaga todos os dados indexados. Use apenas quando necessário.")
        
        # Aguarda que o usuário pressione uma tecla para continuar
        return self._aguardar_tecla()
    
    def _tutorial_passo9(self):
        """
        Tutorial Passo 9: Encerramento
        """
        # Adiciona apenas separação visual em vez de limpar a tela
        self.presenter.exibir_mensagem_sistema("\n\n" + "=" * 50)
        
        # Exibe cabeçalho e mensagem de encerramento
        self.presenter.exibir_mensagem_sistema("\n======= PASSO 9: ENCERRAMENTO =======")
        self.presenter.exibir_mensagem_sucesso("\nParabéns! Você completou o tutorial do Ragner!")
        self.presenter.exibir_mensagem_sistema("\nAgora você entende como funciona a tecnologia RAG (Retrieval-Augmented Generation)")
        self.presenter.exibir_mensagem_sistema("e como o Ragner implementa esse processo para responder perguntas baseadas")
        self.presenter.exibir_mensagem_sistema("nos seus documentos.")
        
        self.presenter.exibir_mensagem_info("\nPróximos passos:")
        self.presenter.exibir_mensagem_sistema("1. Adicione seus próprios documentos na pasta 'documentos'")
        self.presenter.exibir_mensagem_sistema("2. Use o comando 'recarregar_arquivos_da_pasta' para indexá-los")
        self.presenter.exibir_mensagem_sistema("3. Faça perguntas diretamente ou explore os comandos mencionados")
        
        self.presenter.exibir_mensagem_sistema("\nLembre-se de usar o comando 'menu' se precisar consultar a lista de comandos.")
        self.presenter.exibir_mensagem_sucesso("\nObrigado por usar o Ragner e boas consultas!")
        
        # Aguarda que o usuário pressione uma tecla para encerrar
        self._aguardar_tecla("Pressione qualquer tecla para retornar ao programa principal...")