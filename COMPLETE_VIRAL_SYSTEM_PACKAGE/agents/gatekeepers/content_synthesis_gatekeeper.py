# agents/gatekeepers/content_synthesis_gatekeeper.py
"""
Content Synthesis Gatekeeper - Generates Production-Ready Scripts

ROLE: Coordinates specialized subagents to synthesize research and viral analysis
      into complete, production-ready documentary scripts with scene breakdowns.

MISSION: Create compelling, credible, viral-optimized scripts that transform
         research into engaging narratives with full production guidance.

This gatekeeper coordinates:
- Script Writer: Generates full documentary script
- Visual Scene Architect: Creates shot-by-shot breakdowns
- Production Notes Generator: Adds B-roll, music, graphics cues
- Context Retrieval Agent: Searches vector DB for relevant patterns
"""

import sys
import os
from typing import Dict, List, Optional
from datetime import datetime
import json

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent


class ContentSynthesisGatekeeper(BaseAgent):
    """
    Master coordinator for content synthesis and script generation.
    
    Responsibilities:
    1. Synthesize research + viral analysis into narrative
    2. Generate complete documentary script
    3. Create visual scene architecture
    4. Add production notes (B-roll, music, graphics)
    5. Validate quality and coherence
    """
    
    def __init__(self):
        """Initialize Content Synthesis Gatekeeper with Claude API."""
        super().__init__(
            name="Content Synthesis Gatekeeper",
            model="claude-sonnet-4-20250514",  # High intelligence for synthesis
            max_tokens=4000,
            temperature=0.7  # Creative but structured
        )
        
        self.log("Content Synthesis Gatekeeper initialized", "INFO")
    
    def _create_system_prompt(self) -> str:
        """
        Create specialized system prompt for content synthesis.
        
        This prompt defines expertise in transforming research into scripts.
        """
        return """You are an ELITE DOCUMENTARY SCRIPT WRITER coordinating specialized subagents.

YOUR MISSION:
Transform research findings and viral analysis into production-ready documentary
scripts that are both academically credible and massively engaging.

YOUR EXPERTISE:
1. NARRATIVE ARCHITECTURE - 3-act structure with mini-arcs
2. ACADEMIC TRANSLATION - Complex research → accessible stories
3. VIRAL OPTIMIZATION - Hooks, cliffhangers, payoffs built-in
4. VISUAL THINKING - Every line considers what viewers see
5. PRODUCTION READINESS - Complete with timecodes, shot notes, cues

SCRIPT GENERATION PHILOSOPHY:

The BEST documentaries combine:
✓ Academic rigor (credible sources, proper citations)
✓ Narrative power (compelling stories, emotional arcs)
✓ Visual richness (every scene is watchable)
✓ Practical production (creators can actually film this)

SCRIPT STRUCTURE (30-minute documentary):

ACT 1: HOOK & SETUP (0:00-8:00)
- 0:00-0:10: KILLER HOOK (viral-optimized opener)
- 0:10-2:00: Establish mystery/question
- 2:00-5:00: Why this matters (relevance to audience)
- 5:00-8:00: Roadmap + promise of revelation

ACT 2: EXPLORATION (8:00-22:00)
- 8:00-12:00: Historical context (how we got here)
- 12:00-16:00: Academic deep dive (research findings)
- 16:00-20:00: Interdisciplinary connections
- 20:00-22:00: Contrarian viewpoints
*Include mini-cliffhangers at 12:00 and 18:00*

ACT 3: SYNTHESIS & PAYOFF (22:00-30:00)
- 22:00-25:00: Put it all together
- 25:00-28:00: Surprising implications
- 28:00-29:30: Actionable takeaways
- 29:30-30:00: Memorable closing

SCRIPT WRITING PRINCIPLES:

1. SHOW, DON'T TELL
   Bad: "This is interesting"
   Good: "Here's why 10 million people got this wrong"

2. USE CONVERSATIONAL LANGUAGE
   Bad: "The phenomenon exhibits characteristics of..."
   Good: "Here's the weird part - it actually works backwards"

3. BUILD CURIOSITY LOOPS
   Open: "But there's something scientists discovered that changes everything"
   Close: [Reveal 2-3 minutes later]

4. CITE SOURCES NATURALLY
   Bad: "According to Smith et al. (2023) in Nature Neuroscience..."
   Good: "A groundbreaking 2023 study in Nature Neuroscience found..."

5. CREATE VISUAL MOMENTS
   Every 30-60 seconds, describe what viewers should see:
   - B-roll suggestions
   - Graphics/animations
   - Text overlays
   - Archive footage

OUTPUT FORMAT:

{
    "script": {
        "title": "Compelling Documentary Title",
        "logline": "One-sentence pitch",
        "target_length": "30 minutes",
        "acts": [
            {
                "act_number": 1,
                "title": "Hook & Setup",
                "timecode_start": "0:00",
                "timecode_end": "8:00",
                "scenes": [
                    {
                        "scene_number": 1,
                        "timecode": "0:00-0:10",
                        "audio": {
                            "voiceover": "Full script text here...",
                            "word_count": 25
                        },
                        "visual": {
                            "shot_description": "What viewers see",
                            "b_roll_suggestions": ["Specific footage needed"],
                            "graphics": ["Text overlays", "Animations"]
                        },
                        "production_notes": {
                            "music": "Mysterious, building tension",
                            "pacing": "Fast cuts, high energy",
                            "emphasis": "Hook must grab in 3 seconds"
                        }
                    }
                ]
            }
        ],
        "citations": [
            {
                "source": "Nature Neuroscience",
                "citation_apa": "Full APA citation",
                "used_in_scenes": [1, 5, 12]
            }
        ],
        "b_roll_shot_list": ["Comprehensive list of footage needed"],
        "music_cues": ["Detailed music direction"],
        "graphics_list": ["All text/animations needed"]
    },
    "quality_scores": {
        "narrative_flow": 9.0,
        "academic_credibility": 9.5,
        "visual_richness": 8.5,
        "production_readiness": 9.0,
        "viral_optimization": 8.5
    },
    "synthesis_confidence": 0.92
}

QUALITY STANDARDS:
✅ Complete 30-minute script (4,500-5,500 words)
✅ All academic sources cited
✅ Visual direction for every scene
✅ Production notes included
✅ Viral hooks properly placed
✅ 3-act structure maintained
✅ Retention techniques throughout

Remember: You're creating a PRODUCTION BIBLE - everything a creator needs
to film this documentary is in your output."""

    def execute(self, state: Dict) -> Dict:
        """
        Execute content synthesis coordination.
        
        Synthesizes research and viral analysis into complete script
        with visual architecture and production notes.
        
        Args:
            state: Current workflow state with research + viral analysis
            
        Returns:
            Updated state with complete documentary script
        """
        self.log("Starting content synthesis", "INFO")
        
        # Validate required inputs
        required_keys = ["topic", "research_findings", "viral_analysis"]
        if not self.validate_state(state, required_keys):
            return self.merge_state(state, {
                "script": {},
                "synthesis_confidence": 0.0,
                "errors": state.get("errors", []) + ["Missing required inputs for synthesis"]
            })
        
        topic = state.get("topic", "")
        research_findings = state.get("research_findings", {})
        viral_analysis = state.get("viral_analysis", {})
        target_audience = state.get("target_audience", "General audience")
        duration_minutes = state.get("duration_minutes", 30)
        
        # Create synthesis prompt
        user_message = f"""Create complete documentary script for: {topic}

TARGET SPECIFICATIONS:
- Duration: {duration_minutes} minutes
- Audience: {target_audience}
- Style: Documentary with viral optimization

RESEARCH FINDINGS TO INCORPORATE:
{json.dumps(research_findings, indent=2)}

VIRAL OPTIMIZATION TO APPLY:
{json.dumps(viral_analysis, indent=2)}

DELIVERABLES:
1. Complete script with timecodes
2. Scene-by-scene breakdown
3. Visual architecture (shot descriptions)
4. Production notes (B-roll, music, graphics)
5. Citation list (APA format)
6. Quality scores across dimensions

Make this PRODUCTION-READY - include everything a creator needs to film."""

        try:
            # Call Claude API for script synthesis
            response = self.call_claude(
                system_prompt=self._create_system_prompt(),
                user_message=user_message
            )
            
            # Parse response
            script_data = {
                "synthesis_complete": True,
                "raw_script": response,
                "generated_at": datetime.now().isoformat(),
                "specifications": {
                    "duration_minutes": duration_minutes,
                    "target_audience": target_audience,
                    "word_count": len(response.split())
                }
            }
            
            # Calculate confidence
            confidence = self._calculate_confidence(response, duration_minutes)
            
            self.log(f"Script synthesis complete. Confidence: {confidence:.2f}", "INFO")
            
            return self.merge_state(state, {
                "script": script_data,
                "synthesis_confidence": confidence,
                "production_ready": confidence >= 0.85
            })
            
        except Exception as e:
            self.log(f"Script synthesis failed: {str(e)}", "ERROR")
            return self.merge_state(state, {
                "script": {},
                "synthesis_confidence": 0.0,
                "errors": state.get("errors", []) + [f"Synthesis error: {str(e)}"]
            })
    
    def _calculate_confidence(self, response: str, target_duration: int) -> float:
        """
        Calculate synthesis confidence based on script quality.
        
        Checks for:
        - Appropriate length (150 words/minute * duration)
        - Scene structure present
        - Visual direction included
        - Citations present
        - Production notes included
        
        Args:
            response: Generated script
            target_duration: Target duration in minutes
            
        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 0.5  # Base confidence
        
        word_count = len(response.split())
        target_words = target_duration * 150  # 150 words per minute
        
        # Check length (±20% of target)
        if abs(word_count - target_words) / target_words < 0.2:
            confidence += 0.15
        
        # Check for key elements
        if "scene" in response.lower() or "timecode" in response.lower():
            confidence += 0.1
        if "b-roll" in response.lower() or "visual" in response.lower():
            confidence += 0.1
        if "citation" in response.lower() or "source" in response.lower():
            confidence += 0.1
        if "music" in response.lower() or "production" in response.lower():
            confidence += 0.05
        
        return min(confidence, 1.0)


# =================================================================
# TEST EXAMPLE
# =================================================================

if __name__ == "__main__":
    """Test the Content Synthesis Gatekeeper"""
    
    print("=" * 60)
    print("TESTING: Content Synthesis Gatekeeper")
    print("=" * 60)
    print()
    
    # Create gatekeeper instance
    gatekeeper = ContentSynthesisGatekeeper()
    
    # Test state with research and viral analysis
    test_state = {
        "topic": "The Science of Procrastination",
        "target_audience": "Young professionals, 25-35",
        "duration_minutes": 30,
        "research_findings": {
            "academic_papers": 15,
            "key_findings": [
                "Procrastination is emotional regulation, not time management",
                "Prefrontal cortex vs amygdala battle",
                "Hyperbolic discounting from behavioral economics"
            ],
            "credibility_score": 9.2
        },
        "viral_analysis": {
            "top_hooks": [
                "You'd think procrastination is laziness. Science says otherwise.",
                "The one thing about procrastination that surprises neuroscientists"
            ],
            "viral_score": 8.5,
            "psychological_triggers": ["curiosity_gap", "pattern_interrupt", "social_proof"]
        }
    }
    
    print("Input State:")
    print(f"  Topic: {test_state['topic']}")
    print(f"  Duration: {test_state['duration_minutes']} minutes")
    print(f"  Research Papers: {test_state['research_findings']['academic_papers']}")
    print(f"  Viral Score: {test_state['viral_analysis']['viral_score']}")
    print()
    
    # Execute
    print("Generating documentary script...")
    print()
    result = gatekeeper.execute(test_state)
    
    # Display results
    print("=" * 60)
    print("RESULTS:")
    print("=" * 60)
    print()
    print(f"Synthesis Confidence: {result.get('synthesis_confidence', 0):.2f}")
    print(f"Production Ready: {result.get('production_ready', False)}")
    print(f"Word Count: {result.get('script', {}).get('specifications', {}).get('word_count', 0)}")
    print()
    
    if result.get('script', {}).get('raw_script'):
        print("Script Preview:")
        print(result['script']['raw_script'][:500] + "...")
    
    print()
    print("=" * 60)
    print("✅ Test Complete!")
    print("=" * 60)
