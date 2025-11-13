"""TweetInsight - Twitter Research Application with Streamlit UI."""
import streamlit as st
import uuid
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any
from backend import db, twitter_client, vector_store, llm_service, settings

# Page configuration
st.set_page_config(
    page_title="TweetInsight - Twitter Research Tool",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1DA1F2;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #657786;
        margin-bottom: 2rem;
    }
    .tweet-card {
        background-color: #f7f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1DA1F2;
        margin-bottom: 1rem;
    }
    .handle {
        font-weight: bold;
        color: #1DA1F2;
    }
    .metrics {
        color: #657786;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables."""
    if 'current_collection_id' not in st.session_state:
        st.session_state.current_collection_id = None
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'selected_handles' not in st.session_state:
        st.session_state.selected_handles = []


def sidebar():
    """Render sidebar with navigation and collection management."""
    with st.sidebar:
        st.markdown('<div class="main-header">🐦 TweetInsight</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Twitter Research Tool</div>', unsafe_allow_html=True)

        # Navigation
        page = st.radio(
            "Navigation",
            ["🏠 Home", "📚 Collections", "🔍 Research", "📊 Summaries", "⚙️ Settings"],
            label_visibility="collapsed"
        )

        st.divider()

        # Collections list
        st.subheader("Your Collections")
        collections = db.get_all_collections()

        if collections:
            for coll in collections:
                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button(
                        f"📁 {coll['name']}\n({coll['tweet_count']} tweets)",
                        key=f"coll_{coll['collection_id']}",
                        use_container_width=True
                    ):
                        st.session_state.current_collection_id = coll['collection_id']
                        st.rerun()
                with col2:
                    if st.button("🗑️", key=f"del_{coll['collection_id']}"):
                        db.delete_collection(coll['collection_id'])
                        vector_store.delete_collection(coll['collection_id'])
                        if st.session_state.current_collection_id == coll['collection_id']:
                            st.session_state.current_collection_id = None
                        st.rerun()
        else:
            st.info("No collections yet. Create one to get started!")

        st.divider()

        # Quick stats
        st.caption(f"Total Collections: {len(collections)}")
        if st.session_state.current_collection_id:
            current = db.get_collection(st.session_state.current_collection_id)
            if current:
                st.caption(f"Current: {current['name']}")

    return page


def home_page():
    """Render home page."""
    st.markdown('<div class="main-header">Welcome to TweetInsight</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Transform Twitter conversations into structured knowledge</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🎯 Select Handles")
        st.write("Choose up to 5 Twitter accounts to research")

    with col2:
        st.markdown("### 🔍 Ask Questions")
        st.write("Get AI-powered answers from the tweets")

    with col3:
        st.markdown("### 📊 Generate Summaries")
        st.write("Create comprehensive summaries with citations")

    st.divider()

    st.markdown("### 🚀 Quick Start")
    st.write("1. Go to **Collections** to create a new research collection")
    st.write("2. Add Twitter handles and fetch their tweets")
    st.write("3. Use **Research** to ask questions about the tweets")
    st.write("4. Generate **Summaries** to synthesize insights")

    st.divider()

    # API Status Check
    st.markdown("### 🔌 API Status")
    col1, col2 = st.columns(2)

    with col1:
        if twitter_client.verify_credentials():
            st.success("✅ Twitter API: Connected")
        else:
            st.error("❌ Twitter API: Not configured")
            st.caption("Add your Twitter API credentials in Settings")

    with col2:
        if llm_service.client:
            st.success(f"✅ LLM API: Connected ({settings.LLM_PROVIDER})")
        else:
            st.error("❌ LLM API: Not configured")
            st.caption("Add your LLM API key in Settings")


def collections_page():
    """Render collections management page."""
    st.markdown("## 📚 Research Collections")

    # Create new collection
    with st.expander("➕ Create New Collection", expanded=True):
        col_name = st.text_input("Collection Name", placeholder="My AI Research")

        st.write("Add Twitter Handles (up to 5)")
        handle_input = st.text_input(
            "Twitter Handle",
            placeholder="@elonmusk or elonmusk",
            help="Enter handle with or without @"
        )

        if 'selected_handles' not in st.session_state:
            st.session_state.selected_handles = []

        if st.button("Add Handle") and handle_input:
            if len(st.session_state.selected_handles) < settings.MAX_HANDLES_PER_COLLECTION:
                handle = handle_input.strip().lstrip('@')
                if f"@{handle}" not in st.session_state.selected_handles:
                    # Verify handle exists
                    user_info = twitter_client.get_user_info(handle)
                    if user_info:
                        st.session_state.selected_handles.append(f"@{handle}")
                        st.success(f"Added @{handle} ({user_info['name']})")
                        st.rerun()
                    else:
                        st.error(f"Could not find user @{handle}")
                else:
                    st.warning("Handle already added")
            else:
                st.warning(f"Maximum {settings.MAX_HANDLES_PER_COLLECTION} handles allowed")

        # Display selected handles
        if st.session_state.selected_handles:
            st.write("Selected Handles:")
            for i, handle in enumerate(st.session_state.selected_handles):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"- {handle}")
                with col2:
                    if st.button("Remove", key=f"remove_{i}"):
                        st.session_state.selected_handles.remove(handle)
                        st.rerun()

        # Create collection button
        if st.button("Create Collection", type="primary", disabled=not (col_name and st.session_state.selected_handles)):
            with st.spinner("Creating collection and fetching tweets..."):
                # Create collection
                collection_id = str(uuid.uuid4())
                db.create_collection(collection_id, col_name, st.session_state.selected_handles)

                # Fetch tweets
                all_tweets = []
                progress_bar = st.progress(0)
                status_text = st.empty()

                for i, handle in enumerate(st.session_state.selected_handles):
                    status_text.text(f"Fetching tweets from {handle}...")
                    tweets = twitter_client.fetch_user_tweets(
                        handle.lstrip('@'),
                        max_tweets=settings.MAX_TWEETS_PER_HANDLE
                    )

                    # Add collection_id to tweets
                    for tweet in tweets:
                        tweet['collection_id'] = collection_id

                    all_tweets.extend(tweets)
                    progress_bar.progress((i + 1) / len(st.session_state.selected_handles))

                # Save tweets to database
                status_text.text("Saving tweets...")
                tweet_count = db.add_tweets_bulk(all_tweets)
                db.update_collection_tweet_count(collection_id, tweet_count)

                # Add to vector store
                status_text.text("Building search index...")
                vector_store.add_tweets(collection_id, all_tweets)

                status_text.text("")
                progress_bar.empty()

                st.success(f"Collection created with {tweet_count} tweets!")
                st.session_state.selected_handles = []
                st.session_state.current_collection_id = collection_id
                st.rerun()

    st.divider()

    # Display existing collections
    st.markdown("### Existing Collections")
    collections = db.get_all_collections()

    if collections:
        for coll in collections:
            with st.expander(f"📁 {coll['name']} - {coll['tweet_count']} tweets"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Handles:** {', '.join(coll['handles'])}")
                    st.write(f"**Created:** {coll['created_at']}")
                with col2:
                    st.write(f"**Tweets:** {coll['tweet_count']}")
                    st.write(f"**Last Updated:** {coll['last_updated']}")

                if st.button("Open Collection", key=f"open_{coll['collection_id']}"):
                    st.session_state.current_collection_id = coll['collection_id']
                    st.rerun()
    else:
        st.info("No collections yet. Create one above!")


def research_page():
    """Render research/query page."""
    st.markdown("## 🔍 Research & Query")

    if not st.session_state.current_collection_id:
        st.warning("Please select or create a collection first!")
        return

    collection = db.get_collection(st.session_state.current_collection_id)
    if not collection:
        st.error("Collection not found!")
        return

    st.info(f"📁 Current Collection: **{collection['name']}** ({collection['tweet_count']} tweets)")

    # Query input
    query = st.text_area(
        "Ask a question about the tweets",
        placeholder="What are the main opinions about AI regulation?",
        height=100
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        ask_button = st.button("🔍 Ask", type="primary", disabled=not query)
    with col2:
        clear_button = st.button("🗑️ Clear History")

    if clear_button:
        st.session_state.conversation_history = []
        st.rerun()

    if ask_button and query:
        with st.spinner("Searching tweets and generating answer..."):
            # Search for relevant tweets
            relevant_tweets = vector_store.search_similar_tweets(
                st.session_state.current_collection_id,
                query,
                n_results=15
            )

            if not relevant_tweets:
                st.warning("No relevant tweets found.")
                return

            # Generate answer
            answer = llm_service.answer_question(
                query,
                relevant_tweets,
                st.session_state.conversation_history
            )

            # Save query
            query_id = str(uuid.uuid4())
            db.save_query({
                'query_id': query_id,
                'collection_id': st.session_state.current_collection_id,
                'user_query': query,
                'ai_response': answer,
                'source_tweet_ids': [t['tweet_id'] for t in relevant_tweets]
            })

            # Update conversation history
            st.session_state.conversation_history.append({"role": "user", "content": query})
            st.session_state.conversation_history.append({"role": "assistant", "content": answer})

            # Display answer
            st.markdown("### 💡 Answer")
            st.markdown(answer)

            # Display source tweets
            st.markdown("### 📄 Source Tweets")
            for tweet in relevant_tweets[:5]:
                st.markdown(f"""
                <div class="tweet-card">
                    <div class="handle">{tweet['handle']} - {tweet.get('username', '')}</div>
                    <div>{tweet['text']}</div>
                    <div class="metrics">
                        {tweet.get('created_at', '')[:10]} |
                        ❤️ {tweet.get('likes', 0)} |
                        🔄 {tweet.get('retweets', 0)} |
                        Similarity: {tweet.get('similarity_score', 0):.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # Display query history
    st.divider()
    st.markdown("### 📜 Query History")
    history = db.get_query_history(st.session_state.current_collection_id, limit=10)

    if history:
        for q in history:
            with st.expander(f"Q: {q['user_query'][:80]}... - {q['created_at'][:16]}"):
                st.markdown(f"**Question:** {q['user_query']}")
                st.markdown(f"**Answer:** {q['ai_response']}")
    else:
        st.info("No queries yet. Ask a question above!")


def summaries_page():
    """Render summaries generation page."""
    st.markdown("## 📊 Generate Summaries")

    if not st.session_state.current_collection_id:
        st.warning("Please select or create a collection first!")
        return

    collection = db.get_collection(st.session_state.current_collection_id)
    if not collection:
        st.error("Collection not found!")
        return

    st.info(f"📁 Current Collection: **{collection['name']}** ({collection['tweet_count']} tweets)")

    # Summary options
    col1, col2 = st.columns(2)

    with col1:
        summary_type = st.selectbox(
            "Summary Length",
            ["brief", "standard", "comprehensive"],
            index=1
        )

    with col2:
        filter_handle = st.multiselect(
            "Filter by Handle (optional)",
            collection['handles'],
            default=None
        )

    # Generate summary button
    if st.button("📝 Generate Summary", type="primary"):
        with st.spinner("Generating summary..."):
            # Get tweets
            if filter_handle:
                tweets = []
                for handle in filter_handle:
                    tweets.extend(db.get_tweets_by_handle(
                        st.session_state.current_collection_id,
                        handle
                    ))
            else:
                tweets = db.get_tweets_by_collection(
                    st.session_state.current_collection_id
                )

            if not tweets:
                st.warning("No tweets found!")
                return

            # Generate summary
            summary = llm_service.generate_summary(tweets, summary_type)

            # Extract themes
            themes = llm_service.extract_themes(tweets)

            # Display results
            st.markdown("### 📝 Summary")
            st.markdown(summary)

            st.markdown("### 🏷️ Key Themes")
            if themes:
                for theme in themes:
                    st.markdown(f"- {theme}")
            else:
                st.info("No themes extracted")

            st.divider()

            # Export options
            st.markdown("### 💾 Export Summary")
            col1, col2, col3 = st.columns(3)

            with col1:
                # Markdown export
                markdown_content = f"""# {collection['name']} - Summary

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Handles:** {', '.join(collection['handles'])}
**Tweet Count:** {len(tweets)}

## Summary

{summary}

## Key Themes

{chr(10).join(['- ' + theme for theme in themes])}
"""
                st.download_button(
                    "📥 Download Markdown",
                    markdown_content,
                    file_name=f"{collection['name']}_summary.md",
                    mime="text/markdown"
                )

            with col2:
                # Text export
                st.download_button(
                    "📥 Download Text",
                    summary,
                    file_name=f"{collection['name']}_summary.txt",
                    mime="text/plain"
                )

            with col3:
                # CSV export of tweets
                df = pd.DataFrame(tweets)
                csv = df.to_csv(index=False)
                st.download_button(
                    "📥 Download Tweets CSV",
                    csv,
                    file_name=f"{collection['name']}_tweets.csv",
                    mime="text/csv"
                )


def settings_page():
    """Render settings page."""
    st.markdown("## ⚙️ Settings")

    st.markdown("### 🔑 API Configuration")
    st.info("Add your API keys to the `.env` file in the project root directory.")

    # Display current settings (without showing keys)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Twitter API")
        if settings.TWITTER_BEARER_TOKEN or settings.TWITTER_API_KEY:
            st.success("✅ Configured")
        else:
            st.error("❌ Not configured")
            st.code("""
TWITTER_BEARER_TOKEN=your_bearer_token
# OR
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
            """)

    with col2:
        st.markdown("#### LLM API")
        st.write(f"**Provider:** {settings.LLM_PROVIDER}")
        if llm_service.client:
            st.success("✅ Configured")
        else:
            st.error("❌ Not configured")
            st.code("""
# For OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_key

# For Anthropic
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=your_anthropic_key
            """)

    st.divider()

    st.markdown("### 📊 Application Limits")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Max Handles per Collection", settings.MAX_HANDLES_PER_COLLECTION)
        st.metric("Max Tweets per Handle", settings.MAX_TWEETS_PER_HANDLE)

    with col2:
        st.metric("Max Collections (Free)", settings.MAX_COLLECTIONS_FREE)
        st.metric("Max Queries/Month (Free)", settings.MAX_QUERIES_FREE)

    st.divider()

    st.markdown("### 📁 Data Storage")
    st.write(f"**Database:** {settings.DATABASE_PATH}")
    st.write(f"**Vector Store:** {settings.VECTOR_DB_PATH}")

    # Database stats
    collections = db.get_all_collections()
    total_tweets = sum(c['tweet_count'] for c in collections)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Collections", len(collections))
    with col2:
        st.metric("Total Tweets", total_tweets)


def main():
    """Main application entry point."""
    init_session_state()
    page = sidebar()

    # Route to appropriate page
    if page == "🏠 Home":
        home_page()
    elif page == "📚 Collections":
        collections_page()
    elif page == "🔍 Research":
        research_page()
    elif page == "📊 Summaries":
        summaries_page()
    elif page == "⚙️ Settings":
        settings_page()


if __name__ == "__main__":
    main()
