#!/usr/bin/env python3
"""
Simple Travel Planning Agent using Claude API
A conversational agent that helps with travel planning questions and answers.
"""

import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class TravelAgent:
    """Simple travel planning agent powered by Claude."""

    def __init__(self, api_key=None):
        """
        Initialize the Travel Agent.

        Args:
            api_key (str, optional): Anthropic API key. If not provided,
                                    will try to load from environment.
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. "
                "Please set it in .env file or pass it to the constructor."
            )

        self.client = Anthropic(api_key=self.api_key)
        self.conversation_history = []
        self.system_prompt = """You are a helpful and knowledgeable travel planning assistant.
You help users plan their trips by providing information about:
- Destination recommendations
- Travel itineraries and schedules
- Best times to visit places
- Local attractions and activities
- Accommodation suggestions
- Budget planning for trips
- Travel tips and safety advice
- Cultural insights and local customs
- Transportation options
- Food and dining recommendations

Be friendly, concise, and practical. Provide specific, actionable advice.
If you don't know something, be honest about it."""

    def ask(self, question):
        """
        Ask the travel agent a question.

        Args:
            question (str): The travel-related question to ask.

        Returns:
            str: The agent's response.
        """
        # Add user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })

        # Get response from Claude
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system=self.system_prompt,
            messages=self.conversation_history
        )

        # Extract the assistant's response
        assistant_message = response.content[0].text

        # Add assistant response to conversation history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = []
        print("Conversation history cleared.")

    def get_conversation_history(self):
        """Get the full conversation history."""
        return self.conversation_history


def main():
    """Main interactive loop for the travel agent."""
    print("=" * 60)
    print("🌍 Welcome to the Travel Planning Agent! 🌍")
    print("=" * 60)
    print("\nI'm your AI travel assistant powered by Claude.")
    print("Ask me anything about travel planning!\n")
    print("Commands:")
    print("  - Type your question to get travel advice")
    print("  - Type 'reset' to start a new conversation")
    print("  - Type 'quit' or 'exit' to end the session")
    print("=" * 60)

    try:
        agent = TravelAgent()
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease create a .env file with your ANTHROPIC_API_KEY")
        print("Example: ANTHROPIC_API_KEY=sk-ant-xxxxx")
        return

    while True:
        try:
            # Get user input
            user_input = input("\n🤔 You: ").strip()

            # Check for commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thanks for using Travel Planning Agent. Safe travels!")
                break

            if user_input.lower() == 'reset':
                agent.reset_conversation()
                continue

            if not user_input:
                continue

            # Get response from agent
            print("\n🤖 Travel Agent: ", end="", flush=True)
            response = agent.ask(user_input)
            print(response)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Safe travels!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again or type 'quit' to exit.")


if __name__ == "__main__":
    main()
