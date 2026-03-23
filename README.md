# Email Classifier com IA

Aplicacao para classificar emails como **Produtivo** ou **Improdutivo** e gerar resposta automatica profissional com IA.

## Tecnologias
- Python 3.10+
- FastAPI
- OpenAI Responses API

## Como rodar localmente
1. Crie e ative o ambiente virtual.
2. Instale as dependencias: `pip install -r requirements.txt`
3. Crie o arquivo `.env` (pode copiar de `.env.example`).
4. Preencha ao menos `OPENAI_API_KEY` no `.env`.
5. Em um terminal, inicie a API: `uvicorn app.main:app --reload`
6. Em outro terminal, suba o frontend estatico: `python -m http.server 5500 --directory frontend`
7. Acesse:
   - Frontend: `http://127.0.0.1:5500`
   - API: `http://127.0.0.1:8000`
   - Docs Swagger: `http://127.0.0.1:8000/docs`

## Variaveis de ambiente essenciais
```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4.1-mini
OPENAI_TIMEOUT_SECONDS=30
ALLOWED_ORIGINS=*
MAX_EMAIL_CHARS=12000
LOG_LEVEL=INFO
APP_ENV=development
```

## Endpoint principal
`POST /process-email`

Entrada:
- `application/json` com `email_text`
- ou `multipart/form-data` com `file` (`.txt` ou `.pdf`)

Saida:
```json
{
  "category": "Produtivo",
  "reply": "resposta automatica profissional"
}
```

## Deploy no Render (completo)
Fluxo recomendado: **2 servicos** no mesmo repositorio.

### 1) Backend (Web Service)
1. Suba o projeto no GitHub.
2. No Render, crie `New > Web Service`.
3. Conecte o repositorio e branch.
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Configure variaveis de ambiente do backend:
   - `OPENAI_API_KEY`
   - `OPENAI_MODEL` (ex.: `gpt-4.1-mini`)
   - `OPENAI_TIMEOUT_SECONDS`
   - `MAX_EMAIL_CHARS`
   - `LOG_LEVEL`
   - `APP_ENV=production`
   - `ALLOWED_ORIGINS` (URL do frontend em producao, ex.: `https://seu-frontend.onrender.com`)
6. Deploy e valide:
   - `https://seu-backend.onrender.com/health`
   - `https://seu-backend.onrender.com/docs`

### 2) Frontend (Static Site)
1. No Render, crie `New > Static Site`.
2. Use o mesmo repositorio.
3. Configure uma destas opcoes:
   - Opcao A: `Root Directory = frontend`, `Publish Directory = .`, Build vazio
   - Opcao B: `Root Directory` vazio, `Publish Directory = frontend`, Build vazio
4. Antes do deploy, ajuste a URL da API no frontend para o backend de producao.
   - Em `frontend/script.js`, altere para usar sua URL publica de backend no fallback.
5. Redeploy do frontend e teste o fluxo completo pela URL publica.

### Observacoes importantes
- O backend precisa escutar `0.0.0.0` e usar `$PORT` no Render.
- Se der erro de CORS no browser, revise `ALLOWED_ORIGINS` no backend com a URL exata do frontend.
