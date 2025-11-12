"""
CONTEXT RETRIEVAL AGENT SUBAGENT
=================================
Part of: Content Synthesis Gatekeeper
Purpose: Searches the vector database for relevant viral techniques, successful
         content patterns, and proven strategies based on the current topic

This agent interfaces with ChromaDB vector storage to retrieve semantically
similar viral techniques that have worked for similar topics. It provides
data-driven recommendations based on past successful content.

Author: Advanced Multi-Agent System
Created: 2024
"""

import os
from typing import Dict, List, Any, Optional

# ChromaDB imports - vector database for semantic search
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("⚠️  ChromaDB not installed. Install with: pip install chromadb")

class ContextRetrievalAgent:
    """
    CONTEXT RETRIEVAL AGENT - Vector Database Search Specialist
    
    This agent retrieves relevant viral techniques and patterns from a vector
    database based on semantic similarity to the current topic and content.
    
    CAPABILITIES:
    - Semantic search through viral technique library
    - Retrieve similar successful content patterns
    - Find proven engagement strategies
    - Get data-driven recommendations
    - Access historical performance data
    
    The database stores analyzed viral content with embeddings for semantic search.
    When you query with a topic like "procrastination psychology", it finds
    similar topics and returns what viral techniques worked for those.
    """
    
    def __init__(self, db_path: str = "/home/claude/viral_db"):
        """
        INITIALIZATION - Set up the Context Retrieval Agent
        
        This connects to the ChromaDB vector database where viral techniques
        are stored with embeddings for semantic search.
        
        Parameters:
        -----------
        db_path : str
            Path to the ChromaDB database directory
        """
        
        self.db_path = db_path
        self.client = None
        self.collection = None
        
        # Check if ChromaDB is available
        if not CHROMADB_AVAILABLE:
            print("❌ ChromaDB not available")
            print("   Install with: pip install chromadb")
            return
        
        try:
            # Initialize ChromaDB client
            # PersistentClient saves data to disk (vs in-memory)
            self.client = chromadb.PersistentClient(
                path=db_path,
                settings=Settings(
                    anonymized_telemetry=False  # Disable telemetry for privacy
                )
            )
            
            # Get or create the viral techniques collection
            # A collection is like a table in a traditional database
            # It stores documents with their embeddings for semantic search
            self.collection = self.client.get_or_create_collection(
                name="viral_techniques",
                metadata={"description": "Library of analyzed viral content techniques"}
            )
            
            print(f"✅ Context Retrieval Agent: Connected to database")
            print(f"   Database path: {db_path}")
            print(f"   Collection: {self.collection.name}")
            print(f"   Documents stored: {self.collection.count()}")
            
        except Exception as e:
            print(f"❌ Error connecting to database: {str(e)}")
            self.client = None
            self.collection = None
    
    def search_techniques(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        SEARCH TECHNIQUES - Semantic search for relevant viral techniques
        
        This performs a semantic search through the viral technique library
        to find techniques and patterns relevant to your query.
        
        HOW IT WORKS:
        1. Your query is converted to an embedding (vector representation)
        2. ChromaDB compares this to all stored technique embeddings
        3. Returns the most semantically similar techniques
        4. Similarity is measured by cosine distance in embedding space
        
        Parameters:
        -----------
        query : str
            Search query (topic, theme, or concept)
        n_results : int
            Number of results to return (default: 5)
        
        Returns:
        --------
        Dict[str, Any]
            Search results with techniques and metadata
        """
        
        if not self.collection:
            return {
                "error": "Database not connected",
                "results": [],
                "count": 0
            }
        
        try:
            # Perform semantic search
            # ChromaDB automatically:
            # 1. Converts query to embedding
            # 2. Compares to all stored embeddings
            # 3. Returns most similar documents
            results = self.collection.query(
                query_texts=[query],  # Can search multiple queries at once
                n_results=n_results,  # How many results to return
                include=["documents", "metadatas", "distances"]  # What to include
            )
            
            # Format results for easy use
            formatted_results = []
            
            # results are returned as lists of lists (for multiple queries)
            # We only sent one query, so we take index [0]
            if results["documents"] and len(results["documents"][0]) > 0:
                for i in range(len(results["documents"][0])):
                    formatted_results.append({
                        "technique": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "similarity": 1.0 - results["distances"][0][i] if results["distances"] else 0.0  # Convert distance to similarity
                    })
            
            return {
                "query": query,
                "results": formatted_results,
                "count": len(formatted_results)
            }
            
        except Exception as e:
            return {
                "error": f"Search failed: {str(e)}",
                "results": [],
                "count": 0
            }
    
    def retrieve_context(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        MAIN RETRIEVAL METHOD - Get relevant context for current documentary
        
        This method analyzes the current state (topic, research, etc.) and
        retrieves relevant viral techniques from the database.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            Current state with:
            - topic: Documentary topic
            - research_findings: Research content (optional)
            - target_audience: Audience demographics (optional)
        
        Returns:
        --------
        Dict[str, Any]
            Updated state with retrieved viral context
        """
        
        print("\n🔍 Context Retrieval Agent: Searching viral technique library...")
        
        if not self.collection:
            print("❌ Database not connected - skipping retrieval")
            state["retrieved_context"] = "Database not available"
            state["retrieval_success"] = False
            return state
        
        # Extract search parameters from state
        topic = state.get("topic", "")
        research = state.get("research_findings", "")[:500]  # First 500 chars
        audience = state.get("target_audience", "")
        
        # Build comprehensive search query
        # We combine topic with key concepts from research for better matching
        search_query = f"{topic}"
        
        if research:
            # Add key research themes
            search_query += f" {research}"
        
        if audience:
            search_query += f" targeting {audience}"
        
        # Search for relevant techniques
        search_results = self.search_techniques(search_query, n_results=8)
        
        if search_results.get("error"):
            print(f"❌ Search error: {search_results['error']}")
            state["retrieved_context"] = f"Search failed: {search_results['error']}"
            state["retrieval_success"] = False
            return state
        
        # Format results for use
        if search_results["count"] > 0:
            # Create a formatted context string
            context_text = "RELEVANT VIRAL TECHNIQUES FROM DATABASE:\n\n"
            
            for i, result in enumerate(search_results["results"], 1):
                similarity_pct = result["similarity"] * 100
                context_text += f"{i}. (Similarity: {similarity_pct:.1f}%)\n"
                context_text += f"{result['technique']}\n"
                
                # Add metadata if available
                if result["metadata"]:
                    context_text += f"   Metadata: {result['metadata']}\n"
                
                context_text += "\n"
            
            # Add to state
            state["retrieved_context"] = context_text
            state["retrieved_technique_count"] = search_results["count"]
            state["retrieval_success"] = True
            state["retrieval_results"] = search_results["results"]  # Raw results for further processing
            
            # Calculate average similarity
            avg_similarity = sum(r["similarity"] for r in search_results["results"]) / len(search_results["results"])
            state["retrieval_avg_similarity"] = avg_similarity
            
            print(f"✅ Context Retrieval Agent: Found {search_results['count']} relevant techniques")
            print(f"   Average Similarity: {avg_similarity:.2%}")
            
        else:
            print("⚠️  No relevant techniques found in database")
            state["retrieved_context"] = "No relevant techniques found"
            state["retrieved_technique_count"] = 0
            state["retrieval_success"] = True  # Not an error, just empty results
        
        return state
    
    def add_technique(self, 
                     technique_text: str, 
                     technique_id: str, 
                     metadata: Optional[Dict[str, Any]] = None) -> bool:
        """
        ADD TECHNIQUE - Store a new viral technique in the database
        
        This allows you to add new viral techniques to the library.
        Techniques are automatically embedded and become searchable.
        
        Parameters:
        -----------
        technique_text : str
            Description of the viral technique
        technique_id : str
            Unique identifier for this technique
        metadata : Dict[str, Any]
            Additional metadata (e.g., source, performance metrics)
        
        Returns:
        --------
        bool
            True if successful, False otherwise
        """
        
        if not self.collection:
            print("❌ Database not connected")
            return False
        
        try:
            # Add to collection
            # ChromaDB automatically generates embeddings
            self.collection.add(
                documents=[technique_text],
                ids=[technique_id],
                metadatas=[metadata] if metadata else None
            )
            
            print(f"✅ Added technique: {technique_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error adding technique: {str(e)}")
            return False
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        GET DATABASE STATS - Return statistics about the viral technique library
        
        Returns:
        --------
        Dict[str, Any]
            Statistics about the database
        """
        
        if not self.collection:
            return {
                "connected": False,
                "count": 0
            }
        
        try:
            return {
                "connected": True,
                "count": self.collection.count(),
                "name": self.collection.name,
                "metadata": self.collection.metadata
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }


# ==============================================================================
# TESTING SECTION
# ==============================================================================

if __name__ == "__main__":
    """
    TEST THE CONTEXT RETRIEVAL AGENT
    """
    
    print("=" * 70)
    print("TESTING CONTEXT RETRIEVAL AGENT")
    print("=" * 70)
    
    # Create agent
    agent = ContextRetrievalAgent()
    
    # Check database stats
    stats = agent.get_database_stats()
    print(f"\nDatabase Stats:")
    print(f"  Connected: {stats.get('connected', False)}")
    print(f"  Techniques Stored: {stats.get('count', 0)}")
    
    # If database is empty, add some sample techniques
    if stats.get('count', 0) == 0:
        print("\n📝 Adding sample techniques for testing...")
        
        sample_techniques = [
            {
                "id": "hook_contrarian_1",
                "text": "Contrarian Hook: Start by challenging a common belief. Example: 'Everything you know about [topic] is wrong.' Works well for psychology and science topics. Effectiveness: 8.5/10",
                "metadata": {"category": "hook", "effectiveness": 8.5, "type": "contrarian"}
            },
            {
                "id": "retention_loop_1",
                "text": "Open Loop Technique: Ask a question in the first 30 seconds but don't answer until minute 8. Creates curiosity gap. Example: 'But first, why does this happen?' Effectiveness: 9/10",
                "metadata": {"category": "retention", "effectiveness": 9.0, "type": "curiosity_loop"}
            },
            {
                "id": "psychology_identity_1",
                "text": "Identity Trigger: Frame content around viewer's self-concept. 'If you've ever felt [X], you're not alone.' Works for personal development and psychology. Effectiveness: 8.8/10",
                "metadata": {"category": "psychology", "effectiveness": 8.8, "type": "identity"}
            }
        ]
        
        for tech in sample_techniques:
            agent.add_technique(tech["text"], tech["id"], tech["metadata"])
        
        print(f"✅ Added {len(sample_techniques)} sample techniques")
    
    # Test search
    print("\n🔍 Testing search...")
    test_state = {
        "topic": "The Science of Procrastination",
        "target_audience": "Young professionals, students",
        "research_findings": "Procrastination is about emotional regulation..."
    }
    
    result_state = agent.retrieve_context(test_state)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nRetrieval Success: {result_state.get('retrieval_success', False)}")
    print(f"Techniques Found: {result_state.get('retrieved_technique_count', 0)}")
    
    if result_state.get('retrieval_success'):
        print(f"Average Similarity: {result_state.get('retrieval_avg_similarity', 0):.2%}")
        print(f"\nRetrieved Context Preview:")
        context = result_state.get('retrieved_context', '')
        print(context[:400] + "..." if len(context) > 400 else context)
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
    
    print("\nℹ️  NOTE: The Context Retrieval Agent works best when the database")
    print("   is populated with analyzed viral content. Use the YouTube Video")
    print("   Analyzer system to build your viral technique library!")
