# Ragner: Software Educacional para Desmistificar a IA Generativa Aumentada por Recuperação

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completo-brightgreen)](https://github.com/viniciusbuscacio/Ragner3)

> **Versão 1.0** - Julho de 2025

## 📖 Resumo

Este trabalho propõe o desenvolvimento de um **software educacional em Python** para desmistificar a técnica de **Geração Aumentada por Recuperação** (Retrieval-Augmented Generation, RAG).

O objetivo principal é explicar o funcionamento interno do RAG, permitindo a **visualização interativa** de suas etapas através de uma interface de linha de comando (CLI). Usuários, especialmente estudantes de tecnologia, poderão acompanhar cada passo do processo, desde a indexação de documentos até a geração de respostas contextualizadas por uma Inteligência Artificial.

**Palavras-chave:** Modelos de Linguagem Ampla; Busca Vetorial; Vetorização; Ferramenta Didática; Python.

## 🎯 Objetivos

### Objetivo Principal
Desenvolver um software educacional para desmistificar e explicar interativamente o funcionamento da técnica RAG (Retrieval-Augmented Generation).

### Objetivos Específicos
1. **Visualizar o Processo RAG**: Desenvolver um software em Python para demonstrar cada etapa do processo RAG de forma interativa
2. **Avaliar o Aprendizado**: Medir a evolução do conhecimento sobre RAG através de instrumentos de avaliação
3. **Demonstrar Eficácia**: Mostrar a efetividade do RAG em fornecer respostas contextualmente relevantes, incluindo suas limitações

## 🏗️ Metodologia

Este projeto se caracteriza como **Pesquisa Aplicada**, focando em resolver problemas práticos através do desenvolvimento de uma solução tecnológica tangível. A metodologia envolve:

### Desenvolvimento do Software
- **Linguagem**: Python com arquitetura limpa (Clean Architecture)
- **Indexação**: Utilização do FAISS (Facebook AI Similarity Search) para busca vetorial
- **Embeddings**: Modelos de vetorização da OpenAI (text-embedding-3-small)
- **Armazenamento**: SQLite para chunks de texto e FAISS para vetores
- **Interface**: CLI interativa com explicações educacionais

### Avaliação Educacional
Para avaliar a evolução do conhecimento sobre RAG, será realizado um levantamento de campo com estudantes de tecnologia através de:
- Pesquisa quantitativa com questionários estruturados
- Aplicação do mesmo questionário antes e depois do uso do software
- Análise estatística comparativa dos resultados

## ⚙️ Funcionalidades Implementadas

### 1. Configuração da API OpenAI
- **Módulo de configuração** que permite inserção segura da chave API da OpenAI
- **Armazenamento seguro** como variável de ambiente no sistema Windows
- **Validação automática** da chave durante a inicialização

### 2. Indexação de Documentos
- **Suporte a múltiplos formatos**: PDF, DOC/DOCX, TXT
- **Processamento inteligente**: Extração e divisão do conteúdo em chunks otimizados
- **Vetorização**: Utilização do modelo `text-embedding-3-small` da OpenAI
- **Armazenamento duplo**: 
  - Vetores no índice FAISS (1536 dimensões)
  - Chunks de texto no banco SQLite
- **Gerenciamento dinâmico**: Remoção automática de referências quando documentos são deletados
- **Feedback educacional**: Explicações detalhadas de cada etapa no terminal

### 3. Busca e Resposta Aumentada
- **Vetorização de consultas**: Perguntas convertidas em vetores usando o mesmo modelo de embedding
- **Busca por similaridade**: Recuperação dos chunks mais relevantes via FAISS
- **Geração contextualizada**: Respostas geradas pelo modelo `gpt-3.5-turbo` da OpenAI
- **Combinação inteligente**: Pergunta original + contexto recuperado
- **Transparência**: Exibição das fontes utilizadas na resposta

### 4. Interface Educacional
- **CLI Interativa**: Interface de linha de comando intuitiva
- **Tutorial Integrado**: Módulo explicativo dos conceitos RAG passo a passo
- **Comandos Educacionais**:
  - `tutorial` - Explicação interativa do processo RAG
  - `status` - Verificação do estado do sistema
  - `sobre` - Informações sobre o software
  - `teste_vetor` - Demonstração prática de vetorização
  - E mais comandos para exploração

## � Instalação e Configuração

### Pré-requisitos
- **Python 3.8 ou superior**
- **Chave API da OpenAI** (obrigatória)
- **Sistema Operacional Windows** (para executável)

### Opção 1: Instalação via Executável (Recomendada)
1. Baixe o executável `Ragner_Setup.exe` na pasta `installer/`
2. Execute o instalador com privilégios de administrador
3. Siga as instruções do assistente de instalação
4. Configure sua chave API ao iniciar o programa

### Opção 2: Instalação para Desenvolvimento
```bash
# Clone o repositório
git clone [URL_DO_REPOSITORIO]
cd Ragner3

# Instale as dependências
pip install -r requirements.txt

# Execute o programa
python Ragner/Ragner.py
```

### Configuração da API Key
1. **Primeira execução**: O sistema solicitará automaticamente sua chave API
2. **Configuração manual**: Use a opção "Configurar API Key" no menu
3. **Variável de ambiente**: Configure `OPENAI_API_KEY` no sistema

## 🔧 Tecnologias e Arquitetura

### Stack Tecnológico
- **Linguagem Principal**: Python 3.8+
- **API de IA**: OpenAI API (embeddings e chat completion)
- **Busca Vetorial**: FAISS (Facebook AI Similarity Search)
- **Banco de Dados**: SQLite para armazenamento de chunks
- **Processamento de Arquivos**: 
  - PyPDF2 (arquivos PDF)
  - python-docx (arquivos DOC/DOCX)
- **Segurança**: Gerenciamento seguro de chaves API

### Arquitetura do Sistema
O projeto segue os princípios da **Clean Architecture** com separação clara de responsabilidades:

```
📁 Ragner/
├── 🏛️ domain/              # Entidades centrais do sistema
│   ├── Chunk.py            # Representação de fragmentos de texto
│   ├── Documento.py        # Representação de documentos
│   ├── Embedding.py        # Representação de vetores
│   └── ...
├── 🔧 infrastructure/      # Implementações concretas
│   ├── database/           # Acesso ao SQLite
│   ├── file_loaders/       # Processadores de arquivo
│   ├── language_model/     # Interface OpenAI
│   ├── repositories/       # Camada de dados
│   └── vector_store/       # Interface FAISS
├── 🎯 usecases/           # Regras de negócio
│   ├── indexar_documentos_usecase.py
│   ├── buscar_contexto_usecase.py
│   ├── gerar_resposta_usecase.py
│   └── ...
├── 🖥️ presentation/       # Interface com usuário
│   └── cli/               # Interface de linha de comando
└── 🎯 usecases/           # Regras de negócio
    ├── indexar_documentos_usecase.py
    ├── buscar_contexto_usecase.py
    ├── gerar_resposta_usecase.py
    └── ...
```

## 💻 Guia de Utilização

### Interface de Linha de Comando
O Ragner oferece uma interface CLI intuitiva com as seguintes opções:

```
🤖 RAGNER - Sistema RAG Educacional
====================================

[1] 📄 Indexar documentos
[2] ❓ Fazer perguntas
[3] 🔑 Configurar API Key
[4] 📚 Tutorial
[5] 🚪 Sair

Escolha uma opção: _
```

### Fluxo de Trabalho Típico

#### 1. 📄 Indexação de Documentos
- Selecione a opção "Indexar documentos"
- Escolha os arquivos (.txt, .pdf, .docx) na pasta `documentos/`
- O sistema processará automaticamente:
  - Divisão em chunks otimizados
  - Geração de embeddings via OpenAI
  - Armazenamento no banco FAISS

#### 2. ❓ Consultas Inteligentes
- Acesse "Fazer perguntas"
- Digite sua pergunta em linguagem natural
- O sistema:
  - Busca contexto relevante nos documentos
  - Gera resposta usando GPT-4
  - Exibe fontes utilizadas

#### 3. 🔑 Gestão de API Key
- Configure sua chave OpenAI no primeiro uso
- Atualize quando necessário
- Verificação automática de validade

### Exemplos de Uso
```bash
# Exemplo de pergunta eficaz:
"Quais são os principais conceitos de machine learning apresentados no documento?"

# Resultado esperado:
✅ Contexto encontrado: 3 chunks relevantes
📖 Fontes: documento1.pdf (página 15), documento2.txt
🤖 Resposta: [Resposta detalhada baseada no contexto]
```

## 📋 Estrutura do Projeto

### Organização de Diretórios
```
📁 Ragner3/
├── 📄 README.md                    # Documentação principal
├── 📄 requirements.txt             # Dependências Python
├── 📄 Ragner.spec                  # Configuração PyInstaller
├── 📁 Ragner/                      # Código fonte principal
│   ├── 🐍 Ragner.py               # Ponto de entrada
│   ├── 📁 domain/                 # Entidades de domínio
│   ├── 📁 infrastructure/         # Implementações técnicas
│   ├── 📁 usecases/              # Casos de uso
│   └── 📁 presentation/          # Interface usuário
├── 📁 database/                   # Banco SQLite
├── 📁 documentos/                 # Documentos para indexação
├── 📁 faiss_index/               # Índice vetorial FAISS
├── 📁 installer/                  # Executável Windows
└── 📁 documentos/                 # Documentos para indexação
```

### Componentes Principais

#### 🏛️ Domain Layer (Entidades)
- `Chunk.py`: Fragmentos de texto processados
- `Documento.py`: Representação de documentos
- `Embedding.py`: Vetores de embedding
- `Pergunta.py` / `Resposta.py`: Interações do usuário

#### 🔧 Infrastructure Layer (Implementações)
- **Database**: Gerenciamento SQLite
- **File Loaders**: Processadores PDF/DOCX/TXT
- **Language Model**: Gateway OpenAI API
- **Vector Store**: Interface FAISS
- **Repositories**: Camada de persistência

#### 🎯 Use Cases (Regras de Negócio)
- `indexar_documentos_usecase.py`: Processamento de documentos
- `buscar_contexto_usecase.py`: Busca semântica
- `gerar_resposta_usecase.py`: Geração de respostas
- `fazer_pergunta_usecase.py`: Fluxo completo RAG

##  Contribuição e Metodologia

### Metodologia de Desenvolvimento
Este projeto segue uma abordagem acadêmica baseada em:

1. **Análise de Requisitos**: Identificação de necessidades educacionais para RAG
2. **Design Arquitetural**: Implementação de Clean Architecture
3. **Desenvolvimento Iterativo**: Ciclos curtos com feedback contínuo  
4. **Validação Experimental**: Testes com diferentes tipos de documentos
5. **Otimização de Performance**: Ajuste de chunking e embedding

### Como Contribuir
1. **Fork** o repositório
2. **Clone** sua fork localmente
3. **Crie** uma branch para sua feature: `git checkout -b feature/nova-funcionalidade`
4. **Implemente** suas mudanças seguindo a arquitetura existente
5. **Commit** suas mudanças: `git commit -m "Adiciona nova funcionalidade"`
6. **Push** para sua branch: `git push origin feature/nova-funcionalidade`
7. **Abra** um Pull Request

### Diretrizes de Código
- Siga a **Clean Architecture** estabelecida
- Use **type hints** em Python
- Documente **APIs públicas**
- Implemente **tratamento de erros** robusto

## 📚 Recursos Educacionais

### Conceitos Demonstrados
- **Retrieval-Augmented Generation (RAG)**
- **Embeddings semânticos** com OpenAI
- **Busca vetorial** com FAISS
- **Processamento de linguagem natural**
- **Arquitetura limpa** em Python
- **Persistência de dados** com SQLite

### Casos de Uso Acadêmicos
- 📖 **Pesquisa Bibliográfica**: Consulta rápida em papers e livros
- 🎓 **Suporte Educacional**: Respostas baseadas em material didático  
- 📝 **Análise Documental**: Extração de insights de documentos longos
- 🔍 **Exploração de Conhecimento**: Descoberta de relações entre conceitos

## 📄 Licença e Citação

### Licença
Este projeto é distribuído sob licença [MIT](LICENSE). Você é livre para usar, modificar e distribuir este software para fins educacionais e comerciais.

### Como Citar
Se você utilizar este projeto em pesquisa acadêmica, considere citar:

```bibtex
@software{ragner2024,
  title = {Ragner: Sistema RAG Educacional para Demonstração de IA Generativa},
  author = {[Seu Nome]},
  year = {2024},
  url = {https://github.com/[seu-usuario]/Ragner3}
}
```

---

## 🔗 Links Úteis

- 🤖 **OpenAI API**: [platform.openai.com](https://platform.openai.com)
- 📊 **FAISS Documentation**: [faiss.ai](https://faiss.ai)
- 🐍 **Python Docs**: [docs.python.org](https://docs.python.org)
- 🏗️ **Clean Architecture**: [Clean Code Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

## 📞 Suporte e Contato

Para dúvidas, sugestões ou contribuições:
- 📧 **Email**: [seu-email@exemplo.com]
- 💬 **Issues**: Abra uma issue neste repositório
- 🐦 **Social**: [@seu-usuario](https://twitter.com/seu-usuario)

---

<div align="center">

**Ragner** - Democratizando o acesso à tecnologia RAG para educação 🚀

*Construído com ❤️ para a comunidade acadêmica*

</div>
