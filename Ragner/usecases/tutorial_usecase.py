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
            self._exibir_boas_vindas()
            if not self._aguardar_tecla():
                return
                
            # Passo 2: A chave da OpenAI e a conexão inteligente
            self._exibir_chave_api()
            if not self._aguardar_tecla():
                return
                
            # Passo 3: O processo de "entendimento" dos arquivos
            self._exibir_processo_indexacao()
            if not self._aguardar_tecla():
                return
                
            # Passo 4: A magia da busca: vetores e o índice FAISS
            self._exibir_busca_vetorial()
            if not self._aguardar_tecla():
                return
                
            # Passo 5: Pronto para as perguntas: encontrando a resposta
            self._exibir_perguntas_respostas()
            if not self._aguardar_tecla():
                return
                
            # Passo 6: Explore e aprenda!
            self._exibir_exploracao()
            self._aguardar_tecla("Pressione qualquer tecla para retornar ao programa principal...")
            
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
        from presentation.cli.cli_cores import Cores
        self.presenter.exibir_mensagem_sistema(f"\n{Cores.CINZA}{mensagem}{Cores.RESET}")
        
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
    
    def _exibir_boas_vindas(self):
        """
        Exibe a mensagem de boas-vindas e introdução ao tutorial.
        """
        from presentation.cli.cli_cores import Cores
        self.presenter.limpar_tela()
        self.presenter.exibir_mensagem_sistema(f"\n{Cores.AMARELO}======= BOAS-VINDAS AO TUTORIAL DO RAGNER ======={Cores.RESET}")
        
        self.presenter.exibir_mensagem_sucesso("\nBem-vindo ao tutorial do Ragner!")
        
        self.presenter.exibir_mensagem_sistema(f"\nO Ragner é um software educacional projetado para ilustrar o funcionamento da tecnologia {Cores.VERDE}RAG (Retrieval-Augmented Generation){Cores.RESET}, um método poderoso para permitir que modelos de linguagem respondam a perguntas com base nos documentos que o usuário compartilha.")
        
        self.presenter.exibir_mensagem_sistema("\nO objetivo deste tutorial é explicar o processo RAG, mostrando como o Ragner utiliza seus documentos para encontrar informações relevantes e gerar respostas inteligentes.")
    
    def _exibir_chave_api(self):
        """
        Exibe informações sobre a chave da OpenAI e a conexão inteligente.
        """
        from presentation.cli.cli_cores import Cores
        self.presenter.exibir_mensagem_sistema(f"\n\n{Cores.AMARELO}======= PASSO 1: A CHAVE DA OPEN AI E A CONEXÃO INTELIGENTE ======={Cores.RESET}")
        
        self.presenter.exibir_mensagem_sistema("\nPara interagir com a inteligência artificial por trás da análise de texto e geração de respostas, o Ragner utiliza a tecnologia da OpenAI. Para isso, precisamos de uma chave de acesso, chamada API Key.")
        
        self.presenter.exibir_mensagem_sistema("\nEssa chave permite que o Ragner se comunique com os modelos de linguagem da OpenAI em duas etapas, que são:")
        
        self.presenter.exibir_mensagem_sistema(f"\n{Cores.VERDE}1) Transformar texto em vetores (embeddings):{Cores.RESET} Como veremos, o significado das palavras e frases pode ser capturado em sequências numéricas.")
        
        self.presenter.exibir_mensagem_sistema(f"\n{Cores.VERDE}2) Gerar respostas:{Cores.RESET} Utilizar o contexto encontrado nos seus documentos para criar respostas relevantes.")
        
        self.presenter.exibir_mensagem_sistema("\nO Ragner salva essa chave de forma segura como uma variável de ambiente no seu computador (\"OPENAI_API_KEY\"). Você pode gerenciá-la através das configurações de ambiente do Windows (pesquise por \"variáveis de ambiente\").")
    
    def _exibir_processo_indexacao(self):
        """
        Exibe informações sobre o processo de "entendimento" dos arquivos.
        """
        from presentation.cli.cli_cores import Cores
        self.presenter.exibir_mensagem_sistema(f"\n\n{Cores.AMARELO}======= PASSO 2: O PROCESSO DE \"ENTENDIMENTO\" DOS SEUS ARQUIVOS (INDEXAÇÃO) ======={Cores.RESET}")
        
        self.presenter.exibir_mensagem_sistema("\nCom a chave da OpenAI configurada, o Ragner pode começar a processar seus documentos, localizados na pasta \"documentos\". Esse processo de \"entendimento\" envolve várias etapas:")
        
        self.presenter.exibir_mensagem_sistema("\n2.1) Mapeamento dos Arquivos: O Ragner registra os arquivos encontrados para acompanhamento interno.")
        
        self.presenter.exibir_mensagem_sistema("\n2.2) Leitura do Conteúdo Bruto: O texto completo de cada arquivo é lido e armazenado temporariamente.")
        
        self.presenter.exibir_mensagem_sistema(f"\n2.3) Criação dos \"Chunks\": Quebrando o Texto em Partes Menores: Para facilitar a busca por informações relevantes, {Cores.VERDE}o texto é dividido em seções menores, chamadas \"chunks\"{Cores.RESET}. No Ragner, estamos utilizando parágrafos como unidade de chunk. A forma como o texto é dividida é uma área importante em sistemas RAG, e diferentes estratégias podem ser usadas.")
    
    def _exibir_busca_vetorial(self):
        """
        Exibe informações sobre a busca vetorial e o índice FAISS.
        """
        from presentation.cli.cli_cores import Cores
        self.presenter.exibir_mensagem_sistema(f"\n\n{Cores.AMARELO}======= PASSO 3: A MAGIA DA BUSCA: VETORES E O ÍNDICE FAISS ======={Cores.RESET}")
        
        self.presenter.exibir_mensagem_sistema("\nAgora chegamos ao coração do processo RAG: como o Ragner realmente \"entende\" o significado do seu texto para encontrar informações relevantes. Isso é feito através de vetores e um sistema de indexação eficiente.")
        
        self.presenter.exibir_mensagem_sistema(f"\n3.1) Vetorização (Embeddings): Transformando Texto em Números: {Cores.VERDE}Cada chunk de texto é transformado em uma longa sequência de números, chamada vetor ou embedding{Cores.RESET}. Esses vetores são criados utilizando os modelos da OpenAI (aqui usamos a API Key). A grande sacada é que vetores de textos com significados semelhantes ficam \"próximos\" uns dos outros em um espaço matemático multidimensional.")
        
        self.presenter.exibir_mensagem_sistema("\n3.2) O Índice FAISS: Uma Biblioteca para Busca Rápida: Para encontrar rapidamente os vetores mais relevantes, o Ragner utiliza a biblioteca FAISS (Facebook AI Similarity Search). O FAISS cria uma espécie de \"mapa\" (índice) de todos os vetores dos seus documentos, permitindo uma busca extremamente veloz por similaridade.")
        
        self.presenter.exibir_mensagem_sistema(f"\nVocê pode ter uma ideia desses vetores ao usar o comando status_tabela_chunks no programa principal. A saída mostrará sequências numéricas associadas a cada pedaço do seu texto. Além disso, temos também um comando de teste para visualizar os vetores de um chunk específico, {Cores.VERDE}chamado teste_vetor{Cores.RESET}.")
    
    def _exibir_perguntas_respostas(self):
        """
        Exibe informações sobre como fazer perguntas e encontrar respostas.
        """
        from presentation.cli.cli_cores import Cores
        self.presenter.exibir_mensagem_sistema(f"\n\n{Cores.AMARELO}======= PASSO 4: PRONTO PARA AS PERGUNTAS: ENCONTRANDO A RESPOSTA ======={Cores.RESET}")
        
        self.presenter.exibir_mensagem_sistema("\nCom seus documentos processados e seus significados representados por vetores no índice FAISS, o Ragner está pronto para responder às suas perguntas!")
        
        self.presenter.exibir_mensagem_sistema("\nQuando você digita uma pergunta e pressiona Enter, o seguinte acontece:")
        
        self.presenter.exibir_mensagem_sistema(f"\n4.1) Vetorização da Pergunta: Assim como os chunks dos seus documentos, {Cores.VERDE}sua pergunta também é transformada em um vetor{Cores.RESET} utilizando os modelos da OpenAI.")
        
        self.presenter.exibir_mensagem_sistema(f"\n4.2) Busca por Similaridade no FAISS (Retrieval): O Ragner pega o vetor da sua pergunta e usa o índice FAISS para {Cores.VERDE}encontrar os vetores dos chunks de texto que são mais \"próximos\"{Cores.RESET} (ou seja, mais semanticamente similares) a ele. Essa é a etapa de Retrieval do RAG.")
        
        self.presenter.exibir_mensagem_sistema(f"\n4.3) Geração da Resposta (Generation): Os chunks de texto correspondentes aos vetores mais similares são então {Cores.VERDE}enviados para o ChatGPT{Cores.RESET}, juntamente com a sua pergunta original. Esse modelo usa o contexto fornecido pelos chunks para gerar uma resposta relevante e informativa. Essa é a etapa de Generation.")
    
    def _exibir_exploracao(self):
        """
        Exibe informações sobre como explorar e aprender mais sobre o Ragner.
        """
        from presentation.cli.cli_cores import Cores
        self.presenter.exibir_mensagem_sistema(f"\n\n{Cores.AMARELO}======= PASSO 5: EXPLORE E APRENDA! ======={Cores.RESET}")
        
        self.presenter.exibir_mensagem_sistema("\nAgora você entende o fluxo principal do Ragner e como a tecnologia RAG funciona!")
        
        self.presenter.exibir_mensagem_sistema("\nSinta-se à vontade para adicionar seus próprios documentos na pasta \"documentos\" e fazer perguntas. Experimente os comandos como status_tabela_arquivos, status_tabela_chunks e status_faiss para observar o processo em ação.")
        
        self.presenter.exibir_mensagem_sistema("\nO Ragner é uma ferramenta para aprender e explorar o mundo fascinante da Inteligência Artificial e do processamento de linguagem natural. Divirta-se!")