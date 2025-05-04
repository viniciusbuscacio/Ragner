#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caso de uso: Indexar documentos.
"""

import os
import glob
import time
import hashlib
import uuid
import json

from domain.Documento import Documento
from domain.Chunk import Chunk
from domain.Embedding import Embedding
from domain.DadosRaw import DadosRaw
from domain.repositories.ChunkRepository import ChunkRepository
from infrastructure.file_loaders.pdf_loader import PDFLoader
from infrastructure.file_loaders.docx_loader import DocxLoader
from infrastructure.file_loaders.txt_loader import TxtLoader
from presentation.cli.cli_cores import Cores

class IndexarDocumentosUseCase:
    """
    Caso de uso para indexar documentos.
    
    Esta classe é responsável por encontrar documentos, processar seu conteúdo,
    gerar embeddings e armazenar os chunks e embeddings no banco de dados e no FAISS.
    """
    
    def __init__(self, db_gateway, vector_store, language_model, chunk_repository: ChunkRepository):
        """
        Inicializa o caso de uso.
        
        Args:
            db_gateway: Gateway para o banco de dados
            vector_store: Armazenamento de vetores
            language_model: Gateway para o modelo de linguagem
            chunk_repository: Repositório de chunks
        """
        self.db_gateway = db_gateway
        self.vector_store = vector_store
        self.language_model = language_model
        self.chunk_repository = chunk_repository
        
        # Inicializa os loaders de arquivos
        self.loaders = {
            'pdf': PDFLoader(),
            'docx': DocxLoader(),
            'txt': TxtLoader()
        }
    
    def verificar_sincronizacao_faiss(self):
        """
        Verifica se o índice FAISS está sincronizado com o banco de dados.
        Se não estiver, reconstrói o índice apenas com os documentos existentes.
        
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        try:
            print(f"{Cores.CINZA}Verificando sincronização do índice FAISS com o banco de dados...{Cores.RESET}")
            
            # Obter estatísticas do índice FAISS
            estatisticas = self.vector_store.obter_estatisticas()
            
            # Obter contagem de chunks com embeddings no banco de dados
            conn = self.db_gateway.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as total FROM Chunks WHERE chunk_embedding IS NOT NULL')
            row = cursor.fetchone()
            total_chunks_bd = row['total'] if row else 0
            
            print(f"{Cores.CINZA}Total de embeddings no índice FAISS: {estatisticas['vetores']}{Cores.RESET}")
            print(f"{Cores.CINZA}Total de chunks com embeddings no banco de dados: {total_chunks_bd}{Cores.RESET}")
            
            # Se o número de vetores não corresponder, reconstruir o índice
            if estatisticas['vetores'] != total_chunks_bd:
                print(f"{Cores.CINZA}Índice FAISS não está sincronizado com o banco de dados.{Cores.RESET}")
                print(f"{Cores.CINZA}Reconstruindo índice FAISS com base nos documentos existentes...{Cores.RESET}")
                
                # Reconstruir o índice apenas com os documentos existentes
                resultado = self.vector_store.reiniciar_indice_com_documentos_existentes(self.db_gateway)
                
                if resultado:
                    print(f"{Cores.CINZA}Índice FAISS reconstruído com sucesso.{Cores.RESET}")
                else:
                    print(f"{Cores.VERMELHO}Erro ao reconstruir o índice FAISS.{Cores.RESET}")
                return resultado
            else:
                print(f"{Cores.CINZA}Índice FAISS está sincronizado com o banco de dados.{Cores.RESET}")
                return True
                
        except Exception as e:
            print(f"{Cores.VERMELHO}Erro ao verificar sincronização do índice FAISS: {str(e)}{Cores.RESET}")
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
            print(f"{Cores.CINZA}Pasta de documentos criada: {pasta_documentos}{Cores.RESET}")
            return 0, 0
        
        total_documentos = 0
        total_chunks = 0
        
        # Processa documentos PDF
        for arquivo in glob.glob(os.path.join(pasta_documentos, "**/*.pdf"), recursive=True):
            n_docs, n_chunks = self.indexar_documento(arquivo)
            total_documentos += n_docs
            total_chunks += n_chunks
        
        # Processa documentos DOCX
        for arquivo in glob.glob(os.path.join(pasta_documentos, "**/*.docx"), recursive=True):
            n_docs, n_chunks = self.indexar_documento(arquivo)
            total_documentos += n_docs
            total_chunks += n_chunks
        
        # Processa documentos TXT
        for arquivo in glob.glob(os.path.join(pasta_documentos, "**/*.txt"), recursive=True):
            n_docs, n_chunks = self.indexar_documento(arquivo)
            total_documentos += n_docs
            total_chunks += n_chunks
        
        print(f"{Cores.CINZA}Total de documentos indexados: {total_documentos}{Cores.RESET}")
        print(f"{Cores.CINZA}Total de chunks processados: {total_chunks}{Cores.RESET}")
        
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
                print(f"{Cores.VERMELHO}Tipo de arquivo não suportado: {tipo}{Cores.RESET}")    
                return 0, 0
            
            print(f"{Cores.CINZA}Processando documento: {caminho_arquivo}{Cores.RESET}")
            
            # 5.1) Adicionar informações do arquivo na tabela "Arquivos"
            # Criar um novo documento com os dados do arquivo
            nome_arquivo = os.path.basename(caminho_arquivo)
            arquivo_uuid = str(uuid.uuid4())
            data_modificacao = os.path.getmtime(caminho_arquivo)
            tamanho_bytes = os.path.getsize(caminho_arquivo)
            
            # Calcular o hash do arquivo
            with open(caminho_arquivo, 'rb') as f:
                conteudo_binario = f.read()
                hash_arquivo = hashlib.sha256(conteudo_binario).hexdigest()
            
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
                    print(traceback.format_exc())
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
            
            print(f"{Cores.CINZA}Conteúdo de texto de '{documento.arquivo_nome}' adicionado à tabela 'dados_raw'.{Cores.RESET}")
            
            # 5.3) Processar o documento para extrair chunks
            print(f"{Cores.CINZA}Iniciando o processamento de '{documento.arquivo_nome}' para gerar chunks...{Cores.RESET}")
            
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
            for i, texto_chunk in enumerate(chunks_texto):
                
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
                    print(f"{Cores.VERMELHO}Erro ao gerar embedding para chunk {i} do documento {documento.arquivo_nome}: {str(e)}{Cores.RESET}")
                    import traceback
                    print(traceback.format_exc())
            
            # Adicionar os embeddings ao vector store
            if chunk_embeddings:
                self.vector_store.adicionar_embeddings(chunk_embeddings)
            
            print(f"{Cores.CINZA}{tipo.upper()} carregado: {documento.arquivo_nome}, {len(chunk_embeddings)} chunks criados{Cores.RESET}")
            print(f"{Cores.CINZA}Documento indexado: {documento.arquivo_nome}, {len(chunk_embeddings)} chunks{Cores.RESET}")
            
            return 1, len(chunk_embeddings)
        
        except Exception as e:
            print(f"{Cores.VERMELHO}Erro ao indexar documento {caminho_arquivo}: {str(e)}{Cores.RESET}")
            import traceback
            print(traceback.format_exc())
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
            print(f"{Cores.CINZA}Verificando arquivos deletados...{Cores.RESET}")
            
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
                    print(f"{Cores.AMARELO}Arquivo não encontrado no disco: {caminho_arquivo}{Cores.RESET}")
                    print(f"{Cores.AMARELO}Removendo do banco de dados...{Cores.RESET}")
                    
                    # Remover chunks associados
                    chunks_removidos = self.chunk_repository.apagar_chunks_por_arquivo(documento.arquivo_uuid)
                    
                    # Remover dados raw
                    self.db_gateway.apagar_dados_raw_por_arquivo_db(documento.arquivo_uuid)
                    
                    # Remover arquivo
                    if self.db_gateway.apagar_arquivo_db(documento.arquivo_uuid):
                        arquivos_removidos += 1
                        arquivos_para_remover.append(documento)
                        print(f"{Cores.VERDE}Arquivo removido do banco de dados: {caminho_arquivo} (e {chunks_removidos} chunks associados){Cores.RESET}")
                    else:
                        print(f"{Cores.VERMELHO}Erro ao remover arquivo do banco de dados: {caminho_arquivo}{Cores.RESET}")
            
            print(f"{Cores.CINZA}Verificação concluída. {arquivos_removidos} arquivos removidos do banco de dados.{Cores.RESET}")
            return arquivos_removidos
            
        except Exception as e:
            print(f"{Cores.VERMELHO}Erro ao verificar arquivos deletados: {str(e)}{Cores.RESET}")
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