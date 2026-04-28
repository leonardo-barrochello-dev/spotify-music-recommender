# 🎵 Spotify Music Recommender

Sistema de recomendação de músicas full-stack usando Spotify API e TensorFlow, com frontend em TypeScript.

## 🎯 Visão Geral

Este projeto é um sistema de recomendação musical que:
- ✅ Autentica usuários via Spotify OAuth 2.0
- ✅ Analisa os top tracks e artists do usuário
- ✅ Usa **TensorFlow** para calcular similaridade de cosine entre vetores de features
- ✅ Gera recomendações personalizadas baseadas nas preferências do usuário
- ✅ Permite criar playlists diretamente no Spotify
- ✅ **Frontend TypeScript** para type safety completa

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Framework Python
- **TensorFlow** - ML para similaridade de vetores
- **HTTPX** - Cliente HTTP assíncrono
- **Pydantic** - Validação de dados

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS 3** - Estilização
- **React Router** - Navegação
- **Axios** - HTTP client

## 📋 Pré-requisitos

1. **Python 3.10+**
2. **Node.js 18+**
3. **Spotify Developer Account**

### Configurar Spotify App

1. Acesse https://developer.spotify.com/dashboard
2. Crie um novo app
3. Adicione Redirect URI: `http://127.0.0.1:8000/auth/callback`
4. Copie **Client ID** e **Client Secret**

## 🚀 Instalação

### 1. Clone o repositório

```bash
cd spotify-music-recommender
```

### 2. Setup do Backend

```bash
cd backend

# Criar ambiente virtual local
C:\Users\Interfocus\AppData\Local\Programs\Python\Python313\python.exe -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
copy .env.example .env
```

Edite `backend\.env` com suas credenciais do Spotify:

```env
SPOTIFY_CLIENT_ID=SEU_CLIENT_ID
SPOTIFY_CLIENT_SECRET=SEU_CLIENT_SECRET
REDIRECT_URI=http://127.0.0.1:8000/auth/callback
FRONTEND_URL=http://localhost:5173
SECRET_KEY=sua_chave_secreta_aleatoria
```

### 3. Setup do Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Copiar ambiente (opcional)
copy .env.example .env
```

## ▶️ Rodando a Aplicação

### Terminal 1 - Backend

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

Backend disponível em:
- **API:** http://127.0.0.1:8000
- **Docs:** http://127.0.0.1:8000/docs
- **Health:** http://127.0.0.1:8000/health

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

Frontend disponível em: http://localhost:3000

## 🎮 Como Usar

1. **Login**
   - Acesse http://localhost:5173
   - Clique em "Login with Spotify"
   - Autorize o app no Spotify

2. **Dashboard**
   - Veja seus top tracks e artists
   - Filtre por período (4 semanas, 6 meses, todo período)

3. **Recommendations**
   - Selecione um mood (happy, chill, workout, etc.)
   - Veja recomendações baseadas no seu gosto
   - Clique em "Create Playlist" para salvar no Spotify

4. **Spotify Integration**
   - Play: Abre a música no Spotify
   - Create Playlist: Cria playlist com tracks recomendadas

## 📁 Estrutura do Projeto

```
spotify-music-recommender/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app
│   │   ├── config.py               # Settings
│   │   ├── dependencies.py         # Auth dependencies
│   │   ├── models/
│   │   │   └── schemas.py          # Pydantic models
│   │   ├── services/
│   │   │   ├── auth_service.py     # OAuth2
│   │   │   ├── spotify_service.py  # Spotify API
│   │   │   └── token_service.py    # Token management
│   │   ├── routers/
│   │   │   ├── auth.py             # Auth endpoints
│   │   │   ├── user.py             # User endpoints
│   │   │   └── recommendations.py  # Recommendation endpoints
│   │   ├── ml/
│   │   │   ├── feature_engineering.py  # Feature extraction
│   │   │   ├── similarity_model.py     # TensorFlow similarity
│   │   │   └── recommendation_engine.py # ML pipeline
│   │   └── utils/
│   │       └── security.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   ├── types/
│   │   │   └── spotify.ts          # TypeScript types
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── hooks/
│   │   └── utils/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── README.md
│
├── .gitignore
├── README.md
├── QUICKSTART.md
├── setup.bat
├── start-backend.bat
└── start-frontend.bat
```

## 🧠 Machine Learning

### Feature Vector (6 dimensões)
Cada track é representado por:
1. **danceability** (0-1)
2. **energy** (0-1)
3. **valence** (0-1)
4. **tempo** (normalizado 60-200 BPM)
5. **acousticness** (0-1)
6. **instrumentalness** (0-1)

### Pipeline

```
1. Feature Engineering
   └── Extrair features do Spotify API
   └── Normalizar tempo para [0, 1]

