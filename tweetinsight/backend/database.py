"""Database models and operations using SQLite."""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
from contextlib import contextmanager
from .config import settings


class Database:
    """SQLite database manager for TweetInsight."""

    def __init__(self, db_path: str = None):
        """Initialize database connection."""
        self.db_path = db_path or settings.DATABASE_PATH
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _init_db(self):
        """Initialize database schema."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Collections table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS collections (
                    collection_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    handles TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    tweet_count INTEGER DEFAULT 0
                )
            """)

            # Tweets table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tweets (
                    tweet_id TEXT PRIMARY KEY,
                    collection_id TEXT NOT NULL,
                    handle TEXT NOT NULL,
                    username TEXT,
                    text TEXT NOT NULL,
                    created_at TIMESTAMP,
                    likes INTEGER DEFAULT 0,
                    retweets INTEGER DEFAULT 0,
                    replies INTEGER DEFAULT 0,
                    url TEXT,
                    FOREIGN KEY (collection_id) REFERENCES collections (collection_id)
                )
            """)

            # Queries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS queries (
                    query_id TEXT PRIMARY KEY,
                    collection_id TEXT NOT NULL,
                    user_query TEXT NOT NULL,
                    ai_response TEXT,
                    source_tweet_ids TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (collection_id) REFERENCES collections (collection_id)
                )
            """)

            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tweets_collection ON tweets(collection_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tweets_handle ON tweets(handle)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_queries_collection ON queries(collection_id)")

    # Collection operations
    def create_collection(self, collection_id: str, name: str, handles: List[str]) -> bool:
        """Create a new research collection."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO collections (collection_id, name, handles) VALUES (?, ?, ?)",
                (collection_id, name, json.dumps(handles))
            )
            return True

    def get_collection(self, collection_id: str) -> Optional[Dict[str, Any]]:
        """Get collection by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM collections WHERE collection_id = ?", (collection_id,))
            row = cursor.fetchone()
            if row:
                return {
                    "collection_id": row["collection_id"],
                    "name": row["name"],
                    "handles": json.loads(row["handles"]),
                    "created_at": row["created_at"],
                    "last_updated": row["last_updated"],
                    "tweet_count": row["tweet_count"]
                }
            return None

    def get_all_collections(self) -> List[Dict[str, Any]]:
        """Get all collections."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM collections ORDER BY last_updated DESC")
            rows = cursor.fetchall()
            return [
                {
                    "collection_id": row["collection_id"],
                    "name": row["name"],
                    "handles": json.loads(row["handles"]),
                    "created_at": row["created_at"],
                    "last_updated": row["last_updated"],
                    "tweet_count": row["tweet_count"]
                }
                for row in rows
            ]

    def update_collection_tweet_count(self, collection_id: str, count: int):
        """Update tweet count for a collection."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE collections SET tweet_count = ?, last_updated = CURRENT_TIMESTAMP WHERE collection_id = ?",
                (count, collection_id)
            )

    def delete_collection(self, collection_id: str) -> bool:
        """Delete a collection and all associated data."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM queries WHERE collection_id = ?", (collection_id,))
            cursor.execute("DELETE FROM tweets WHERE collection_id = ?", (collection_id,))
            cursor.execute("DELETE FROM collections WHERE collection_id = ?", (collection_id,))
            return True

    # Tweet operations
    def add_tweet(self, tweet_data: Dict[str, Any]) -> bool:
        """Add a single tweet."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO tweets
                (tweet_id, collection_id, handle, username, text, created_at, likes, retweets, replies, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tweet_data["tweet_id"],
                tweet_data["collection_id"],
                tweet_data["handle"],
                tweet_data.get("username", ""),
                tweet_data["text"],
                tweet_data.get("created_at"),
                tweet_data.get("likes", 0),
                tweet_data.get("retweets", 0),
                tweet_data.get("replies", 0),
                tweet_data.get("url", "")
            ))
            return True

    def add_tweets_bulk(self, tweets: List[Dict[str, Any]]) -> int:
        """Add multiple tweets in bulk."""
        count = 0
        with self.get_connection() as conn:
            cursor = conn.cursor()
            for tweet in tweets:
                try:
                    cursor.execute("""
                        INSERT OR REPLACE INTO tweets
                        (tweet_id, collection_id, handle, username, text, created_at, likes, retweets, replies, url)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        tweet["tweet_id"],
                        tweet["collection_id"],
                        tweet["handle"],
                        tweet.get("username", ""),
                        tweet["text"],
                        tweet.get("created_at"),
                        tweet.get("likes", 0),
                        tweet.get("retweets", 0),
                        tweet.get("replies", 0),
                        tweet.get("url", "")
                    ))
                    count += 1
                except Exception as e:
                    print(f"Error adding tweet {tweet.get('tweet_id')}: {e}")
                    continue
            return count

    def get_tweets_by_collection(self, collection_id: str, limit: int = 1000) -> List[Dict[str, Any]]:
        """Get all tweets for a collection."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tweets WHERE collection_id = ? ORDER BY created_at DESC LIMIT ?",
                (collection_id, limit)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_tweets_by_handle(self, collection_id: str, handle: str) -> List[Dict[str, Any]]:
        """Get tweets for a specific handle in a collection."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tweets WHERE collection_id = ? AND handle = ? ORDER BY created_at DESC",
                (collection_id, handle)
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def search_tweets(self, collection_id: str, keyword: str) -> List[Dict[str, Any]]:
        """Search tweets by keyword."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tweets WHERE collection_id = ? AND text LIKE ? ORDER BY created_at DESC",
                (collection_id, f"%{keyword}%")
            )
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    # Query operations
    def save_query(self, query_data: Dict[str, Any]) -> bool:
        """Save a query and its response."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO queries (query_id, collection_id, user_query, ai_response, source_tweet_ids)
                VALUES (?, ?, ?, ?, ?)
            """, (
                query_data["query_id"],
                query_data["collection_id"],
                query_data["user_query"],
                query_data["ai_response"],
                json.dumps(query_data.get("source_tweet_ids", []))
            ))
            return True

    def get_query_history(self, collection_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get query history for a collection."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM queries WHERE collection_id = ? ORDER BY created_at DESC LIMIT ?",
                (collection_id, limit)
            )
            rows = cursor.fetchall()
            return [
                {
                    "query_id": row["query_id"],
                    "collection_id": row["collection_id"],
                    "user_query": row["user_query"],
                    "ai_response": row["ai_response"],
                    "source_tweet_ids": json.loads(row["source_tweet_ids"]),
                    "created_at": row["created_at"]
                }
                for row in rows
            ]


# Global database instance
db = Database()
