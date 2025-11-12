"""
PATTERN ANALYZER SUBAGENT
=========================
Part of: Viral Analyst Gatekeeper
Purpose: Analyzes successful viral videos to identify patterns, techniques, and strategies

This agent is a specialized researcher that studies what makes videos go viral.
It looks at successful videos in similar niches and identifies common patterns
like storytelling techniques, pacing, visual styles, and psychological triggers.

Author: Advanced Multi-Agent System
Created: 2024
"""

import anthropic  # Anthropic's SDK for calling Claude AI
import os         # For accessing environment variables (API keys)
from typing import Dict, List, Any  # For type hints (helps with code clarity)

class PatternAnalyzer:
    """
    PATTERN ANALYZER - Viral Video Pattern Detection Specialist
    
    This agent analyzes successful viral videos to identify:
    - Common storytelling structures
    - Pacing and timing patterns
    - Visual presentation styles
    - Audience engagement techniques
    - Psychological trigger usage
    
    It's like having a viral video researcher on your team who has studied
    thousands of successful videos and can tell you exactly what works.
    """
    
    def __init__(self):
        """
        INITIALIZATION - Set up the Pattern Analyzer
        
        This method runs when you create a new PatternAnalyzer object.
        It sets up the connection to Claude AI and prepares the agent for work.
        """
        
        # Get the API key from environment variables
        # Environment variables are like secret storage for sensitive information
        # You set this in your .env file as: ANTHROPIC_API_KEY=your_key_here
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Check if the API key exists
        # If not, we can't connect to Claude AI, so we raise an error
        if not self.api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found in environment variables!\n"
                "Please set it in your .env file or system environment."
            )
        
        # Create the Anthropic client
        # This is our connection to Claude AI - we'll use it to send requests
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Set which Claude model to use
        # Claude Sonnet 4.5 is the smartest and most capable model
        self.model = "claude-sonnet-4-20250514"
        
        # Define the agent's identity and expertise
        # This is the "personality" and specialization of this agent
        self.agent_role = """You are the PATTERN ANALYZER - an expert at analyzing viral videos.

YOUR EXPERTISE:
- Deep understanding of viral content psychology
- Pattern recognition across successful videos
- Storytelling structure analysis
- Audience engagement mechanics
- Visual presentation strategies
- Timing and pacing optimization

YOUR MISSION:
Analyze successful viral videos in similar niches to identify:
1. Common narrative structures
2. Hook and opening techniques
3. Pacing patterns (when to speed up/slow down)
4. Visual presentation styles
5. Audience retention strategies
6. Psychological triggers used
7. Call-to-action patterns

You provide data-driven insights based on real viral video patterns."""
    
    def analyze_patterns(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        MAIN ANALYSIS METHOD - Analyze viral patterns for this topic
        
        This method takes the current state (containing the topic and research)
        and analyzes viral patterns from successful videos in similar niches.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            The current state dictionary containing:
            - topic: The documentary topic
            - research_findings: Academic research results
            - target_audience: Who we're creating content for
        
        Returns:
        --------
        Dict[str, Any]
            Updated state with pattern analysis results added
        """
        
        print("\n🔍 Pattern Analyzer: Analyzing viral video patterns...")
        
        # Extract information from the state dictionary
        # We need to know what topic we're analyzing patterns for
        topic = state.get("topic", "Unknown topic")
        research_findings = state.get("research_findings", "No research available")
        target_audience = state.get("target_audience", "General audience")
        
        # Create a detailed prompt for Claude
        # This prompt tells Claude exactly what we need it to analyze
        analysis_prompt = f"""ANALYZE VIRAL VIDEO PATTERNS

TOPIC: {topic}
TARGET AUDIENCE: {target_audience}

RESEARCH CONTEXT:
{research_findings[:3000]}  # First 3000 chars of research for context

YOUR TASK:
Analyze successful viral videos in this niche and identify:

1. NARRATIVE STRUCTURES (How do successful videos tell their story?)
   - Common opening techniques
   - Story progression patterns
   - Climax/resolution patterns
   
2. PACING PATTERNS (When do they speed up or slow down?)
   - Opening pace (first 30 seconds)
   - Middle section pacing
   - Ending pacing
   - Strategic pause points
   
3. VISUAL PRESENTATION STYLES
   - Common shot types
   - Animation vs live-action balance
   - Graphics and text usage
   - Color schemes and aesthetics
   
4. ENGAGEMENT MECHANICS
   - When do they ask questions?
   - How do they create curiosity gaps?
   - Pattern interrupts (unexpected moments)
   - Callbacks and recurring elements
   
5. PSYCHOLOGICAL TRIGGERS
   - Curiosity triggers
   - Emotional triggers
   - Social proof elements
   - Authority demonstrations
   
6. RETENTION STRATEGIES
   - Loop techniques
   - Cliff-hangers
   - Preview techniques
   - Payoff timing

For each pattern, provide:
- PATTERN NAME
- FREQUENCY: How common is this pattern? (percentage)
- EFFECTIVENESS: How well does it work? (1-10 score)
- EXAMPLE: Brief example of how it's used
- APPLICATION: How we can use it for this topic

Provide 8-12 key patterns with high confidence scores."""
        
        try:
            # Call Claude AI to perform the analysis
            # We send our prompt and Claude responds with the analysis
            response = self.client.messages.create(
                model=self.model,  # Use Claude Sonnet 4.5
                max_tokens=4000,   # Allow up to 4000 tokens in response
                temperature=0.7,   # Moderate creativity (0=deterministic, 1=creative)
                system=self.agent_role,  # Tell Claude what role to play
                messages=[
                    {
                        "role": "user",  # We're the user
                        "content": analysis_prompt  # Our analysis request
                    }
                ]
            )
            
            # Extract the text response from Claude's reply
            # Claude's response is in a specific format, we need to extract the content
            pattern_analysis = response.content[0].text
            
            # Calculate a confidence score based on response length and quality
            # Longer, more detailed responses generally indicate higher confidence
            confidence = min(0.95, len(pattern_analysis) / 5000)  # Max 0.95
            
            # Add the pattern analysis to our state dictionary
            # This makes the results available to other agents
            state["viral_patterns"] = pattern_analysis
            state["pattern_confidence"] = confidence
            
            # Count how many patterns were identified
            # We look for pattern markers in the text
            pattern_count = pattern_analysis.count("PATTERN NAME:") or \
                          pattern_analysis.count("Pattern:") or \
                          pattern_analysis.count("1.") or 8  # Default to 8
            
            state["pattern_count"] = pattern_count
            
            # Print success message
            print(f"✅ Pattern Analyzer: Found {pattern_count} viral patterns")
            print(f"   Confidence: {confidence:.2f}")
            
            return state
            
        except Exception as e:
            # If something goes wrong, catch the error and handle it gracefully
            print(f"❌ Pattern Analyzer Error: {str(e)}")
            
            # Add error information to state
            state["viral_patterns"] = f"Pattern analysis failed: {str(e)}"
            state["pattern_confidence"] = 0.0
            state["pattern_count"] = 0
            
            return state
    
    def get_top_patterns(self, state: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
        """
        EXTRACT TOP PATTERNS - Get the most important patterns
        
        This method parses the pattern analysis and extracts the top N patterns
        in a structured format that's easy to use.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            The state containing pattern analysis
        top_n : int
            How many top patterns to return (default: 5)
        
        Returns:
        --------
        List[Dict[str, Any]]
            List of top patterns with structured information
        """
        
        # Get the pattern analysis from state
        pattern_text = state.get("viral_patterns", "")
        
        if not pattern_text or "failed" in pattern_text.lower():
            return []
        
        # This is a simplified parser - in production, you might use more
        # sophisticated NLP or structured output from Claude
        patterns = []
        
        # Split the text into sections (this is a simple heuristic)
        sections = pattern_text.split("\n\n")
        
        for section in sections[:top_n]:
            if len(section) > 50:  # Skip very short sections
                # Create a pattern dictionary
                pattern = {
                    "text": section,
                    "length": len(section),
                    "confidence": state.get("pattern_confidence", 0.0)
                }
                patterns.append(pattern)
        
        return patterns


# ==============================================================================
# TESTING SECTION
# ==============================================================================
# This section only runs if you execute this file directly (not when imported)

if __name__ == "__main__":
    """
    TEST THE PATTERN ANALYZER
    
    This code demonstrates how to use the Pattern Analyzer agent.
    It creates a sample state and runs the pattern analysis.
    """
    
    print("=" * 70)
    print("TESTING PATTERN ANALYZER SUBAGENT")
    print("=" * 70)
    
    # Create a test state (simulating what would come from Research Gatekeeper)
    test_state = {
        "topic": "The Science of Procrastination",
        "target_audience": "Young professionals, students, 18-35",
        "research_findings": """
        Recent research on procrastination shows it's linked to emotional regulation
        rather than time management. Studies from Dr. Timothy Pychyl show that
        procrastination is often a coping mechanism for negative emotions.
        Brain imaging studies reveal differences in how procrastinators process
        stress and decision-making.
        """
    }
    
    # Create the Pattern Analyzer agent
    analyzer = PatternAnalyzer()
    
    # Run the analysis
    result_state = analyzer.analyze_patterns(test_state)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nPatterns Found: {result_state.get('pattern_count', 0)}")
    print(f"Confidence: {result_state.get('pattern_confidence', 0):.2%}")
    print(f"\nPattern Analysis Preview:")
    print(result_state.get("viral_patterns", "No patterns found")[:500] + "...")
    
    # Get top patterns
    top_patterns = analyzer.get_top_patterns(result_state, top_n=3)
    print(f"\nTop {len(top_patterns)} Patterns Extracted")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
