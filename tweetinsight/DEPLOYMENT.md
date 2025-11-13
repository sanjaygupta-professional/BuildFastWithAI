# 🚀 TweetInsight Deployment Guide

This guide covers various deployment options for TweetInsight, from local development to cloud production.

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Streamlit Cloud (Free)](#streamlit-cloud)
3. [Heroku](#heroku)
4. [AWS](#aws)
5. [Google Cloud Platform](#google-cloud-platform)
6. [Azure](#azure)
7. [Docker Deployment](#docker-deployment)
8. [VPS Deployment](#vps-deployment)

---

## 🏠 Local Development

### Quick Start

```bash
# Navigate to project directory
cd tweetinsight

# Run the startup script
./run.sh
```

### Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Run the application
streamlit run app.py
```

Access at: `http://localhost:8501`

---

## ☁️ Streamlit Cloud

**Best for**: Quick demos, free hosting, sharing with team

### Steps

1. **Prepare Repository**
```bash
git add .
git commit -m "Add TweetInsight application"
git push origin main
```

2. **Deploy to Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your GitHub repository
   - Set main file path: `tweetinsight/app.py`
   - Click "Deploy"

3. **Configure Secrets**
   - In app settings, go to "Secrets"
   - Add your API keys in TOML format:

```toml
# Twitter API
TWITTER_BEARER_TOKEN = "your_bearer_token_here"

# LLM API (choose one)
LLM_PROVIDER = "openai"
OPENAI_API_KEY = "your_openai_key_here"
# OR
# LLM_PROVIDER = "anthropic"
# ANTHROPIC_API_KEY = "your_anthropic_key_here"

# Optional: Override defaults
MAX_HANDLES_PER_COLLECTION = 5
MAX_TWEETS_PER_HANDLE = 200
```

4. **Reboot App**
   - Click "Reboot app" to apply secrets

**Pros**:
- Free for public apps
- Easy deployment
- Automatic updates from GitHub
- SSL certificate included

**Cons**:
- Limited resources (free tier)
- Public by default
- Data storage not persistent (use external DB for production)

---

## 🟣 Heroku

**Best for**: Small to medium apps, easy scaling

### Prerequisites
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login
```

### Deployment Steps

1. **Create Heroku App**
```bash
cd tweetinsight
heroku create your-app-name
```

2. **Add Buildpack**
```bash
heroku buildpacks:set heroku/python
```

3. **Create Procfile**
```bash
echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
```

4. **Set Environment Variables**
```bash
heroku config:set TWITTER_BEARER_TOKEN=your_token
heroku config:set OPENAI_API_KEY=your_key
heroku config:set LLM_PROVIDER=openai
```

5. **Deploy**
```bash
git add .
git commit -m "Configure for Heroku"
git push heroku main
```

6. **Open App**
```bash
heroku open
```

**Scaling**:
```bash
# Scale dynos
heroku ps:scale web=1

# View logs
heroku logs --tail
```

**Pros**:
- Easy deployment
- Built-in monitoring
- Add-ons for databases, logging
- Free tier available

**Cons**:
- Dynos sleep after inactivity (free tier)
- More expensive for production
- Limited storage on ephemeral filesystem

---

## 🟠 AWS

**Best for**: Production apps, enterprise scale

### Option 1: AWS Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB**
```bash
cd tweetinsight
eb init -p python-3.11 tweetinsight

# Create environment
eb create tweetinsight-env
```

3. **Configure Environment Variables**
```bash
eb setenv TWITTER_BEARER_TOKEN=your_token \
          OPENAI_API_KEY=your_key \
          LLM_PROVIDER=openai
```

4. **Deploy**
```bash
eb deploy
```

5. **Open**
```bash
eb open
```

### Option 2: AWS ECS with Docker

1. **Build and Push Docker Image**
```bash
# Create ECR repository
aws ecr create-repository --repository-name tweetinsight

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t tweetinsight .
docker tag tweetinsight:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/tweetinsight:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/tweetinsight:latest
```

2. **Create ECS Task Definition**
   - Use AWS Console or CLI to create task
   - Set environment variables
   - Map port 8501

3. **Create ECS Service**
   - Deploy task to ECS cluster
   - Configure load balancer
   - Set auto-scaling

**Pros**:
- Highly scalable
- Full AWS ecosystem integration
- Professional features (monitoring, backups)

**Cons**:
- More complex setup
- Higher cost
- Requires AWS knowledge

---

## 🔵 Google Cloud Platform

**Best for**: GCP users, Cloud Run simplicity

### Cloud Run Deployment

1. **Build Container**
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/tweetinsight
```

2. **Deploy to Cloud Run**
```bash
gcloud run deploy tweetinsight \
  --image gcr.io/PROJECT_ID/tweetinsight \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars TWITTER_BEARER_TOKEN=your_token,OPENAI_API_KEY=your_key,LLM_PROVIDER=openai
```

3. **Access URL**
```bash
gcloud run services describe tweetinsight --format='value(status.url)'
```

**Pros**:
- Serverless, pay per use
- Auto-scaling
- Easy HTTPS setup
- Good free tier

**Cons**:
- Cold starts
- Request timeout limits

---

## 🔷 Azure

**Best for**: Azure/Microsoft ecosystem users

### Azure Container Instances

1. **Create Resource Group**
```bash
az group create --name tweetinsight-rg --location eastus
```

2. **Create Container Registry**
```bash
az acr create --resource-group tweetinsight-rg --name tweetinsightacr --sku Basic
```

3. **Build and Push Image**
```bash
az acr build --registry tweetinsightacr --image tweetinsight:latest .
```

4. **Deploy Container**
```bash
az container create \
  --resource-group tweetinsight-rg \
  --name tweetinsight \
  --image tweetinsightacr.azurecr.io/tweetinsight:latest \
  --dns-name-label tweetinsight-app \
  --ports 8501 \
  --environment-variables \
    TWITTER_BEARER_TOKEN=your_token \
    OPENAI_API_KEY=your_key \
    LLM_PROVIDER=openai
```

5. **Get FQDN**
```bash
az container show --resource-group tweetinsight-rg --name tweetinsight --query ipAddress.fqdn
```

**Pros**:
- Simple container deployment
- Integration with Azure services
- Enterprise features

**Cons**:
- More expensive than some alternatives
- Requires Azure familiarity

---

## 🐳 Docker Deployment

**Best for**: Consistent environments, any platform

### Docker Compose (Recommended)

1. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. **Start Application**
```bash
docker-compose up -d
```

3. **View Logs**
```bash
docker-compose logs -f
```

4. **Stop Application**
```bash
docker-compose down
```

### Docker Only

```bash
# Build
docker build -t tweetinsight .

# Run
docker run -d \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  --name tweetinsight \
  tweetinsight

# Logs
docker logs -f tweetinsight

# Stop
docker stop tweetinsight
docker rm tweetinsight
```

---

## 🖥️ VPS Deployment

**Best for**: DigitalOcean, Linode, Vultr, etc.

### Setup on Ubuntu 22.04

1. **Connect to VPS**
```bash
ssh root@your_vps_ip
```

2. **Install Dependencies**
```bash
# Update system
apt update && apt upgrade -y

# Install Python and tools
apt install python3.11 python3-pip git -y

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

3. **Clone Repository**
```bash
cd /opt
git clone https://github.com/yourusername/BuildFastWithAI.git
cd BuildFastWithAI/tweetinsight
```

4. **Configure Application**
```bash
cp .env.example .env
nano .env  # Add your API keys
```

5. **Option A: Run with Docker**
```bash
docker-compose up -d
```

6. **Option B: Run with Systemd**

Create service file:
```bash
nano /etc/systemd/system/tweetinsight.service
```

Add content:
```ini
[Unit]
Description=TweetInsight Application
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/BuildFastWithAI/tweetinsight
ExecStart=/usr/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
Environment="PATH=/usr/bin"

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
systemctl daemon-reload
systemctl enable tweetinsight
systemctl start tweetinsight
systemctl status tweetinsight
```

7. **Setup Nginx Reverse Proxy**
```bash
apt install nginx -y

# Create nginx config
nano /etc/nginx/sites-available/tweetinsight
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
ln -s /etc/nginx/sites-available/tweetinsight /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

8. **Setup SSL with Let's Encrypt**
```bash
apt install certbot python3-certbot-nginx -y
certbot --nginx -d your-domain.com
```

**Access**: `https://your-domain.com`

---

## 🔒 Security Best Practices

### Environment Variables
- Never commit `.env` to git
- Use secrets management in production (AWS Secrets Manager, Azure Key Vault, etc.)
- Rotate API keys regularly

### Network Security
- Use HTTPS in production
- Configure firewall rules
- Implement rate limiting
- Use VPC/private networks for cloud deployments

### Application Security
- Keep dependencies updated
- Enable Streamlit authentication for sensitive data
- Monitor API usage and costs
- Implement backup strategies

---

## 📊 Monitoring & Maintenance

### Logging
```bash
# Streamlit logs
streamlit run app.py --logger.level=debug

# Docker logs
docker logs -f tweetinsight

# Systemd logs
journalctl -u tweetinsight -f
```

### Health Checks
```bash
# Check if app is running
curl http://localhost:8501/_stcore/health
```

### Backups
```bash
# Backup data directory
tar -czf tweetinsight-backup-$(date +%Y%m%d).tar.gz data/

# Automated backup script
0 2 * * * cd /opt/BuildFastWithAI/tweetinsight && tar -czf ~/backups/tweetinsight-$(date +\%Y\%m\%d).tar.gz data/
```

---

## 🆘 Troubleshooting

### Common Issues

**Port already in use**
```bash
# Find process
lsof -i :8501

# Kill process
kill -9 PID
```

**Permission denied**
```bash
# Fix data directory permissions
chmod -R 755 data/
```

**Out of memory**
```bash
# Check memory usage
free -h

# Increase Docker memory limit
docker run -m 2g ...
```

---

## 📞 Support

For deployment issues:
1. Check application logs
2. Verify API credentials
3. Review deployment guide
4. Create GitHub issue with details

---

**Happy Deploying! 🚀**
