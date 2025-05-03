# Ragner Chatbot: Desvendando o Retrieval-Augmented Generation (RAG)

## Objetivo

Este software educacional, desenvolvido em Python, tem como objetivo demonstrar de forma clara e interativa o funcionamento interno da técnica de Geração Aumentada por Recuperação (RAG). Através de uma interface de linha de comando (CLI), usuários, especialmente estudantes de tecnologia, poderão acompanhar cada etapa do processo, desde a indexação de documentos até a geração de respostas contextualizadas por uma Inteligência Artificial.

## Funcionalidades Principais

* **Indexação de Documentos:** Permite adicionar arquivos nos formatos TXT, DOC/DOCX e PDF a uma pasta específica. O software processa esses arquivos, divide-os em partes (chunks) e cria representações vetoriais (embeddings) utilizando modelos da OpenAI.
* **Armazenamento Vetorial:** Utiliza a biblioteca FAISS (Facebook AI Similarity Search) para construir um índice eficiente das representações vetoriais dos chunks.
* **Armazenamento de Chunks:** Os chunks de texto são armazenados em um banco de dados SQLite para posterior recuperação.
* **Busca Semântica:** Ao receber uma pergunta do usuário, o software utiliza o FAISS para buscar os chunks mais relevantes semanticamente à pergunta.
* **Geração Aumentada:** A pergunta do usuário, juntamente com o contexto dos documentos relevantes (os chunks recuperados), são enviados para a API da OpenAI para gerar uma resposta informada.
* **Interface Interativa (CLI):** O usuário interage com o chatbot através de comandos de texto no terminal, acompanhando cada etapa do processo com explicações detalhadas.
* **Menu de Opções:** Oferece comandos para:
    * Exibir informações sobre o chatbot (`sobre`).
    * Obter ajuda e explicações (`tutorial`).
    * Verificar o status do banco de dados e do índice FAISS (`status`, `status_tabela_arquivos`, `status_tabela_chunks`, `status_faiss`).
    * Recarregar arquivos da pasta de documentos (`recarregar_arquivos_da_pasta`).
    * Apagar todos os dados do chatbot (`apagar_tudo`).
    * Sair do programa (`sair`).

## Como Utilizar

1.  **Pré-requisitos:**
    * Python 3.x instalado no seu sistema.
    * Uma chave de API da OpenAI. Você pode obter uma gratuitamente no site da [OpenAI](https://www.openai.com).

    * Clone este repositório (se aplicável) ou copie os arquivos do software para o seu computador.
    * Para executar (no PowerShell):
       ```powershell
       git clone https://github.com/viniciusbuscacio/Ragner.git
       python -m venv venv
       .\venv\Scripts\activate
       python -m pip install -r .\requirements.txt
       python Ragner/Ragner.py
       ```

2.  **Configuração:**
    * Ao executar o `Ragner.py` pela primeira vez (ou se a chave não for encontrada), o software solicitará que você configure a sua chave de API da OpenAI. Siga as instruções exibidas no terminal. A chave será salva para uso futuro (de forma segura, se possível, ou via variável de ambiente).

3.  **Adicionando Documentos:**
    * Para que o chatbot tenha informações para responder, você precisa adicionar arquivos (TXT, DOC/DOCX, PDF, XLS/XLSX, PPT/PPTX) na pasta `documentos` localizada no mesmo diretório do script `Ragner.py`.
    * Após adicionar os arquivos, o software os processará em segundo plano (ou você pode usar o comando `recarregar_arquivos_da_pasta` no menu).

4.  **Interagindo com o Chatbot:**
    * Execute o script `Ragner.py` no seu terminal: `python Ragner.py`
    * O chatbot será iniciado e você poderá digitar suas perguntas diretamente.
    * Para acessar o menu de opções, digite `menu` e pressione Enter.
    * Para sair do programa, digite `sair` e pressione Enter.

## Funcionamento Interno e Metodologia

Este software implementa as seguintes etapas para demonstrar o funcionamento da técnica RAG:

**Configuração:** Para acessar os modelos de linguagem da OpenAI, o usuário precisa configurar uma chave API, obtida gratuitamente no site da OpenAI, seguindo as instruções fornecidas pelo software.

**Indexação:** Após a configuração da chave API, o usuário pode adicionar arquivos nos formatos PDF, DOC/DOCX, XLS/XLSX, PPT/PPTX e TXT a uma pasta específica. O software utiliza a biblioteca Facebook AI Similarity Search (FAISS) e os modelos de vetorização (embedding) da OpenAI (como o `text-embedding-ada-002` ou similar) para indexar esses arquivos. Os blocos de texto (chunks) extraídos dos arquivos são armazenados em tabelas em um banco de dados transacional SQLite, que são consultadas para a coleta desses chunks durante a busca. Todas as ações do aplicativo são exibidas no prompt com explicações para o usuário acompanhar o processo.

**Busca e Resposta:** O usuário pode fazer perguntas ao chatbot. O software envia a pergunta, juntamente com o contexto dos documentos relevantes, para a API da OpenAI. Os modelos de linguagem da OpenAI são responsáveis por gerar a resposta. A similaridade semântica entre a pergunta e os documentos é calculada utilizando o módulo FAISS.

**Avaliação do Aprendizado:** Para avaliar a evolução do conhecimento sobre o RAG como consequência da utilização deste software, será realizado um levantamento de campo com estudantes de tecnologia. Uma pesquisa quantitativa com perguntas estruturadas será aplicada antes e depois do uso do software para coletar dados sobre o conhecimento dos estudantes sobre os conceitos do RAG (ex: o que são embeddings, como funciona a busca vetorial, etc.). Os dados coletados serão analisados estatisticamente para comparar o número de respostas corretas antes e depois do uso do software, permitindo quantificar o ganho de conhecimento.

## Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **OpenAI API:** Para geração de embeddings e respostas de linguagem natural.
* **FAISS (Facebook AI Similarity Search):** Para busca eficiente de similaridade vetorial.
* **SQLite:** Banco de dados leve para armazenamento dos chunks.
* **PyPDF2:** Para leitura de arquivos PDF.
* **python-docx:** Para leitura de arquivos DOC e DOCX.
* **Outras bibliotecas:** Para leitura de outros formatos de arquivo (XLS/XLSX, PPT/PPTX).
* **SQLAlchemy:** Para interação mais robusta com o SQLite.

## Para Aprender Mais

* [Retrieval-Augmented Generation (RAG)](https://www.google.com/search?q=retrieval+augmented+generation)
* [Facebook AI Similarity Search (FAISS)](https://github.com/facebookresearch/faiss)
* [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
* [SQLite Documentation](https://www.sqlite.org/docs.html)

## Contribuição

(Opcional, se você quiser abrir o projeto para contribuições)

## Licença

(Opcional, adicione a licença do seu projeto)