#./usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Use Case de Tutorial: Implementa a lógica de negócio do tutorial interativo do Ragner.
"""

import os
import time


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
            # Página inicial: Boas-vindas e visão geral dos 5 passos
            if not self._exibir_boas_vindas():
                return
                
            # Passo 1 detalhado: Documentos → Blocos
            if not self._exibir_processo_indexacao():
                return
                
            # Passo 2 detalhado: Blocos → Números (Vetorização)
            self._exibir_vetorizacao()
            if not self._aguardar_tecla():
                return
                
            # Passo 3 detalhado: Pergunta → Números
            self._exibir_busca_vetorial()
                
            # Passo 4 detalhado: Comparação Matemática
            self._exibir_comparacao_matematica()
            if not self._aguardar_tecla():
                return
                
            # Passo 5 detalhado: ChatGPT Responde
            self._exibir_perguntas_respostas()
            if not self._aguardar_tecla():
                return
                
            # Conclusão: Explore e aprenda.
            self._exibir_exploracao()
            self._aguardar_tecla("Pressione Enter para retornar ao programa principal...")
            
        except Exception as e:
            self.presenter.exibir_mensagem_erro(f"Erro durante o tutorial: {str(e)}")
            self.presenter.exibir_mensagem_sistema("Pressione Enter para voltar ao programa principal...")
            input()
    
    def _aguardar_tecla(self, mensagem="Pressione Enter para continuar ou digite 'sair' para encerrar"):
        """
        Aguarda que o usuário pressione uma tecla.
        
        Args:
            mensagem: Mensagem a ser exibida antes de aguardar a tecla
            
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Usa o presenter para exibir a mensagem, delegando a formatação
        self.presenter.exibir_texto_aguardar(mensagem)
        
        # Aguarda entrada do usuário
        entrada = input().strip().lower()
        
        # Se o usuário digitou 'sair', retorna False
        if entrada in ['sair', 'exit', 'quit', 'esc']:
            return False
            
        # Qualquer outra entrada significa continuar
        return True
    
    def _exibir_boas_vindas(self):
        """
        Exibe a mensagem de boas-vindas e introdução ao tutorial.
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        # Limpa a tela no início do tutorial
        self.presenter.limpar_tela()
        
        # Exibe o título do tutorial
        self.presenter.exibir_titulo_tutorial("BEM-VINDO AO RAGNER")
        
        # Texto de boas-vindas
        boas_vindas = "Olá! Bem-vindo ao Ragner, um software educacional para desmistificar a IA Generativa Aumentada por Recuperação (RAG - Retrieval-Augmented Generation)."
        self.presenter.exibir_texto_tutorial(boas_vindas)
        
        # Explicação sobre RAG
        explicacao_rag = "O RAG é uma técnica que permite que modelos de linguagem, como o ChatGPT, respondam suas perguntas com base em documentos específicos que você fornece. Isso é um processo útil para obter respostas mais precisas e para que ocorram menos eventos de \"alucinação\" das IA's."
        self.presenter.exibir_texto_tutorial(explicacao_rag, destacar=["obter respostas mais precisas"])
        
        # Objetivo do Ragner
        objetivo = "O objetivo do Ragner é que você entenda como funcione o processo de RAG, vendo na prática os passos envolvidos."
        self.presenter.exibir_texto_tutorial(objetivo)
        
        # Aguarda tecla para continuar
        if not self._aguardar_tecla():
            return False
        
        # VISÃO GERAL: RAG em 4 Passos
        self.presenter.exibir_titulo_tutorial("RAG EM 4 PASSOS: A JORNADA DE SEUS DOCUMENTOS À RESPOSTA")
        
        introducao_passos = "Quando você usa o Ragner, o sistema executa um fluxo completo, desde o processamento dos seus documentos até a geração de uma resposta. Para simplificar, dividimos esse processo em 4 passos principais."
        self.presenter.exibir_texto_tutorial(introducao_passos, destacar=["4 passos"])
        
        # Os 4 passos
        passo1 = "Passo 1 - Preparação: Seus documentos são transformados em pequenos blocos de texto (chunks) e, em seguida, em números (vetores)."
        self.presenter.exibir_texto_tutorial(passo1, destacar=["Passo 1"])
        
        passo2 = "Passo 2 - Sua Pergunta: Sua pergunta também é convertida para estes números."
        self.presenter.exibir_texto_tutorial(passo2, destacar=["Passo 2"])
        
        passo3 = "Passo 3 - A Busca: O sistema faz cálculos matemáticos para encontrar os blocos de texto mais relevantes para a sua pergunta."
        self.presenter.exibir_texto_tutorial(passo3, destacar=["Passo 3"])
        
        passo4 = "Passo 4 - A Resposta: O sistema envia sua pergunta e os blocos encontrados para o ChatGPT, da OpenAI, que então gera uma resposta baseada apenas nas suas informações."
        self.presenter.exibir_texto_tutorial(passo4, destacar=["Passo 4"])
        
        # Próximos passos
        proximos_passos = "Nas próximas telas, vamos detalhar cada um desses passos, mostrando como o Ragner funciona por dentro."
        self.presenter.exibir_texto_tutorial(proximos_passos)
        
        # Aguarda tecla para continuar antes do Passo 1
        if not self._aguardar_tecla():
            return False
        
        return True
    
    def _exibir_chave_api(self):
        """
        Este método não é mais necessário no novo tutorial.
        """
        pass
    
    def _exibir_processo_indexacao(self):
        """
        Explica o processo de indexação de documentos (Passo 1: Preparação).
        
        Returns:
            bool: True se o usuário quer continuar, False se quer sair
        """
        self.presenter.exibir_titulo_tutorial("PASSO 1: PREPARAÇÃO - DE DOCUMENTOS A NÚMEROS")
        
        # Explicação inicial
        explicacao_inicial = "Para que o Ragner possa encontrar a informação certa, ele precisa primeiro ler e entender seus documentos. Para isso, ele segue dois sub-passos:"
        self.presenter.exibir_texto_tutorial(explicacao_inicial)
        
        # Sub-passo 1.1
        sub_passo_1 = "1.1. De Documentos para Blocos de Texto (Chunks)"
        self.presenter.exibir_texto_tutorial(sub_passo_1, destacar=["(Chunks)"])
        
        explicacao_chunks = "O Ragner pega seus arquivos e os divide em pequenos pedaços de texto, chamados de chunks. Essa divisão garante que a busca seja mais precisa e rápida."
        self.presenter.exibir_texto_tutorial(explicacao_chunks)
        
        pratica_titulo = "Na prática:"
        self.presenter.exibir_texto_tutorial(pratica_titulo)
        
        pratica_1 = " - Você adiciona arquivos (PDF, DOCX, TXT) na pasta 'documentos' (durante a instalação, foi criado um atalho para esta na sua Área de Trabalho, mas como referência, o caminho no seu computador é \"C:\\Users\\SEU USUÁRIO AQUI\\AppData\\Local\\Ragner\\documentos\""
        self.presenter.exibir_texto_tutorial(pratica_1)
    
        pratica_2 = " - O Ragner divide cada arquivo em chunks de aproximadamente 500 a 1000 caracteres, respeitando parágrafos e frases."
        self.presenter.exibir_texto_tutorial(pratica_2)
        
        pratica_3 = " - Cada chunk é adicionado ao banco de dados (SQLite) com o nome do arquivo de origem."
        self.presenter.exibir_texto_tutorial(pratica_3)

        # Aguarda tecla para continuar
        if not self._aguardar_tecla():
            return False

        # Sub-passo 1.2
        sub_passo_2 = "1.2. De Blocos de Texto para Números (Vetorização)"
        self.presenter.exibir_texto_tutorial(sub_passo_2, destacar=["(Vetorização)"])
        
        explicacao_numeros = "Computadores não entendem palavras, mas sim números. Por isso, a parte mais importante é traduzir cada chunk para uma linguagem numérica."
        self.presenter.exibir_texto_tutorial(explicacao_numeros)
        
        # A mágica dos embeddings
        magica_titulo = "A mágica dos Embeddings:"
        self.presenter.exibir_texto_tutorial(magica_titulo, destacar=["Embeddings:"])
        
        magica_explicacao = "O Ragner envia cada chunk para um modelo da OpenAI, que o transforma em uma sequência de 1.536 números. Esses números, chamados de vetores, não são aleatórios: eles capturam o significado semântico do texto. Isso significa que textos com significados parecidos geram vetores numericamente semelhantes."
        self.presenter.exibir_texto_tutorial(magica_explicacao)
        
        # Aguarda tecla para continuar
        if not self._aguardar_tecla():
            return False
        
        exemplo_titulo = "Exemplo:"
        self.presenter.exibir_texto_tutorial(exemplo_titulo)
        
        exemplo_vetores = """Para ver quão grande estes números são, você pode digitar no Ragner "teste_vetor". O Ragner vai te pedir um texto (que pode ser uma palavra, uma frase, etc), e vai transformar este em um vetor usando o modelo text-embedding-3-small da Open AI. Este número é gigante, composto de 1536 números que vão de -1 a 1."""
        
        self.presenter.exibir_texto_tutorial(exemplo_vetores, destacar=["teste_vetor"])
        
        # Exemplo de uso em cinza
        exemplo_uso = """> Você: teste_vetor
