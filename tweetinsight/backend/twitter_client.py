"""Twitter API integration for fetching tweets."""
import tweepy
from typing import List, Dict, Any, Optional
from datetime import datetime
from .config import settings


class TwitterClient:
    """Twitter API client for fetching tweets from handles."""

    def __init__(self):
        """Initialize Twitter API client."""
        self.client = None
        self.api = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Twitter API."""
        # Try bearer token authentication (API v2)
        if settings.TWITTER_BEARER_TOKEN:
            self.client = tweepy.Client(
                bearer_token=settings.TWITTER_BEARER_TOKEN,
                wait_on_rate_limit=True
            )

        # Try OAuth 1.0a authentication (API v1.1) for more features
        if all([
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET,
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_SECRET
        ]):
            auth = tweepy.OAuthHandler(
                settings.TWITTER_API_KEY,
                settings.TWITTER_API_SECRET
            )
            auth.set_access_token(
                settings.TWITTER_ACCESS_TOKEN,
                settings.TWITTER_ACCESS_SECRET
            )
            self.api = tweepy.API(auth, wait_on_rate_limit=True)

            # Also create v2 client with OAuth
            if not self.client:
                self.client = tweepy.Client(
                    consumer_key=settings.TWITTER_API_KEY,
                    consumer_secret=settings.TWITTER_API_SECRET,
                    access_token=settings.TWITTER_ACCESS_TOKEN,
                    access_token_secret=settings.TWITTER_ACCESS_SECRET,
                    wait_on_rate_limit=True
                )

    def verify_credentials(self) -> bool:
        """Verify Twitter API credentials."""
        try:
            if self.client:
                # Try a simple request to verify credentials
                self.client.get_me()
                return True
            return False
        except Exception as e:
            print(f"Authentication error: {e}")
            return False

    def get_user_info(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information by username."""
        try:
            # Remove @ if present
            username = username.lstrip('@')

            if self.client:
                user = self.client.get_user(
                    username=username,
                    user_fields=['public_metrics', 'description', 'profile_image_url']
                )
                if user.data:
                    return {
                        'id': user.data.id,
                        'username': user.data.username,
                        'name': user.data.name,
                        'description': user.data.description,
                        'followers_count': user.data.public_metrics.get('followers_count', 0),
                        'following_count': user.data.public_metrics.get('following_count', 0),
                        'tweet_count': user.data.public_metrics.get('tweet_count', 0),
                        'profile_image_url': user.data.profile_image_url
                    }
            return None
        except Exception as e:
            print(f"Error fetching user info for {username}: {e}")
            return None

    def fetch_user_tweets(
        self,
        username: str,
        max_tweets: int = 200,
        exclude_replies: bool = True,
        exclude_retweets: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Fetch tweets from a user's timeline.

        Args:
            username: Twitter username (with or without @)
            max_tweets: Maximum number of tweets to fetch
            exclude_replies: Exclude reply tweets
            exclude_retweets: Exclude retweets

        Returns:
            List of tweet dictionaries
        """
        tweets = []
        try:
            # Remove @ if present
            username = username.lstrip('@')

            # Get user ID
            user_info = self.get_user_info(username)
            if not user_info:
                return []

            user_id = user_info['id']

            # Build exclusions
            exclusions = []
            if exclude_replies:
                exclusions.append('replies')
            if exclude_retweets:
                exclusions.append('retweets')

            # Fetch tweets using API v2
            if self.client:
                response = self.client.get_users_tweets(
                    id=user_id,
                    max_results=min(max_tweets, 100),  # API limit is 100 per request
                    tweet_fields=['created_at', 'public_metrics', 'entities', 'conversation_id'],
                    exclude=exclusions if exclusions else None
                )

                if response.data:
                    for tweet in response.data:
                        tweet_data = {
                            'tweet_id': str(tweet.id),
                            'handle': f"@{username}",
                            'username': user_info['name'],
                            'text': tweet.text,
                            'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
                            'likes': tweet.public_metrics.get('like_count', 0) if tweet.public_metrics else 0,
                            'retweets': tweet.public_metrics.get('retweet_count', 0) if tweet.public_metrics else 0,
                            'replies': tweet.public_metrics.get('reply_count', 0) if tweet.public_metrics else 0,
                            'url': f"https://twitter.com/{username}/status/{tweet.id}"
                        }
                        tweets.append(tweet_data)

                # Handle pagination if we need more tweets
                if len(tweets) < max_tweets and response.meta.get('next_token'):
                    while len(tweets) < max_tweets:
                        response = self.client.get_users_tweets(
                            id=user_id,
                            max_results=min(max_tweets - len(tweets), 100),
                            tweet_fields=['created_at', 'public_metrics', 'entities', 'conversation_id'],
                            exclude=exclusions if exclusions else None,
                            pagination_token=response.meta.get('next_token')
                        )

                        if not response.data:
                            break

                        for tweet in response.data:
                            tweet_data = {
                                'tweet_id': str(tweet.id),
                                'handle': f"@{username}",
                                'username': user_info['name'],
                                'text': tweet.text,
                                'created_at': tweet.created_at.isoformat() if tweet.created_at else None,
                                'likes': tweet.public_metrics.get('like_count', 0) if tweet.public_metrics else 0,
                                'retweets': tweet.public_metrics.get('retweet_count', 0) if tweet.public_metrics else 0,
                                'replies': tweet.public_metrics.get('reply_count', 0) if tweet.public_metrics else 0,
                                'url': f"https://twitter.com/{username}/status/{tweet.id}"
                            }
                            tweets.append(tweet_data)

                        if not response.meta.get('next_token'):
                            break

        except Exception as e:
            print(f"Error fetching tweets for {username}: {e}")

        return tweets[:max_tweets]

    def fetch_tweets_for_handles(
        self,
        handles: List[str],
        max_tweets_per_handle: int = 200
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch tweets from multiple handles.

        Args:
            handles: List of Twitter usernames
            max_tweets_per_handle: Maximum tweets to fetch per handle

        Returns:
            Dictionary mapping handle to list of tweets
        """
        results = {}
        for handle in handles:
            tweets = self.fetch_user_tweets(
                username=handle,
                max_tweets=max_tweets_per_handle
            )
            results[handle] = tweets
            print(f"Fetched {len(tweets)} tweets for {handle}")

        return results


# Global Twitter client instance
twitter_client = TwitterClient()
