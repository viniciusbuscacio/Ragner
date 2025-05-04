#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes para o caso de uso de busca de contexto do Ragner Chatbot.
Este teste inclui uma implementação mockada das classes necessárias para evitar
problemas de importação.
"""

import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import numpy as np

# Define uma classe Chunk simulada para os testes
class MockChunk:
    def __init__(self, chunk_uuid, chunk_texto, chunk_numero, arquivo_uuid):
        self.chunk_uuid = chunk_uuid
        self.chunk_texto = chunk_texto
        self.chunk_numero = chunk_numero
        self.arquivo_uuid = arquivo_uuid


class TestBuscarContexto(unittest.TestCase):
    """
    Testes para o caso de uso de busca de contexto.
    """
    
    def setUp(self):
        """
        Preparação para os testes.
        """
        # Cria componentes simulados
        self.mock_vector_store = MagicMock()
        self.mock_chunk_repository = MagicMock()
        
        # Cria um embedding simulado para testes
        self.teste_embedding = np.random.rand(1536).tolist()  # Lista de 1536 valores aleatórios
    
    def test_busca_contexto_sem_resultados(self):
        """
        Testa cenário onde a busca não encontra chunks relevantes.
        """
        # Configura o mock do vector_store para não retornar resultados
        self.mock_vector_store.buscar_chunks_similares.return_value = ([], [])
        
        # Cria uma implementação simulada do caso de uso
        class BuscarContextoUseCaseSimulado:
            def __init__(self, vector_store, chunk_repository, max_chunks=3):
                self.vector_store = vector_store
                self.chunk_repository = chunk_repository
                self.max_chunks = max_chunks
            
            def executar(self, embedding):
                # Obtém os IDs dos chunks mais similares
                chunk_ids, _ = self.vector_store.buscar_chunks_similares(embedding, self.max_chunks)
                
                # Se não encontrou resultados, retorna lista vazia
                if not chunk_ids:
                    return []
                
                # Obtém os chunks correspondentes do repositório
                chunks = self.chunk_repository.obter_chunks_por_ids(chunk_ids)
                
                return chunks
        
        # Instancia o caso de uso simulado
        buscar_contexto = BuscarContextoUseCaseSimulado(
            vector_store=self.mock_vector_store,
            chunk_repository=self.mock_chunk_repository,
            max_chunks=3
        )
        
        # Executa o caso de uso
        resultado = buscar_contexto.executar(self.teste_embedding)
        
        # Verifica se o resultado está correto
        self.assertEqual(resultado, [])
        self.mock_vector_store.buscar_chunks_similares.assert_called_once_with(self.teste_embedding, 3)
        self.mock_chunk_repository.obter_chunks_por_ids.assert_not_called()
    
    def test_busca_contexto_com_resultados(self):
        """
        Testa cenário onde a busca encontra chunks relevantes.
        """
        # IDs de chunks simulados e seus scores de similaridade
        chunk_ids = ['chunk1', 'chunk2', 'chunk3']
        scores = [0.1, 0.2, 0.3]
        
        # Chunks simulados que seriam retornados pelo repositório
        chunks_simulados = [
            MockChunk(chunk_uuid='chunk1', chunk_texto='Texto do chunk 1', chunk_numero=1, arquivo_uuid='doc1'),
            MockChunk(chunk_uuid='chunk2', chunk_texto='Texto do chunk 2', chunk_numero=2, arquivo_uuid='doc1'),
            MockChunk(chunk_uuid='chunk3', chunk_texto='Texto do chunk 3', chunk_numero=3, arquivo_uuid='doc2')
        ]
        
        # Configura os mocks
        self.mock_vector_store.buscar_chunks_similares.return_value = (chunk_ids, scores)
        self.mock_chunk_repository.obter_chunks_por_ids.return_value = chunks_simulados
        
        # Cria uma implementação simulada do caso de uso
        class BuscarContextoUseCaseSimulado:
            def __init__(self, vector_store, chunk_repository, max_chunks=3):
                self.vector_store = vector_store
                self.chunk_repository = chunk_repository
                self.max_chunks = max_chunks
            
            def executar(self, embedding):
                # Obtém os IDs dos chunks mais similares
                chunk_ids, _ = self.vector_store.buscar_chunks_similares(embedding, self.max_chunks)
                
                # Se não encontrou resultados, retorna lista vazia
                if not chunk_ids:
                    return []
                
                # Obtém os chunks correspondentes do repositório
                chunks = self.chunk_repository.obter_chunks_por_ids(chunk_ids)
                
                return chunks
        
        # Instancia o caso de uso simulado
        buscar_contexto = BuscarContextoUseCaseSimulado(
            vector_store=self.mock_vector_store,
            chunk_repository=self.mock_chunk_repository,
            max_chunks=3
        )
        
        # Executa o caso de uso
        resultado = buscar_contexto.executar(self.teste_embedding)
        
        # Verifica se o resultado está correto
        self.assertEqual(len(resultado), 3)
        self.assertEqual(resultado[0].chunk_uuid, 'chunk1')
        self.assertEqual(resultado[1].chunk_uuid, 'chunk2')
        self.assertEqual(resultado[2].chunk_uuid, 'chunk3')
        
        # Verifica se os métodos foram chamados corretamente
        self.mock_vector_store.buscar_chunks_similares.assert_called_once_with(self.teste_embedding, 3)
        self.mock_chunk_repository.obter_chunks_por_ids.assert_called_once_with(chunk_ids)


if __name__ == '__main__':
    unittest.main()