2. User Vector
   └── Média dos vetores dos top tracks do usuário

3. Candidate Generation
   └── Pegar related artists dos top artists
   └── Pegar top tracks dos related artists
   └── Filtrar tracks já conhecidas

4. Similarity Computation (TensorFlow)
   └── Cosine similarity: user_vector vs candidate_matrix
   └── tf.nn.l2_normalize + tf.linalg.dot

5. Ranking
   └── Ordenar por score de similaridade
   └── Retornar top N recommendations
```

### Mood Filters

Os moods ajustam o user vector com pesos específicos:
- **Happy**: ↑ valence, ↑ energy, ↑ danceability
- **Chill**: ↓ energy, ↑ acousticness
- **Workout**: ↑ energy, ↑ danceability, ↑ tempo
- **Sad**: ↓ valence, ↓ energy, ↑ acousticness
- **Energetic**: ↑ energy, ↑ tempo

## 🔌 API Endpoints

### Authentication
- `GET /auth/login` - Redirect Spotify OAuth
- `GET /auth/callback` - OAuth callback
- `GET /auth/logout` - Logout user

### User
- `GET /user/profile` - User profile
- `GET /user/top-tracks` - Top tracks
- `GET /user/top-artists` - Top artists
- `GET /user/profile/full` - Full profile

### Recommendations
- `GET /recommendations/?limit=20&mood=happy` - Get recommendations
- `POST /recommendations/playlist/create` - Create playlist
- `POST /recommendations/playlist/from-recommendations` - Create from recs

## 🔒 Segurança

- OAuth 2.0 com state parameter para CSRF protection
- Tokens armazenados em memória (backend)
- Session tokens com expiração de 7 dias
- CORS configurado para frontend específico
- HTTPS recomendado em produção

## 🐛 Troubleshooting

### Backend não inicia
```bash
cd backend
venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

### Frontend TypeScript errors
```bash
cd frontend
npx tsc --noEmit  # Check for type errors
```

### Frontend não conecta ao backend
- Verificar se backend está rodando em `http://127.0.0.1:8000`
- Verificar CORS no `backend/app/main.py`
- Limpar localStorage do navegador

### Erro de autenticação Spotify
- Verificar se Client ID e Secret estão corretos no `.env`
- Verificar se Redirect URI está configurado no Spotify Dashboard
- Verificar se scopes estão corretos

## 📝 Notas

- Tokens do Spotify expiram após 1 hora (refresh automático implementado)
- Rate limiting do Spotify: ~180 requests/minuto
- Requer conta Spotify Premium para playback completo

## 🎯 Próximos Passos (Bonus Features)

- [ ] Cache de recomendações (Redis)
- [ ] Histórico de recomendações
- [ ] Share de playlists
- [ ] Filtros avançados (década, gênero)
- [ ] Deploy em produção (Docker + AWS/GCP)

## 📄 License

MIT License

## 👥 Autor

Desenvolvido como projeto full-stack de recomendação musical com Spotify API e TensorFlow.
