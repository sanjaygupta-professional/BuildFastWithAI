# Quick Start Guide

Get your Travel Planning Agent running in 3 minutes!

## Step 1: Install Dependencies

```bash
cd travel_agent
pip install -r requirements.txt
```

## Step 2: Get Your API Key

1. Visit [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key

## Step 3: Configure API Key

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and paste your API key:

```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
```

## Step 4: Run the Agent

### Option A: Interactive Mode (Chat)

```bash
python agent.py
```

Then start asking travel questions!

### Option B: See Examples First

```bash
python example.py
```

This will show you how to use the agent programmatically.

## Your First Question

Try asking:

```
I'm planning a trip to Paris for 5 days. What should I see?
```

## That's it! 🎉

You now have a fully functional AI travel planning agent.

---

**Need Help?**
- See [README.md](README.md) for full documentation
- Check [example.py](example.py) for code examples
- Visit [Anthropic Docs](https://docs.anthropic.com/) for API details