> Digite um texto para ver seu vetor embedding: carro
> Processando geração do embedding...
> 
> Embedding para o texto: 'carro'
> Dimensão do vetor: 1536
> 
> Valores do embedding:
> 0.026904 -0.007592 -0.041182 0.010810 0.006155 -0.020218 -0.005210 0.040300 -0.030819 0.005838 0.002297 0.028352 0.012683 -0.012377 0.004797 -0.003021 0.020195 -0.014006 0.002372 0.009317 0.033805 0.004463 0.039281 [etc]"""
        
        self.presenter.exibir_texto_aguardar(exemplo_uso)
        
       
        resultado = "O resultado do processamento dos arquivos que você adicionou à pasta é um banco de dados onde cada chunk está associado ao seu vetor numérico, criando uma \"biblioteca\" que o computador entende perfeitamente."
        self.presenter.exibir_texto_tutorial(resultado)
        
        # Aguarda tecla para continuar antes do Passo 2
        if not self._aguardar_tecla():
            return False
        
        return True
    
    def _exibir_vetorizacao(self):
        """
        Explica como a pergunta é transformada em números (Passo 2: Sua Pergunta).
        """
        self.presenter.exibir_titulo_tutorial("PASSO 2: SUA PERGUNTA - TRANSFORMANDO PALAVRAS EM NÚMEROS")
        
        # Explicação principal
        explicacao_principal = "Quando você digita sua pergunta no Ragner, o sistema faz exatamente o que fez com seus documentos: ele envia sua pergunta para a OpenAI, que a converte em um vetor numérico de 1.536 dimensões."
        self.presenter.exibir_texto_tutorial(explicacao_principal)
        
        # Resultado
        resultado = "Agora, sua pergunta e todos os seus chunks estão na mesma representação numérica. É com base nessa similaridade numérica que o Ragner irá encontrar a resposta."
        self.presenter.exibir_texto_tutorial(resultado, destacar=["chunks"])
        
        # Exemplo
        exemplo_titulo = "Exemplo:"
        self.presenter.exibir_texto_tutorial(exemplo_titulo)
        
        exemplo = "Sua pergunta \"Como acender um LED?\" se transforma em um vetor como [0.2345, -0.1234, 0.8765, ...]."
        self.presenter.exibir_texto_tutorial(exemplo)
    
    def _exibir_comparacao_matematica(self):
        """
        Este método não é mais necessário pois foi incorporado ao _exibir_busca_vetorial.
        """
        pass
    
    def _exibir_busca_vetorial(self):
        """
        Explica a busca vetorial (Passo 3: A Busca).
        """
        self.presenter.exibir_titulo_tutorial("PASSO 3: A BUSCA - ENCONTRANDO OS CHUNKS MAIS RELEVANTES")
        
        # Introdução
        introducao = "Com sua pergunta e os chunks representados como vetores, o Ragner pode agora encontrar a melhor resposta. Ele compara o vetor da sua pergunta com todos os vetores dos seus chunks para encontrar os mais \"próximos\" matematicamente."
        self.presenter.exibir_texto_tutorial(introducao)
        
        # Como funciona a comparação
        titulo_comparacao = "Como funciona a comparação?"
        self.presenter.exibir_texto_tutorial(titulo_comparacao)
        
        explicacao_comparacao = "O Ragner usa uma técnica muito rápida chamada Distância Euclidiana. Pense em cada vetor como um ponto em um mapa. O sistema mede a distância linear entre:"
        self.presenter.exibir_texto_tutorial(explicacao_comparacao)
        
        pontos = "- O ponto da sua pergunta\n- O ponto de cada bloco de texto"
        self.presenter.exibir_texto_tutorial(pontos)
        
        proximidade = "Quanto menor a distância entre os pontos, maior a similaridade de significado entre eles. É como encontrar os pontos mais próximos da sua pergunta no mapa."
        self.presenter.exibir_texto_tutorial(proximidade)
        
        # Aguarda tecla para continuar
        if not self._aguardar_tecla():
            return False
        
        velocidade = "Graças à biblioteca FAISS (Facebook AI Similarity Search), essa comparação é feita em milissegundos, mesmo com milhares de documentos. O Ragner instantaneamente identifica os 3 a 5 chunks mais similares à sua pergunta, que são os trechos que provavelmente contêm a resposta."
        self.presenter.exibir_texto_tutorial(velocidade)
        
        # Exemplo
        titulo_exemplo = "Exemplo:"
        self.presenter.exibir_texto_tutorial(titulo_exemplo)
        
        exemplo = """Vetor da sua pergunta: [0.7, 0.3, 0.8, ...]
