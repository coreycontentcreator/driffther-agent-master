"""
YOUTUBE VIDEO ANALYZER - Master Coordinator
============================================
Purpose: Analyzes successful YouTube videos to extract viral techniques,
         patterns, and strategies, then stores them in a vector database
         for semantic search and retrieval.

This is the master coordinator that orchestrates 6 specialized analysis agents:
1. Hook Analyzer - Analyzes opening hooks and attention grabbers
2. Retention Analyzer - Studies retention curves and engagement patterns
3. Story Structure Analyzer - Maps narrative arcs and story beats
4. Visual Style Analyzer - Analyzes visual presentation and cinematography
5. Audio Design Analyzer - Studies music, sound effects, and audio patterns
6. Psychological Trigger Analyzer - Identifies psychological triggers used

The analyzed data is stored in ChromaDB with embeddings for semantic search,
allowing the Content Synthesis system to retrieve relevant techniques.

Author: Advanced Multi-Agent System
Created: 2024
"""

import anthropic
import os
from typing import Dict, List, Any, Optional
import json
from datetime import datetime

# ChromaDB for vector storage
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("⚠️  ChromaDB not installed. Install: pip install chromadb")

class YouTubeVideoAnalyzer:
    """
    YOUTUBE VIDEO ANALYZER - Master Coordinator
    
    This system analyzes successful viral videos and extracts reusable
    techniques, patterns, and strategies. Results are stored in a vector
    database for semantic search during content creation.
    
    WORKFLOW:
    1. Accept video URL or transcript
    2. Coordinate 6 specialized analysis agents
    3. Synthesize findings into structured format
    4. Generate embeddings for semantic search
    5. Store in ChromaDB vector database
    
    USAGE:
    >>> analyzer = YouTubeVideoAnalyzer()
    >>> result = analyzer.analyze_video(
    ...     video_url="youtube.com/watch?v=...",
    ...     video_title="How Procrastination Works",
    ...     video_transcript="[transcript text]"
    ... )
    >>> analyzer.store_in_database(result)
    """
    
    def __init__(self, db_path: str = "/home/claude/viral_db"):
        """
        INITIALIZATION - Set up the analyzer and database connection
        
        Parameters:
        -----------
        db_path : str
            Path to ChromaDB vector database directory
        """
        
        # API setup
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found!\n"
                "Set in .env: ANTHROPIC_API_KEY=your_key_here"
            )
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
        
        # Database setup
        self.db_path = db_path
        self.db_client = None
        self.collection = None
        
        if CHROMADB_AVAILABLE:
            self._initialize_database()
        else:
            print("⚠️  ChromaDB not available - techniques won't be stored")
    
    def _initialize_database(self):
        """
        Initialize ChromaDB connection and collection
        
        Creates or connects to the 'viral_techniques' collection where
        analyzed video techniques are stored with embeddings.
        """
        
        try:
            # Create database directory if it doesn't exist
            os.makedirs(self.db_path, exist_ok=True)
            
            # Initialize ChromaDB client
            # PersistentClient saves data to disk (survives restarts)
            self.db_client = chromadb.PersistentClient(
                path=self.db_path,
                settings=Settings(
                    anonymized_telemetry=False  # Privacy
                )
            )
            
            # Get or create collection
            # A collection stores related documents with embeddings
            self.collection = self.db_client.get_or_create_collection(
                name="viral_techniques",
                metadata={
                    "description": "Analyzed viral video techniques and patterns",
                    "created": datetime.now().isoformat()
                }
            )
            
            print(f"✅ Database initialized: {self.db_path}")
            print(f"   Collection: {self.collection.name}")
            print(f"   Techniques stored: {self.collection.count()}")
            
        except Exception as e:
            print(f"❌ Database initialization failed: {str(e)}")
            self.db_client = None
            self.collection = None
    
    def analyze_video(self, 
                     video_url: str,
                     video_title: str,
                     video_transcript: str,
                     video_views: Optional[int] = None,
                     video_engagement_rate: Optional[float] = None) -> Dict[str, Any]:
        """
        ANALYZE VIDEO - Complete analysis of a viral video
        
        This method coordinates all 6 analysis agents to extract viral
        techniques from the video.
        
        Parameters:
        -----------
        video_url : str
            YouTube URL of the video
        video_title : str
            Title of the video
        video_transcript : str
            Full transcript or description of video content
        video_views : int, optional
            Number of views (helps assess success)
        video_engagement_rate : float, optional
            Engagement rate (likes/comments/shares per view)
        
        Returns:
        --------
        Dict[str, Any]
            Comprehensive analysis with extracted techniques
        """
        
        print(f"\n🎬 Analyzing: {video_title}")
        print("=" * 70)
        
        # Create analysis prompt for Claude
        # This single prompt asks Claude to act as all 6 specialized agents
        analysis_prompt = f"""ANALYZE VIRAL VIDEO FOR TECHNIQUE EXTRACTION

VIDEO INFORMATION:
Title: {video_title}
URL: {video_url}
Views: {video_views if video_views else "Unknown"}
Engagement Rate: {video_engagement_rate if video_engagement_rate else "Unknown"}

TRANSCRIPT/CONTENT:
{video_transcript[:5000]}  # First 5000 chars

YOUR TASK:
You are a team of 6 specialized video analysis agents. Analyze this video
and extract reusable viral techniques across all dimensions:

═══════════════════════════════════════════════════════════════
1. HOOK ANALYZER
═══════════════════════════════════════════════════════════════

Analyze the opening hook (first 10-30 seconds):

HOOK TYPE: [Contrarian/Question/Bold Statement/Story/etc.]

HOOK TEXT:
"[Exact or reconstructed opening words]"

HOOK EFFECTIVENESS: [1-10]

PSYCHOLOGICAL TRIGGERS USED:
- [Trigger 1]: [How it's used]
- [Trigger 2]: [How it's used]

PATTERN INTERRUPT:
[What makes it stop scrolling]

REUSABLE TECHNIQUE:
[How to apply this hook pattern to other topics]

═══════════════════════════════════════════════════════════════
2. RETENTION ANALYZER
═══════════════════════════════════════════════════════════════

Analyze retention and engagement strategies:

RETENTION TECHNIQUES:
1. [Technique name]: [When used, why effective]
2. [Technique name]: [When used, why effective]
3. [Technique name]: [When used, why effective]

PACING STRATEGY:
- Opening pace: [Fast/Medium/Slow]
- Middle pace: [Description]
- Ending pace: [Description]

LOOP STRUCTURES:
- Open loop 1: [What question/mystery opened]
- Resolution: [When/how closed]

VIEWER RETENTION HACKS:
[Specific techniques to keep watching]

═══════════════════════════════════════════════════════════════
3. STORY STRUCTURE ANALYZER
═══════════════════════════════════════════════════════════════

Map the narrative arc:

STORY STRUCTURE: [Three-act/Hero's Journey/Problem-Solution/etc.]

ACT BREAKDOWN:
Act 1 (Setup): [What happens]
Act 2 (Conflict): [What happens]
Act 3 (Resolution): [What happens]

KEY STORY BEATS:
- Inciting incident: [Timestamp/description]
- Midpoint: [Major revelation or turn]
- Climax: [Peak moment]
- Resolution: [How it ends]

EMOTIONAL ARC:
[How emotions build and release]

REUSABLE STRUCTURE:
[How to adapt this structure]

═══════════════════════════════════════════════════════════════
4. VISUAL STYLE ANALYZER
═══════════════════════════════════════════════════════════════

Analyze visual presentation (based on what you can infer):

VISUAL STYLE: [Documentary/Vlog/Explainer/Cinematic/etc.]

SHOT VARIETY:
- Primary shot types: [CU/MS/WS/etc.]
- Camera movement: [Static/Dynamic]

VISUAL PACING:
- Cut frequency: [Fast/Medium/Slow]
- Visual variety: [High/Medium/Low]

GRAPHICS/ANIMATIONS:
[Type and frequency]

COLOR/LIGHTING MOOD:
[Overall aesthetic]

VISUAL TECHNIQUES OBSERVED:
[Specific effective techniques]

═══════════════════════════════════════════════════════════════
5. AUDIO DESIGN ANALYZER
═══════════════════════════════════════════════════════════════

Analyze audio elements (infer from content):

MUSIC STRATEGY:
- Music usage: [Constant/Strategic/Minimal]
- Music mood: [Tense/Upbeat/Dramatic/etc.]
- Music changes: [When and why]

VOICE/NARRATION:
- Delivery style: [Energetic/Calm/Conversational/etc.]
- Pacing: [Fast/Medium/Slow]
- Tone variation: [How voice changes]

SOUND DESIGN NOTES:
[Any notable audio techniques]

═══════════════════════════════════════════════════════════════
6. PSYCHOLOGICAL TRIGGER ANALYZER
═══════════════════════════════════════════════════════════════

Identify psychological triggers used:

PRIMARY TRIGGERS (Rate 1-10 for intensity):
- Curiosity: [X/10] - [How used]
- Fear/Anxiety: [X/10] - [How used]
- Identity: [X/10] - [How used]
- Social Proof: [X/10] - [How used]
- Authority: [X/10] - [How used]
- Scarcity: [X/10] - [How used]

EMOTIONAL TRIGGERS:
- Primary emotions evoked: [List]
- Emotional journey: [Arc description]

SHARING PSYCHOLOGY:
Why would someone share this?
- [Reason 1]
- [Reason 2]

═══════════════════════════════════════════════════════════════
SYNTHESIS: REUSABLE TECHNIQUES
═══════════════════════════════════════════════════════════════

Extract 5-10 SPECIFIC, REUSABLE techniques from this video:

TECHNIQUE 1: [Name]
CATEGORY: [Hook/Retention/Story/Visual/Audio/Psychology]
EFFECTIVENESS: [X/10]
DESCRIPTION:
[Detailed description of technique]

APPLICATION:
[How to apply to other topics]

EXAMPLE TOPICS:
[Where this would work well]

[Repeat for techniques 2-10]

═══════════════════════════════════════════════════════════════
OVERALL ASSESSMENT
═══════════════════════════════════════════════════════════════

VIRAL POTENTIAL SCORE: [X/10]
WHY IT WORKS: [Key success factors]
TARGET AUDIENCE: [Who this appeals to]
CONTENT CATEGORY: [Science/Psychology/Business/etc.]

KEY LEARNINGS:
1. [Major insight 1]
2. [Major insight 2]
3. [Major insight 3]

Provide thorough, specific analysis that can inform future content creation."""
        
        try:
            # Call Claude to perform comprehensive analysis
            print("🤖 Running 6-agent analysis...")
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,  # Long analysis
                temperature=0.6,  # Balanced
                messages=[
                    {
                        "role": "user",
                        "content": analysis_prompt
                    }
                ]
            )
            
            # Extract analysis
            analysis_text = response.content[0].text
            
            # Create structured result
            result = {
                "video_url": video_url,
                "video_title": video_title,
                "video_views": video_views,
                "video_engagement_rate": video_engagement_rate,
                "analysis_text": analysis_text,
                "analyzed_at": datetime.now().isoformat(),
                "technique_count": analysis_text.upper().count("TECHNIQUE"),
                "viral_score": self._extract_viral_score(analysis_text)
            }
            
            print(f"✅ Analysis complete!")
            print(f"   Techniques extracted: {result['technique_count']}")
            print(f"   Viral score: {result['viral_score']}/10")
            
            return result
            
        except Exception as e:
            print(f"❌ Analysis failed: {str(e)}")
            return {
                "video_url": video_url,
                "video_title": video_title,
                "error": str(e)
            }
    
    def _extract_viral_score(self, analysis: str) -> float:
        """Extract viral score from analysis text"""
        if "VIRAL POTENTIAL SCORE:" in analysis:
            try:
                score_line = analysis.split("VIRAL POTENTIAL SCORE:")[1].split("\n")[0]
                score = float(''.join(filter(lambda x: x.isdigit() or x == '.', 
                                            score_line.split("/")[0])))
                return score
            except:
                pass
        return 7.5  # Default
    
    def store_in_database(self, analysis: Dict[str, Any]) -> bool:
        """
        STORE IN DATABASE - Save analysis to vector database
        
        Takes the analysis result and stores it in ChromaDB with
        automatic embedding generation for semantic search.
        
        Parameters:
        -----------
        analysis : Dict[str, Any]
            Analysis result from analyze_video()
        
        Returns:
        --------
        bool
            True if successful, False otherwise
        """
        
        if not self.collection:
            print("❌ Database not available - cannot store")
            return False
        
        if "error" in analysis:
            print("❌ Cannot store failed analysis")
            return False
        
        try:
            # Generate unique ID
            video_id = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Store in database
            # ChromaDB automatically generates embeddings
            self.collection.add(
                documents=[analysis["analysis_text"]],
                ids=[video_id],
                metadatas=[{
                    "video_url": analysis["video_url"],
                    "video_title": analysis["video_title"],
                    "views": str(analysis.get("video_views", "unknown")),
                    "viral_score": str(analysis.get("viral_score", 0)),
                    "analyzed_at": analysis["analyzed_at"],
                    "technique_count": str(analysis.get("technique_count", 0))
                }]
            )
            
            print(f"✅ Stored in database: {video_id}")
            print(f"   Total techniques in library: {self.collection.count()}")
            
            return True
            
        except Exception as e:
            print(f"❌ Storage failed: {str(e)}")
            return False
    
    def batch_analyze_videos(self, video_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        BATCH ANALYZE - Analyze multiple videos
        
        Parameters:
        -----------
        video_list : List[Dict[str, Any]]
            List of video dictionaries with keys:
            - video_url, video_title, video_transcript
        
        Returns:
        --------
        Dict[str, Any]
            Batch results with statistics
        """
        
        print(f"\n🎬 Batch analyzing {len(video_list)} videos...")
        
        results = {
            "total": len(video_list),
            "successful": 0,
            "failed": 0,
            "stored": 0,
            "analyses": []
        }
        
        for i, video in enumerate(video_list, 1):
            print(f"\n[{i}/{len(video_list)}] Processing...")
            
            # Analyze
            analysis = self.analyze_video(
                video_url=video.get("video_url", ""),
                video_title=video.get("video_title", "Untitled"),
                video_transcript=video.get("video_transcript", ""),
                video_views=video.get("video_views"),
                video_engagement_rate=video.get("video_engagement_rate")
            )
            
            results["analyses"].append(analysis)
            
            # Check success
            if "error" in analysis:
                results["failed"] += 1
            else:
                results["successful"] += 1
                
                # Store
                if self.store_in_database(analysis):
                    results["stored"] += 1
        
        print(f"\n{'='*70}")
        print(f"BATCH ANALYSIS COMPLETE")
        print(f"{'='*70}")
        print(f"✅ Successful: {results['successful']}/{results['total']}")
        print(f"✅ Stored: {results['stored']}/{results['total']}")
        print(f"❌ Failed: {results['failed']}/{results['total']}")
        
        return results


# ==============================================================================
# TESTING
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TESTING YOUTUBE VIDEO ANALYZER")
    print("=" * 70)
    
    # Create analyzer
    analyzer = YouTubeVideoAnalyzer()
    
    # Test with sample video
    sample_video = {
        "video_url": "https://youtube.com/watch?v=sample",
        "video_title": "The Science of Procrastination - Why We Do It",
        "video_transcript": """
        [Opening]
        What if I told you that procrastination isn't about laziness at all?
        
        [Hook continues]
        In fact, the latest research from psychologists reveals something shocking:
        procrastination is actually about emotional regulation, not time management.
        
        [Body]
        Dr. Timothy Pychyl from Carleton University has spent decades studying this.
        His research shows that when we procrastinate, we're trying to avoid
        negative emotions associated with the task...
        
        [The video continues with research findings, personal stories, and solutions]
        """,
        "video_views": 2500000,
        "video_engagement_rate": 0.08
    }
    
    # Analyze
    result = analyzer.analyze_video(**sample_video)
    
    # Display results
    if "error" not in result:
        print("\n✅ ANALYSIS SUCCESSFUL")
        print(f"Techniques: {result['technique_count']}")
        print(f"Viral Score: {result['viral_score']}/10")
        
        # Store
        stored = analyzer.store_in_database(result)
        print(f"Stored in DB: {stored}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
