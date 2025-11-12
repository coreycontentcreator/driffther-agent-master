"""
PRODUCTION NOTES GENERATOR SUBAGENT
====================================
Part of: Content Synthesis Gatekeeper
Purpose: Generates comprehensive production notes including music cues, sound design,
         graphics requirements, technical specifications, and post-production guidance

This agent creates the detailed production bible that guides the entire filming
and post-production process, ensuring nothing is forgotten and quality is consistent.

Author: Advanced Multi-Agent System
Created: 2024
"""

import anthropic
import os
from typing import Dict, List, Any

class ProductionNotesGenerator:
    """
    PRODUCTION NOTES GENERATOR - Production Management Specialist
    
    This agent creates comprehensive production documentation:
    - Music cues and mood specifications
    - Sound effects and audio design
    - Graphics and text overlay requirements
    - Technical specifications
    - Equipment lists
    - Post-production guides
    - Timeline and scheduling
    - Budget considerations
    
    The output is a complete production manual.
    """
    
    def __init__(self):
        """
        INITIALIZATION - Set up Production Notes Generator
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
        
        # Model
        self.model = "claude-sonnet-4-20250514"
        
        # Agent expertise
        self.agent_role = """You are the PRODUCTION NOTES GENERATOR - a documentary production specialist.

YOUR EXPERTISE:
- Documentary production workflow
- Music supervision and licensing
- Sound design and audio post
- Motion graphics production
- Color grading direction
- Technical specifications
- Production scheduling
- Budget planning

YOUR KNOWLEDGE:

1. MUSIC CATEGORIES:
   - Score (Original/Licensed)
   - Mood music (Tension/Calm/Energy)
   - Transitions and stingers
   - Ambient soundscapes

2. SOUND DESIGN:
   - Foley effects
   - Ambient sound
   - Sound transitions
   - Audio emphasis

3. GRAPHICS TYPES:
   - Lower thirds (names/titles)
   - Data visualizations
   - Animated sequences
   - Text overlays
   - Transitions

4. TECHNICAL SPECS:
   - Resolution (4K/HD)
   - Frame rate
   - Color space
   - Audio format
   - Delivery format

5. PRODUCTION PHASES:
   - Pre-production
   - Production (filming)
   - Post-production
   - Distribution

