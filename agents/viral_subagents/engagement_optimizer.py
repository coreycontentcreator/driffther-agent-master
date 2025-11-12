"""
ENGAGEMENT OPTIMIZER SUBAGENT
==============================
Part of: Viral Analyst Gatekeeper
Purpose: Optimizes watch time, retention, and engagement throughout the entire video

This agent designs the pacing, retention strategies, and engagement mechanics
that keep viewers watching from start to finish. It creates a retention curve
strategy with specific techniques placed at critical moments.

Author: Advanced Multi-Agent System
Created: 2024
"""

import anthropic
import os
from typing import Dict, List, Any

class EngagementOptimizer:
    """
    ENGAGEMENT OPTIMIZER - Watch Time & Retention Specialist
    
    This agent creates a comprehensive engagement strategy that maximizes
    viewer retention throughout the entire video.
    
    KEY FOCUS AREAS:
    - Retention curve design (preventing drop-off points)
    - Pacing optimization (when to speed up/slow down)
    - Strategic loops (bringing viewers back to earlier points)
    - Cliffhangers and curiosity gaps
    - Pattern interrupts (keeping attention fresh)
    - Call-to-action placement
    
    The goal: Keep as many viewers as possible watching until the end.
    """
    
    def __init__(self):
        """
        INITIALIZATION - Set up the Engagement Optimizer
        
        Prepares the agent for creating engagement strategies.
        """
        
        # Get API key from environment
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found!\n"
                "Set it in .env: ANTHROPIC_API_KEY=your_key_here"
            )
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Use the most capable model
        self.model = "claude-sonnet-4-20250514"
        
        # Define agent's expertise and role
        self.agent_role = """You are the ENGAGEMENT OPTIMIZER - a specialist in viewer retention.

YOUR EXPERTISE:
- YouTube analytics and retention curves
- Attention span psychology
- Pacing and timing strategies
- Curiosity gap mechanics
- Pattern interrupt techniques
- Information layering
- Payoff timing optimization

YOUR MISSION:
Create engagement strategies that maximize watch time by:

1. RETENTION CURVE DESIGN
   - Identify critical drop-off points (30s, 2min, 5min, etc.)
   - Design retention "hooks" at these moments
   - Create anticipation for upcoming content

2. PACING OPTIMIZATION
   - Fast-paced sections (high energy, quick cuts)
   - Slow-paced sections (depth, reflection)
   - Strategic pacing shifts (keep brain engaged)

3. LOOP STRUCTURES
   - Open loops (questions that need answers)
   - Closed loops (satisfying payoffs)
   - Callback loops (returning to earlier points)

4. PATTERN INTERRUPTS
   - Visual changes
   - Tone shifts
   - Unexpected information
   - Format changes

5. CURIOSITY MECHANICS
   - Information gaps (questions to answer)
   - Preview techniques (showing what's coming)
   - Mystery elements (reveal timing)

You provide minute-by-minute engagement strategies with specific techniques."""
    
    def optimize_engagement(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        MAIN OPTIMIZATION METHOD - Create engagement strategy
        
        This method analyzes the content and creates a detailed engagement
        strategy with specific techniques placed at strategic moments.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            Current state with:
            - topic: The video topic
            - duration_minutes: Target video length
            - research_findings: Content to work with
            - viral_patterns: Identified patterns
            - viral_hooks: Generated hooks
        
        Returns:
        --------
        Dict[str, Any]
            Updated state with engagement strategy
        """
        
        print("\n⚡ Engagement Optimizer: Designing retention strategy...")
        
        # Extract state information
        topic = state.get("topic", "Unknown")
        duration = state.get("duration_minutes", 30)
        research = state.get("research_findings", "No research")[:2000]
        patterns = state.get("viral_patterns", "No patterns")[:1500]
        hooks = state.get("viral_hooks", "No hooks")[:1500]
        audience = state.get("target_audience", "General")
        
        # Build the optimization prompt
        optimization_prompt = f"""CREATE ENGAGEMENT OPTIMIZATION STRATEGY

VIDEO SPECS:
- Topic: {topic}
- Duration: {duration} minutes
- Target Audience: {audience}

RESEARCH CONTENT:
{research}

VIRAL PATTERNS:
{patterns}

HOOK OPTIONS:
{hooks}

YOUR TASK:
Design a minute-by-minute engagement strategy that maximizes retention.

Provide:

1. OVERALL RETENTION STRATEGY
   - Target retention curve shape
   - Key engagement goals
   - Critical save points

2. MINUTE-BY-MINUTE BREAKDOWN

For each section, provide:

[MINUTES 0-2: Opening & Hook]
RETENTION TARGET: 90-100%
ENGAGEMENT TECHNIQUES:
- [Specific technique 1]
- [Specific technique 2]
- [Specific technique 3]

PACING: [Fast/Medium/Slow]
WHY THIS WORKS: [Psychological reasoning]

CRITICAL MOMENT: [Exact timestamp and what happens]

---

[Continue for all time segments through the {duration}-minute video]

3. RETENTION CHECKPOINTS

Create 5-7 "retention checkpoints" - critical moments where viewers
typically drop off, and specific techniques to prevent this:

CHECKPOINT 1: [Timestamp]
DROP-OFF RISK: [Why viewers might leave]
RETENTION TECHNIQUE: [Specific strategy]
EFFECTIVENESS: [1-10 score]

4. LOOP STRUCTURE MAP

Show all open and closed loops:
- When loops open (creating curiosity)
- When loops close (providing payoff)
- Strategic timing of each

5. PATTERN INTERRUPT SCHEDULE

List 8-12 pattern interrupts throughout video:
[Timestamp]: [What changes] - [Why it works]

6. ENGAGEMENT METRICS PREDICTION

Predict performance:
- Expected average view duration: X minutes (X%)
- Expected retention at key points
- Engagement rate prediction
- Viral potential: X/10

Provide actionable, timestamp-specific strategies."""
        
        try:
            # Call Claude for optimization strategy
            response = self.client.messages.create(
                model=self.model,
                max_tokens=5000,  # Long response for detailed breakdown
                temperature=0.7,  # Balanced creativity
                system=self.agent_role,
                messages=[
                    {
                        "role": "user",
                        "content": optimization_prompt
                    }
                ]
            )
            
            # Extract the strategy
            strategy = response.content[0].text
            
            # Parse key metrics if present
            # Look for predicted retention percentage
            predicted_retention = 0.0
            if "%" in strategy:
                # Try to find retention prediction
                for line in strategy.split("\n"):
                    if "retention" in line.lower() and "%" in line:
                        try:
                            # Extract percentage
                            pct = float(''.join(filter(lambda x: x.isdigit() or x == '.', 
                                                      line.split("%")[0].split()[-1])))
                            predicted_retention = max(predicted_retention, pct)
                        except:
                            pass
            
            # If no specific prediction found, estimate based on strategy quality
            if predicted_retention == 0.0:
                predicted_retention = 65.0  # Conservative default
            
            # Count techniques mentioned
            technique_count = strategy.count("TECHNIQUE") + strategy.count("technique")
            checkpoint_count = strategy.count("CHECKPOINT")
            
            # Add to state
            state["engagement_strategy"] = strategy
            state["predicted_retention_pct"] = predicted_retention
            state["engagement_technique_count"] = technique_count
            state["retention_checkpoint_count"] = checkpoint_count
            
            # Calculate engagement score based on strategy comprehensiveness
            engagement_score = min(10.0, 
                                  (len(strategy) / 1000) +  # Strategy detail
                                  (technique_count * 0.3) +   # Number of techniques
                                  (checkpoint_count * 0.5))   # Critical checkpoints
            
            state["engagement_optimization_score"] = engagement_score
            
            # Success message
            print(f"✅ Engagement Optimizer: Strategy created")
            print(f"   Predicted Retention: {predicted_retention:.1f}%")
            print(f"   Engagement Score: {engagement_score:.1f}/10")
            print(f"   Techniques: {technique_count} | Checkpoints: {checkpoint_count}")
            
            return state
            
        except Exception as e:
            # Handle errors
            print(f"❌ Engagement Optimizer Error: {str(e)}")
            
            state["engagement_strategy"] = f"Optimization failed: {str(e)}"
            state["predicted_retention_pct"] = 0.0
            state["engagement_optimization_score"] = 0.0
            
            return state
    
    def get_retention_checkpoints(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        EXTRACT RETENTION CHECKPOINTS - Get critical moments
        
        Parses the strategy to extract the specific retention checkpoints
        where viewers are most likely to drop off.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State with engagement strategy
        
        Returns:
        --------
        List[Dict[str, Any]]
            List of checkpoints with timestamps and techniques
        """
        
        strategy = state.get("engagement_strategy", "")
        
        if not strategy:
            return []
        
        checkpoints = []
        
        # Split into lines and look for CHECKPOINT markers
        lines = strategy.split("\n")
        current_checkpoint = {}
        
        for line in lines:
            if "CHECKPOINT" in line.upper():
                # Save previous checkpoint if exists
                if current_checkpoint:
                    checkpoints.append(current_checkpoint)
                
                # Start new checkpoint
                current_checkpoint = {
                    "line": line.strip(),
                    "details": []
                }
            elif current_checkpoint and line.strip():
                # Add details to current checkpoint
                current_checkpoint["details"].append(line.strip())
        
        # Add last checkpoint
        if current_checkpoint:
            checkpoints.append(current_checkpoint)
        
        return checkpoints
    
    def get_pacing_breakdown(self, state: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        GET PACING BREAKDOWN - Extract pacing recommendations
        
        Returns a dictionary showing fast vs slow paced sections.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State with engagement strategy
        
        Returns:
        --------
        Dict[str, List[str]]
            Dictionary with 'fast', 'medium', 'slow' pacing sections
        """
        
        strategy = state.get("engagement_strategy", "")
        
        pacing = {
            "fast": [],
            "medium": [],
            "slow": []
        }
        
        if not strategy:
            return pacing
        
        # Look for pacing indicators
        lines = strategy.split("\n")
        current_section = None
        
        for line in lines:
            # Check for section headers (minutes)
            if "MINUTES" in line.upper() or "MINUTE" in line.upper():
                current_section = line.strip()
            
            # Check for pacing indicators
            if "PACING:" in line.upper():
                pace_line = line.upper()
                
                if "FAST" in pace_line:
                    if current_section:
                        pacing["fast"].append(current_section)
                elif "SLOW" in pace_line:
                    if current_section:
                        pacing["slow"].append(current_section)
                elif "MEDIUM" in pace_line:
                    if current_section:
                        pacing["medium"].append(current_section)
        
        return pacing


# ==============================================================================
# TESTING SECTION
# ==============================================================================

if __name__ == "__main__":
    """
    TEST THE ENGAGEMENT OPTIMIZER
    """
    
    print("=" * 70)
    print("TESTING ENGAGEMENT OPTIMIZER SUBAGENT")
    print("=" * 70)
    
    # Test state
    test_state = {
        "topic": "The Science of Procrastination",
        "duration_minutes": 15,
        "target_audience": "Young professionals, students, 18-35",
        "research_findings": "Procrastination is emotional regulation...",
        "viral_patterns": "Contrarian hooks work well, myth-busting format...",
        "viral_hooks": "Hook 1: 'What if procrastination isn't laziness...'..."
    }
    
    # Create optimizer
    optimizer = EngagementOptimizer()
    
    # Run optimization
    result_state = optimizer.optimize_engagement(test_state)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nPredicted Retention: {result_state.get('predicted_retention_pct', 0):.1f}%")
    print(f"Engagement Score: {result_state.get('engagement_optimization_score', 0):.1f}/10")
    print(f"Techniques Identified: {result_state.get('engagement_technique_count', 0)}")
    print(f"Retention Checkpoints: {result_state.get('retention_checkpoint_count', 0)}")
    
    # Show checkpoints
    checkpoints = optimizer.get_retention_checkpoints(result_state)
    print(f"\n📍 RETENTION CHECKPOINTS: {len(checkpoints)}")
    for i, cp in enumerate(checkpoints[:3], 1):
        print(f"  {i}. {cp.get('line', 'N/A')}")
    
    # Show pacing
    pacing = optimizer.get_pacing_breakdown(result_state)
    print(f"\n🎬 PACING BREAKDOWN:")
    print(f"  Fast sections: {len(pacing['fast'])}")
    print(f"  Medium sections: {len(pacing['medium'])}")
    print(f"  Slow sections: {len(pacing['slow'])}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
