#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Controllers: Classes responsáveis por gerenciar a interação entre a interface CLI e os casos de uso.
"""

import os
import sys
from presentation.cli.cli_cores import Cores

class ChatController:
    """
    Controlador para o chat CLI.
    
    Esta classe é responsável por coordenar os casos de uso e gerenciar
    o fluxo de interação com o usuário.
    """
    
    def __init__(self, configurar_api_key_usecase, indexar_documentos_usecase, 
                 buscar_contexto_usecase, fazer_pergunta_usecase, gerar_resposta_usecase,
                 presenter):
        """
        Inicializa o controlador.
        
        Args:
            configurar_api_key_usecase: Caso de uso para configuração da chave de API
            indexar_documentos_usecase: Caso de uso para indexação de documentos
            buscar_contexto_usecase: Caso de uso para busca de contexto relevante
            fazer_pergunta_usecase: Caso de uso para processamento de perguntas
            gerar_resposta_usecase: Caso de uso para geração de respostas
            presenter: Presenter para exibição de mensagens
        """
        self.configurar_api_key_usecase = configurar_api_key_usecase
        self.indexar_documentos_usecase = indexar_documentos_usecase
        self.buscar_contexto_usecase = buscar_contexto_usecase
        self.fazer_pergunta_usecase = fazer_pergunta_usecase
        self.gerar_resposta_usecase = gerar_resposta_usecase
        self.presenter = presenter
        
        # Obtém o caminho para a pasta de documentos
        self.pasta_documentos = self._obter_pasta_documentos()
    
    def _obter_pasta_documentos(self):
        """
        Obtém o caminho para a pasta de documentos.
        
        Returns:
            str: Caminho para a pasta de documentos
        """
        # Obtém o diretório raiz do projeto (assume que estamos em Ragner/presentation/cli)
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        diretorio_raiz = os.path.dirname(os.path.dirname(os.path.dirname(diretorio_atual)))
        
        # Define o caminho para a pasta de documentos
        pasta_documentos = os.path.join(diretorio_raiz, "documentos")
        
        # Cria a pasta se não existir
        if not os.path.exists(pasta_documentos):
            os.makedirs(pasta_documentos)
            print(f"Pasta de documentos criada em: {pasta_documentos}")
        
        return pasta_documentos
    
    def verificar_e_configurar_api_key(self):
        """
        Verifica se a chave de API está configurada. Se não, solicita ao usuário.
        """
        print(f"{Cores.CINZA}Verificando a chave da OpenAI...{Cores.RESET}")
        
        # Verifica se a chave de API já está configurada
        if not self.configurar_api_key_usecase.obter_api_key_configurada():
            print(f"{Cores.CINZA}Erro ao validar a chave da OpenAI: Chave inválida{Cores.RESET}")
            
            while True:
                # Solicita a chave de API ao usuário com um prompt claro
                api_key = input(f"{Cores.AMARELO}Digite sua chave da OpenAI (ou 'sair' para encerrar): {Cores.RESET}")
                
                if api_key.lower() == 'sair':
                    print("Tchau!")
                    sys.exit(0)
                
                # Configura a chave de API
                if self.configurar_api_key_usecase.executar(api_key):
                    self.presenter.exibir_mensagem_sucesso(f"{Cores.CINZA}Chave de API configurada com sucesso!{Cores.RESET}")
                    break
                else:
                    print(f"{Cores.CINZA}Erro ao validar a chave da OpenAI: Chave inválida{Cores.RESET}")
        else:
            # Verifica se a chave configurada é válida
            if not self.configurar_api_key_usecase.openai_gateway.verificar_api_key():
                print(f"{Cores.CINZA}Erro ao validar a chave da OpenAI: Chave inválida{Cores.RESET}")
                
                while True:
                    # Solicita uma nova chave de API ao usuário
                    api_key = input(f"{Cores.AMARELO}Digite sua chave da OpenAI (ou 'sair' para encerrar): {Cores.RESET}")
                    
                    if api_key.lower() == 'sair':
                        print("Bye!")
                        sys.exit(0)
                    
                    # Configura a nova chave de API
                    if self.configurar_api_key_usecase.executar(api_key):
                        self.presenter.exibir_mensagem_sucesso("Chave de API configurada com sucesso!")
                        break
                    else:
                        print(f"{Cores.CINZA}Erro ao validar a chave da OpenAI: Chave inválida{Cores.RESET}")
            else:
                print(f"{Cores.CINZA}Chave da OpenAI validada com sucesso.{Cores.RESET}")
    
    def verificar_e_indexar_documentos(self):
        """
        Verifica se existem documentos na pasta e os indexa, se necessário.
        """
        # Verifica se há documentos na pasta
        arquivos_encontrados = False
        for extensao in ["pdf", "docx", "txt"]:
            if any(arquivo.endswith(f".{extensao}") for arquivo in os.listdir(self.pasta_documentos)):
                arquivos_encontrados = True
                break
        
        # Se não houver documentos, exibe uma mensagem
        if not arquivos_encontrados:
            self.presenter.exibir_mensagem_info(f"Não foram encontrados documentos na pasta {Cores.AMARELO}{self.pasta_documentos}{Cores.RESET}")
            self.presenter.exibir_mensagem_info(f"Adicione documentos (PDF, DOCX, TXT) nesta pasta e use o comando {Cores.AMARELO}'recarregar_arquivos_da_pasta'{Cores.RESET}")
            return
        
        # Indexa os documentos
        self.presenter.exibir_processando("indexação de documentos")
        total_docs, total_chunks = self.indexar_documentos_usecase.indexar_pasta(self.pasta_documentos)
        
        if total_docs > 0:
            self.presenter.exibir_mensagem_sucesso(f"{Cores.CINZA}Indexação concluída: {total_docs} documentos, {total_chunks} chunks{Cores.RESET}")
        else:
            self.presenter.exibir_mensagem_info("Nenhum documento novo para indexar.")
    
    def recarregar_arquivos_da_pasta(self):
        """
        Recarrega os arquivos da pasta, verifica arquivos deletados e sincroniza o índice FAISS.
        Este método executa o mesmo processo que ocorre na inicialização do programa.
        """
        # 1) Verificar documentos na pasta
        self.presenter.exibir_mensagem_info("Verificando documentos na pasta...")
        
        arquivos_na_pasta = []
        extensoes_validas = ["pdf", "docx", "txt"]
        
        for arquivo in os.listdir(self.pasta_documentos):
            extensao = arquivo.lower().split('.')[-1] if '.' in arquivo else ""
            if extensao in extensoes_validas:
                caminho_completo = os.path.join(self.pasta_documentos, arquivo)
                if os.path.isfile(caminho_completo):
                    arquivos_na_pasta.append({
                        'nome': arquivo,
                        'caminho': caminho_completo,
                        'tipo': extensao
                    })
        
        self.presenter.exibir_mensagem_info(f"Encontrados {len(arquivos_na_pasta)} documento(s) na pasta:")
        for arquivo in arquivos_na_pasta:
            self.presenter.exibir_mensagem_info(f"- {arquivo['nome']}")
        
        # 2) Verificar documentos processados no banco de dados
        self.presenter.exibir_mensagem_info("Verificando documentos processados no banco de dados...")
        db_gateway = self.indexar_documentos_usecase.db_gateway
        documentos_no_banco = db_gateway.listar_arquivos_db()
        arquivos_processados = [doc['arquivo_nome'] for doc in documentos_no_banco]
        
        self.presenter.exibir_mensagem_info(f"Documentos já processados: {len(arquivos_processados)}")
        if arquivos_processados:
            for nome in arquivos_processados:
                self.presenter.exibir_mensagem_info(f"- {nome}")
        
        # 3) Verificar arquivos removidos da pasta
        self.presenter.exibir_mensagem_info("Verificando se há arquivos que foram removidos da pasta de documentos...")
        arquivos_removidos = self.indexar_documentos_usecase.verificar_arquivos_deletados(self.pasta_documentos)
        
        if arquivos_removidos > 0:
            self.presenter.exibir_mensagem_info(f"Foram removidos {arquivos_removidos} arquivo(s) que não existem mais na pasta.")
        
        # 4) Identificar novos documentos
        novos_documentos = [doc for doc in arquivos_na_pasta if doc['nome'] not in arquivos_processados]
        
        self.presenter.exibir_mensagem_info(f"Documentos a processar: {len(novos_documentos)}")
        if novos_documentos:
            for doc in novos_documentos:
                self.presenter.exibir_mensagem_info(f"- {doc['nome']}")
        
            # 5) Processar novos documentos
            self.presenter.exibir_mensagem_info("Iniciando processamento automático de novos documentos...")
            total_docs = 0
            total_chunks = 0
            for doc in novos_documentos:
                self.presenter.exibir_mensagem_info(f"Processando documento: {doc['nome']}")
                try:
                    # Usar o caso de uso existente para indexar o documento
                    docs, chunks = self.indexar_documentos_usecase.indexar_documento(doc['caminho'])
                    total_docs += docs
                    total_chunks += chunks
                    if docs > 0:
                        self.presenter.exibir_mensagem_sucesso(f"Documento '{doc['nome']}' processado com sucesso: {chunks} chunks gerados")
                    else:
                        self.presenter.exibir_mensagem_erro(f"Falha ao processar documento '{doc['nome']}'")
                except Exception as e:
                    self.presenter.exibir_mensagem_erro(f"Erro ao processar documento '{doc['nome']}': {str(e)}")
            
            self.presenter.exibir_mensagem_sucesso(f"Processamento automático concluído. {total_docs} documentos e {total_chunks} chunks processados.")
        
        # 6) Inicializar e sincronizar o índice FAISS
        self.presenter.exibir_mensagem_info("Inicializando índice FAISS no final do processo...")
        
        # Inicializar explicitamente o índice FAISS
        vector_store = self.indexar_documentos_usecase.vector_store
        vector_store.inicializar_indice()
        
        # Verificar e sincronizar o índice FAISS com o banco de dados
        self.presenter.exibir_mensagem_info("Verificando sincronização do índice FAISS...")
        self.indexar_documentos_usecase.verificar_sincronizacao_faiss()
        
        self.presenter.exibir_mensagem_info(f"{Cores.CINZA}Inicialização do FAISS concluída.{Cores.RESET}")
    
    def processar_comando(self, comando, argumento=None):
        """
        Processa um comando do usuário.
        
        Args:
            comando: Comando a ser processado
            argumento: Argumento opcional para o comando
            
        Returns:
            bool: True se o programa deve continuar, False se deve encerrar
        """
        if comando == "sobre":
            self.presenter.exibir_sobre()
            
        elif comando == "tutorial":
            self.presenter.exibir_tutorial()
            
        elif comando == "configurar_api_key":
            self._configurar_nova_api_key()
            
        elif comando == "status":
            self._exibir_status()
            
        elif comando == "status_tabela_arquivos":
            self._exibir_status_arquivos()
            
        elif comando == "status_tabela_chunks":
            self._exibir_status_chunks()
            
        elif comando == "status_faiss":
            self._exibir_status_faiss()
            
        elif comando == "menu":
            self.presenter.exibir_menu()
            
        elif comando == "recarregar_arquivos_da_pasta":
            self.recarregar_arquivos_da_pasta()
            
        elif comando == "reconstruir_indice_faiss":
            self._reconstruir_indice_faiss()
            
        elif comando == "apagar_tudo":
            self._confirmar_e_apagar_tudo()
            
        elif comando == "sair":
            print("Encerrando o Ragner Chatbot. Até logo!")
            return False
        
        return True
    
    def processar_pergunta(self, texto_pergunta):
        """
        Processa uma pergunta do usuário e gera uma resposta.
        
        Args:
            texto_pergunta: Texto da pergunta
        """
        # Verifica se a pergunta não é vazia
        if not texto_pergunta.strip():
            return
        
        # Exibe a pergunta formatada
        self.presenter.exibir_pergunta(texto_pergunta)
        
        try:
            # Etapa 1: Calculando o valor de embeddings da pergunta
            self.presenter.exibir_progresso("Etapa 1", "Calculando o valor embeddings da sua pergunta...")
            language_model = self.configurar_api_key_usecase.openai_gateway
            pergunta, embedding = self.fazer_pergunta_usecase.executar(texto_pergunta, language_model)
            
            # Exibe uma amostra do vetor embedding resultante
            if embedding is not None:
                # Exibir os primeiros 5 valores do embedding
                embedding_sample = embedding[:5]
                embedding_str = ', '.join([f"{val:.6f}" for val in embedding_sample])
                self.presenter.exibir_mensagem_info(f"Embedding gerado: [{embedding_str}, ...]")
            
            # Se não foi possível gerar o embedding, retorna
            if embedding is None:
                self.presenter.exibir_mensagem_erro("Não foi possível processar sua pergunta. Tente novamente.")
                return
            
            # Etapa 2: Busca no módulo FAISS vetores mais próximos
            self.presenter.exibir_progresso("Etapa 2", "Buscando no módulo FAISS vetores mais próximos...")
            
            # Buscar chunks similares diretamente do vetor_store para mostrar informações sobre a busca
            top_k = self.buscar_contexto_usecase.max_chunks
            try:
                chunk_ids, scores = self.buscar_contexto_usecase.vector_store.buscar_chunks_similares(embedding, top_k)
                
                # Exibir o número de vetores encontrados
                self.presenter.exibir_progresso("Etapa 3", f"Encontrados {len(chunk_ids)} vetores similares")
                
                # Se encontrou algum vetor similar, mostre o score do primeiro
                if len(chunk_ids) > 0 and len(scores) > 0:
                    best_score = scores[0]
                    self.presenter.exibir_mensagem_info(f"Score do vetor mais similar: {best_score:.6f} (menor valor = mais similar)")
            except Exception as e:
                self.presenter.exibir_mensagem_erro(f"Erro ao buscar vetores similares: {str(e)}")
                self.presenter.exibir_progresso("Etapa 3", "Encontrados 0 vetores similares")
            
            # Etapa 4: Buscando no banco de dados os chunks associados com estes vetores
            self.presenter.exibir_progresso("Etapa 4", "Buscando no banco de dados os chunks (pedaços de textos) associados com estes vetores...")
            chunks_relevantes = self.buscar_contexto_usecase.executar(embedding)
            
            # Etapa 5: Anexando chunks à pergunta que será enviada ao ChatGPT
            num_chunks = len(chunks_relevantes)
            self.presenter.exibir_progresso("Etapa 5", f"Anexando {num_chunks} chunks à pergunta que será enviada ao ChatGPT...")
            
            # Se não encontrou chunks relevantes, informe o usuário
            if num_chunks == 0:
                self.presenter.exibir_mensagem_info("Nenhum chunk relevante encontrado. A pergunta será enviada sem contexto adicional.")
            
            # Exibe o contexto encontrado
            self.presenter.exibir_contexto(chunks_relevantes)
            
            # Etapa 6: Anexando o contexto e enviando a pergunta ao ChatGPT
            self.presenter.exibir_progresso("Etapa 6", "Anexando o contexto encontrado e enviando a pergunta ao ChatGPT...")
            
            # Etapa 7: Coletando a resposta do ChatGPT
            self.presenter.exibir_progresso("Etapa 7", "Coletando a resposta do ChatGPT...")
            resposta = self.gerar_resposta_usecase.executar(pergunta, chunks_relevantes)
            
            # Etapa 8: Respondendo ao usuário
            self.presenter.exibir_progresso("Etapa 8", "Respondendo ao usuário...")
            
            # Exibe a resposta
            self.presenter.exibir_resposta(resposta)
        
        except Exception as e:
            self.presenter.exibir_mensagem_erro(f"Erro ao processar a pergunta: {str(e)}")
    
    def _exibir_status(self):
        """Exibe o status geral do sistema."""
        # TODO: Implementar estatísticas sobre documentos, chunks e índice
        self.presenter.exibir_mensagem_info("Status do sistema:")
        
        # Número de documentos e chunks
        self.presenter.exibir_mensagem_info("Verificando banco de dados...")
        # Este trecho assume que temos acesso ao db_gateway através do indexar_documentos_usecase
        db_gateway = self.indexar_documentos_usecase.db_gateway
        num_documentos = db_gateway.contar_documentos()
        num_chunks = db_gateway.contar_chunks()
        self.presenter.exibir_mensagem_info(f"Documentos indexados: {num_documentos}")
        self.presenter.exibir_mensagem_info(f"Chunks processados: {num_chunks}")
        
        # Informações do índice FAISS
        self.presenter.exibir_mensagem_info("Verificando índice vetorial...")
        vector_store = self.indexar_documentos_usecase.vector_store
        estatisticas = vector_store.obter_estatisticas()
        self.presenter.exibir_mensagem_info(f"Índice FAISS: {'Inicializado' if estatisticas['inicializado'] else 'Não inicializado'}")
        self.presenter.exibir_mensagem_info(f"Vetores no índice: {estatisticas['vetores']}")
        self.presenter.exibir_mensagem_info(f"Dimensão dos vetores: {estatisticas['dimensao']}")
    
    def _exibir_status_arquivos(self):
        """Exibe a lista de arquivos indexados."""
        db_gateway = self.indexar_documentos_usecase.db_gateway
        documentos = db_gateway.listar_documentos()
        
        if not documentos:
            self.presenter.exibir_mensagem_info("Nenhum arquivo indexado.")
            return
        
        self.presenter.exibir_mensagem_info(f"Arquivos indexados ({len(documentos)}):")
        for doc in documentos:
            self.presenter.exibir_mensagem_info(f"- {doc['arquivo_nome']} (ID: {doc['arquivo_uuid']}, tipo: {doc['arquivo_tipo']})")
    
    def _exibir_status_chunks(self):
        """Exibe informações sobre os chunks indexados."""
        db_gateway = self.indexar_documentos_usecase.db_gateway
        num_chunks = db_gateway.contar_chunks()
        
        self.presenter.exibir_mensagem_info(f"Total de chunks: {num_chunks}")
        # TODO: Implementar mais estatísticas sobre chunks se necessário
    
    def _exibir_status_faiss(self):
        """Exibe informações sobre o índice FAISS."""
        vector_store = self.indexar_documentos_usecase.vector_store
        estatisticas = vector_store.obter_estatisticas()
        
        self.presenter.exibir_mensagem_info("Índice vetorial FAISS:")
        self.presenter.exibir_mensagem_info(f"Status: {'Inicializado' if estatisticas['inicializado'] else 'Não inicializado'}")
        self.presenter.exibir_mensagem_info(f"Número de vetores: {estatisticas['vetores']}")
        self.presenter.exibir_mensagem_info(f"Dimensão dos vetores: {estatisticas['dimensao']}")
    
    def _confirmar_e_apagar_tudo(self):
        """Solicita confirmação do usuário e apaga todos os dados."""
        self.presenter.exibir_mensagem_info("Esta operação apagará todos os dados indexados.")
        confirmacao = input("Você tem certeza? (s/N): ").strip().lower()
        
        if confirmacao == 's':
            self.presenter.exibir_processando("limpeza de dados")
            
            try:
                db_gateway = self.indexar_documentos_usecase.db_gateway
                vector_store = self.indexar_documentos_usecase.vector_store
                
                # Apaga todos os dados do banco de dados
                db_gateway.apagar_tudo()
                
                # Reinicia o índice FAISS
                vector_store.reiniciar_indice()
                
                self.presenter.exibir_mensagem_sucesso("Todos os dados foram apagados com sucesso.")
                
            except Exception as e:
                self.presenter.exibir_mensagem_erro(f"Erro ao apagar dados: {str(e)}")
        else:
            self.presenter.exibir_mensagem_info("Operação cancelada.")
    
    def _configurar_nova_api_key(self):
        """Solicita ao usuário uma nova chave de API e a configura."""
        print("Configuração de chave de API da OpenAI")
        print("A chave será salva nas variáveis de ambiente do usuário no Windows.")
        print("Isso permitirá que o Ragner use a chave automaticamente nos próximos inicializações.")
        
        api_key = input("\nPor favor, insira sua chave de API da OpenAI: ")
        
        if self.configurar_api_key_usecase.executar(api_key):
            self.presenter.exibir_mensagem_sucesso("Chave de API configurada com sucesso!")
            self.presenter.exibir_mensagem_info("A chave foi salva nas variáveis de ambiente do usuário e estará disponível em futuros inicializações do programa.")
        else:
            self.presenter.exibir_mensagem_erro("Falha ao configurar a chave de API. Verifique se a chave está correta.")
            self.presenter.exibir_mensagem_info("Acesse https://platform.openai.com/api-keys para obter uma chave válida.")
    
    def _reconstruir_indice_faiss(self):
        """
        Reconstrói o índice FAISS a partir dos documentos existentes no banco de dados.
        Esta função é útil para resolver problemas de sincronização entre o índice e o banco.
        """
        self.presenter.exibir_mensagem_info("Iniciando reconstrução do índice FAISS...")
        try:
            vector_store = self.indexar_documentos_usecase.vector_store
            db_gateway = self.indexar_documentos_usecase.db_gateway
            
            # Verificar se há embeddings armazenados no banco de dados
            conn = db_gateway.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as total FROM Chunks WHERE chunk_embedding IS NOT NULL')
            total_chunks_com_embedding = cursor.fetchone()['total']
            
            # Usa o método melhorado para reconstruir o índice
            self.presenter.exibir_mensagem_info(f"Reconstruindo índice com {total_chunks_com_embedding} chunks do banco de dados...")
            resultado = vector_store.reiniciar_indice_com_documentos_existentes(db_gateway)
            
            if resultado:
                self.presenter.exibir_mensagem_sucesso("Índice FAISS reconstruído com sucesso!")
                
                # Exibe as estatísticas do índice reconstruído
                estatisticas = vector_store.obter_estatisticas()
                self.presenter.exibir_mensagem_info(f"Vetores no índice: {estatisticas['vetores']}")
                self.presenter.exibir_mensagem_info(f"Dimensão dos vetores: {estatisticas['dimensao']}")
            else:
                self.presenter.exibir_mensagem_erro("Falha ao reconstruir o índice FAISS.")
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.presenter.exibir_mensagem_erro(f"Erro ao reconstruir o índice FAISS: {str(e)}")