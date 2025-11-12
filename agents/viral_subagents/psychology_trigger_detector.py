"""
PSYCHOLOGY TRIGGER DETECTOR SUBAGENT
=====================================
Part of: Viral Analyst Gatekeeper
Purpose: Identifies and strategically applies psychological triggers that drive
         engagement, sharing, and viral spread

This agent is a specialist in behavioral psychology and applies specific
psychological triggers (curiosity, fear, identity, social proof, etc.) at
strategic moments to maximize engagement and sharing behavior.

Author: Advanced Multi-Agent System
Created: 2024
"""

import anthropic
import os
from typing import Dict, List, Any

class PsychologyTriggerDetector:
    """
    PSYCHOLOGY TRIGGER DETECTOR - Behavioral Psychology Specialist
    
    This agent identifies which psychological triggers will be most effective
    for the target audience and content, then creates a strategy for applying
    them throughout the video.
    
    KEY TRIGGERS ANALYZED:
    - Curiosity (information gaps, mysteries)
    - Fear/Anxiety (loss aversion, threats)
    - Identity (self-perception, group belonging)
    - Social Proof (what others do/think)
    - Authority (expert opinions, credentials)
    - Scarcity (limited time/access)
    - Reciprocity (giving value first)
    - Consistency (building on prior beliefs)
    - Emotion (joy, anger, surprise, sadness)
    
    The goal: Create content that triggers sharing and engagement behaviors.
    """
    
    def __init__(self):
        """
        INITIALIZATION - Set up the Psychology Trigger Detector
        
        Prepares the agent for analyzing and applying psychological triggers.
        """
        
        # Get API key from environment variables
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found!\n"
                "Add to .env file: ANTHROPIC_API_KEY=your_key_here"
            )
        
        # Initialize the Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Use the most advanced Claude model
        self.model = "claude-sonnet-4-20250514"
        
        # Define the agent's specialized role and knowledge
        self.agent_role = """You are the PSYCHOLOGY TRIGGER DETECTOR - an expert in behavioral psychology and viral content.

YOUR EXPERTISE:
- Behavioral psychology (Cialdini's principles, Kahneman's work)
- Emotional triggers and limbic system responses
- Social psychology and group dynamics
- Cognitive biases and heuristics
- Viral content psychology
- Neuroscience of decision-making
- Identity and self-concept triggers

YOUR KNOWLEDGE OF KEY TRIGGERS:

1. CURIOSITY TRIGGERS
   - Information gaps (Loewenstein's theory)
   - Mystery and suspense
   - Pattern violation
   - Delayed resolution

2. FEAR/ANXIETY TRIGGERS
   - Loss aversion (Kahneman & Tversky)
   - Threat perception
   - Uncertainty amplification
   - Safety/security needs

3. IDENTITY TRIGGERS
   - Self-concept reinforcement
   - Group belonging signals
   - Status and recognition
   - Values alignment

4. SOCIAL PROOF
   - Bandwagon effect
   - Authority figures
   - Testimonials and reviews
   - Crowd behavior

5. EMOTION TRIGGERS
   - High-arousal emotions (anger, awe, anxiety)
   - Positive emotions (joy, surprise)
   - Moral emotions (outrage, elevation)
   - Nostalgic emotions

6. SCARCITY & URGENCY
   - Time limitation
   - Exclusivity
   - Limited access
   - FOMO (Fear of Missing Out)

YOUR MISSION:
Analyze content and identify which psychological triggers will be most effective,
then create a trigger application strategy with specific placements and intensities."""
    
    def detect_triggers(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        MAIN DETECTION METHOD - Identify and strategize trigger usage
        
        This method analyzes the content, audience, and objectives to determine
        which psychological triggers to use and how to apply them.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            Current state with:
            - topic: The content topic
            - target_audience: Demographic info
            - research_findings: Content substance
            - viral_hooks: Generated hooks
            - engagement_strategy: Engagement plan
        
        Returns:
        --------
        Dict[str, Any]
            Updated state with trigger strategy
        """
        
        print("\n🧠 Psychology Trigger Detector: Analyzing psychological triggers...")
        
        # Extract information from state
        topic = state.get("topic", "Unknown")
        audience = state.get("target_audience", "General audience")
        research = state.get("research_findings", "No research")[:2000]
        hooks = state.get("viral_hooks", "No hooks")[:1500]
        engagement = state.get("engagement_strategy", "No strategy")[:1500]
        duration = state.get("duration_minutes", 30)
        
        # Build the trigger analysis prompt
        trigger_prompt = f"""ANALYZE PSYCHOLOGICAL TRIGGERS

CONTENT ANALYSIS:
Topic: {topic}
Target Audience: {audience}
Duration: {duration} minutes

RESEARCH CONTENT:
{research}

HOOK STRATEGIES:
{hooks}

ENGAGEMENT PLAN:
{engagement}

YOUR TASK:
Identify the most effective psychological triggers for this content and create
a comprehensive trigger application strategy.

Provide:

1. TRIGGER EFFECTIVENESS ANALYSIS

For each major trigger category, rate its potential effectiveness:

CURIOSITY:
Effectiveness: X/10
Why: [Specific reasons based on topic and audience]
Key Opportunities: [Where in content this applies]

FEAR/ANXIETY:
Effectiveness: X/10
Why: [Reasoning]
Key Opportunities: [Applications]

IDENTITY:
Effectiveness: X/10
Why: [Reasoning]
Key Opportunities: [Applications]

SOCIAL PROOF:
Effectiveness: X/10
Why: [Reasoning]
Key Opportunities: [Applications]

EMOTION:
Effectiveness: X/10
Primary Emotions: [Which specific emotions]
Why: [Reasoning]
Key Opportunities: [Applications]

[Continue for other relevant triggers]

2. TOP 3 TRIGGER STRATEGY

Select the 3 most powerful triggers for this content:

TRIGGER 1: [Name]
POWER RATING: X/10
APPLICATION STRATEGY:
- Opening (0-2 min): [How to deploy]
- Middle (3-7 min): [How to amplify]
- Closing (8-10 min): [How to reinforce]

SPECIFIC TECHNIQUES:
1. [Technique name]: [How it works]
2. [Technique name]: [How it works]
3. [Technique name]: [How it works]

EXPECTED IMPACT:
- Engagement boost: +X%
- Sharing likelihood: +X%
- Emotional resonance: X/10

[Repeat for Trigger 2 and 3]

3. TRIGGER PLACEMENT MAP

Create a timeline showing when to deploy each trigger:

[0:00-2:00] Opening
PRIMARY TRIGGERS: [List]
INTENSITY: [Low/Medium/High]
TECHNIQUE: [Specific method]

[2:00-5:00] Building
PRIMARY TRIGGERS: [List]
INTENSITY: [Low/Medium/High]
TECHNIQUE: [Specific method]

[Continue through entire video]

4. VIRAL PSYCHOLOGY SCORE

Rate the viral potential based on psychological triggers:

CURIOSITY SCORE: X/10
EMOTIONAL INTENSITY: X/10
IDENTITY RESONANCE: X/10
SOCIAL SHARING TRIGGERS: X/10
OVERALL VIRAL PSYCHOLOGY: X/10

Explanation: [Why these scores]

5. SHARING PSYCHOLOGY

What will make people share this?
- Trigger 1: [Name] - "I want others to feel/know..."
- Trigger 2: [Name] - "This reflects who I am..."
- Trigger 3: [Name] - "People need to see this..."

6. OPTIMIZATION RECOMMENDATIONS

Based on psychology, what would make this more viral?
- Recommendation 1: [Specific suggestion]
- Recommendation 2: [Specific suggestion]
- Recommendation 3: [Specific suggestion]

Provide research-backed, specific strategies."""
        
        try:
            # Call Claude to analyze psychological triggers
            response = self.client.messages.create(
                model=self.model,
                max_tokens=5000,  # Long, detailed response
                temperature=0.6,  # Balanced - needs accuracy + creativity
                system=self.agent_role,
                messages=[
                    {
                        "role": "user",
                        "content": trigger_prompt
                    }
                ]
            )
            
            # Extract the trigger analysis
            trigger_analysis = response.content[0].text
            
            # Parse out viral psychology score if present
            viral_score = 7.0  # Default
            if "OVERALL VIRAL PSYCHOLOGY:" in trigger_analysis:
                try:
                    score_section = trigger_analysis.split("OVERALL VIRAL PSYCHOLOGY:")[1].split("\n")[0]
                    viral_score = float(''.join(filter(lambda x: x.isdigit() or x == '.', 
                                                       score_section.split("/")[0])))
                except:
                    pass
            
            # Count triggers identified
            trigger_count = (
                trigger_analysis.upper().count("TRIGGER") + 
                trigger_analysis.upper().count("EFFECTIVENESS:")
            )
            
            # Parse trigger effectiveness scores
            effectiveness_scores = []
            for line in trigger_analysis.split("\n"):
                if "Effectiveness:" in line and "/10" in line:
                    try:
                        score = float(''.join(filter(lambda x: x.isdigit() or x == '.', 
                                                    line.split("Effectiveness:")[1].split("/")[0])))
                        effectiveness_scores.append(score)
                    except:
                        pass
            
            avg_effectiveness = (sum(effectiveness_scores) / len(effectiveness_scores) 
                                if effectiveness_scores else 7.5)
            
            # Add results to state
            state["psychology_triggers"] = trigger_analysis
            state["viral_psychology_score"] = viral_score
            state["trigger_count"] = len(effectiveness_scores)
            state["avg_trigger_effectiveness"] = avg_effectiveness
            state["trigger_effectiveness_scores"] = effectiveness_scores
            
            # Calculate overall psychological impact
            psychological_impact = (viral_score + avg_effectiveness) / 2
            state["psychological_impact_score"] = psychological_impact
            
            # Success message
            print(f"✅ Psychology Trigger Detector: Analysis complete")
            print(f"   Viral Psychology Score: {viral_score:.1f}/10")
            print(f"   Triggers Identified: {len(effectiveness_scores)}")
            print(f"   Avg Effectiveness: {avg_effectiveness:.1f}/10")
            print(f"   Overall Impact: {psychological_impact:.1f}/10")
            
            return state
            
        except Exception as e:
            # Handle errors gracefully
            print(f"❌ Psychology Trigger Detector Error: {str(e)}")
            
            state["psychology_triggers"] = f"Trigger analysis failed: {str(e)}"
            state["viral_psychology_score"] = 0.0
            state["psychological_impact_score"] = 0.0
            
            return state
    
    def get_top_triggers(self, state: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        EXTRACT TOP TRIGGERS - Get the most effective triggers
        
        Parses the analysis to extract the top N most effective psychological
        triggers with their strategies.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State with trigger analysis
        top_n : int
            Number of top triggers to return (default: 3)
        
        Returns:
        --------
        List[Dict[str, Any]]
            List of top triggers with effectiveness and strategies
        """
        
        analysis = state.get("psychology_triggers", "")
        scores = state.get("trigger_effectiveness_scores", [])
        
        if not analysis or not scores:
            return []
        
        # This is a simplified parser
        # In production, you might want more sophisticated parsing
        triggers = []
        
        # Look for trigger sections
        sections = analysis.split("\n\n")
        
        for i, section in enumerate(sections):
            if "Effectiveness:" in section and i < len(scores):
                trigger_name = section.split(":")[0].strip() if ":" in section else f"Trigger {i+1}"
                
                triggers.append({
                    "name": trigger_name,
                    "effectiveness": scores[i] if i < len(scores) else 0.0,
                    "description": section[:200] + "..."
                })
        
        # Sort by effectiveness
        triggers.sort(key=lambda x: x["effectiveness"], reverse=True)
        
        return triggers[:top_n]
    
    def get_sharing_psychology(self, state: Dict[str, Any]) -> Dict[str, str]:
        """
        GET SHARING PSYCHOLOGY - Extract why people will share this
        
        Returns the psychological reasons people will want to share the content.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State with trigger analysis
        
        Returns:
        --------
        Dict[str, str]
            Dictionary with sharing motivations
        """
        
        analysis = state.get("psychology_triggers", "")
        
        if not analysis or "SHARING PSYCHOLOGY" not in analysis:
            return {}
        
        # Extract the sharing psychology section
        if "SHARING PSYCHOLOGY" in analysis:
            sharing_section = analysis.split("SHARING PSYCHOLOGY")[1].split("\n\n")[0]
            
            return {
                "analysis": sharing_section,
                "viral_score": state.get("viral_psychology_score", 0.0)
            }
        
        return {}


# ==============================================================================
# TESTING SECTION
# ==============================================================================

if __name__ == "__main__":
    """
    TEST THE PSYCHOLOGY TRIGGER DETECTOR
    """
    
    print("=" * 70)
    print("TESTING PSYCHOLOGY TRIGGER DETECTOR SUBAGENT")
    print("=" * 70)
    
    # Test state
    test_state = {
        "topic": "The Science of Procrastination",
        "duration_minutes": 15,
        "target_audience": "Young professionals, students, 18-35",
        "research_findings": "Procrastination is emotional regulation not laziness...",
        "viral_hooks": "Hook: What if procrastination isn't what you think...",
        "engagement_strategy": "Fast opening, slow deep sections, loop structures..."
    }
    
    # Create detector
    detector = PsychologyTriggerDetector()
    
    # Run detection
    result_state = detector.detect_triggers(test_state)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nViral Psychology Score: {result_state.get('viral_psychology_score', 0):.1f}/10")
    print(f"Psychological Impact: {result_state.get('psychological_impact_score', 0):.1f}/10")
    print(f"Triggers Identified: {result_state.get('trigger_count', 0)}")
    print(f"Avg Effectiveness: {result_state.get('avg_trigger_effectiveness', 0):.1f}/10")
    
    # Show top triggers
    print("\n🎯 TOP 3 TRIGGERS:")
    top_triggers = detector.get_top_triggers(result_state, top_n=3)
    for i, trigger in enumerate(top_triggers, 1):
        print(f"\n  {i}. {trigger['name']}")
        print(f"     Effectiveness: {trigger['effectiveness']:.1f}/10")
    
    # Show sharing psychology
    sharing = detector.get_sharing_psychology(result_state)
    if sharing:
        print(f"\n💬 SHARING PSYCHOLOGY:")
        print(f"   Viral Score: {sharing.get('viral_score', 0):.1f}/10")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
