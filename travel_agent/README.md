# 🌍 Travel Planning Agent

A simple, conversational AI travel planning assistant powered by Claude's Python SDK. Get instant answers to your travel questions, plan itineraries, and receive personalized travel advice.

## Features

- 💬 **Conversational Interface** - Natural, chat-based interaction
- 🧠 **Smart Recommendations** - Powered by Claude AI
- 📝 **Context-Aware** - Remembers conversation history
- 🎯 **Travel-Focused** - Specialized in travel planning and advice
- ⚡ **Simple & Lightweight** - Easy to use Python SDK

## What Can It Help With?

- Destination recommendations
- Travel itinerary planning
- Best times to visit places
- Local attractions and activities
- Accommodation suggestions
- Budget planning
- Travel tips and safety advice
- Cultural insights and customs
- Transportation options
- Food and dining recommendations

## Installation

### 1. Clone the Repository

```bash
cd travel_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Key

1. Get your Anthropic API key from [https://console.anthropic.com/](https://console.anthropic.com/)
2. Create a `.env` file in the `travel_agent` directory:

```bash
cp .env.example .env
```

3. Edit `.env` and add your API key:

```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

## Usage

### Interactive Mode (Recommended)

Run the agent in interactive mode for a conversational experience:

```bash
python agent.py
```

**Example Session:**

```
🌍 Welcome to the Travel Planning Agent! 🌍
============================================================

🤔 You: I'm planning a trip to Japan in April. What should I know?

🤖 Travel Agent: Great choice! April is one of the best times to visit Japan...

🤔 You: What are must-visit places in Tokyo?

🤖 Travel Agent: Tokyo has amazing attractions! Here are the must-visits...

🤔 You: quit
```

### Programmatic Usage

Use the agent in your own Python scripts:

```python
from agent import TravelAgent

# Initialize the agent
agent = TravelAgent()

# Ask questions
response = agent.ask("What's the best time to visit Bali?")
print(response)

# Continue the conversation
response = agent.ask("What activities would you recommend there?")
print(response)

# Reset conversation if needed
agent.reset_conversation()
```

### With Custom API Key

```python
from agent import TravelAgent

# Pass API key directly (instead of using .env)
agent = TravelAgent(api_key="your_api_key_here")
response = agent.ask("Plan a 3-day trip to Paris")
print(response)
```

## Example Questions

Try asking the agent:

- "Plan a 5-day itinerary for Rome"
- "What's the best time to visit Iceland?"
- "I have $2000 for a week in Thailand. What can I do?"
- "What are some hidden gems in Barcelona?"
- "What should I pack for a winter trip to Norway?"
- "Are there any cultural customs I should know before visiting Morocco?"
- "What's the best way to get around in Amsterdam?"
- "Where can I find authentic street food in Vietnam?"

## Commands

When running in interactive mode:

- Type your question to get travel advice
- Type `reset` to start a fresh conversation
- Type `quit` or `exit` to end the session
- Press `Ctrl+C` to force quit

## Architecture

```
travel_agent/
├── agent.py              # Main agent script
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── .env                 # Your API key (create this)
└── README.md            # Documentation
```

## Key Components

### TravelAgent Class

- `__init__(api_key=None)` - Initialize with optional API key
- `ask(question)` - Ask a travel question and get a response
- `reset_conversation()` - Clear conversation history
- `get_conversation_history()` - Retrieve full conversation

### System Prompt

The agent is configured with a specialized system prompt that focuses on:
- Travel planning expertise
- Practical, actionable advice
- Friendly and helpful tone
- Honesty about limitations

## Requirements

- Python 3.7+
- `anthropic` - Official Anthropic Python SDK
- `python-dotenv` - Environment variable management

## Troubleshooting

### API Key Error

```
❌ Error: ANTHROPIC_API_KEY not found
```

**Solution:** Make sure you've created a `.env` file with your API key.

### Module Not Found

```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:** Install dependencies with `pip install -r requirements.txt`

### Rate Limits

If you hit rate limits, the agent will show an error. Wait a moment and try again.

## Customization

### Change the AI Model

Edit `agent.py` line 67:

```python
model="claude-3-5-sonnet-20241022",  # Change to another model
```

Available models:
- `claude-3-5-sonnet-20241022` (Recommended - Best performance)
- `claude-3-opus-20240229` (Most capable)
- `claude-3-haiku-20240307` (Fastest)

### Modify System Prompt

Edit the `system_prompt` in `agent.py` (lines 33-47) to customize the agent's behavior and expertise.

### Adjust Response Length

Edit `max_tokens` in `agent.py` line 68:

```python
max_tokens=2048,  # Increase for longer responses
```

## Cost Considerations

The agent uses Claude 3.5 Sonnet by default. Costs are based on:
- Input tokens (conversation history + question)
- Output tokens (response)

Check current pricing at [https://www.anthropic.com/pricing](https://www.anthropic.com/pricing)

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review Anthropic's documentation: [https://docs.anthropic.com/](https://docs.anthropic.com/)
3. Open an issue in the repository

---

**Built with ❤️ using Claude API**
