# 🐦 TweetInsight - Twitter Research Application

Transform scattered Twitter conversations into structured, searchable knowledge bases with AI-powered synthesis and insights.

## 📋 Overview

TweetInsight enables knowledge workers to efficiently synthesize insights from multiple Twitter/X thought leaders by:
- Aggregating tweets from up to 5 selected handles
- Storing tweets in a structured, searchable database
- Enabling natural language querying with AI
- Generating comprehensive summaries with citations
- Exporting research findings in multiple formats

## ✨ Features

### Core Features (MVP)
- **🎯 Twitter Handle Selection**: Add up to 5 Twitter handles per research collection
- **📥 Tweet Aggregation**: Automatically fetch and store tweets (up to 200 per handle)
- **🔍 Intelligent Querying**: Ask natural language questions about your tweet collection
- **📊 Summary Generation**: Create brief, standard, or comprehensive summaries
- **💾 Export Options**: Download summaries as Markdown, Text, or CSV

### Technical Features
- **Semantic Search**: ChromaDB vector store for intelligent tweet retrieval
- **LLM Integration**: Support for OpenAI (GPT-4) and Anthropic (Claude) APIs
- **Conversation History**: Context-aware follow-up questions
- **Source Attribution**: Every answer includes citations to source tweets
- **Theme Extraction**: Automatically identify key topics and themes

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Twitter API credentials (Bearer Token or OAuth)
- OpenAI or Anthropic API key

### Installation

1. **Clone the repository**
```bash
cd tweetinsight
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Run the application**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🔑 API Configuration

### Twitter API Setup

1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Create a new project and app
3. Generate a Bearer Token (recommended) or OAuth credentials
4. Add to `.env`:

```env
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

### LLM API Setup

**Option 1: OpenAI (Recommended)**
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Add to `.env`:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
LLM_MODEL=gpt-4-turbo-preview
```

**Option 2: Anthropic**
1. Get API key from [Anthropic Console](https://console.anthropic.com/)
2. Add to `.env`:

```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_api_key_here
LLM_MODEL=claude-3-5-sonnet-20241022
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. **Build and run**
```bash
docker-compose up -d
```

3. **Access the application**
```
http://localhost:8501
```

4. **View logs**
```bash
docker-compose logs -f
```

5. **Stop the application**
```bash
docker-compose down
```

### Using Docker Directly

```bash
# Build image
docker build -t tweetinsight .

# Run container
docker run -p 8501:8501 -v $(pwd)/data:/app/data --env-file .env tweetinsight
```

## ☁️ Cloud Deployment

### Deploy to Streamlit Cloud (Free)

