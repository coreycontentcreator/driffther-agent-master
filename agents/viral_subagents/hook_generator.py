"""
HOOK GENERATOR SUBAGENT
=======================
Part of: Viral Analyst Gatekeeper
Purpose: Generates highly effective attention hooks and video openings

This agent specializes in creating the critical first 10 seconds that determine
if viewers will watch or click away. It generates multiple hook options with
psychological triggers and engagement mechanics built in.

Author: Advanced Multi-Agent System
Created: 2024
"""

import anthropic  # Anthropic's SDK for calling Claude AI
import os         # For accessing environment variables (API keys)
from typing import Dict, List, Any  # For type hints

class HookGenerator:
    """
    HOOK GENERATOR - Viral Opening & Attention Hook Specialist
    
    This agent creates killer opening hooks that grab attention immediately.
    
    The first 10 seconds of a video are CRITICAL - 50-70% of viewers decide
    whether to continue watching in this timeframe. This agent generates
    multiple hook options designed to maximize retention.
    
    Each hook includes:
    - Opening statement (first 3 seconds)
    - Hook amplification (seconds 4-7)
    - Promise/payoff setup (seconds 8-10)
    - Psychological trigger used
    - Estimated effectiveness score
    """
    
    def __init__(self):
        """
        INITIALIZATION - Set up the Hook Generator
        
        This method runs when you create a new HookGenerator object.
        It sets up the AI connection and prepares the agent for work.
        """
        
        # Get the API key from environment variables
        # This is stored securely in your .env file
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Verify API key exists
        if not self.api_key:
            raise ValueError(
                "❌ ANTHROPIC_API_KEY not found!\n"
                "Set it in your .env file: ANTHROPIC_API_KEY=your_key_here"
            )
        
        # Create the Anthropic client for API calls
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # Specify which AI model to use (Claude Sonnet 4.5 is the smartest)
        self.model = "claude-sonnet-4-20250514"
        
        # Define this agent's role and expertise
        # This shapes how Claude will respond to our requests
        self.agent_role = """You are the HOOK GENERATOR - a master of viral video openings.

YOUR EXPERTISE:
- Psychology of attention and curiosity
- Pattern interrupt techniques
- Emotional trigger deployment
- Promise-payoff dynamics
- Viral video opening formulas
- Audience retention optimization

YOUR MISSION:
Generate powerful opening hooks that:
1. Stop scrolling immediately (pattern interrupt)
2. Create intense curiosity (information gap)
3. Make a bold promise (payoff setup)
4. Use psychological triggers (emotion, identity, fear, desire)
5. Establish credibility quickly
6. Set up the narrative arc

HOOK STRUCTURES YOU KNOW:
- "What if I told you..." (Curiosity + Promise)
- "Most people don't know..." (Exclusivity + Gap)
- "The truth about..." (Revelation + Authority)
- "Here's why..." (Direct + Explanation)
- "You've been lied to about..." (Contrarian + Trust breach)
- "In the next X minutes..." (Time commitment + Promise)

Each hook must include specific psychological triggers and engagement mechanics."""
    
    def generate_hooks(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        MAIN GENERATION METHOD - Create multiple hook options
        
        This method generates 5-8 different hook options for the video,
        each with different psychological approaches and triggers.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            The current state containing:
            - topic: The documentary topic
            - research_findings: Academic research
            - viral_patterns: Identified viral patterns
            - target_audience: Target demographic
        
        Returns:
        --------
        Dict[str, Any]
            Updated state with hooks added
        """
        
        print("\n🎣 Hook Generator: Creating viral hooks...")
        
        # Extract information from state
        topic = state.get("topic", "Unknown topic")
        research = state.get("research_findings", "No research")[:2000]  # Limit size
        patterns = state.get("viral_patterns", "No patterns")[:2000]
        audience = state.get("target_audience", "General audience")
        
        # Build the hook generation prompt
        # This tells Claude exactly what types of hooks we want
        hook_prompt = f"""GENERATE VIRAL VIDEO HOOKS

TOPIC: {topic}
TARGET AUDIENCE: {audience}

RESEARCH INSIGHTS:
{research}

VIRAL PATTERNS IDENTIFIED:
{patterns}

YOUR TASK:
Generate 7 different opening hooks for this video. Each hook must:

1. GRAB ATTENTION in first 3 seconds (pattern interrupt)
2. CREATE CURIOSITY seconds 4-7 (information gap)
3. SETUP PROMISE seconds 8-10 (payoff preview)

For EACH hook, provide:

HOOK #[number]: [Catchy name for this hook type]

OPENING (0-3 seconds):
[Exact words for the opening statement]

AMPLIFICATION (4-7 seconds):
[How to amplify the curiosity/tension]

PROMISE (8-10 seconds):
[What payoff you're setting up]

PSYCHOLOGICAL TRIGGERS USED:
- [List 2-3 specific triggers: curiosity, fear, identity, social proof, etc.]

EFFECTIVENESS SCORE: [1-10]
[Why you rated it this way]

TARGET EMOTION: [What emotion you're targeting]

EXAMPLE APPLICATION:
[Quick example of how this would sound in narration]

---

REQUIREMENTS:
- Vary the psychological approaches across hooks
- Use different hook structures (contrarian, curiosity, promise, revelation, etc.)
- Some hooks should be bold, others should be subtle
- Include at least one "pattern interrupt" hook
- Include at least one "insider knowledge" hook
- Score each hook honestly based on viral potential

Generate 7 unique hooks now."""
        
        try:
            # Call Claude AI to generate the hooks
            # We use temperature=0.9 for maximum creativity
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,  # Long response needed for 7 detailed hooks
                temperature=0.9,  # High creativity for generating diverse hooks
                system=self.agent_role,
                messages=[
                    {
                        "role": "user",
                        "content": hook_prompt
                    }
                ]
            )
            
            # Extract the generated hooks from Claude's response
            hooks_content = response.content[0].text
            
            # Parse out individual hooks
            # We split by "HOOK #" to separate each hook
            hook_sections = hooks_content.split("HOOK #")[1:]  # Skip first empty element
            
            # Count how many hooks were generated
            hook_count = len(hook_sections)
            
            # Extract effectiveness scores if present
            # We look for "EFFECTIVENESS SCORE:" patterns in the text
            scores = []
            for section in hook_sections:
                if "EFFECTIVENESS SCORE:" in section:
                    # Try to extract the number
                    try:
                        score_line = section.split("EFFECTIVENESS SCORE:")[1].split("\n")[0]
                        # Extract first number found
                        score = float(''.join(filter(lambda x: x.isdigit() or x == '.', score_line.split()[0])))
                        scores.append(score)
                    except:
                        scores.append(7.0)  # Default score
            
            # Calculate average effectiveness
            avg_effectiveness = sum(scores) / len(scores) if scores else 7.5
            
            # Add hooks to state
            state["viral_hooks"] = hooks_content
            state["hook_count"] = hook_count
            state["hook_effectiveness_avg"] = avg_effectiveness
            state["hook_effectiveness_scores"] = scores
            
            # Success message
            print(f"✅ Hook Generator: Created {hook_count} hooks")
            print(f"   Average Effectiveness: {avg_effectiveness:.1f}/10")
            print(f"   Best Hook Score: {max(scores) if scores else 'N/A'}/10")
            
            return state
            
        except Exception as e:
            # Handle any errors gracefully
            print(f"❌ Hook Generator Error: {str(e)}")
            
            # Add error info to state
            state["viral_hooks"] = f"Hook generation failed: {str(e)}"
            state["hook_count"] = 0
            state["hook_effectiveness_avg"] = 0.0
            
            return state
    
    def get_best_hook(self, state: Dict[str, Any]) -> Dict[str, str]:
        """
        EXTRACT BEST HOOK - Get the highest-scoring hook
        
        This method parses all generated hooks and returns the one
        with the highest effectiveness score.
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State containing generated hooks
        
        Returns:
        --------
        Dict[str, str]
            Dictionary containing the best hook's components
        """
        
        hooks_text = state.get("viral_hooks", "")
        scores = state.get("hook_effectiveness_scores", [])
        
        if not hooks_text or not scores:
            return {"error": "No hooks available"}
        
        # Find the index of the highest score
        best_index = scores.index(max(scores))
        
        # Split into individual hooks
        hook_sections = hooks_text.split("HOOK #")[1:]
        
        if best_index < len(hook_sections):
            best_hook_text = "HOOK #" + hook_sections[best_index]
            
            # Parse the components (simplified parser)
            result = {
                "full_text": best_hook_text,
                "score": scores[best_index],
                "preview": best_hook_text[:200] + "..."
            }
            
            return result
        
        return {"error": "Could not extract best hook"}
    
    def get_all_hooks_summary(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        GET ALL HOOKS SUMMARY - Return a structured list of all hooks
        
        Parameters:
        -----------
        state : Dict[str, Any]
            State containing generated hooks
        
        Returns:
        --------
        List[Dict[str, Any]]
            List of all hooks with their scores
        """
        
        hooks_text = state.get("viral_hooks", "")
        scores = state.get("hook_effectiveness_scores", [])
        
        if not hooks_text:
            return []
        
        # Split into individual hooks
        hook_sections = hooks_text.split("HOOK #")[1:]
        
        summaries = []
        for i, section in enumerate(hook_sections):
            score = scores[i] if i < len(scores) else 0.0
            
            # Get first line as title
            title = section.split("\n")[0].strip()
            
            summaries.append({
                "number": i + 1,
                "title": title,
                "score": score,
                "preview": section[:150] + "..."
            })
        
        # Sort by score (highest first)
        summaries.sort(key=lambda x: x["score"], reverse=True)
        
        return summaries


# ==============================================================================
# TESTING SECTION
# ==============================================================================

if __name__ == "__main__":
    """
    TEST THE HOOK GENERATOR
    
    This demonstrates how to use the Hook Generator agent.
    """
    
    print("=" * 70)
    print("TESTING HOOK GENERATOR SUBAGENT")
    print("=" * 70)
    
    # Create test state (simulating previous agents' output)
    test_state = {
        "topic": "The Science of Procrastination",
        "target_audience": "Young professionals, students, 18-35",
        "research_findings": """
        Procrastination is linked to emotional regulation, not time management.
        Brain imaging shows differences in stress processing. Dr. Pychyl's
        research reveals it's a coping mechanism for negative emotions.
        """,
        "viral_patterns": """
        Pattern 1: Contrarian openings (effectiveness: 8.5/10)
        Pattern 2: Personal vulnerability (effectiveness: 8.2/10)
        Pattern 3: Myth-busting format (effectiveness: 8.8/10)
        """
    }
    
    # Create the Hook Generator
    generator = HookGenerator()
    
    # Generate hooks
    result_state = generator.generate_hooks(test_state)
    
    # Display results
    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)
    print(f"\nHooks Generated: {result_state.get('hook_count', 0)}")
    print(f"Average Effectiveness: {result_state.get('hook_effectiveness_avg', 0):.1f}/10")
    
    # Show all hooks summary
    print("\n📊 ALL HOOKS SUMMARY (Ranked by Effectiveness):")
    summaries = generator.get_all_hooks_summary(result_state)
    for hook in summaries:
        print(f"\n  Hook #{hook['number']}: {hook['title']}")
        print(f"  Score: {hook['score']:.1f}/10")
    
    # Show best hook
    print("\n🏆 BEST HOOK:")
    best = generator.get_best_hook(result_state)
    print(f"Score: {best.get('score', 'N/A')}/10")
    print(f"Preview: {best.get('preview', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
