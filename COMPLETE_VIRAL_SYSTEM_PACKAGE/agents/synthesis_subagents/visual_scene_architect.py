"""
VISUAL SCENE ARCHITECT SUBAGENT
================================
Part of: Content Synthesis Gatekeeper
Purpose: Generates detailed shot-by-shot visual breakdowns, cinematography
         direction, and visual storytelling guidance for the documentary

This agent is a visual storytelling expert that translates the script into
specific visual scenes, camera angles, shot types, and visual elements that
will make the documentary visually compelling.

Author: Advanced Multi-Agent System
Created: 2024
"""

import anthropic
import os
from typing import Dict, List, Any

class VisualSceneArchitect:
    """
    VISUAL SCENE ARCHITECT - Cinematography & Visual Design Specialist
    
    This agent creates comprehensive visual direction for the documentary:
    - Shot-by-shot breakdowns
    - Camera angle specifications
    - Visual composition guidance
    - B-roll suggestions
    - Graphics and animation notes
    - Color and lighting mood
    - Visual metaphors and symbolism
    
    The output is a visual bible that directors and editors can follow
    to create a visually stunning documentary.
    """
    
    def __init__(self):
        """
        INITIALIZATION - Set up the Visual Scene Architect
        
        Prepares the agent for generating visual direction.
        """
        
        # Get API key
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found!\n"
                "Set in .env: ANTHROPIC_API_KEY=your_key_here"
            )
        
        # Initialize client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Model selection
        self.model = "claude-sonnet-4-20250514"
        
        # Define visual expertise
        self.agent_role = """You are the VISUAL SCENE ARCHITECT - a master of documentary cinematography.

YOUR EXPERTISE:
- Documentary filmmaking techniques
- Shot composition and framing
- Camera movement and angles
- Visual storytelling principles
- Color theory and mood creation
- Lighting design
- B-roll planning
- Motion graphics integration

YOUR KNOWLEDGE OF SHOTS:
1. SHOT TYPES:
   - ECU (Extreme Close-Up): Maximum detail/emotion
   - CU (Close-Up): Subject detail, intimacy
   - MCU (Medium Close-Up): Face and shoulders
   - MS (Medium Shot): Waist up
   - MLS (Medium Long Shot): Full body
   - LS (Long Shot): Subject in environment
   - ELS (Extreme Long Shot): Establishing, scope
   - POV (Point of View): Subjective perspective

2. CAMERA ANGLES:
   - Eye Level: Neutral, objective
   - High Angle: Diminishing, vulnerable
   - Low Angle: Empowering, imposing
   - Dutch Angle: Unease, disorientation
   - Overhead: God's eye, patterns

3. CAMERA MOVEMENT:
   - Static: Stability, observation
   - Pan: Following action, revealing
   - Tilt: Up/down reveal, scale
   - Dolly: Smooth in/out, immersion
   - Tracking: Following subject
   - Crane: Dramatic elevation changes
   - Handheld: Energy, urgency, intimacy

4. VISUAL ELEMENTS:
   - B-roll: Supporting footage
   - Graphics: Text, diagrams, data viz
   - Animation: Explanatory, transitions
   - Archive: Historical context
   - Re-enactments: Dramatization
   - Interviews: Talking heads
   - Nature/Abstract: Metaphorical

5. COMPOSITION RULES:
   - Rule of Thirds
   - Leading Lines
   - Symmetry/Balance
   - Depth of Field
   - Negative Space

YOUR MISSION:
Create shot-by-shot visual direction that:
1. Enhances the narrative
2. Maintains visual variety
3. Uses visual metaphors effectively
4. Matches pacing and mood
5. Guides practical production"""
    
    def design_visual_architecture(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        MAIN DESIGN METHOD - Create visual scene architecture
        
        This method takes the completed script and generates detailed
        visual direction for every scene.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            Current state with:
            - documentary_script: The complete script
            - topic: Documentary topic
            - engagement_strategy: Pacing and retention plan
            - duration_minutes: Video length
        
        Returns:
        --------
        Dict[str, Any]
            Updated state with visual architecture
        """
        
        print("\n🎥 Visual Scene Architect: Designing visual direction...")
        
        # Extract information
        script = state.get("documentary_script", "No script")[:4000]
        topic = state.get("topic", "Unknown")
        duration = state.get("duration_minutes", 30)
        engagement = state.get("engagement_strategy", "No strategy")[:1500]
        
        # Build visual design prompt
        visual_prompt = f"""CREATE VISUAL ARCHITECTURE

DOCUMENTARY DETAILS:
Topic: {topic}
Duration: {duration} minutes

SCRIPT:
{script}

ENGAGEMENT STRATEGY:
{engagement}

YOUR TASK:
Create a complete shot-by-shot visual breakdown for this documentary.

For EACH MAJOR SCENE (every 30-60 seconds), provide:

SCENE [NUMBER]: [Descriptive Scene Name]
TIMECODE: [MM:SS-MM:SS]
SCRIPT REFERENCE: [Key quote from this section]

VISUAL DIRECTION:

Shot 1:
- SHOT TYPE: [ECU/CU/MCU/MS/LS/ELS]
- ANGLE: [Eye level/High/Low/Dutch]
- MOVEMENT: [Static/Pan/Tilt/Dolly/Track]
- SUBJECT: [What we're filming]
- COMPOSITION: [Visual arrangement]
- DURATION: [Seconds]
- MOOD: [Emotional tone]
- PURPOSE: [Why this shot]

Shot 2:
[Same structure]

[Continue for 3-5 shots per scene]

B-ROLL NEEDED:
- [Specific B-roll footage description 1]
- [Specific B-roll footage description 2]
- [Specific B-roll footage description 3]

GRAPHICS/ANIMATIONS:
- [Specific graphic/animation needs]

LIGHTING MOOD: [Bright/Soft/Dramatic/etc.]
COLOR PALETTE: [Color mood - Warm/Cool/Vibrant/Muted]
PACING: [Fast cuts/Slow transitions/Mixed]

VISUAL METAPHOR:
[Any visual symbolism or metaphorical elements]

PRODUCTION NOTES:
[Practical filming considerations]

---

OVERALL VISUAL STRATEGY:

1. VISUAL THEMES
   - Primary visual motif: [Description]
   - Secondary elements: [Description]
   - Recurring imagery: [Description]

2. PACING THROUGH VISUALS
   - Opening (0-2 min): [Fast/Medium/Slow cuts, why]
   - Middle sections: [Visual pacing strategy]
   - Climax: [Peak visual intensity]
   - Closing: [Resolution visual style]

3. SHOT VARIETY BREAKDOWN
   - % Close-ups: X%
   - % Medium shots: X%
   - % Wide shots: X%
   - % Special shots: X%

4. VISUAL PROGRESSION
   How visuals evolve through the documentary:
   [Describe arc of visual complexity/style]

5. PRACTICAL PRODUCTION REQUIREMENTS
   - Location types needed: [List]
   - Props/materials needed: [List]
   - Special equipment: [List]
   - Estimated filming days: X

6. EDITOR'S GUIDE
   - Suggested editing pace
   - Transition styles
   - Color grading direction
   - Audio-visual sync points

Create detailed direction for {min(20, int(duration * 1.5))} distinct scenes."""
        
        try:
            # Call Claude to generate visual architecture
            response = self.client.messages.create(
                model=self.model,
                max_tokens=7000,  # Long, detailed visual descriptions
                temperature=0.75,  # Creative but structured
                system=self.agent_role,
                messages=[
                    {
                        "role": "user",
                        "content": visual_prompt
                    }
                ]
            )
            
            # Extract visual architecture
            visual_architecture = response.content[0].text
            
            # Count scenes
            scene_count = visual_architecture.upper().count("SCENE ")
            
            # Count shots
            shot_count = visual_architecture.upper().count("SHOT ")
            
            # Check for key elements
            has_broll = "B-ROLL" in visual_architecture.upper()
            has_graphics = "GRAPHICS" in visual_architecture.upper() or "ANIMATION" in visual_architecture.upper()
            has_lighting = "LIGHTING" in visual_architecture.upper()
            has_color = "COLOR" in visual_architecture.upper()
            
            # Calculate visual quality score
            quality_score = 0.0
            
            # Scene coverage
            if scene_count >= duration * 0.5:  # At least 1 scene per 2 minutes
                quality_score += 3.0
            elif scene_count > 0:
                quality_score += 1.5
            
            # Shot detail
            if shot_count >= scene_count * 2:  # Multiple shots per scene
                quality_score += 2.5
            elif shot_count > 0:
                quality_score += 1.0
            
            # Production elements
            if has_broll:
                quality_score += 1.5
            if has_graphics:
                quality_score += 1.0
            if has_lighting:
                quality_score += 1.0
            if has_color:
                quality_score += 1.0
            
            quality_score = min(10.0, quality_score)
            
            # Add to state
            state["visual_architecture"] = visual_architecture
            state["scene_count"] = scene_count
            state["shot_count"] = shot_count
            state["visual_quality_score"] = quality_score
            state["has_broll_direction"] = has_broll
            state["has_graphics_direction"] = has_graphics
            
            # Success message
            print(f"✅ Visual Scene Architect: Architecture created")
            print(f"   Scenes Designed: {scene_count}")
            print(f"   Shots Specified: {shot_count}")
            print(f"   Quality Score: {quality_score:.1f}/10")
            print(f"   B-roll: {'✓' if has_broll else '✗'} | Graphics: {'✓' if has_graphics else '✗'}")
            
            return state
            
        except Exception as e:
            # Handle errors
            print(f"❌ Visual Scene Architect Error: {str(e)}")
            
            state["visual_architecture"] = f"Visual design failed: {str(e)}"
            state["visual_quality_score"] = 0.0
            
            return state
    
    def get_scene_list(self, state: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        EXTRACT SCENE LIST - Get all scenes with timecodes
        
        Parses the visual architecture to extract a list of all scenes.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State with visual architecture
        
        Returns:
        --------
        List[Dict[str, str]]
            List of scenes with details
        """
        
        architecture = state.get("visual_architecture", "")
        
        if not architecture:
            return []
        
        scenes = []
        lines = architecture.split("\n")
        current_scene = {}
        
        for line in lines:
            if "SCENE " in line.upper() and ":" in line:
                # Save previous scene
                if current_scene:
                    scenes.append(current_scene)
                
                # New scene
                scene_name = line.split(":", 1)[1].strip() if ":" in line else line
                current_scene = {
                    "name": scene_name,
                    "details": []
                }
            elif "TIMECODE:" in line.upper() and current_scene:
                current_scene["timecode"] = line.split(":", 1)[1].strip()
            elif current_scene and line.strip():
                current_scene["details"].append(line.strip())
        
        # Add last scene
        if current_scene:
            scenes.append(current_scene)
        
        return scenes
    
    def get_broll_list(self, state: Dict[str, Any]) -> List[str]:
        """
        EXTRACT B-ROLL LIST - Get all B-roll requirements
        
        Compiles a master list of all B-roll footage needed.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State with visual architecture
        
        Returns:
        --------
        List[str]
            List of B-roll footage descriptions
        """
        
        architecture = state.get("visual_architecture", "")
        
        if not architecture:
            return []
        
        broll_list = []
        lines = architecture.split("\n")
        in_broll_section = False
        
        for line in lines:
            if "B-ROLL" in line.upper():
                in_broll_section = True
                continue
            
            if in_broll_section:
                # Check if we've left the B-roll section
                if line.strip() and not line.strip().startswith("-") and not line.strip().startswith("•"):
                    if line.isupper() or ":" in line:
                        in_broll_section = False
                        continue
                
                # Extract B-roll item
                if line.strip().startswith("-") or line.strip().startswith("•"):
                    broll_item = line.strip().lstrip("-•").strip()
                    if broll_item:
                        broll_list.append(broll_item)
        
        return broll_list


# ==============================================================================
# TESTING SECTION
# ==============================================================================

if __name__ == "__main__":
    """
    TEST THE VISUAL SCENE ARCHITECT
    """
    
    print("=" * 70)
    print("TESTING VISUAL SCENE ARCHITECT SUBAGENT")
    print("=" * 70)
    
    # Test state
    test_state = {
        "topic": "The Science of Procrastination",
        "duration_minutes": 10,
        "documentary_script": "[00:00] What if everything you know about procrastination is wrong? [PAUSE]...",
        "engagement_strategy": "Fast opening, slow middle exploration, emotional climax..."
    }
    
    # Create architect
    architect = VisualSceneArchitect()
    
    # Design visuals
    result_state = architect.design_visual_architecture(test_state)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nScenes Designed: {result_state.get('scene_count', 0)}")
    print(f"Shots Specified: {result_state.get('shot_count', 0)}")
    print(f"Quality Score: {result_state.get('visual_quality_score', 0):.1f}/10")
    print(f"Has B-roll Direction: {result_state.get('has_broll_direction', False)}")
    print(f"Has Graphics Direction: {result_state.get('has_graphics_direction', False)}")
    
    # Show scene list
    scenes = architect.get_scene_list(result_state)
    print(f"\n🎬 SCENES: {len(scenes)}")
    for i, scene in enumerate(scenes[:3], 1):
        print(f"  {i}. {scene.get('name', 'N/A')}")
        print(f"     Timecode: {scene.get('timecode', 'N/A')}")
    
    # Show B-roll list
    broll = architect.get_broll_list(result_state)
    print(f"\n📹 B-ROLL ITEMS: {len(broll)}")
    for i, item in enumerate(broll[:3], 1):
        print(f"  {i}. {item}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
