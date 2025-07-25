#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caso de uso: Indexar documentos.
"""

import os
import glob
import time
import xxhash
import uuid
import json
from typing import Optional

from domain.Documento import Documento
from domain.Chunk import Chunk
from domain.Embedding import Embedding
from domain.DadosRaw import DadosRaw
from domain.Log import Logger
from domain.repositories.ChunkRepository import ChunkRepository
from infrastructure.file_loaders.pdf_loader import PDFLoader
from infrastructure.file_loaders.docx_loader import DOCXLoader
from infrastructure.file_loaders.txt_loader import TXTLoader
from infrastructure.utils.progress_bar import ProgressBar
from presentation.cli.cli_cores import Cores

class IndexarDocumentosUseCase:
    """
    Caso de uso para indexar documentos.
    
    Esta classe é responsável por encontrar documentos, processar seu conteúdo,
    gerar embeddings e armazenar os chunks e embeddings no banco de dados e no FAISS.
    """
    
    def __init__(self, db_gateway, vector_store, language_model, chunk_repository: ChunkRepository, logger: Optional[Logger] = None):
        """
        Inicializa o caso de uso.
        
        Args:
            db_gateway: Gateway para o banco de dados
            vector_store: Armazenamento de vetores
            language_model: Gateway para o modelo de linguagem
            chunk_repository: Repositório de chunks
            logger: Interface para logging (opcional)
        """
        self.db_gateway = db_gateway
        self.vector_store = vector_store
        self.language_model = language_model
        self.chunk_repository = chunk_repository
        self.logger = logger
        
        # Inicializa os loaders de arquivos, injetando o logger
        self.loaders = {
            'pdf': PDFLoader(logger=self.logger),
            'docx': DOCXLoader(logger=self.logger),
            'txt': TXTLoader(logger=self.logger)
        }
    
    def verificar_sincronizacao_faiss(self):
        """
        Verifica se o índice FAISS está sincronizado com o banco de dados.
        Se não estiver, reconstrói o índice apenas com os documentos existentes.
        
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        try:
            if self.logger:
                self.logger.registrar_info("Verificando sincronização do índice FAISS com o banco de dados...")
            
            # Obter estatísticas do índice FAISS
            estatisticas = self.vector_store.obter_estatisticas()
            
            # Obter contagem de chunks com embeddings no banco de dados
            conn = self.db_gateway.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as total FROM Chunks WHERE chunk_embedding IS NOT NULL')
            row = cursor.fetchone()
            total_chunks_bd = row['total'] if row else 0
            
            if self.logger:
                self.logger.registrar_info(f"Total de embeddings no índice FAISS: {estatisticas['vetores']}")
                self.logger.registrar_info(f"Total de chunks com embeddings no banco de dados: {total_chunks_bd}")
            
            # Se o número de vetores não corresponder, reconstruir o índice
            if estatisticas['vetores'] != total_chunks_bd:
                if self.logger:
                    self.logger.registrar_info("Índice FAISS não está sincronizado com o banco de dados.")
                    self.logger.registrar_info("Reconstruindo índice FAISS com base nos documentos existentes...")
                
                # Reconstruir o índice apenas com os documentos existentes
                resultado = self.vector_store.reiniciar_indice_com_documentos_existentes(self.db_gateway)
                
                if resultado:
                    if self.logger:
                        self.logger.registrar_info("Índice FAISS reconstruído com sucesso.")
                else:
                    if self.logger:
                        self.logger.registrar_erro("Erro ao reconstruir o índice FAISS.")
                return resultado
            else:
                if self.logger:
                    self.logger.registrar_info("Índice FAISS está sincronizado com o banco de dados.")
                return True
                
        except Exception as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro ao verificar sincronização do índice FAISS: {str(e)}")
            return False
    
    def indexar_pasta(self, pasta_documentos):
        """
        Indexa todos os documentos em uma pasta.
        
        Args:
            pasta_documentos: Caminho para a pasta de documentos
            
        Returns:
            tuple: (Número de documentos indexados, Número de chunks processados)
        """
        # Primeiro, verificamos se o índice FAISS está sincronizado
        self.verificar_sincronizacao_faiss()
        
        if not os.path.exists(pasta_documentos):
            os.makedirs(pasta_documentos)
            if self.logger:
                self.logger.registrar_info(f"Pasta de documentos criada: {pasta_documentos}")
            return 0, 0
        
        # Coletar todos os arquivos primeiro
        todos_arquivos = []
        todos_arquivos.extend(glob.glob(os.path.join(pasta_documentos, "**/*.pdf"), recursive=True))
        todos_arquivos.extend(glob.glob(os.path.join(pasta_documentos, "**/*.docx"), recursive=True))
        todos_arquivos.extend(glob.glob(os.path.join(pasta_documentos, "**/*.txt"), recursive=True))
        
        if not todos_arquivos:
            if self.logger:
                self.logger.registrar_info("Nenhum documento encontrado para indexar.")
            return 0, 0
        
        total_documentos = 0
        total_chunks = 0
        
        # Criar barra de progresso para múltiplos arquivos (SEMPRE mostrar)
        progress_arquivos = None
        if len(todos_arquivos) >= 1:  # Mostrar para qualquer quantidade de arquivos
            if self.logger:
                self.logger.registrar_info(f"Encontrados {len(todos_arquivos)} documentos para processar...")
            
            print(f"{Cores.CINZA}Indexando {len(todos_arquivos)} documentos...{Cores.RESET}")
            progress_arquivos = ProgressBar(
                total=len(todos_arquivos),
                prefixo="Documentos"
            )
        
        # Processar cada arquivo
        for i, arquivo in enumerate(todos_arquivos):
            if progress_arquivos:
                nome_arquivo = os.path.basename(arquivo)
                progress_arquivos.atualizar(i + 1)
            
            n_docs, n_chunks = self.indexar_documento(arquivo)
            total_documentos += n_docs
            total_chunks += n_chunks
        
        # Finalizar barra de progresso dos arquivos
        if progress_arquivos:
            progress_arquivos.finalizar(f"Indexação concluída: {total_documentos} documentos, {total_chunks} chunks")
        
        if self.logger:
            self.logger.registrar_info(f"Total de documentos indexados: {total_documentos}")
            self.logger.registrar_info(f"Total de chunks processados: {total_chunks}")
        
        return total_documentos, total_chunks
    
    def indexar_documento(self, caminho_arquivo):
        """
        Indexa um único documento.
        
        Args:
            caminho_arquivo: Caminho para o arquivo do documento
            
        Returns:
            tuple: (1 se o documento foi indexado, Número de chunks processados)
        """
        try:
            tipo = os.path.splitext(caminho_arquivo)[1].lower().replace('.', '')
            
            if tipo not in self.loaders:
                if self.logger:
                    self.logger.registrar_erro(f"Tipo de arquivo não suportado: {tipo}")    
                return 0, 0

            # Calcular o hash do arquivo usando xxhash (mais eficiente)
            with open(caminho_arquivo, 'rb') as f:
                conteudo_binario = f.read()
                hash_arquivo = xxhash.xxh64(conteudo_binario).hexdigest()
            
            # Verificar se o arquivo já existe no banco de dados
            nome_arquivo = os.path.basename(caminho_arquivo)
            arquivos_existentes = self.db_gateway.listar_arquivos_db()
            
            for arquivo_existente in arquivos_existentes:
                if arquivo_existente['arquivo_nome'] == nome_arquivo:
                    # Arquivo já existe, verificar se foi modificado
                    if arquivo_existente['arquivo_hash'] == hash_arquivo:
                        if self.logger:
                            self.logger.registrar_info(f"Arquivo {nome_arquivo} não foi modificado, pulando...")
                        return 0, 0
                    else:
                        if self.logger:
                            self.logger.registrar_info(f"Arquivo {nome_arquivo} foi modificado, removendo versão antiga...")
                        # Remover a versão antiga
                        chunks_removidos = self.chunk_repository.apagar_chunks_por_arquivo(arquivo_existente['arquivo_uuid'])
                        self.db_gateway.apagar_dados_raw_por_arquivo_db(arquivo_existente['arquivo_uuid'])
                        self.db_gateway.apagar_arquivo_db(arquivo_existente['arquivo_uuid'])
                        if self.logger:
                            self.logger.registrar_info(f"Versão antiga removida ({chunks_removidos} chunks)")
                        break
            
            # 5.1) Adicionar informações do arquivo na tabela "Arquivos"
            # Criar um novo documento com os dados do arquivo
            arquivo_uuid = str(uuid.uuid4())
            data_modificacao = os.path.getmtime(caminho_arquivo)
            tamanho_bytes = os.path.getsize(caminho_arquivo)
            
            # Criar um objeto Documento com os novos campos
            documento = Documento(
                arquivo_uuid=arquivo_uuid,
                arquivo_nome=nome_arquivo,
                arquivo_caminho=caminho_arquivo,
                arquivo_tipo=tipo,
                data_modificacao=data_modificacao,
                tamanho_bytes=tamanho_bytes,
                arquivo_hash=hash_arquivo
            )
            
            # Salvar o documento no banco de dados
            self.db_gateway.criar_arquivo_db(
                arquivo_uuid=documento.arquivo_uuid,
                arquivo_caminho=documento.arquivo_caminho,
                arquivo_nome=documento.arquivo_nome,
                data_modificacao=documento.data_modificacao,
                tamanho_bytes=documento.tamanho_bytes,
                arquivo_tipo=documento.arquivo_tipo,
                arquivo_hash=documento.arquivo_hash,
                data_indexacao=time.time()
            )
            
            # 5.2) Extrair o conteúdo de texto do arquivo
            conteudo_texto = ""
            
            # Para arquivos de texto, podemos ler diretamente
            if tipo == "txt":
                with open(caminho_arquivo, 'r', encoding='utf-8', errors='ignore') as f:
                    conteudo_texto = f.read()
            else:
                # Para outros tipos de arquivo (PDF, DOCX), usamos o loader para extrair o texto
                try:
                    chunks_texto = self.loaders[tipo].carregar(caminho_arquivo)
                    
                    # Verificar o que foi retornado pelo loader
                    if isinstance(chunks_texto, list):
                        conteudo_texto = "\n\n".join(chunks_texto)
                    else:
                        if hasattr(chunks_texto, 'chunks'):
                            conteudo_texto = "\n\n".join([chunk.chunk_texto for chunk in chunks_texto.chunks])
                        else:
                            conteudo_texto = str(chunks_texto)
                except Exception as e:
                    import traceback
                    if self.logger:
                        self.logger.registrar_erro(f"Erro ao extrair texto de {caminho_arquivo}: {str(e)}")
                        self.logger.registrar_erro(traceback.format_exc())
                    raise
            
            # Preencher a tabela "dados_raw" com o conteúdo de texto extraído
            dados_raw = DadosRaw(
                raw_uuid=str(uuid.uuid4()),
                arquivo_uuid=documento.arquivo_uuid,
                raw_conteudo=conteudo_texto,
                data_armazenamento=time.time()
            )
            
            # Salvar os dados brutos no banco de dados
            self.db_gateway.criar_dados_raw_db(
                raw_uuid=dados_raw.raw_uuid,
                arquivo_uuid=dados_raw.arquivo_uuid,
                raw_conteudo=dados_raw.raw_conteudo,
                data_armazenamento=dados_raw.data_armazenamento
            )
            
            # 5.3) Processar o documento para extrair chunks
            # Carrega o documento usando o loader apropriado para processar chunks
            chunks_texto = self.loaders[tipo].carregar(caminho_arquivo)
            
            # Verificar o tipo do retorno
            if not isinstance(chunks_texto, list):
                # Tentativa de converter para lista se não for uma lista
                if hasattr(chunks_texto, 'chunks'):
                    chunks_texto = [chunk.chunk_texto for chunk in chunks_texto.chunks]
                else:
                    chunks_texto = [str(chunks_texto)]
            
            # Processar os chunks
            chunk_embeddings = []
            
            # Criar barra de progresso para chunks (SEMPRE mostrar)
            progress_chunks = None
            if len(chunks_texto) >= 1:  # Mostrar para qualquer arquivo com 1 ou mais chunks
                progress_chunks = ProgressBar(
                    total=len(chunks_texto), 
                    prefixo="Chunks"
                )
            
            for i, texto_chunk in enumerate(chunks_texto):
                
                # Atualizar barra de progresso
                if progress_chunks:
                    progress_chunks.atualizar(i + 1)
                elif len(chunks_texto) > 1:  # Para arquivos sem barra, mostrar progresso
                    if (i + 1) % 5 == 0 or i == len(chunks_texto) - 1:
                        print(f"\rProcessando chunk {i+1}/{len(chunks_texto)}...", end='', flush=True)
                
                # Criar um objeto Chunk
                chunk = Chunk(
                    chunk_uuid=str(uuid.uuid4()),
                    arquivo_uuid=documento.arquivo_uuid,
                    chunk_texto=texto_chunk,
                    chunk_numero=i,
                    chunk_tamanho_tokens=len(texto_chunk.split())  # Estimativa simplificada
                )
                
                # Salvar o chunk no banco de dados usando o repositório
                try:
                    chunk = self.chunk_repository.salvar_chunk(chunk)
                except Exception as e:
                    continue
                
                # Gerar o embedding para o chunk
                try:
                    # Verificar se o chunk tem UUID válido
                    if not chunk.chunk_uuid:
                        if self.logger:
                            self.logger.registrar_erro(f"Chunk {i} do documento {documento.arquivo_nome} não possui UUID válido")
                        continue
                        
                    vetor = self.language_model.gerar_embedding(chunk.chunk_texto)
                    embedding = Embedding(
                        id=str(uuid.uuid4()),
                        chunk_id=chunk.chunk_uuid,
                        vetor=vetor,
                        modelo=self.language_model.embedding_model
                    )
                    
                    # Atualizar o embedding do chunk usando o repositório
                    self.chunk_repository.atualizar_embedding(chunk.chunk_uuid, embedding)
                    
                    # Adicionar à lista para o vector store
                    chunk.chunk_embedding = embedding
                    chunk_embeddings.append((chunk, embedding))
                except Exception as e:
                    if self.logger:
                        self.logger.registrar_erro(f"Erro ao gerar embedding para chunk {i} do documento {documento.arquivo_nome}: {str(e)}")
                    import traceback
                    if self.logger:
                        self.logger.registrar_erro(traceback.format_exc())
            
            # Finalizar barra de progresso dos chunks (APÓS o loop)
            if progress_chunks:
                progress_chunks.finalizar(f"Chunks processados: {len(chunk_embeddings)}/{len(chunks_texto)}")
            elif len(chunks_texto) > 1:
                print(f"\n✓ Chunks processados: {len(chunk_embeddings)}/{len(chunks_texto)}")
            
            # Adicionar os embeddings ao vector store com barra de progresso
            if chunk_embeddings:
                if len(chunk_embeddings) >= 1:  # SEMPRE mostrar barra para qualquer embedding
                    progress_embeddings = ProgressBar(
                        total=len(chunk_embeddings),
                        prefixo="FAISS"
                    )
                    
                    # Simular progresso durante adição ao FAISS
                    for i in range(len(chunk_embeddings)):
                        progress_embeddings.atualizar(i + 1)
                        time.sleep(0.01)  # Pequena pausa para visualizar o progresso
                    
                    progress_embeddings.finalizar("Vetores indexados no FAISS")
                
                self.vector_store.adicionar_embeddings(chunk_embeddings)
            
            # Logs removidos para evitar duplicação no terminal
            return 1, len(chunk_embeddings)
        
        except Exception as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro ao indexar documento {caminho_arquivo}: {str(e)}")
            import traceback
            if self.logger:
                self.logger.registrar_erro(traceback.format_exc())
            return 0, 0
    
    def verificar_arquivos_deletados(self, pasta_documentos):
        """
        Verifica se algum arquivo foi deletado da pasta e remove do banco de dados.
        Não remove do FAISS neste momento, isso será feito posteriormente na verificação de sincronização.
        
        Args:
            pasta_documentos: Caminho para a pasta de documentos
            
        Returns:
            int: Número de arquivos removidos
        """
        try:
            # Listar todos os documentos no banco de dados
            arquivos = self.db_gateway.listar_arquivos_db()
            documentos = []
            
            # Converter dados de arquivos para objetos Documento
            for arquivo in arquivos:
                documento = Documento(
                    arquivo_uuid=arquivo['arquivo_uuid'],
                    arquivo_nome=arquivo['arquivo_nome'],
                    arquivo_caminho=arquivo['arquivo_caminho'],
                    arquivo_tipo=arquivo['arquivo_tipo'],
                    data_modificacao=arquivo['data_modificacao'],
                    tamanho_bytes=arquivo['tamanho_bytes'],
                    arquivo_hash=arquivo['arquivo_hash']
                )
                documentos.append(documento)
            
            # Verificar cada documento
            arquivos_removidos = 0
            arquivos_para_remover = []
            
            for documento in documentos:
                caminho_arquivo = documento.arquivo_caminho
                
                # Se o arquivo não existir mais no disco, removemos do banco de dados
                if not os.path.exists(caminho_arquivo):
                    if self.logger:
                        self.logger.registrar_info(f"Arquivo não encontrado no disco: {caminho_arquivo}")
                        self.logger.registrar_info("Removendo do banco de dados...")
                    
                    # Remover chunks associados
                    chunks_removidos = self.chunk_repository.apagar_chunks_por_arquivo(documento.arquivo_uuid)
                    
                    # Remover dados raw
                    self.db_gateway.apagar_dados_raw_por_arquivo_db(documento.arquivo_uuid)
                    
                    # Remover arquivo
                    if self.db_gateway.apagar_arquivo_db(documento.arquivo_uuid):
                        arquivos_removidos += 1
                        arquivos_para_remover.append(documento)
                        if self.logger:
                            self.logger.registrar_info(f"Arquivo removido do banco de dados: {caminho_arquivo} (e {chunks_removidos} chunks associados)")
                    else:
                        if self.logger:
                            self.logger.registrar_erro(f"Erro ao remover arquivo do banco de dados: {caminho_arquivo}")
            
            if self.logger:
                self.logger.registrar_info(f"Verificação concluída. {arquivos_removidos} arquivos removidos do banco de dados.")
            return arquivos_removidos
            
        except Exception as e:
            if self.logger:
                self.logger.registrar_erro(f"Erro ao verificar arquivos deletados: {str(e)}")
            return 0
    
    def reindexar_tudo(self, pasta_documentos):
        """
        Limpa os índices existentes e reindexifica todos os documentos.
        
        Args:
            pasta_documentos: Caminho para a pasta de documentos
            
        Returns:
            tuple: (Número de documentos indexados, Número de chunks processados)
        """
        # Apaga todos os dados do banco de dados
        self.db_gateway.apagar_tudo_db()
        
        # Reinicia o índice FAISS
        self.vector_store.reiniciar_indice()
        
        # Reindexifica todos os documentos
        return self.indexar_pasta(pasta_documentos)