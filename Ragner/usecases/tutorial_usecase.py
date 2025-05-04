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
        # Usa o presenter para exibir a mensagem, delegando a formatação
        self.presenter.exibir_texto_aguardar(mensagem)
        
        # Limpar qualquer evento de tecla pendente
        keyboard.read_event(suppress=True)
        
        # Aguardar a próxima tecla
        evento = keyboard.read_event(suppress=True)
        
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
        # Limpa a tela no início do tutorial
        self.presenter.limpar_tela()
        
        # Exibe o título do tutorial
        self.presenter.exibir_titulo_tutorial("BOAS-VINDAS AO TUTORIAL DO RAGNER")
        
        # Exibe a saudação inicial
        self.presenter.exibir_saudacao("Bem-vindo ao tutorial do Ragner!")
        
        # Exibe o texto de introdução com destaque para o termo RAG
        intro_text = "O Ragner é um software educacional projetado para ilustrar o funcionamento da tecnologia RAG (Retrieval-Augmented Generation), um método poderoso para permitir que modelos de linguagem respondam a perguntas com base nos documentos que o usuário compartilha."
        self.presenter.exibir_texto_tutorial(intro_text, destacar=["RAG (Retrieval-Augmented Generation)"])
        
        # Exibe o objetivo do tutorial
        objetivo = "O objetivo deste tutorial é explicar o processo RAG, mostrando como o Ragner utiliza seus documentos para encontrar informações relevantes e gerar respostas inteligentes."
        self.presenter.exibir_texto_tutorial(objetivo)
    
    def _exibir_chave_api(self):
        """
        Exibe informações sobre a chave da OpenAI e a conexão inteligente.
        """
        # Exibe o título da seção
        self.presenter.exibir_titulo_tutorial("PASSO 1: A CHAVE DA OPEN AI E A CONEXÃO INTELIGENTE")
        
        # Texto de explicação sobre a API key
        texto_api = "Para interagir com a inteligência artificial por trás da análise de texto e geração de respostas, o Ragner utiliza a tecnologia da OpenAI. Para isso, precisamos de uma chave de acesso, chamada API Key."
        self.presenter.exibir_texto_tutorial(texto_api)
        
        # Introdução às etapas
        self.presenter.exibir_texto_tutorial("Essa chave permite que o Ragner se comunique com os modelos de linguagem da OpenAI em duas etapas, que são:")
        
        # Etapa 1 com destaque
        etapa1 = "1) Transformar texto em vetores (embeddings): Como veremos, o significado das palavras e frases pode ser capturado em sequências numéricas."
        self.presenter.exibir_texto_tutorial(etapa1, destacar=["1) Transformar texto em vetores (embeddings):"])
        
        # Etapa 2 com destaque
        etapa2 = "2) Gerar respostas: Utilizar o contexto encontrado nos seus documentos para criar respostas relevantes."
        self.presenter.exibir_texto_tutorial(etapa2, destacar=["2) Gerar respostas:"])
        
        # Informação sobre armazenamento da chave
        texto_armazenamento = "O Ragner salva essa chave de forma segura como uma variável de ambiente no seu computador (\"OPENAI_API_KEY\"). Você pode gerenciá-la através das configurações de ambiente do Windows (pesquise por \"variáveis de ambiente\")."
        self.presenter.exibir_texto_tutorial(texto_armazenamento)
    
    def _exibir_processo_indexacao(self):
        """
        Exibe informações sobre o processo de "entendimento" dos arquivos.
        """
        # Exibe o título da seção
        self.presenter.exibir_titulo_tutorial("PASSO 2: O PROCESSO DE \"ENTENDIMENTO\" DOS SEUS ARQUIVOS (INDEXAÇÃO)")
        
        # Introdução ao processo de indexação
        intro = "Com a chave da OpenAI configurada, o Ragner pode começar a processar seus documentos, localizados na pasta \"documentos\". Esse processo de \"entendimento\" envolve várias etapas:"
        self.presenter.exibir_texto_tutorial(intro)
        
        # Seção 2.1: Mapeamento dos arquivos
        self.presenter.exibir_secao_numerada("2.1", "Mapeamento dos Arquivos", 
                                            "O Ragner registra os arquivos encontrados para acompanhamento interno.")
        
        # Seção 2.2: Leitura do conteúdo bruto
        self.presenter.exibir_secao_numerada("2.2", "Leitura do Conteúdo Bruto", 
                                            "O texto completo de cada arquivo é lido e armazenado temporariamente.")
        
        # Seção 2.3: Criação dos chunks
        chunk_text = "Criação dos \"Chunks\": Quebrando o Texto em Partes Menores: Para facilitar a busca por informações relevantes, o texto é dividido em seções menores, chamadas \"chunks\". No Ragner, estamos utilizando parágrafos como unidade de chunk. A forma como o texto é dividida é uma área importante em sistemas RAG, e diferentes estratégias podem ser usadas."
        self.presenter.exibir_secao_numerada("2.3", "Criação dos \"Chunks\"", 
                                            "Quebrando o Texto em Partes Menores: Para facilitar a busca por informações relevantes, o texto é dividido em seções menores, chamadas \"chunks\". No Ragner, estamos utilizando parágrafos como unidade de chunk. A forma como o texto é dividida é uma área importante em sistemas RAG, e diferentes estratégias podem ser usadas.",
                                            destacar=["o texto é dividido em seções menores, chamadas \"chunks\""])
    
    def _exibir_busca_vetorial(self):
        """
        Exibe informações sobre a busca vetorial e o índice FAISS.
        """
        # Exibe o título da seção
        self.presenter.exibir_titulo_tutorial("PASSO 3: A MAGIA DA BUSCA: VETORES E O ÍNDICE FAISS")
        
        # Introdução à busca vetorial
        intro = "Agora chegamos ao coração do processo RAG: como o Ragner realmente \"entende\" o significado do seu texto para encontrar informações relevantes. Isso é feito através de vetores e um sistema de indexação eficiente."
        self.presenter.exibir_texto_tutorial(intro)
        
        # Seção 3.1: Vetorização
        vetorizacao = "3.1) Vetorização (Embeddings): Transformando Texto em Números: Cada chunk de texto é transformado em uma longa sequência de números, chamada vetor ou embedding. Esses vetores são criados utilizando os modelos da OpenAI (lembra da API Key?). A grande sacada é que vetores de textos com significados semelhantes ficam \"próximos\" uns dos outros em um espaço matemático multidimensional."
        self.presenter.exibir_texto_tutorial(vetorizacao, destacar=["Cada chunk de texto é transformado em uma longa sequência de números, chamada vetor ou embedding"])
        
        # Seção 3.2: Índice FAISS
        faiss = "3.2) O Índice FAISS: Uma Biblioteca para Busca Rápida: Para encontrar rapidamente os vetores mais relevantes, o Ragner utiliza a biblioteca FAISS (Facebook AI Similarity Search). O FAISS cria uma espécie de \"mapa\" (índice) de todos os vetores dos seus documentos, permitindo uma busca extremamente veloz por similaridade."
        self.presenter.exibir_texto_tutorial(faiss)
        
        # Instrução sobre como visualizar vetores
        visualizacao = "Você pode ter uma ideia desses vetores ao usar o comando status_tabela_chunks no programa principal. A saída mostrará sequências numéricas associadas a cada pedaço do seu texto. Além disso, temos também um comando de teste para visualizar os vetores de um texto específico, chamado teste_vetor."
        self.presenter.exibir_texto_tutorial(visualizacao, destacar=["teste_vetor"])
    
    def _exibir_perguntas_respostas(self):
        """
        Exibe informações sobre como fazer perguntas e encontrar respostas.
        """
        # Exibe o título da seção
        self.presenter.exibir_titulo_tutorial("PASSO 4: PRONTO PARA AS PERGUNTAS: ENCONTRANDO A RESPOSTA")
        
        # Introdução ao processo de perguntas e respostas
        intro = "Com seus documentos processados e seus significados representados por vetores no índice FAISS, o Ragner está pronto para responder às suas perguntas!"
        self.presenter.exibir_texto_tutorial(intro)
        
        # Explicação do fluxo
        fluxo = "Quando você digita uma pergunta e pressiona Enter, o seguinte acontece:"
        self.presenter.exibir_texto_tutorial(fluxo)
        
        # Passo 4.1: Vetorização da pergunta
        vetorizacao = "4.1) Vetorização da Pergunta: Assim como os chunks dos seus documentos, sua pergunta também é transformada em um vetor utilizando os modelos da OpenAI."
        self.presenter.exibir_texto_tutorial(vetorizacao, destacar=["sua pergunta também é transformada em um vetor"])
        
        # Passo 4.2: Busca por similaridade
        busca = "4.2) Busca por Similaridade no FAISS (Retrieval): O Ragner pega o vetor da sua pergunta e usa o índice FAISS para encontrar os vetores dos chunks de texto que são mais \"próximos\" (ou seja, mais semanticamente similares) a ele. Essa é a etapa de Retrieval do RAG."
        self.presenter.exibir_texto_tutorial(busca, destacar=["encontrar os vetores dos chunks de texto que são mais \"próximos\""])
        
        # Passo 4.3: Geração da resposta
        geracao = "4.3) Geração da Resposta (Generation): Os chunks de texto correspondentes aos vetores mais similares são então enviados para outro modelo de linguagem da OpenAI, juntamente com a sua pergunta original. Esse modelo usa o contexto fornecido pelos chunks para gerar uma resposta relevante e informativa. Essa é a etapa de Generation."
        self.presenter.exibir_texto_tutorial(geracao, destacar=["enviados para outro modelo de linguagem da OpenAI"])
    
    def _exibir_exploracao(self):
        """
        Exibe informações sobre como explorar e aprender mais sobre o Ragner.
        """
        # Exibe o título da seção
        self.presenter.exibir_titulo_tutorial("PASSO 5: EXPLORE E APRENDA!")
        
        # Conclusão do tutorial
        conclusao = "Agora você entende o fluxo principal do Ragner e como a tecnologia RAG funciona!"
        self.presenter.exibir_texto_tutorial(conclusao)
        
        # Sugestões para exploração
        exploracao = "Sinta-se à vontade para adicionar seus próprios documentos na pasta \"documentos\" e fazer perguntas. Experimente os comandos como status_tabela_arquivos, status_tabela_chunks e status_faiss para observar o processo em ação."
        self.presenter.exibir_texto_tutorial(exploracao, destacar=["status_tabela_arquivos", "status_tabela_chunks", "status_faiss"])
        
        # Encerramento
        encerramento = "O Ragner é uma ferramenta para aprender e explorar o mundo fascinante da Inteligência Artificial e do processamento de linguagem natural. Divirta-se!"
        self.presenter.exibir_texto_tutorial(encerramento)