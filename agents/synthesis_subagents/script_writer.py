"""
SCRIPT WRITER SUBAGENT
======================
Part of: Content Synthesis Gatekeeper
Purpose: Generates complete, production-ready scripts with timecodes, narration,
         and dialogue that synthesizes research with viral optimization

This agent is the master storyteller that takes all the research, viral patterns,
hooks, and engagement strategies and weaves them into a compelling narrative
that's ready to be filmed.

Author: Advanced Multi-Agent System
Created: 2024
"""

import anthropic
import os
from typing import Dict, List, Any

class ScriptWriter:
    """
    SCRIPT WRITER - Documentary Script Generation Specialist
    
    This agent creates production-ready scripts that:
    - Synthesize academic research into engaging narratives
    - Implement viral hooks and engagement strategies
    - Include precise timecodes for every section
    - Balance entertainment with credibility
    - Incorporate psychological triggers strategically
    - Maintain proper pacing throughout
    
    The output is a complete script ready for voice-over recording,
    including narrator lines, pause markers, and emphasis notes.
    """
    
    def __init__(self):
        """
        INITIALIZATION - Set up the Script Writer
        
        Prepares the agent for generating complete documentary scripts.
        """
        
        # Get API key from environment
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found!\n"
                "Set in .env: ANTHROPIC_API_KEY=your_key_here"
            )
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Use most capable model
        self.model = "claude-sonnet-4-20250514"
        
        # Define the agent's expertise
        self.agent_role = """You are the SCRIPT WRITER - a master documentary scriptwriter.

YOUR EXPERTISE:
- Documentary narrative structure
- Voice-over narration writing
- Academic-to-entertainment translation
- Pacing and timing optimization
- Dialogue and monologue crafting
- Story arc construction
- Emotional beat placement

YOUR WRITING STYLE:
- Clear, conversational voice
- Sophisticated but accessible language
- Strong narrative drive
- Rhythmic variation (short and long sentences)
- Strategic use of questions
- Vivid imagery and examples
- Precise word economy

YOUR KNOWLEDGE:
- Three-act structure for documentaries
- Hero's journey adaptation for science content
- Tension and release patterns
- Call-back and setup/payoff techniques
- Narrative hooks and curiosity gaps
- Transitional language
- Emphasis and pacing markers

YOUR MISSION:
Write complete, production-ready scripts that:
1. Open with powerful hooks
2. Maintain engagement throughout
3. Deliver research insights compellingly
4. Build to satisfying conclusions
5. Include precise timecodes
6. Mark emphasis, pauses, and pacing notes

You write scripts that are both academically rigorous AND highly watchable."""
    
    def write_script(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        MAIN WRITING METHOD - Generate complete script
        
        This method synthesizes all previous analysis (research, viral strategies,
        engagement plans, psychology triggers) into a complete, production-ready
        documentary script.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            Current state with:
            - topic: The documentary topic
            - duration_minutes: Target length
            - research_findings: Academic content
            - viral_hooks: Generated hooks
            - engagement_strategy: Engagement plan
            - psychology_triggers: Trigger strategy
            - target_audience: Demographics
        
        Returns:
        --------
        Dict[str, Any]
            Updated state with complete script
        """
        
        print("\n✍️ Script Writer: Generating documentary script...")
        
        # Extract all necessary information
        topic = state.get("topic", "Unknown")
        duration = state.get("duration_minutes", 30)
        research = state.get("research_findings", "No research")[:3000]
        hooks = state.get("viral_hooks", "No hooks")[:2000]
        engagement = state.get("engagement_strategy", "No strategy")[:2000]
        psychology = state.get("psychology_triggers", "No triggers")[:2000]
        audience = state.get("target_audience", "General")
        patterns = state.get("viral_patterns", "No patterns")[:1500]
        
        # Calculate word count target
        # Average speaking rate: 150 words per minute
        # Documentary narration: ~130 words per minute (slower, clearer)
        target_words = int(duration * 130)
        
        # Build comprehensive script generation prompt
        script_prompt = f"""WRITE COMPLETE DOCUMENTARY SCRIPT

PROJECT SPECIFICATIONS:
Topic: {topic}
Duration: {duration} minutes
Target Word Count: {target_words} words (~130 words/minute)
Target Audience: {audience}

RESEARCH FOUNDATION:
{research}

VIRAL HOOK OPTIONS:
{hooks}

ENGAGEMENT STRATEGY:
{engagement}

PSYCHOLOGICAL TRIGGERS:
{psychology}

VIRAL PATTERNS TO IMPLEMENT:
{patterns}

YOUR TASK:
Write a COMPLETE, production-ready documentary script.

SCRIPT STRUCTURE:

[00:00-00:10] COLD OPEN / HOOK
- Implement strongest viral hook
- Pattern interrupt
- Curiosity trigger
- No introduction yet - jump straight in

[00:10-00:30] OPENING SEQUENCE
- Establish the mystery/question
- Create information gap
- Preview what's coming
- First major curiosity hook

[00:30-02:00] ACT 1: SETUP
- Introduce the topic formally
- Establish why it matters
- Present common misconceptions
- Set up the journey
- Build credibility

[02:00-05:00] ACT 1: COMPLICATION
- Reveal deeper complexity
- Challenge assumptions
- Present research findings
- Build tension
- Strategic loop openings

[05:00-08:00] ACT 2: INVESTIGATION
- Dive into research details
- Present evidence
- Use examples and case studies
- Maintain pacing with varies sentence lengths
- Close some loops, open others

[08:00-12:00] ACT 2: REVELATION
- Major insights
- "Aha!" moments
- Connect dots
- Deliver on promises
- Emotional peaks

[12:00-{duration-2}:00] ACT 3: SYNTHESIS
- Bring it all together
- Answer central questions
- Resolve remaining loops
- Build to climax

[{duration-2}:00-{duration}:00] CLOSING
- Satisfying conclusion
- Call to action
- Final thought/question
- Strong ending impression

FOR EACH SECTION, PROVIDE:

[TIMECODE RANGE]

**NARRATION:**
"Complete narration text here. Use quotation marks for direct speech. 
[PAUSE] for timing marks. *Emphasize* key words. Keep authentic documentary voice."

**PACING NOTES:** [Fast/Medium/Slow]
**EMOTIONAL TONE:** [Describe target emotion]
**KEY TRIGGER:** [Which psychological trigger is active]

---

CRITICAL REQUIREMENTS:
1. Total word count must be ~{target_words} words (±10%)
2. Include ALL timecodes in [MM:SS] format
3. Write in natural, conversational voice
4. Vary sentence length for rhythm
5. Use vivid, concrete examples
6. Include strategic pauses [PAUSE]
7. Mark emphasis with *asterisks*
8. Cite research naturally (no footnotes in narration)
9. Build and resolve tension
10. End strong - no weak conclusions

WORD COUNT TRACKING:
- Check word count as you write
- Adjust pacing to hit target duration
- Don't rush ending or pad middle

Write the COMPLETE script now. This is the final production script - 
make every word count."""
        
        try:
            # Call Claude to generate the script
            # Using max tokens to allow full script
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,  # Long script needs many tokens
                temperature=0.8,  # Creative but controlled
                system=self.agent_role,
                messages=[
                    {
                        "role": "user",
                        "content": script_prompt
                    }
                ]
            )
            
            # Extract the script
            script = response.content[0].text
            
            # Count actual words in script
            word_count = len(script.split())
            
            # Calculate actual duration based on word count
            actual_duration = word_count / 130  # 130 words per minute
            
            # Count how many timecodes are present
            timecode_count = script.count("[") - script.count("[[")  # Exclude [PAUSE]
            
            # Check for key elements
            has_pauses = "[PAUSE]" in script
            has_emphasis = "*" in script
            has_structure = "ACT" in script.upper() or "SECTION" in script.upper()
            
            # Calculate quality score
            quality_score = 0.0
            
            # Word count accuracy (closer to target = higher score)
            word_accuracy = 1.0 - min(1.0, abs(word_count - target_words) / target_words)
            quality_score += word_accuracy * 3.0
            
            # Timecode presence
            if timecode_count >= duration:
                quality_score += 2.0
            elif timecode_count > 0:
                quality_score += 1.0
            
            # Production marks
            if has_pauses:
                quality_score += 1.5
            if has_emphasis:
                quality_score += 1.5
            if has_structure:
                quality_score += 2.0
            
            # Length quality
            if len(script) > 2000:
                quality_score = min(10.0, quality_score)
            
            # Add script to state
            state["documentary_script"] = script
            state["script_word_count"] = word_count
            state["script_duration_minutes"] = actual_duration
            state["script_timecode_count"] = timecode_count
            state["script_quality_score"] = quality_score
            state["script_has_pauses"] = has_pauses
            state["script_has_emphasis"] = has_emphasis
            
            # Success message
            print(f"✅ Script Writer: Script generated")
            print(f"   Word Count: {word_count} words (target: {target_words})")
            print(f"   Duration: {actual_duration:.1f} minutes (target: {duration})")
            print(f"   Quality Score: {quality_score:.1f}/10")
            print(f"   Timecodes: {timecode_count}")
            
            return state
            
        except Exception as e:
            # Handle errors
            print(f"❌ Script Writer Error: {str(e)}")
            
            state["documentary_script"] = f"Script generation failed: {str(e)}"
            state["script_quality_score"] = 0.0
            
            return state
    
    def get_script_sections(self, state: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        EXTRACT SCRIPT SECTIONS - Parse script into timestamped sections
        
        Breaks the script into sections based on timecodes for easier
        reference and production planning.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State with complete script
        
        Returns:
        --------
        List[Dict[str, str]]
            List of script sections with timecodes and content
        """
        
        script = state.get("documentary_script", "")
        
        if not script:
            return []
        
        sections = []
        current_section = {}
        
        # Split by lines
        lines = script.split("\n")
        
        for line in lines:
            # Look for timecodes
            if "[" in line and "]" in line and ":" in line:
                # Save previous section if exists
                if current_section:
                    sections.append(current_section)
                
                # Start new section
                timecode = line[line.find("["):line.find("]")+1]
                current_section = {
                    "timecode": timecode,
                    "content": []
                }
            elif current_section:
                # Add content to current section
                if line.strip():
                    current_section["content"].append(line)
        
        # Add last section
        if current_section:
            sections.append(current_section)
        
        return sections
    
    def export_script_to_file(self, state: Dict[str, Any], filename: str = "documentary_script.txt") -> str:
        """
        EXPORT SCRIPT - Save script to file
        
        Exports the script to a properly formatted text file.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State with script
        filename : str
            Output filename
        
        Returns:
        --------
        str
            Path to exported file
        """
        
        script = state.get("documentary_script", "")
        
        if not script:
            return "No script to export"
        
        # Add header
        header = f"""DOCUMENTARY SCRIPT
=====================================
Topic: {state.get('topic', 'Unknown')}
Duration: {state.get('script_duration_minutes', 0):.1f} minutes
Word Count: {state.get('script_word_count', 0)} words
Generated: [CURRENT_DATE]

=====================================

"""
        
        full_export = header + script
        
        # Write to file
        filepath = f"/home/claude/{filename}"
        with open(filepath, 'w') as f:
            f.write(full_export)
        
        return filepath


# ==============================================================================
# TESTING SECTION
# ==============================================================================

if __name__ == "__main__":
    """
    TEST THE SCRIPT WRITER
    """
    
    print("=" * 70)
    print("TESTING SCRIPT WRITER SUBAGENT")
    print("=" * 70)
    
    # Test state with all inputs
    test_state = {
        "topic": "The Science of Procrastination",
        "duration_minutes": 10,
        "target_audience": "Young professionals, 18-35",
        "research_findings": "Procrastination is emotional regulation...",
        "viral_hooks": "Hook: What if procrastination isn't laziness...",
        "engagement_strategy": "Fast open, curiosity loops...",
        "psychology_triggers": "Use identity, fear triggers..."
    }
    
    # Create writer
    writer = ScriptWriter()
    
    # Generate script
    result_state = writer.write_script(test_state)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nWord Count: {result_state.get('script_word_count', 0)}")
    print(f"Duration: {result_state.get('script_duration_minutes', 0):.1f} minutes")
    print(f"Quality Score: {result_state.get('script_quality_score', 0):.1f}/10")
    print(f"Timecodes: {result_state.get('script_timecode_count', 0)}")
    print(f"Has Pauses: {result_state.get('script_has_pauses', False)}")
    print(f"Has Emphasis: {result_state.get('script_has_emphasis', False)}")
    
    # Show first 500 characters
    script = result_state.get("documentary_script", "")
    print(f"\n📄 SCRIPT PREVIEW (first 500 chars):")
    print(script[:500] + "...")
    
    # Show sections
    sections = writer.get_script_sections(result_state)
    print(f"\n📋 SCRIPT SECTIONS: {len(sections)}")
    for i, section in enumerate(sections[:3], 1):
        print(f"  {i}. {section.get('timecode', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
