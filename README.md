# Email Classifier com IA

Aplicacao web full-stack para classificar emails como **Produtivo** ou **Improdutivo** e gerar uma resposta automatica profissional com apoio de IA.

## Stack
- Backend: Python 3.10+, FastAPI
- IA: OpenAI Responses API
- Frontend: HTML, CSS e JavaScript
- Configuracao: variaveis de ambiente (`.env`)

## Estrutura do Projeto
```text
/app
  /api
  /services
  /utils
  main.py
/frontend
  index.html
  script.js
  styles.css
requirements.txt
README.md
Implementação_case_pratico
```

## Pre-requisitos
- Python 3.10+
- Conta com chave de API da OpenAI

## Setup Inicial (visao geral)
1. Criar e ativar ambiente virtual.
2. Instalar dependencias com `pip install -r requirements.txt`.
3. Criar arquivo `.env` na raiz do projeto com as variaveis necessarias.
4. Executar a API com Uvicorn.

## Variaveis de Ambiente (base)
Exemplo inicial de chaves que serao usadas nas proximas etapas:

```env
OPENAI_API_KEY=sua_chave_aqui
OPENAI_MODEL=gpt-4.1-mini
APP_ENV=development
```

## Ordem de Entregas
1. README inicial
2. Backend FastAPI completo
3. Frontend
4. README final enxuto e atualizado

## Status
- Etapa 1: em andamento/concluida nesta entrega
- Etapas 2, 3 e 4: pendentes
