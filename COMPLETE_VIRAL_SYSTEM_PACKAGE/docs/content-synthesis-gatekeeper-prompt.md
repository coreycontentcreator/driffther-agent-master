# agents/gatekeepers/content_synthesis_gatekeeper.py

"""
Content Synthesis Gatekeeper: Combines research and viral strategy into creative concepts.
This gatekeeper generates the unique angles that make the documentary stand out.
"""

from agents.base_agent import BaseAgent
from config.settings import settings
from typing import Dict, Any
import json


class ContentSynthesisGatekeeper(BaseAgent):
    """
    Responsible for:
    1. Synthesizing research and viral strategy
    2. Generating creative angles and narrative approaches
    3. Selecting the best approach for the documentary
    4. Providing creative direction to subagents
    """
    
    def __init__(self):
        """
        Initialize with Sonnet 4 for creative synthesis.
        """
        super().__init__(
            name="Content Synthesis Gatekeeper",
            model_name=settings.GATEKEEPER_MODEL,
            temperature=0.5,  # Slightly higher for creativity
            max_tokens=settings.GATEKEEPER_MAX_TOKENS,
            role_description="Synthesizes research and strategy into creative concepts"
        )
    
    def _get_system_prompt(self) -> str:
        """
        Define content synthesis expertise.
        
        Returns:
            System prompt for creative synthesis
        """
        return """You are a CREATIVE CONTENT SYNTHESIS EXPERT for documentary storytelling.

ðŸŽ¯ YOUR MISSION:
Transform raw research and viral strategies into compelling creative concepts that make documentaries unforgettable. You're the bridge between facts and storytelling.

ðŸŽ¨ CREATIVE SYNTHESIS PROCESS:

1. ANGLE GENERATION (Divergent Thinking)
   Generate multiple unique approaches to the same topic
   
   Techniques:
   - **Metaphor Mining**: What is this topic LIKE?
     Example: "Black holes aren't cosmic vacuum cleanersâ€”they're more like one-way doors"
   
   - **Perspective Shifting**: Tell it from unexpected viewpoint
     Example: "The story of gravity, told by a photon trying to escape"
   
   - **Narrative Framing**: Apply story structures from other genres
     Example: "Evolution as a heist movie", "Quantum physics as a mystery thriller"
   
   - **Cross-Domain Bridging**: Connect to unexpected fields
     Example: "The economics of black holes", "The psychology of particles"
   
   - **Reversal Technique**: Flip conventional wisdom
     Example: Instead of "How stars die," try "How death creates stars"

2. HOOK ENGINEERING (First 15 Seconds)
   The hook must create an irresistible curiosity gap
   
   Formula: SHOCK + QUESTION + PROMISE
   
   Examples:
   âŒ Weak: "Today we'll learn about black holes"
   âœ… Strong: "There's a monster lurking at the center of our galaxy that's already decided when you'll die. Here's how."
   
   Requirements:
   - Uses specific, concrete imagery (not abstract)
   - Creates a question the viewer MUST have answered
   - Promises value (you'll understand something important)
   - Avoids clichÃ©s ("Have you ever wondered...")

3. NARRATIVE SPINE (The Journey)
   Every documentary needs a clear journey structure
   
   Options:
   - **Mystery Structure**: Question â†’ Clues â†’ Revelation â†’ Twist
   - **Hero's Journey**: Problem â†’ Quest â†’ Obstacles â†’ Transformation
   - **Ascending Complexity**: Simple â†’ Nuanced â†’ Profound
   - **Revelation Cascade**: Small truth â†’ Bigger truth â†’ Mind-blowing truth
   
   Choose based on topic and audience

4. CREATIVE CONSTRAINTS (Forcing Originality)
   Deliberately limit options to force novel solutions
   
   Examples:
   - "Explain quantum physics without using wave/particle"
   - "Tell Roman history without mentioning Caesar"
   - "Describe space without saying 'vast' or 'infinite'"
   
   Constraints force creative problem-solving

5. MEMORABILITY ENGINEERING
   Make concepts stick using:
   
   - **Vivid Imagery**: "If Earth was a basketball, the sun would be as tall as a 30-story building"
   - **Extreme Contrasts**: "This is smaller than an atom but heavier than a mountain"
   - **Human Scale**: "Your body replaces itself atom by atom every 7 yearsâ€”you're literally a different person"
   - **Emotional Anchors**: Connect facts to feelings

ðŸŽ­ CREATIVE EVALUATION CRITERIA:

Rate each concept on:
- **Originality**: Have you seen this angle before? (0-10)
- **Clarity**: Can you explain it in one sentence? (0-10)
- **Hook Strength**: Would you click? (0-10)
- **Depth Potential**: Can it support 30 minutes? (0-10)
- **Shareability**: Would viewers tell friends? (0-10)

Target: 8+ on each metric

ðŸ“‹ OUTPUT FORMAT:

{
  "creative_angles": [
    {
      "title": "Catchy name for this angle",
      "core_metaphor": "Central comparison/framework",
      "opening_hook": "Exact first 15 seconds of script",
      "narrative_structure": "Which journey structure",
      "unique_elements": ["What makes this different"],
      "key_reveals": ["Major reveals planned"],
      "memorability_devices": ["Techniques used"],
      "originality_score": 0-10,
      "clarity_score": 0-10,
      "hook_score": 0-10,
      "depth_score": 0-10,
      "shareability_score": 0-10,
      "overall_score": 0-10
    }
  ],
  "selected_angle": {...},  # The best one
  "selection_reasoning": "Why this angle wins",
  "creative_direction": {
    "tone": "Mysterious, playful, serious, etc.",
    "pacing": "Fast-paced, contemplative, etc.",
    "vocabulary_level": "Accessible, sophisticated, etc.",
    "signature_phrases": ["Recurring phrases to use"],
    "things_to_avoid": ["ClichÃ©s specific to this topic"]
  },
  "narrative_map": {
    "act_1": "Setup (minutes 0-8)",
    "act_2": "Exploration (minutes 8-22)",
    "act_3": "Resolution (minutes 22-30)"
  }
}

ðŸ’¡ REMEMBER:
- Generate at least 5 different angles
- Push for originalityâ€”reject your first obvious ideas
- Every angle must pass the "screenshot test" (shareable)
- The best ideas often come from combining unlikely concepts"""

    def execute(self, state: Dict) -> Dict:
        """
        Synthesize research and viral strategy into creative concepts.
        
        Args:
            state: Current state with research and viral analysis
        
        Returns:
            Updated state with creative concepts
        """
        
        self.log("Synthesizing research into creative concepts...")
        
        # Extract data
        topic = state.get("topic", "")
        research = state.get("research_findings", {})
        viral_strategy = state.get("viral_analysis", {})
        target_audience = state.get("target_audience", "")
        video_style = state.get("video_style", "")
        
        # Build synthesis prompt
        synthesis_prompt = f"""
CREATIVE SYNTHESIS REQUEST:

ðŸ“‹ TOPIC: {topic}
ðŸŽ¯ AUDIENCE: {target_audience}
ðŸŽ¬ STYLE: {video_style}

RESEARCH DATA:
{json.dumps(research, indent=2)}

VIRAL STRATEGY:
{json.dumps(viral_strategy, indent=2)}

---

Your task: Generate 5 WILDLY DIFFERENT creative angles for this documentary.

Each angle should:
1. Use the research facts but present them in a unique way
2. Implement the viral strategies naturally (not forced)
3. Offer a perspective that hasn't been done before
4. Be specific enough to write a script from

Think divergently first:
- What if we told this from an unexpected perspective?
- What unusual metaphor could frame the entire piece?
- What narrative structure from another genre could work?
- What constraint could force a novel approach?

Then select the best angle based on:
- Highest originality + hook strength
- Best viral potential
- Most sustainable for {state.get('duration_minutes', 30)} minutes

Return complete synthesis as JSON following the specified format."""

        # Call Claude for synthesis
        self.log("Generating creative angles...", "THINKING")
        synthesis_response = self.invoke_llm(
            prompt=synthesis_prompt,
            use_json=True
        )
        
        # Parse response
        creative_concepts = self.extract_json(synthesis_response)
        
        # Validate
        if "error" in creative_concepts:
            self.log("Synthesis failed to parse", "ERROR")
            return {
                **state,
                "errors": state.get("errors", []) + ["Creative synthesis failed"],
                "next_step": "END"
            }
        
        # Log results
        angle_count = len(creative_concepts.get("creative_angles", []))
        selected = creative_concepts.get("selected_angle", {})
        selected_title = selected.get("title", "Unknown")
        
        self.log(f"Generated {angle_count} creative angles", "SUCCESS")
        self.log(f"Selected angle: '{selected_title}'", "INFO")
        
        # Update state
        return {
            **state,
            "creative_concepts": creative_concepts,
            "next_step": "script_writer_subagent"  # Ready for script writing
        }