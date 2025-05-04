#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FAISS Vector Store: Implementação do armazenamento de vetores usando FAISS.
"""

import os
import faiss
import numpy as np
import pickle
import json
from presentation.cli.cli_cores import Cores
from presentation.cli.cli_logger import CLILogger

# Inicializa o logger para a interface CLI
cli_logger = CLILogger()

class FaissVectorStore:
    """
    Implementação do armazenamento de vetores usando FAISS.
    
    Esta classe é responsável por criar e gerenciar o índice FAISS
    que permite buscas eficientes por similaridade semântica.
    """
    
    def __init__(self, index_dir=None):
        """
        Inicializa o armazenamento de vetores FAISS.
        
        Args:
            index_dir: Diretório onde o índice FAISS será salvo
        """
        if index_dir is None:
            # Define o diretório do índice no mesmo diretório do script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Volta dois níveis para chegar ao diretório raiz do projeto
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
            index_dir = os.path.join(project_root, 'faiss_index')
        
        self.index_dir = index_dir
        self.index_path = os.path.join(self.index_dir, 'faiss_index.bin')
        self.mapping_path = os.path.join(self.index_dir, 'id_mapping.pkl')
        self.index = None
        self.id_to_index = {}  # Mapeamento de ID do chunk para índice
        self.index_to_id = {}  # Mapeamento de índice para ID do chunk
        self.index_dimension = 0
        self._initialized = False
        
        # Certifica-se de que o diretório do índice existe
        os.makedirs(self.index_dir, exist_ok=True)
        
        # Não carrega o índice no construtor
        # self.carregar_ou_criar_indice()
    
    def inicializar_indice(self, dimension=1536):
        """
        Método explícito para inicializar o índice FAISS.
        Este método deve ser chamado manualmente quando quisermos inicializar o índice.
        
        Args:
            dimension: Dimensão dos vetores para um novo índice
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        try:
            if os.path.exists(self.index_path) and os.path.exists(self.mapping_path):
                # Carrega o índice existente
                self.carregar_ou_criar_indice(dimension)
            else:
                # Cria um novo índice e o salva imediatamente em disco
                self.index_dimension = dimension
                self.index = faiss.IndexFlatL2(dimension)
                self.id_to_index = {}
                self.index_to_id = {}
                cli_logger.registrar_info(f"{Cores.CINZA}Novo índice FAISS criado com dimensão {dimension}{Cores.RESET}")
                
                # Importante: Salva o índice vazio em disco para persistência
                self.salvar_indice()
                
            self._initialized = True
            return True
        except Exception as e:
            cli_logger.registrar_info(f"Erro ao inicializar índice FAISS: {str(e)}")
            return False
    
    def carregar_ou_criar_indice(self, dimension=1536):
        """
        Carrega um índice existente ou cria um novo.
        
        Args:
            dimension: Dimensão dos vetores para um novo índice (padrão: 1536 para text-embedding-3-small)
        """
        try:
            if os.path.exists(self.index_path) and os.path.exists(self.mapping_path):
                # Carregando o índice existente
                self.index = faiss.read_index(self.index_path)
                with open(self.mapping_path, 'rb') as f:
                    mappings = pickle.load(f)
                    self.id_to_index = mappings.get('id_to_index', {})
                    self.index_to_id = mappings.get('index_to_id', {})
                    
                self.index_dimension = self.index.d
                cli_logger.registrar_info(f"{Cores.CINZA}Índice FAISS carregado com sucesso. Dimensão: {self.index_dimension}, Número de vetores: {self.index.ntotal}{Cores.RESET}")
            else:
                # Cria um novo índice
                self.index_dimension = dimension
                self.index = faiss.IndexFlatL2(dimension)
                self.id_to_index = {}
                self.index_to_id = {}
                cli_logger.registrar_info(f"{Cores.CINZA}Novo índice FAISS criado com dimensão {dimension}{Cores.RESET}")
        except Exception as e:
            cli_logger.registrar_info(f"Erro ao carregar o índice FAISS: {str(e)}")
            import traceback
            traceback.print_exc()
            cli_logger.registrar_info(f"{Cores.CINZA}Criando um novo índice...{Cores.RESET}")
            self.index_dimension = dimension
            self.index = faiss.IndexFlatL2(dimension)
            self.id_to_index = {}
            self.index_to_id = {}
    
    def _ensure_initialized(self, dimension=1536):
        """
        Garante que o índice está inicializado antes de usá-lo.
        Para uso interno nos métodos da classe.
        
        Args:
            dimension: Dimensão dos vetores para um novo índice
        """
        if not self._initialized:
            self.carregar_ou_criar_indice(dimension)
            self._initialized = True
    
    def adicionar_embeddings(self, chunk_embeddings):
        """
        Adiciona embeddings ao índice FAISS.
        
        Args:
            chunk_embeddings: Lista de tuplas (chunk, embedding)
            
        Returns:
            bool: True se os embeddings foram adicionados com sucesso
        """
        if not chunk_embeddings:
            cli_logger.registrar_info(f"{Cores.CINZA}Nenhum embedding para adicionar.{Cores.RESET}")
            return False
        
        # Verifica a dimensionalidade do primeiro embedding
        first_dim = len(chunk_embeddings[0][1].vetor)
        
        # Garante que o índice está inicializado
        self._ensure_initialized(first_dim)
        
        # Verifica se a dimensão do embedding coincide com a dimensão do índice
        if first_dim != self.index_dimension:
            raise ValueError(f"Dimensão do embedding ({first_dim}) não coincide com a dimensão do índice ({self.index_dimension})")
        
        embeddings_to_add = []
        chunks_to_add = []
        
        # Primeiro, vamos coletar os chunks e embeddings que não estão no índice
        for chunk, embedding in chunk_embeddings:
            # Pula se o chunk já está no índice
            if chunk.chunk_uuid in self.id_to_index:
                continue
            
            embeddings_to_add.append(embedding.vetor)
            chunks_to_add.append(chunk)
        
        if not embeddings_to_add:
            cli_logger.registrar_info(f"{Cores.CINZA}Todos os embeddings já estão no índice.{Cores.RESET}")
            return True
        
        try:
            # Converte para array numpy
            embeddings_array = np.array(embeddings_to_add, dtype=np.float32)
            
            # Guarda o índice inicial (total de vetores no índice)
            start_idx = self.index.ntotal
            
            # Adiciona os embeddings ao índice
            self.index.add(embeddings_array)
            
            # Cria os mapeamentos para todos os novos vetores
            for i, chunk in enumerate(chunks_to_add):
                # O índice real é o índice inicial mais o deslocamento atual
                idx = start_idx + i
                
                # Salva os mapeamentos em ambas as direções
                self.id_to_index[chunk.chunk_uuid] = idx
                self.index_to_id[idx] = chunk.chunk_uuid
            
            # Salva o índice e os mapeamentos
            self.salvar_indice()
            
            cli_logger.registrar_info(f"{Cores.CINZA}Adicionados {len(embeddings_to_add)} embeddings ao índice. Total: {self.index.ntotal}{Cores.RESET}")
            return True
        
        except Exception as e:
            cli_logger.registrar_info(f"Erro ao adicionar embeddings ao índice: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def buscar_chunks_similares(self, query_embedding, k=5):
        """
        Busca os chunks mais similares a um embedding de consulta.
        
        Args:
            query_embedding: Embedding da consulta
            k: Número de resultados a retornar
            
        Returns:
            tuple: (IDs dos chunks, scores de similaridade)
        """
        if self.index is None or self.index.ntotal == 0:
            cli_logger.registrar_info(f"{Cores.CINZA}Índice FAISS vazio ou não inicializado.{Cores.RESET}")
            return [], []
        
        # Verifica se a dimensão do embedding coincide com a dimensão do índice
        if len(query_embedding) != self.index_dimension:
            raise ValueError(f"Dimensão do embedding de consulta ({len(query_embedding)}) não coincide com a dimensão do índice ({self.index_dimension})")
        
        # Converte para array numpy
        query_array = np.array([query_embedding], dtype=np.float32)
        
        try:
            # Busca os k vizinhos mais próximos
            scores, indices = self.index.search(query_array, k)
            
            # Converte índices FAISS para IDs de chunks
            chunk_ids = []
            for idx in indices[0]:
                if idx != -1 and idx in self.index_to_id:
                    chunk_id = self.index_to_id[idx]
                    chunk_ids.append(chunk_id)
            
            return chunk_ids, scores[0]
        except Exception as e:
            cli_logger.registrar_info(f"Erro durante a busca: {str(e)}")
            import traceback
            traceback.print_exc()
            return [], []
    
    def salvar_indice(self):
        """Salva o índice FAISS e os mapeamentos em disco."""
        try:
            # Salva o índice
            faiss.write_index(self.index, self.index_path)
            
            # Salva os mapeamentos
            with open(self.mapping_path, 'wb') as f:
                pickle.dump({
                    'id_to_index': self.id_to_index,
                    'index_to_id': self.index_to_id
                }, f)
            
            cli_logger.registrar_info(f"{Cores.CINZA}Índice FAISS salvo em {self.index_path}{Cores.RESET}")
            return True
        except Exception as e:
            cli_logger.registrar_info(f"Erro ao salvar o índice FAISS: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def reiniciar_indice(self, dimension=1536):
        """
        Remove o índice existente e cria um novo.
        
        Args:
            dimension: Dimensão dos vetores para o novo índice
        """
        # Remove os arquivos existentes
        if os.path.exists(self.index_path):
            os.remove(self.index_path)
        if os.path.exists(self.mapping_path):
            os.remove(self.mapping_path)
        
        # Cria um novo índice
        self.index_dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.id_to_index = {}
        self.index_to_id = {}
        
        cli_logger.registrar_info(f"{Cores.CINZA}Índice FAISS reiniciado com dimensão {dimension}{Cores.RESET}")
        return True
    
    def reiniciar_indice_com_documentos_existentes(self, db_gateway):
        """
        Remove e reconstrói o índice FAISS apenas com os documentos que ainda existem no banco de dados.
        Isso é útil após a remoção de documentos para garantir que os vetores removidos não permaneçam no índice.
        
        Args:
            db_gateway: Gateway para o banco de dados para acessar chunks e embeddings
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        try:
            # Reinicia o índice com a mesma dimensão que já temos
            dimensao = self.index_dimension
            self.reiniciar_indice(dimensao)
            
            # Busca todos os chunks com embeddings do banco de dados
            conn = db_gateway.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT c.chunk_uuid, c.chunk_texto, c.chunk_embedding FROM Chunks c WHERE c.chunk_embedding IS NOT NULL')
            chunks_embeddings = cursor.fetchall()
            
            # Se não houver chunks com embeddings, o trabalho está concluído
            if not chunks_embeddings:
                cli_logger.registrar_info(f"Nenhum embedding encontrado no banco de dados. Índice FAISS vazio criado.")
                return True
            
            # Lista para armazenar todos os vetores e mapeamentos
            vetores = []
            chunk_ids = []
            
            # Processa cada chunk
            for i, row in enumerate(chunks_embeddings):
                chunk_uuid = row['chunk_uuid']
                embedding_str = row['chunk_embedding']
                
                # Desserializa o embedding (convertendo de string JSON para vetor numpy)
                try:
                    if embedding_str:
                        vetor = np.array(json.loads(embedding_str), dtype=np.float32)
                        if len(vetor) == dimensao:  # Garante que a dimensão corresponda
                            vetores.append(vetor)
                            chunk_ids.append(chunk_uuid)
                        else:
                            cli_logger.registrar_info(f"Dimensão incorreta para chunk {chunk_uuid}: esperado {dimensao}, encontrado {len(vetor)}")
                except Exception as e:
                    cli_logger.registrar_info(f"Erro ao desserializar embedding para chunk {chunk_uuid}: {str(e)}")
            
            if not vetores:
                cli_logger.registrar_info("Nenhum embedding válido encontrado para adicionar ao índice.")
                return True
                
            # Converte a lista de vetores para um array numpy
            embeddings_array = np.array(vetores, dtype=np.float32)
            
            # Limpa os mapeamentos existentes
            self.id_to_index = {}
            self.index_to_id = {}
            
            # Adiciona os embeddings ao índice
            self.index.add(embeddings_array)
            
            # Cria novos mapeamentos
            for i, chunk_id in enumerate(chunk_ids):
                self.id_to_index[chunk_id] = i
                self.index_to_id[i] = chunk_id
            
            # Salva o índice e os mapeamentos
            self.salvar_indice()
            
            cli_logger.registrar_info(f"{Cores.CINZA}Índice FAISS reconstruído com {len(vetores)} embeddings dos documentos existentes.{Cores.RESET}")
            return True
            
        except Exception as e:
            cli_logger.registrar_info(f"Erro ao reconstruir o índice FAISS: {str(e)}")
            import traceback
            traceback.print_exc()
            # Em caso de erro, cria um índice vazio para não deixar o sistema inconsistente
            self.reiniciar_indice(self.index_dimension)
            return False
    
    def obter_estatisticas(self):
        """
        Obtém estatísticas do índice FAISS.
        
        Returns:
            dict: Estatísticas do índice
        """
        if self.index is None:
            return {
                "inicializado": False,
                "vetores": 0,
                "dimensao": 0
            }
        
        return {
            "inicializado": True,
            "vetores": self.index.ntotal,
            "dimensao": self.index_dimension
        }
    
    def remover_chunks_por_arquivo(self, arquivo_uuid, db_gateway):
        """
        Remove todos os vectors/embeddings associados a um arquivo específico.
        
        Args:
            arquivo_uuid: UUID do arquivo cujos chunks devem ser removidos
            db_gateway: Gateway para o banco de dados para consultar chunks
            
        Returns:
            bool: True se a operação foi bem-sucedida
        """
        try:
            # Obtém todos os chunks associados ao arquivo
            conn = db_gateway.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT chunk_uuid FROM Chunks WHERE arquivo_uuid = ?', (arquivo_uuid,))
            chunk_uuids = [row['chunk_uuid'] for row in cursor.fetchall()]
            
            if not chunk_uuids:
                cli_logger.registrar_info(f"Nenhum chunk encontrado para o arquivo {arquivo_uuid}")
                return True
            
            # Lista para rastrear quais índices devem ser removidos
            indices_para_remover = []
            chunk_ids_para_remover = []
            
            # Identifica os índices FAISS correspondentes aos chunks
            for chunk_uuid in chunk_uuids:
                if chunk_uuid in self.id_to_index:
                    indices_para_remover.append(self.id_to_index[chunk_uuid])
                    chunk_ids_para_remover.append(chunk_uuid)
            
            if not indices_para_remover:
                cli_logger.registrar_info(f"Nenhum embedding encontrado no índice FAISS para os chunks do arquivo {arquivo_uuid}")
                return True
            
            cli_logger.registrar_info(f"Removendo {len(indices_para_remover)} embeddings do índice FAISS para o arquivo {arquivo_uuid}")
            
            # Como o FAISS não permite remover vetores diretamente, precisamos reconstruir o índice
            # Vamos reconstruir o índice sem os vetores do arquivo excluído
            dimensao = self.index_dimension
            old_index = self.index
            old_ntotal = old_index.ntotal
            
            # Criamos um novo índice com a mesma dimensão
            novo_index = faiss.IndexFlatL2(dimensao)
            
            # Atualiza os mapeamentos
            novo_id_to_index = {}
            novo_index_to_id = {}
            
            # Copia todos os vetores, exceto os que devem ser removidos
            if old_ntotal > 0:
                # Extraímos todos os vetores do índice antigo
                all_vectors = faiss.vector_to_array(old_index.index_data()).reshape(-1, dimensao)
                
                # Adicionamos de volta apenas os vetores que queremos manter
                vetores_para_manter = []
                chunk_ids_para_manter = []
                
                novo_idx = 0
                for idx in range(old_ntotal):
                    if idx in self.index_to_id and idx not in indices_para_remover:
                        chunk_id = self.index_to_id[idx]
                        vetores_para_manter.append(all_vectors[idx])
                        chunk_ids_para_manter.append(chunk_id)
                        
                        novo_id_to_index[chunk_id] = novo_idx
                        novo_index_to_id[novo_idx] = chunk_id
                        novo_idx += 1
                
                if vetores_para_manter:
                    vetores_array = np.array(vetores_para_manter, dtype=np.float32)
                    novo_index.add(vetores_array)
            
            # Atualiza o índice e os mapeamentos
            self.index = novo_index
            self.id_to_index = novo_id_to_index
            self.index_to_id = novo_index_to_id
            
            # Salva o novo índice em disco
            self.salvar_indice()
            
            cli_logger.registrar_info(f"Índice FAISS reconstruído com sucesso. Removidos {len(indices_para_remover)} embeddings.")
            return True
            
        except Exception as e:
            cli_logger.registrar_info(f"Erro ao remover embeddings do arquivo {arquivo_uuid}: {str(e)}")
            return False