1. **Push to GitHub**
```bash
git add .
git commit -m "Add TweetInsight application"
git push
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select the `tweetinsight` folder
   - Set `app.py` as the main file
   - Add your API keys in "Secrets" section:

```toml
TWITTER_BEARER_TOKEN = "your_token"
OPENAI_API_KEY = "your_key"
LLM_PROVIDER = "openai"
```

### Deploy to Heroku

1. **Create Heroku app**
```bash
heroku create your-app-name
```

2. **Set environment variables**
```bash
heroku config:set TWITTER_BEARER_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
heroku config:set LLM_PROVIDER=openai
```

3. **Create Procfile**
```bash
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
```

4. **Deploy**
```bash
git push heroku main
```

### Deploy to AWS/GCP/Azure

Use the Docker image with your preferred cloud service:
- **AWS ECS**: Use Docker Compose or ECS task definitions
- **Google Cloud Run**: Deploy containerized Streamlit app
- **Azure Container Instances**: Run the Docker image

## 📖 Usage Guide

### 1. Create a Collection

1. Navigate to **Collections** page
2. Enter a collection name (e.g., "AI Research")
3. Add Twitter handles (e.g., @elonmusk, @sama, @ylecun)
4. Click **Create Collection**
5. Wait for tweets to be fetched and indexed

### 2. Ask Questions

1. Navigate to **Research** page
2. Select your collection from the sidebar
3. Type a question (e.g., "What are the main concerns about AGI?")
4. Click **Ask**
5. View the AI-generated answer with source citations

### 3. Generate Summaries

1. Navigate to **Summaries** page
2. Select summary length (brief/standard/comprehensive)
3. Optionally filter by specific handles
4. Click **Generate Summary**
5. Download as Markdown, Text, or CSV

## 🏗️ Architecture

```
tweetinsight/
├── app.py                      # Main Streamlit application
├── backend/
│   ├── __init__.py
│   ├── config.py              # Configuration management
│   ├── database.py            # SQLite database operations
│   ├── twitter_client.py      # Twitter API integration
│   ├── vector_store.py        # ChromaDB for semantic search
│   └── llm_service.py         # LLM integration (OpenAI/Anthropic)
├── data/                       # Data storage (auto-created)
│   ├── tweetinsight.db        # SQLite database
│   └── chromadb/              # Vector store
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This file
```

## 🔧 Configuration

All settings can be configured via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `TWITTER_BEARER_TOKEN` | Twitter API Bearer Token | Required |
| `LLM_PROVIDER` | LLM provider (openai/anthropic) | openai |
| `OPENAI_API_KEY` | OpenAI API key | Required if using OpenAI |
| `ANTHROPIC_API_KEY` | Anthropic API key | Required if using Anthropic |
| `MAX_HANDLES_PER_COLLECTION` | Max handles per collection | 5 |
| `MAX_TWEETS_PER_HANDLE` | Max tweets to fetch per handle | 200 |
| `DATABASE_PATH` | SQLite database path | ./data/tweetinsight.db |
| `VECTOR_DB_PATH` | ChromaDB storage path | ./data/chromadb |

## 📊 Data Storage

- **SQLite Database**: Stores collections, tweets, and query history
- **ChromaDB**: Vector embeddings for semantic search
- **Local Storage**: All data stored locally in `./data/` directory

## 🔐 Privacy & Security

- All data stored locally on your machine or server
- API keys stored in `.env` file (never committed to git)
- No data sent to third parties except API providers
- Tweets fetched only from public Twitter accounts

## 🐛 Troubleshooting

### Twitter API Errors

**Error: "401 Unauthorized"**
- Check your Twitter API credentials
- Ensure Bearer Token is valid
- Verify app permissions in Twitter Developer Portal

**Error: "429 Rate Limit Exceeded"**
- Twitter API has rate limits
- Wait for the rate limit window to reset
- Consider upgrading Twitter API tier

### LLM API Errors

**Error: "Invalid API Key"**
- Verify API key is correct in `.env`
- Check for extra spaces or quotes
- Ensure key has proper permissions

**Error: "Insufficient Credits"**
- Check your OpenAI/Anthropic account balance
- Add credits to your account

### Application Issues

**Port already in use**
```bash
# Change port in run command
streamlit run app.py --server.port=8502
```

**ChromaDB errors**
```bash
# Clear vector store
rm -rf data/chromadb
# Restart application
```

## 📝 Development

### Running in Development Mode

```bash
# Enable debug mode
export DEBUG=true

# Run with auto-reload
streamlit run app.py --server.runOnSave=true
```

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests (when available)
pytest tests/
```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Twitter API via [Tweepy](https://www.tweepy.org/)
- Vector search with [ChromaDB](https://www.trychroma.com/)
- LLM APIs: [OpenAI](https://openai.com/) and [Anthropic](https://www.anthropic.com/)

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the PRD document for detailed specifications
- Review the deployment guide above

## 🗺️ Roadmap

### Phase 2 Features (Coming Soon)
- Visualization & Analytics (word clouds, timelines)
- Advanced filtering (sentiment, engagement)
- Collaboration features (shared collections)
- Smart alerts (topic notifications)
- PDF export with formatting
- Multi-user support with authentication

---

**Built with ❤️ for researchers, analysts, and knowledge workers**
