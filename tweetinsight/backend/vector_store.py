"""Vector store for semantic search using ChromaDB."""
import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from pathlib import Path
from .config import settings


class VectorStore:
    """ChromaDB vector store for tweet embeddings and semantic search."""

    def __init__(self, persist_directory: str = None):
        """Initialize ChromaDB client."""
        self.persist_directory = persist_directory or settings.VECTOR_DB_PATH
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=ChromaSettings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

    def get_or_create_collection(self, collection_id: str):
        """Get or create a ChromaDB collection for a research collection."""
        try:
            collection = self.client.get_or_create_collection(
                name=f"collection_{collection_id}",
                metadata={"description": f"Tweets for collection {collection_id}"}
            )
            return collection
        except Exception as e:
            print(f"Error creating collection: {e}")
            return None

    def add_tweets(
        self,
        collection_id: str,
        tweets: List[Dict[str, Any]]
    ) -> bool:
        """
        Add tweets to the vector store.

        Args:
            collection_id: Research collection ID
            tweets: List of tweet dictionaries

        Returns:
            Success status
        """
        try:
            collection = self.get_or_create_collection(collection_id)
            if not collection:
                return False

            # Prepare data for ChromaDB
            documents = []
            metadatas = []
            ids = []

            for tweet in tweets:
                # Combine tweet text with username for better context
                document = f"@{tweet['handle']}: {tweet['text']}"
                documents.append(document)

                # Store metadata
                metadata = {
                    "tweet_id": str(tweet["tweet_id"]),
                    "handle": tweet["handle"],
                    "username": tweet.get("username", ""),
                    "created_at": tweet.get("created_at", ""),
                    "likes": str(tweet.get("likes", 0)),
                    "retweets": str(tweet.get("retweets", 0)),
                    "url": tweet.get("url", "")
                }
                metadatas.append(metadata)
                ids.append(str(tweet["tweet_id"]))

            # Add to collection in batches
            batch_size = 100
            for i in range(0, len(documents), batch_size):
                batch_docs = documents[i:i + batch_size]
                batch_metas = metadatas[i:i + batch_size]
                batch_ids = ids[i:i + batch_size]

                collection.add(
                    documents=batch_docs,
                    metadatas=batch_metas,
                    ids=batch_ids
                )

            return True

        except Exception as e:
            print(f"Error adding tweets to vector store: {e}")
            return False

    def search_similar_tweets(
        self,
        collection_id: str,
        query: str,
        n_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for tweets semantically similar to the query.

        Args:
            collection_id: Research collection ID
            query: Search query
            n_results: Number of results to return

        Returns:
            List of similar tweets with metadata
        """
        try:
            collection = self.get_or_create_collection(collection_id)
            if not collection:
                return []

            # Query the collection
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )

            # Format results
            similar_tweets = []
            if results and results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i]
                    distance = results['distances'][0][i] if 'distances' in results else 0

                    similar_tweets.append({
                        'tweet_id': metadata.get('tweet_id'),
                        'handle': metadata.get('handle'),
                        'username': metadata.get('username'),
                        'text': doc.split(': ', 1)[1] if ': ' in doc else doc,
                        'created_at': metadata.get('created_at'),
                        'likes': int(metadata.get('likes', 0)),
                        'retweets': int(metadata.get('retweets', 0)),
                        'url': metadata.get('url'),
                        'similarity_score': 1 - distance  # Convert distance to similarity
                    })

            return similar_tweets

        except Exception as e:
            print(f"Error searching tweets: {e}")
            return []

    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection from the vector store."""
        try:
            self.client.delete_collection(name=f"collection_{collection_id}")
            return True
        except Exception as e:
            print(f"Error deleting collection: {e}")
            return False

    def get_collection_count(self, collection_id: str) -> int:
        """Get the number of tweets in a collection."""
        try:
            collection = self.get_or_create_collection(collection_id)
            if collection:
                return collection.count()
            return 0
        except Exception as e:
            print(f"Error getting collection count: {e}")
            return 0


# Global vector store instance
vector_store = VectorStore()
