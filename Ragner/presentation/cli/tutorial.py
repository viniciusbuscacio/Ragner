#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tutorial Interface: Classe responsável por intermediar a interação entre
o presenter e o caso de uso do tutorial.
"""

import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from usecases.tutorial_usecase import TutorialUseCase
except ImportError:
    # Fallback para quando executado como executável
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    sys.path.insert(0, parent_dir)
    from usecases.tutorial_usecase import TutorialUseCase


class TutorialInterface:
    """
    Interface para o tutorial interativo do Ragner.
    
    Esta classe segue o padrão adapter/facade, simplificando a interação
    entre o presenter e o caso de uso do tutorial.
    """
    
    def __init__(self, presenter, db_gateway=None, doc_indexador=None, chat_controller=None):
        """
        Inicializa a interface do tutorial.
        
        Args:
            presenter: O presenter que exibirá as mensagens
            db_gateway: Gateway para acesso ao banco de dados
            doc_indexador: Serviço responsável pela indexação de documentos
            chat_controller: Controlador do chat para executar comandos como recarregar_arquivos_da_pasta
        """
        self.presenter = presenter
        self.db_gateway = db_gateway
        self.doc_indexador = doc_indexador
        self.chat_controller = chat_controller
        
    def executar_tutorial(self):
        """
        Executa o tutorial interativo completo.
        
        Este método cria e utiliza o caso de uso apropriado para
        executar o tutorial, isolando o presenter da implementação.
        """
        try:
            # Criar e executar o caso de uso
            tutorial_usecase = TutorialUseCase(
                presenter=self.presenter,
                db_gateway=self.db_gateway,
                doc_indexador=self.doc_indexador,
                chat_controller=self.chat_controller
            )
            
            # Delega a execução para o caso de uso
            tutorial_usecase.executar_tutorial()
            
        except ImportError:
            self.presenter.exibir_mensagem_erro("Erro: O módulo de tutorial não foi encontrado.")
        except Exception as e:
            self.presenter.exibir_mensagem_erro(f"Erro ao executar o tutorial: {str(e)}")