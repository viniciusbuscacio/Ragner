#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Caso de uso: Buscar contexto relevante para uma pergunta.
"""

from domain.Documento import Documento
from domain.Chunk import Chunk

class BuscarContextoUseCase:
    """
    Caso de uso para buscar contexto relevante para uma pergunta.
    
    Esta classe é responsável por encontrar os chunks mais relevantes
    semanticamente para uma pergunta do usuário.
    """
    
    def __init__(self, vector_store, db_gateway):
        """
        Inicializa o caso de uso.
        
        Args:
            vector_store: Armazenamento de vetores
            db_gateway: Gateway para o banco de dados
        """
        self.vector_store = vector_store
        self.db_gateway = db_gateway
        self.max_chunks = 5  # Número máximo de chunks a retornar
    
    def executar(self, pergunta_embedding, top_k=None, limite_similaridade=1.2):
        """
        Busca os chunks mais relevantes para uma pergunta.
        
        Args:
            pergunta_embedding: Embedding da pergunta
            top_k: Número de resultados a retornar (opcional)
            limite_similaridade: Limite máximo para considerar um chunk relevante (menor = mais similar)
            
        Returns:
            list: Lista de chunks relevantes
        """
        if top_k is None:
            top_k = self.max_chunks
        
        # Busca os IDs dos chunks mais similares
        try:
            chunk_ids, scores = self.vector_store.buscar_chunks_similares(pergunta_embedding, top_k)
            
            # Busca os chunks completos do banco de dados
            chunks = []
            for i, chunk_id in enumerate(chunk_ids):
                # Verifica se o score de similaridade está dentro do limite aceitável
                if scores[i] > limite_similaridade:
                    continue
                    
                chunk_data = self.db_gateway.buscar_chunk_por_id_db(chunk_id)
                if chunk_data:
                    # Criar objeto Chunk
                    chunk = Chunk(
                        chunk_uuid=chunk_data['chunk_uuid'],
                        arquivo_uuid=chunk_data['arquivo_uuid'],
                        chunk_texto=chunk_data['chunk_texto'],
                        chunk_numero=chunk_data['chunk_numero'],
                        chunk_tamanho_tokens=chunk_data['chunk_tamanho_tokens'],
                        chunk_embedding=chunk_data['chunk_embedding']
                    )
                    
                    # Busca o documento associado
                    arquivo_data = self.db_gateway.ler_arquivo_db(chunk_data['arquivo_uuid'])
                    if arquivo_data:
                        # Criar objeto Documento
                        documento = Documento(
                            arquivo_uuid=arquivo_data['arquivo_uuid'],
                            arquivo_nome=arquivo_data['arquivo_nome'],
                            arquivo_caminho=arquivo_data['arquivo_caminho'],
                            arquivo_tipo=arquivo_data['arquivo_tipo'],
                            data_modificacao=arquivo_data['data_modificacao'],
                            tamanho_bytes=arquivo_data['tamanho_bytes'],
                            arquivo_hash=arquivo_data['arquivo_hash']
                        )
                        
                        # Adiciona informações do documento no contexto
                        chunks.append({
                            "chunk": chunk,
                            "documento": documento,
                            "texto": chunk.chunk_texto,
                            "fonte": documento.arquivo_nome,
                            "score": scores[i]  # Adicionamos o score para uso posterior
                        })
            
            return chunks
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return []
    
    def formatar_contexto(self, chunks_relevantes):
        """
        Formata os chunks relevantes em um texto de contexto.
        
        Args:
            chunks_relevantes: Lista de dicionários com chunks e documentos
            
        Returns:
            str: Texto formatado com o contexto
        """
        if not chunks_relevantes:
            return ""
        
        contexto = "CONTEXTO RELEVANTE:\n\n"
        
        for i, item in enumerate(chunks_relevantes):
            chunk = item["chunk"]
            documento = item["documento"]
            
            contexto += f"[Fonte: {documento.arquivo_nome}]\n"
            contexto += f"{chunk.chunk_texto}\n\n"
        
        return contexto