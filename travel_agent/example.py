#!/usr/bin/env python3
"""
Example usage of the Travel Planning Agent
Demonstrates how to use the agent programmatically.
"""

from agent import TravelAgent


def example_single_question():
    """Example: Ask a single question."""
    print("\n" + "=" * 60)
    print("Example 1: Single Question")
    print("=" * 60)

    agent = TravelAgent()
    question = "What are the top 3 destinations to visit in Europe in summer?"

    print(f"\nQuestion: {question}")
    print("\nAnswer:")
    response = agent.ask(question)
    print(response)


def example_conversation():
    """Example: Have a multi-turn conversation."""
    print("\n" + "=" * 60)
    print("Example 2: Multi-turn Conversation")
    print("=" * 60)

    agent = TravelAgent()

    questions = [
        "I want to plan a trip to Thailand for 10 days. What's a good itinerary?",
        "What's the best time of year to visit?",
        "What's the approximate budget I should plan for?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question}")
        print("\nAnswer:")
        response = agent.ask(question)
        print(response)
        print("\n" + "-" * 60)


def example_trip_planning():
    """Example: Plan a complete trip."""
    print("\n" + "=" * 60)
    print("Example 3: Complete Trip Planning")
    print("=" * 60)

    agent = TravelAgent()

    # Define trip parameters
    trip_info = {
        "destination": "Bali",
        "duration": "7 days",
        "travelers": "couple",
        "interests": "beaches, culture, and food"
    }

    # Build the question
    question = f"""I'm planning a {trip_info['duration']} trip to {trip_info['destination']}
    for a {trip_info['travelers']}. We're interested in {trip_info['interests']}.
    Can you create a day-by-day itinerary with accommodation suggestions?"""

    print(f"\nTrip Details: {trip_info}")
    print(f"\nQuestion: {question.strip()}")
    print("\nItinerary:")
    response = agent.ask(question)
    print(response)

    # Follow-up questions
    follow_ups = [
        "What should we pack?",
        "Any safety tips?"
    ]

    for follow_up in follow_ups:
        print(f"\n\nFollow-up: {follow_up}")
        print("Answer:")
        response = agent.ask(follow_up)
        print(response)


def example_conversation_history():
    """Example: Working with conversation history."""
    print("\n" + "=" * 60)
    print("Example 4: Conversation History")
    print("=" * 60)

    agent = TravelAgent()

    # Ask a few questions
    agent.ask("What's special about Kyoto?")
    agent.ask("When is cherry blossom season there?")

    # Get conversation history
    history = agent.get_conversation_history()

    print(f"\nConversation has {len(history) // 2} exchanges")
    print("\nConversation History:")
    for msg in history:
        role = "User" if msg["role"] == "user" else "Agent"
        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
        print(f"\n{role}: {content}")

    # Reset conversation
    print("\n\nResetting conversation...")
    agent.reset_conversation()
    print(f"History length after reset: {len(agent.get_conversation_history())}")


def main():
    """Run all examples."""
    print("\n🌍 Travel Planning Agent - Usage Examples 🌍\n")

    try:
        # Run examples
        example_single_question()
        input("\nPress Enter to continue to next example...")

        example_conversation()
        input("\nPress Enter to continue to next example...")

        example_trip_planning()
        input("\nPress Enter to continue to next example...")

        example_conversation_history()

        print("\n\n✅ All examples completed!")
        print("Now try running: python agent.py")

    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Created a .env file with ANTHROPIC_API_KEY")
        print("2. Installed requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