Vetor do Chunk A:      [0.6, 0.4, 0.7, ...] (muito próximo)
Vetor do Chunk B:      [0.1, 0.9, 0.2, ...] (distante)

O sistema seleciona o Chunk A, pois sua "distância" para a pergunta é menor."""
        
        self.presenter.exibir_texto_tutorial(exemplo)
    
    def _exibir_perguntas_respostas(self):
        """
        Exibe informações sobre o passo 4: como o ChatGPT gera a resposta final.
        """
        self.presenter.exibir_titulo_tutorial("PASSO 4: A RESPOSTA - GERANDO UMA RESPOSTA COM O CHATGPT")
        
        # Introdução
        introducao = "Este é o último e crucial passo. O Ragner monta um pedido especial para a API do ChatGPT, combinando três elementos:"
        self.presenter.exibir_texto_tutorial(introducao)
        
        # Os três elementos
        elementos = """1. Sua pergunta original.
2. Os chunks mais relevantes encontrados no passo anterior.
3. Uma instrução clara do tipo: "Responda à pergunta usando APENAS as informações fornecidas nos trechos abaixo.\""""
        self.presenter.exibir_texto_tutorial(elementos)
        
        # Importância da instrução
        importancia_instrucao = "Essa instrução é a chave. Ela garante que o ChatGPT não \"invente\" ou use seu conhecimento prévio. A resposta será gerada exclusivamente com base nos seus documentos. O Ragner então exibe a resposta e mostra as fontes utilizadas para que você possa verificar a informação."
        self.presenter.exibir_texto_tutorial(importancia_instrucao)
    
    def _exibir_exploracao(self):
        """
        Exibe informações sobre como explorar e aprender mais sobre o Ragner.
        """
        # Conclusão
        conclusao_titulo = "Agora, explore as funcionalidades do Ragner para ver o RAG em ação:"
        self.presenter.exibir_texto_tutorial(conclusao_titulo)
        
        # Lista de comandos para exploração
        exploracoes = [
            "- Adicione seus arquivos à pasta documentos (você deve ter um atalho para ela na sua Área de Trabalho).",
            "- Use o comando recarregar_arquivos_da_pasta para processar novos arquivos (começe com arquivos menores, pois quanto maior o arquivo, maior o tempo de processamento).",
            "- Use o comando teste_vetor para ver como um texto vira números.",
            "- Use status_tabela_chunks para visualizar os pedaços de texto gerados.",
            "Faça perguntas e veja como o Ragner encontra as respostas nos seus documentos, indicando as fontes."
        ]
        
        for exploracao in exploracoes:
            if "recarregar_arquivos_da_pasta" in exploracao:
                self.presenter.exibir_texto_tutorial(exploracao, destacar=["recarregar_arquivos_da_pasta"])
            elif "teste_vetor" in exploracao:
                self.presenter.exibir_texto_tutorial(exploracao, destacar=["teste_vetor"])
            elif "status_tabela_chunks" in exploracao:
                self.presenter.exibir_texto_tutorial(exploracao, destacar=["status_tabela_chunks"])
            else:
                self.presenter.exibir_texto_tutorial(exploracao)