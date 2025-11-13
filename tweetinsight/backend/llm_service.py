"""LLM service for Q&A and summarization using OpenAI or Anthropic."""
from typing import List, Dict, Any, Optional
from .config import settings


class LLMService:
    """LLM service for intelligent querying and summarization."""

    def __init__(self):
        """Initialize LLM client based on provider."""
        self.provider = settings.LLM_PROVIDER.lower()
        self.client = None
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate LLM client."""
        if self.provider == "openai":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.model = settings.LLM_MODEL or "gpt-4-turbo-preview"
            except ImportError:
                print("OpenAI library not installed. Install with: pip install openai")
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")

        elif self.provider == "anthropic":
            try:
                from anthropic import Anthropic
                self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                self.model = settings.LLM_MODEL or "claude-3-5-sonnet-20241022"
            except ImportError:
                print("Anthropic library not installed. Install with: pip install anthropic")
            except Exception as e:
                print(f"Error initializing Anthropic client: {e}")

    def answer_question(
        self,
        question: str,
        relevant_tweets: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Answer a question based on relevant tweets.

        Args:
            question: User's question
            relevant_tweets: List of relevant tweet dictionaries
            conversation_history: Optional conversation history

        Returns:
            AI-generated answer
        """
        if not self.client:
            return "Error: LLM client not initialized. Please check your API keys."

        # Build context from tweets
        tweet_context = self._format_tweets_for_context(relevant_tweets)

        # Build system prompt
        system_prompt = """You are an AI research assistant for TweetInsight, helping users analyze and understand tweets from multiple Twitter/X accounts.

Your task is to:
1. Answer questions based ONLY on the provided tweets
2. Cite specific tweets using the format [@handle on DATE]
3. Provide balanced, objective analysis
4. If the tweets don't contain enough information, say so clearly
5. Highlight agreements, disagreements, or patterns across different accounts

Be concise but thorough. Always cite your sources."""

        # Build user prompt
        user_prompt = f"""Question: {question}

Relevant Tweets:
{tweet_context}

Please answer the question based on these tweets. Include specific citations."""

        try:
            if self.provider == "openai":
                messages = [{"role": "system", "content": system_prompt}]

                # Add conversation history if provided
                if conversation_history:
                    messages.extend(conversation_history)

                messages.append({"role": "user", "content": user_prompt})

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content

            elif self.provider == "anthropic":
                messages = []

                # Add conversation history if provided
                if conversation_history:
                    messages.extend(conversation_history)

                messages.append({"role": "user", "content": user_prompt})

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    system=system_prompt,
                    messages=messages
                )
                return response.content[0].text

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_summary(
        self,
        tweets: List[Dict[str, Any]],
        summary_type: str = "standard",
        focus_areas: Optional[List[str]] = None
    ) -> str:
        """
        Generate a summary of tweets.

        Args:
            tweets: List of tweet dictionaries
            summary_type: "brief", "standard", or "comprehensive"
            focus_areas: Optional list of topics to focus on

        Returns:
            AI-generated summary
        """
        if not self.client:
            return "Error: LLM client not initialized. Please check your API keys."

        # Build context from tweets
        tweet_context = self._format_tweets_for_context(tweets)

        # Adjust length based on summary type
        length_instructions = {
            "brief": "Provide a brief summary in 2-3 paragraphs.",
            "standard": "Provide a comprehensive summary in 4-6 paragraphs.",
            "comprehensive": "Provide a detailed, comprehensive summary with key themes, notable quotes, and insights. Use 8-10 paragraphs."
        }

        length_instruction = length_instructions.get(summary_type, length_instructions["standard"])

        # Build focus areas instruction
        focus_instruction = ""
        if focus_areas:
            focus_instruction = f"\n\nFocus particularly on these topics: {', '.join(focus_areas)}"

        # Build system prompt
        system_prompt = f"""You are an AI research assistant for TweetInsight, helping users synthesize insights from multiple Twitter/X accounts.

Your task is to:
1. Identify main themes and topics discussed in the tweets
2. Highlight key insights and perspectives from different accounts
3. Note areas of agreement or disagreement
4. Include relevant quotes with proper attribution [@handle]
5. Organize the summary in a clear, readable format

{length_instruction}{focus_instruction}"""

        user_prompt = f"""Please generate a summary of these tweets:

{tweet_context}

Summary:"""

        try:
            max_tokens = {
                "brief": 500,
                "standard": 1000,
                "comprehensive": 2000
            }.get(summary_type, 1000)

            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content

            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                return response.content[0].text

        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def extract_themes(self, tweets: List[Dict[str, Any]]) -> List[str]:
        """
        Extract main themes from tweets.

        Args:
            tweets: List of tweet dictionaries

        Returns:
            List of theme strings
        """
        if not self.client or len(tweets) == 0:
            return []

        tweet_context = self._format_tweets_for_context(tweets[:50])  # Limit for theme extraction

        system_prompt = """Extract the main themes and topics from these tweets. Return them as a simple list, one theme per line."""

        user_prompt = f"""Tweets:
{tweet_context}

Extract 5-10 main themes or topics discussed in these tweets. Return only the theme names, one per line."""

        try:
            if self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.5,
                    max_tokens=300
                )
                themes_text = response.choices[0].message.content

            elif self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=300,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}]
                )
                themes_text = response.content[0].text

            # Parse themes
            themes = [theme.strip('- ').strip() for theme in themes_text.split('\n') if theme.strip()]
            return themes[:10]

        except Exception as e:
            print(f"Error extracting themes: {e}")
            return []

    def _format_tweets_for_context(self, tweets: List[Dict[str, Any]]) -> str:
        """Format tweets for LLM context."""
        formatted_tweets = []
        for i, tweet in enumerate(tweets, 1):
            handle = tweet.get('handle', 'Unknown')
            text = tweet.get('text', '')
            created_at = tweet.get('created_at', 'Unknown date')
            likes = tweet.get('likes', 0)
            retweets = tweet.get('retweets', 0)

            # Format date
            try:
                from datetime import datetime
                if created_at and created_at != 'Unknown date':
                    dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    created_at = dt.strftime('%Y-%m-%d')
            except:
                pass

            formatted = f"""[{i}] {handle} ({created_at})
{text}
[Likes: {likes}, Retweets: {retweets}]
"""
            formatted_tweets.append(formatted)

        return "\n".join(formatted_tweets)


# Global LLM service instance
llm_service = LLMService()
