# agents/gatekeepers/viral_analyst_gatekeeper.py
"""
Viral Analyst Gatekeeper - Analyzes and Optimizes for Viral Potential

ROLE: Coordinates specialized subagents to analyze viral patterns, generate hooks,
      and optimize content for maximum engagement and shareability.

MISSION: Transform research into viral-ready content by applying proven psychological
         triggers, engagement patterns, and attention-capture techniques.

This gatekeeper coordinates:
- Pattern Analyzer: Studies successful viral videos
- Hook Generator: Creates attention-grabbing openings
- Engagement Optimizer: Maximizes watch time and retention
- Psychology Trigger Detector: Identifies and applies triggers
"""

import sys
import os
from typing import Dict, List, Optional

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent


class ViralAnalystGatekeeper(BaseAgent):
    """
    Master coordinator for viral content optimization.
    
    Responsibilities:
    1. Coordinate viral analysis subagents
    2. Generate viral-optimized hooks and patterns
    3. Apply psychological triggers
    4. Validate engagement potential
    5. Provide viral score and recommendations
    """
    
    def __init__(self):
        """Initialize Viral Analyst Gatekeeper with Claude API."""
        super().__init__(
            name="Viral Analyst Gatekeeper",
            model="claude-sonnet-4-20250514",  # High intelligence for coordination
            max_tokens=4000,
            temperature=0.5  # Balanced: creative but strategic
        )
        
        self.log("Viral Analyst Gatekeeper initialized", "INFO")
    
    def _create_system_prompt(self) -> str:
        """
        Create specialized system prompt for viral analysis coordination.
        
        This prompt defines the gatekeeper's expertise in viral content.
        """
        return """You are an ELITE VIRAL CONTENT ANALYST coordinating specialized subagents.

YOUR MISSION:
Transform research findings into viral-ready content that captures attention,
maintains engagement, and drives shares.

YOUR EXPERTISE:
1. VIRAL PATTERNS - Analyze successful videos (1M+ views)
2. PSYCHOLOGICAL TRIGGERS - Apply proven engagement drivers
3. HOOK GENERATION - Create irresistible openings (3-second rule)
4. ENGAGEMENT OPTIMIZATION - Maximize watch time and retention
5. SHAREABILITY - Design content people MUST share

COORDINATION STRATEGY:

PHASE 1: Pattern Analysis
- Study 10+ successful videos on similar topics
- Identify common patterns in:
  * Opening hooks (first 3-10 seconds)
  * Story structure (pacing, climaxes, payoffs)
  * Visual elements (what kept viewers watching)
  * Comments (what viewers found most engaging)
- Extract viral formula for this specific topic

PHASE 2: Hook Generation
- Create 5-10 potential hooks using:
  * Curiosity Gap ("The one thing experts won't tell you...")
  * Pattern Interrupt ("Everything you know about X is wrong")
  * Bold Claims ("This will change how you see X forever")
  * Emotional Triggers (surprise, shock, awe, humor)
- Score each hook (1-10) on attention-capture potential
- Select top 3 hooks for different audience segments

PHASE 3: Engagement Optimization
- Design retention strategies:
  * Mini-cliffhangers every 2-3 minutes
  * Pattern interrupts at predicted drop-off points
  * Callback loops (reference earlier points)
  * Payoff moments (reward sustained attention)
- Optimize pacing for 60%+ average watch time

PHASE 4: Psychology Trigger Application
Apply these proven triggers throughout content:
- CURIOSITY GAP: Open loops that demand closure
- SOCIAL PROOF: "Millions believe..." / "Experts agree..."
- SCARCITY: "Rarely discussed..." / "Hidden research..."
- AUTHORITY: Cite credible sources prominently
- STORYTELLING: Human narratives > dry facts
- SURPRISE: Counter-intuitive revelations
- PRACTICAL VALUE: Actionable takeaways

PHASE 5: Viral Score Calculation
Score content (1-10) across dimensions:
- Hook Strength (first 10 seconds)
- Engagement Potential (will they watch to end?)
- Shareability (will they tell others?)
- Emotional Impact (do they feel something?)
- Practical Value (did they learn something useful?)

Overall Viral Score = weighted average with emphasis on Hook + Engagement

OUTPUT FORMAT:
{
    "viral_analysis": {
        "pattern_insights": [...],
        "top_hooks": [
            {
                "hook_text": "...",
                "hook_type": "curiosity_gap",
                "attention_score": 9.2,
                "target_audience": "science enthusiasts"
            }
        ],
        "engagement_strategy": {
            "retention_techniques": [...],
            "pacing_guidelines": "...",
            "drop_off_prevention": [...]
        },
        "psychological_triggers": [
            {
                "trigger": "curiosity_gap",
                "application": "...",
                "placement": "0:00-0:10"
            }
        ],
        "viral_scores": {
            "hook_strength": 9.0,
            "engagement_potential": 8.5,
            "shareability": 8.0,
            "emotional_impact": 7.5,
            "practical_value": 8.0,
            "overall_viral_score": 8.2
        }
    },
    "viral_confidence": 0.89,
    "recommendations": [...]
}

QUALITY STANDARDS:
✅ Overall viral score ≥ 7.0
✅ Hook strength ≥ 8.0
✅ At least 3 psychological triggers identified
✅ Specific placement timestamps for all elements
✅ Evidence-based (cite successful video examples)

Remember: You're not just analyzing - you're ENGINEERING virality through
systematic application of proven patterns and psychological principles."""

    def execute(self, state: Dict) -> Dict:
        """
        Execute viral analysis coordination.
        
        Coordinates subagents to analyze patterns, generate hooks,
        and optimize for viral potential.
        
        Args:
            state: Current workflow state with research findings
            
        Returns:
            Updated state with viral analysis and optimization
        """
        self.log("Starting viral analysis coordination", "INFO")
        
        # Validate required inputs
        if not self.validate_state(state, ["topic"]):
            return self.merge_state(state, {
                "viral_analysis": {},
                "viral_confidence": 0.0,
                "errors": state.get("errors", []) + ["Missing topic for viral analysis"]
            })
        
        topic = state.get("topic", "")
        research_findings = state.get("research_findings", {})
        target_audience = state.get("target_audience", "General audience")
        
        # Create analysis prompt
        user_message = f"""Analyze viral potential for: {topic}

TARGET AUDIENCE: {target_audience}

RESEARCH FINDINGS AVAILABLE:
{json.dumps(research_findings, indent=2) if research_findings else "No research findings yet"}

TASK:
1. Analyze viral patterns from successful videos on this topic
2. Generate 5 powerful hooks (score each 1-10)
3. Design engagement optimization strategy
4. Identify psychological triggers to apply
5. Calculate viral score across all dimensions

Provide actionable viral optimization recommendations."""

        try:
            # Call Claude API for viral analysis
            response = self.call_claude(
                system_prompt=self._create_system_prompt(),
                user_message=user_message
            )
            
            # Parse response (in production, would parse JSON properly)
            # For now, return structured response
            viral_analysis = {
                "analysis_complete": True,
                "raw_analysis": response,
                "timestamp": datetime.now().isoformat()
            }
            
            # Calculate confidence based on response quality
            confidence = self._calculate_confidence(response)
            
            self.log(f"Viral analysis complete. Confidence: {confidence:.2f}", "INFO")
            
            return self.merge_state(state, {
                "viral_analysis": viral_analysis,
                "viral_confidence": confidence,
                "viral_optimization_ready": confidence >= 0.75
            })
            
        except Exception as e:
            self.log(f"Viral analysis failed: {str(e)}", "ERROR")
            return self.merge_state(state, {
                "viral_analysis": {},
                "viral_confidence": 0.0,
                "errors": state.get("errors", []) + [f"Viral analysis error: {str(e)}"]
            })
    
    def _calculate_confidence(self, response: str) -> float:
        """
        Calculate confidence score based on response quality.
        
        Checks for:
        - Presence of specific hooks
        - Viral scores mentioned
        - Psychological triggers identified
        - Actionable recommendations
        
        Args:
            response: Claude's analysis response
            
        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 0.5  # Base confidence
        
        # Check for key elements
        if "hook" in response.lower():
            confidence += 0.1
        if "viral" in response.lower():
            confidence += 0.1
        if "trigger" in response.lower() or "psychological" in response.lower():
            confidence += 0.1
        if "engagement" in response.lower():
            confidence += 0.1
        if len(response) > 500:  # Substantial response
            confidence += 0.1
        
        return min(confidence, 1.0)


# =================================================================
# TEST EXAMPLE
# =================================================================

if __name__ == "__main__":
    """Test the Viral Analyst Gatekeeper"""
    
    print("=" * 60)
    print("TESTING: Viral Analyst Gatekeeper")
    print("=" * 60)
    print()
    
    # Create gatekeeper instance
    gatekeeper = ViralAnalystGatekeeper()
    
    # Test state
    test_state = {
        "topic": "The Science of Procrastination",
        "target_audience": "Young professionals, 25-35",
        "research_findings": {
            "academic_papers": 15,
            "key_insight": "Procrastination is emotional regulation, not time management",
            "surprising_fact": "Leonardo da Vinci took 16 years to complete Mona Lisa"
        }
    }
    
    print("Input State:")
    print(f"  Topic: {test_state['topic']}")
    print(f"  Audience: {test_state['target_audience']}")
    print()
    
    # Execute
    print("Executing viral analysis...")
    print()
    result = gatekeeper.execute(test_state)
    
    # Display results
    print("=" * 60)
    print("RESULTS:")
    print("=" * 60)
    print()
    print(f"Viral Confidence: {result.get('viral_confidence', 0):.2f}")
    print(f"Ready for Optimization: {result.get('viral_optimization_ready', False)}")
    print()
    
    if result.get('viral_analysis', {}).get('raw_analysis'):
        print("Viral Analysis Preview:")
        print(result['viral_analysis']['raw_analysis'][:500] + "...")
    
    print()
    print("=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)