YOUR MISSION:
Create detailed production notes that ensure smooth execution from filming to delivery."""
    
    def generate_production_notes(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        MAIN GENERATION METHOD - Create complete production notes
        
        Parameters:
        -----------
        state : Dict[str, Any]
            Current state with:
            - documentary_script: Complete script
            - visual_architecture: Shot breakdowns
            - topic: Documentary topic
            - duration_minutes: Video length
        
        Returns:
        --------
        Dict[str, Any]
            Updated state with production notes
        """
        
        print("\n📋 Production Notes Generator: Creating production documentation...")
        
        # Extract information
        script = state.get("documentary_script", "No script")[:3000]
        visuals = state.get("visual_architecture", "No visuals")[:3000]
        topic = state.get("topic", "Unknown")
        duration = state.get("duration_minutes", 30)
        
        # Build production notes prompt
        notes_prompt = f"""GENERATE PRODUCTION NOTES

PROJECT:
Topic: {topic}
Duration: {duration} minutes

SCRIPT (EXCERPT):
{script}

VISUAL ARCHITECTURE (EXCERPT):
{visuals}

YOUR TASK:
Create comprehensive production notes for this documentary.

1. MUSIC CUE SHEET

For each section, specify:

[TIMECODE RANGE]
MUSIC CUE: [Descriptive name]
MOOD/STYLE: [Specific description]
TEMPO: [BPM range or Fast/Medium/Slow]
INSTRUMENTATION: [What instruments/sounds]
INTENSITY: [1-10]
PURPOSE: [What this music accomplishes]
REFERENCE TRACKS: [Similar existing music]
LICENSING NOTES: [Royalty-free/Licensed/Original]

Create 8-12 distinct music cues throughout the {duration} minutes.

2. SOUND DESIGN NOTES

AMBIENT SOUND:
- Location ambience needs
- Background soundscapes
- Atmospheric layers

SOUND EFFECTS:
[Timecode]: [Specific SFX] - [Purpose]
[Continue for all needed SFX]

AUDIO TRANSITIONS:
- Whoosh transitions: [Where and why]
- Fade patterns: [Specifications]
- Audio emphasis: [Key moments]

DIALOGUE/VO TREATMENT:
- EQ settings suggestions
- Compression needs
- Reverb/room tone
- Special processing

3. GRAPHICS REQUIREMENTS

LOWER THIRDS:
[Timecode]: [Name/Title] - [Style notes]

DATA VISUALIZATIONS:
[Timecode]: [Chart/Graph type] - [Data to display]

ANIMATED SEQUENCES:
[Timecode]: [Animation description] - [Duration] - [Style]

TEXT OVERLAYS:
[Timecode]: [Text content] - [Style/positioning]

GRAPHIC STYLE GUIDE:
- Font family: [Recommendation]
- Color scheme: [Palette]
- Animation style: [Smooth/Energetic/Minimal]
- Consistency notes

4. TECHNICAL SPECIFICATIONS

VIDEO:
- Resolution: [4K/HD]
- Frame rate: [24/30/60fps]
- Aspect ratio: [16:9/etc]
- Color space: [Rec.709/etc]
- Codec: [H.264/ProRes/etc]

AUDIO:
- Sample rate: [48kHz/96kHz]
- Bit depth: [24-bit/etc]
- Channels: [Stereo/5.1]
- Format: [WAV/AAC/etc]

DELIVERY:
- Export format
- File size target
- Platform optimization

5. EQUIPMENT LIST

CAMERA GEAR:
- Camera bodies needed
- Lenses required
- Stabilization (gimbal/tripod)
- Lighting kit

AUDIO GEAR:
- Microphones
- Recorders
- Monitors

POST-PRODUCTION:
- Editing software
- Color grading tools
- Graphics software
- Audio mixing tools

6. PRODUCTION TIMELINE

PRE-PRODUCTION:
- Research gathering: [Days]
- Location scouting: [Days]
- Equipment prep: [Days]
- Talent/interview booking: [Days]

PRODUCTION:
- Principal photography: [Days]
- B-roll collection: [Days]
- Interview recordings: [Days]

POST-PRODUCTION:
- Rough cut: [Days]
- Fine cut: [Days]
- Color grading: [Days]
- Sound design/mix: [Days]
- Graphics/VFX: [Days]
- Final export: [Days]

TOTAL TIMELINE: [Weeks]

7. BUDGET ESTIMATES

(Rough estimates for indie production)

PRE-PRODUCTION: $[amount]
PRODUCTION: $[amount]
POST-PRODUCTION: $[amount]
MUSIC LICENSING: $[amount]
GRAPHICS/VFX: $[amount]
MISC: $[amount]

TOTAL ESTIMATED: $[amount]

COST-SAVING TIPS:
- [Specific suggestions]

8. POST-PRODUCTION WORKFLOW

EDITING PHASE:
1. Assembly: [Guidelines]
2. Rough cut: [Goals]
3. Fine cut: [Standards]

COLOR GRADING:
- Look/mood: [Description]
- Key scenes: [Special treatment]

SOUND MIX:
- Dialogue level: [dB]
- Music level: [dB]
- SFX level: [dB]
- Master output: [dB]

9. QUALITY CHECKPOINTS

□ Audio sync perfect
□ Color consistency
□ Graphics accuracy
□ Pacing matches engagement strategy
□ Music rights cleared
□ Timecodes accurate
□ Export settings correct

10. DISTRIBUTION PREP

YOUTUBE OPTIMIZATION:
- Title: [Recommendations]
- Description: [Structure]
- Tags: [Suggestions]
- Thumbnail: [Design notes]

OTHER PLATFORMS:
- [Platform-specific notes]

Provide actionable, specific production guidance."""
        
        try:
            # Generate production notes
            response = self.client.messages.create(
                model=self.model,
                max_tokens=6000,
                temperature=0.6,  # More structured, less creative
                system=self.agent_role,
                messages=[
                    {
                        "role": "user",
                        "content": notes_prompt
                    }
                ]
            )
            
            # Extract notes
            production_notes = response.content[0].text
            
            # Count elements
            music_cues = production_notes.upper().count("MUSIC CUE") or production_notes.count("CUE:")
            graphics_count = production_notes.upper().count("GRAPHIC") + production_notes.upper().count("ANIMATION")
            sfx_count = production_notes.upper().count("SFX") or production_notes.upper().count("SOUND EFFECT")
            
            # Check for completeness
            has_budget = "$" in production_notes or "BUDGET" in production_notes.upper()
            has_timeline = "TIMELINE" in production_notes.upper() or "DAYS" in production_notes.upper()
            has_equipment = "EQUIPMENT" in production_notes.upper() or "GEAR" in production_notes.upper()
            has_technical = "RESOLUTION" in production_notes.upper() or "TECHNICAL" in production_notes.upper()
            
            # Calculate completeness score
            completeness_score = 0.0
            
            if music_cues >= 5:
                completeness_score += 2.5
            elif music_cues > 0:
                completeness_score += 1.0
            
            if graphics_count >= 5:
                completeness_score += 2.0
            elif graphics_count > 0:
                completeness_score += 1.0
            
            if has_budget:
                completeness_score += 1.5
            if has_timeline:
                completeness_score += 1.5
            if has_equipment:
                completeness_score += 1.5
            if has_technical:
                completeness_score += 1.0
            
            completeness_score = min(10.0, completeness_score)
            
            # Add to state
            state["production_notes"] = production_notes
            state["music_cue_count"] = music_cues
            state["graphics_requirement_count"] = graphics_count
            state["sfx_count"] = sfx_count
            state["production_completeness_score"] = completeness_score
            state["has_budget_estimate"] = has_budget
            state["has_production_timeline"] = has_timeline
            
            # Success
            print(f"✅ Production Notes Generator: Documentation created")
            print(f"   Music Cues: {music_cues}")
            print(f"   Graphics: {graphics_count}")
            print(f"   SFX: {sfx_count}")
            print(f"   Completeness: {completeness_score:.1f}/10")
            
            return state
            
        except Exception as e:
            print(f"❌ Production Notes Generator Error: {str(e)}")
            
            state["production_notes"] = f"Production notes generation failed: {str(e)}"
            state["production_completeness_score"] = 0.0
            
            return state
    
    def export_production_package(self, state: Dict[str, Any], output_dir: str = "/home/claude/production_package") -> Dict[str, str]:
        """
        EXPORT PRODUCTION PACKAGE - Save all production files
        
        Creates a complete production package with all documents.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            Complete state with all components
        output_dir : str
            Directory to save files
        
        Returns:
        --------
        Dict[str, str]
            Dictionary of created files
        """
        
        import os
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        files_created = {}
        
        # Export script
        if state.get("documentary_script"):
            script_path = f"{output_dir}/01_SCRIPT.txt"
            with open(script_path, 'w') as f:
                f.write(f"DOCUMENTARY SCRIPT\n")
                f.write(f"Topic: {state.get('topic', 'Unknown')}\n")
                f.write(f"=" * 70 + "\n\n")
                f.write(state["documentary_script"])
            files_created["script"] = script_path
        
        # Export visual architecture
        if state.get("visual_architecture"):
            visual_path = f"{output_dir}/02_VISUAL_ARCHITECTURE.txt"
            with open(visual_path, 'w') as f:
                f.write(f"VISUAL SCENE ARCHITECTURE\n")
                f.write(f"=" * 70 + "\n\n")
                f.write(state["visual_architecture"])
            files_created["visuals"] = visual_path
        
        # Export production notes
        if state.get("production_notes"):
            notes_path = f"{output_dir}/03_PRODUCTION_NOTES.txt"
            with open(notes_path, 'w') as f:
                f.write(f"PRODUCTION NOTES\n")
                f.write(f"=" * 70 + "\n\n")
                f.write(state["production_notes"])
            files_created["production"] = notes_path
        
        # Export research citations
        if state.get("research_findings"):
            research_path = f"{output_dir}/04_RESEARCH_CITATIONS.txt"
            with open(research_path, 'w') as f:
                f.write(f"RESEARCH CITATIONS\n")
                f.write(f"=" * 70 + "\n\n")
                f.write(state["research_findings"][:5000])  # First 5000 chars
            files_created["research"] = research_path
        
        # Create README
        readme_path = f"{output_dir}/README.md"
        with open(readme_path, 'w') as f:
            f.write(f"# Documentary Production Package\n\n")
            f.write(f"## {state.get('topic', 'Documentary')}\n\n")
            f.write(f"**Duration:** {state.get('duration_minutes', 'Unknown')} minutes\n\n")
            f.write(f"**Files Included:**\n\n")
            for name, path in files_created.items():
                f.write(f"- `{os.path.basename(path)}`\n")
        files_created["readme"] = readme_path
        
        return files_created


# ==============================================================================
# TESTING
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TESTING PRODUCTION NOTES GENERATOR")
    print("=" * 70)
    
    test_state = {
        "topic": "The Science of Procrastination",
        "duration_minutes": 10,
        "documentary_script": "[00:00] Opening hook...",
        "visual_architecture": "Scene 1: Opening shots..."
    }
    
    generator = ProductionNotesGenerator()
    result_state = generator.generate_production_notes(test_state)
    
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nMusic Cues: {result_state.get('music_cue_count', 0)}")
    print(f"Graphics: {result_state.get('graphics_requirement_count', 0)}")
    print(f"SFX: {result_state.get('sfx_count', 0)}")
    print(f"Completeness: {result_state.get('production_completeness_score', 0):.1f}/10")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
