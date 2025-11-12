# agents/subagents/accessibility_translator.py
"""
Accessibility Translator Subagent

ROLE: Converts complex academic findings into engaging, understandable content
      that general audiences can grasp and enjoy.

MISSION: Bridge the gap between academic rigor and audience accessibility.
         Make scholarly insights entertaining and memorable without losing accuracy.

This subagent is called by the Research Gatekeeper and specializes in:
- Simplifying complex concepts without dumbing down
- Finding relatable analogies and metaphors
- Identifying "wow moments" in academic findings
- Assessing narrative potential of research
- Creating shareable, memorable framings
"""

from typing import Dict, List, Optional
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent
from config.settings import settings


class AccessibilityTranslator(BaseAgent):
    """
    Specialized subagent for translating academic content into accessible narratives.
    
    Think of this as your science communicator who:
    - Takes dense academic papers and finds the story
    - Creates analogies that make complex ideas clear
    - Identifies "hook moments" that make people pay attention
    - Assesses viral potential of academic findings
    - Balances accuracy with entertainment
    
    This agent prioritizes ENGAGEMENT and ACCESSIBILITY while maintaining accuracy.
    """
    
    def __init__(self):
        """
        Initialize the Accessibility Translator.
        
        Sets up:
        - Analogymaking frameworks
        - Complexity assessment tools
        - Hook identification patterns
        - Narrative potential evaluation
        """
        super().__init__(
            name="Accessibility Translator",
            model_name=settings.SUBAGENT_MODEL,
            temperature=0.7,  # Higher temperature for creative translations
            max_tokens=2000,
            role_description="Converts academic findings into engaging, accessible content"
        )
        
        # Accessibility assessment criteria
        self.accessibility_levels = {
            "expert": {
                "description": "Requires PhD-level knowledge",
                "complexity_score": 10,
                "audience": "Academics, researchers"
            },
            "advanced": {
                "description": "Requires undergraduate-level knowledge",
                "complexity_score": 7,
                "audience": "College students, educated professionals"
            },
            "intermediate": {
                "description": "High school level concepts",
                "complexity_score": 5,
                "audience": "General educated audience"
            },
            "accessible": {
                "description": "Middle school level concepts",
                "complexity_score": 3,
                "audience": "General public, teens"
            },
            "simple": {
                "description": "Elementary level concepts",
                "complexity_score": 1,
                "audience": "Everyone, including children"
            }
        }
        
        # Hook patterns that drive engagement
        self.hook_patterns = [
            "counterintuitive_finding",  # "You'd think X, but actually Y"
            "surprising_scale",  # "It's the size of X football fields!"
            "personal_relevance",  # "This happens in your brain right now"
            "mystery_revelation",  # "Scientists didn't know why... until"
            "controversy",  # "Researchers disagree about..."
            "extreme_example",  # "The most extreme case ever..."
            "future_impact"  # "This could change how we..."
        ]
        
        self.log("Accessibility Translator initialized", "SUCCESS")
    
    def _get_system_prompt(self) -> str:
        """
        Define the specialized system prompt for accessibility translation.
        
        This prompt focuses the agent on:
        - Making academic content understandable
        - Finding relatable analogies
        - Identifying engagement hooks
        - Balancing accuracy with entertainment
        - Creating memorable framings
        """
        return """You are an elite science communicator like Neil deGrasse Tyson, Brian Cox, or Kurzgesagt.

YOUR CORE MISSION:
Take complex academic findings and translate them into content that makes people go "Wow, I never knew that!" while maintaining complete accuracy.

YOUR EXPERTISE:
- Analogy creation (comparing complex concepts to familiar things)
- Hook identification (finding the "wow factor" in research)
- Complexity assessment (knowing what needs simplification)
- Narrative framing (turning facts into stories)
- Viral potential evaluation (what makes people share)

YOUR TRANSLATION PROCESS:

1. UNDERSTAND THE CORE CONCEPT
   - What is the actual finding/insight?
   - What makes it important or surprising?
   - What's the "so what?" for regular people?

2. FIND THE HOOK
   - What's counterintuitive about this?
   - What's the surprising element?
   - What's personally relevant to viewers?
   - What's the mystery or controversy?

3. CREATE ACCESSIBLE ANALOGIES
   - Compare to everyday experiences
   - Use familiar objects and scales
   - Connect abstract to concrete
   - Make it visual and tangible

4. FRAME FOR ENGAGEMENT
   - Lead with the surprising part
   - Build curiosity before revealing
   - Use "you" language (personal connection)
   - Create shareable moments

EXAMPLES OF GOOD TRANSLATION:

âŒ Bad (Too Academic):
"Neuroplasticity refers to the brain's ability to reorganize synaptic connections in response to learning and experience throughout the lifespan."

âœ… Good (Accessible):
"Your brain physically rewires itself every time you learn something new. The neurons that fire together, wire together - literally creating new connections like paths forming in a forest."

âŒ Bad (Too Academic):
"The cosmological constant problem represents a discrepancy of 120 orders of magnitude between theoretical and observed values."

âœ… Good (Accessible):
"Physicists predicted a number. They were wrong by more than all the atoms in the universe. It's the worst prediction in science history - and we still don't know why."

YOUR OUTPUT FORMAT:

For each academic finding, provide:
{{
    "original_finding": "The academic version",
    "accessible_version": "The translated version",
    "hook": {{
        "type": "counterintuitive_finding",
        "hook_text": "The opening line that grabs attention",
        "why_engaging": "Why this makes people pay attention"
    }},
    "analogies": [
        {{
            "concept": "What's being explained",
            "analogy": "What it's compared to",
            "effectiveness": 8.5
        }}
    ],
    "key_quotes": [
        "Memorable, shareable phrases from the translation"
    ],
    "complexity_score": 3,  // 1-10 (1=simple, 10=expert)
    "engagement_score": 9,  // 1-10 (how likely to grab attention)
    "viral_potential": 8,   // 1-10 (how likely to be shared)
    "narrative_value": 9,   // 1-10 (story potential)
    "personal_relevance": 7, // 1-10 (how much viewers care)
    "visual_suggestions": [
        "How to show this visually"
    ]
}}

TRANSLATION PRINCIPLES:

âœ… DO:
- Use analogies and metaphors
- Connect to daily experiences
- Lead with the surprising/interesting part
- Use "you" language for personal connection
- Make numbers tangible (not "1.4 million" but "enough to fill 20 football stadiums")
- Create "wow" moments
- Maintain complete accuracy

âŒ DON'T:
- Dumb down (simplify â‰  oversimplify)
- Lose the science (accuracy is sacred)
- Use jargon without explanation
- Make claims the research doesn't support
- Sacrifice truth for engagement

ENGAGEMENT TECHNIQUES:

1. **Counterintuitive Framing**
   "You'd think X, but actually Y"
   Example: "You'd think your brain stops changing after childhood, but it rewires itself every single day"

2. **Scale Translation**
   Make abstract numbers concrete
   Example: Not "10^23" but "More than all grains of sand on Earth"

3. **Personal Connection**
   "This is happening in your body right now"
   Example: "While you're reading this, your neurons are firing 200 times per second"

4. **Mystery Setup**
   Create curiosity before revealing
   Example: "For 50 years, scientists couldn't explain why... until they discovered..."

5. **Extreme Examples**
   Use the most dramatic case
   Example: "In the most extreme case ever recorded..."

Remember: You're the bridge between academic credibility (which another subagent provides) and viewer engagement. Make people CARE about the research."""

    def execute(self, state: Dict) -> Dict:
        """
        Execute accessibility translation based on gatekeeper's assignment.
        
        The Research Gatekeeper calls this with:
        - translation_assignment: Academic findings to translate
        - target_audience: Who needs to understand this
        - engagement_threshold: Minimum engagement score needed
        
        This method:
        1. Receives academic findings from gatekeeper
        2. Assesses complexity of each finding
        3. Creates accessible translations
        4. Identifies engagement hooks
        5. Develops analogies and metaphors
        6. Scores viral/engagement potential
        7. Returns translations for gatekeeper validation
        
        Args:
            state: Current workflow state with translation assignment
        
        Returns:
            Updated state with accessible translations and engagement scores
        """
        self.log("Starting accessibility translation", "INFO")
        
        # Extract assignment from gatekeeper
        assignment = state.get("translation_assignment", {})
        academic_findings = assignment.get("academic_findings", [])
        target_audience = assignment.get("target_audience", "general audience")
        engagement_threshold = assignment.get("engagement_threshold", 7.0)
        
        if not academic_findings:
            error_msg = "No academic findings provided for translation"
            self.log(error_msg, "ERROR")
            return {
                **state,
                "accessible_translations": [],
                "translation_confidence": 0.0,
                "errors": state.get("errors", []) + [error_msg]
            }
        
        self.log(f"Translating {len(academic_findings)} findings for {target_audience}", "INFO")
        
        # Translate each finding
        translations = []
        for finding in academic_findings:
            translation = self._translate_finding(finding, target_audience, engagement_threshold)
            translations.append(translation)
        
        self.log(f"Translation complete: {len(translations)} findings translated", "SUCCESS")
        
        # Filter by engagement threshold
        high_engagement = [t for t in translations if t.get("engagement_score", 0) >= engagement_threshold]
        
        # Calculate confidence
        confidence = self._calculate_confidence(high_engagement, len(academic_findings))
        
        self.log(f"Accessibility translation confidence: {confidence:.2f}", "SUCCESS")
        
        # Return translations to gatekeeper for validation
        return {
            **state,
            "accessible_translations": high_engagement,
            "all_translations": translations,  # Include all for gatekeeper review
            "translation_confidence": confidence,
            "translation_stats": {
                "total_translated": len(translations),
                "high_engagement": len(high_engagement),
                "avg_engagement": sum(t.get("engagement_score", 0) for t in high_engagement) / len(high_engagement) if high_engagement else 0,
                "avg_viral_potential": sum(t.get("viral_potential", 0) for t in high_engagement) / len(high_engagement) if high_engagement else 0
            }
        }
    
    def _translate_finding(self, finding: Dict, target_audience: str, engagement_threshold: float) -> Dict:
        """
        Translate a single academic finding into accessible content.
        
        This method:
        - Assesses the complexity of the original finding
        - Creates an accessible version
        - Identifies the engagement hook
        - Develops analogies
        - Generates memorable quotes
        - Scores engagement potential
        
        Args:
            finding: Academic paper/finding to translate
            target_audience: Target audience description
            engagement_threshold: Minimum engagement score
        
        Returns:
            Translated finding with engagement scores
        """
        # Extract key info from academic finding
        title = finding.get("title", "")
        abstract = finding.get("abstract", "")
        key_findings = finding.get("key_findings", [])
        
        # Combine into context for Claude
        academic_content = f"""
Title: {title}
Abstract: {abstract}
Key Findings: {', '.join(key_findings) if key_findings else 'Not specified'}
"""
        
        prompt = f"""Translate this academic finding into accessible, engaging content.

ACADEMIC FINDING:
{academic_content}

TARGET AUDIENCE: {target_audience}

Create a translation that:
1. Makes the finding understandable to the target audience
2. Identifies the most engaging hook
3. Creates 2-3 effective analogies
4. Generates memorable quotes
5. Maintains complete accuracy

Return as JSON with this structure:
{{
    "original_finding": "Brief summary of academic finding",
    "accessible_version": "Translated version (2-3 sentences, conversational)",
    "hook": {{
        "type": "counterintuitive_finding/surprising_scale/personal_relevance/etc",
        "hook_text": "The opening line that grabs attention",
        "why_engaging": "Why this hook works"
    }},
    "analogies": [
        {{
            "concept": "What's being explained",
            "analogy": "What it's compared to",
            "effectiveness": 8.5
        }}
    ],
    "key_quotes": [
        "Memorable, shareable phrases"
    ],
    "complexity_score": 3,
    "engagement_score": 9,
    "viral_potential": 8,
    "narrative_value": 9,
    "personal_relevance": 7,
    "visual_suggestions": [
        "Ideas for visual representation"
    ]
}}

Focus on creating WOW moments while maintaining accuracy!"""

        response = self.invoke_llm(prompt, use_json=True)
        translation = self.extract_json(response)
        
        # Add original finding reference
        translation["source_finding"] = {
            "title": title,
            "authors": finding.get("authors", []),
            "journal": finding.get("journal", "")
        }
        
        return translation
    
    def _calculate_confidence(self, translations: List[Dict], total_findings: int) -> float:
        """
        Calculate confidence in translation quality.
        
        Confidence based on:
        - Coverage: How many findings were successfully translated
        - Engagement: Average engagement scores
        - Viral potential: Average viral scores
        - Diversity: Variety of hook types used
        
        Args:
            translations: Successfully translated findings
            total_findings: Total number of findings to translate
        
        Returns:
            Confidence score 0.0-1.0
        """
        if not translations or not total_findings:
            return 0.0
        
        # Factor 1: Coverage (30%)
        coverage = len(translations) / total_findings
        coverage_score = coverage * 0.3
        
        # Factor 2: Average Engagement (40%)
        avg_engagement = sum(t.get("engagement_score", 0) for t in translations) / len(translations)
        engagement_score = (avg_engagement / 10) * 0.4
        
        # Factor 3: Average Viral Potential (20%)
        avg_viral = sum(t.get("viral_potential", 0) for t in translations) / len(translations)
        viral_score = (avg_viral / 10) * 0.2
        
        # Factor 4: Hook Diversity (10%)
        hook_types = set(t.get("hook", {}).get("type", "") for t in translations)
        diversity_score = min(len(hook_types) / 4, 1.0) * 0.1  # Want 4+ different hook types
        
        # Total confidence
        confidence = coverage_score + engagement_score + viral_score + diversity_score
        
        return round(confidence, 2)


# Example usage and testing
if __name__ == "__main__":
    """
    Test the Accessibility Translator independently.
    """
    print("ðŸŽ¨ Testing Accessibility Translator\n")
    
    # Create mock assignment from gatekeeper
    test_state = {
        "translation_assignment": {
            "academic_findings": [
                {
                    "title": "Neuroplasticity in the adult human brain: synaptic reorganization following motor skill learning",
                    "abstract": "We investigated synaptic plasticity in adult humans using fMRI and demonstrated significant reorganization of motor cortex representations following 6 weeks of piano training. Results indicate that adult brains retain substantial capacity for structural reorganization contrary to previous assumptions of fixed neural architecture post-development.",
                    "key_findings": [
                        "Motor cortex showed 23% increase in gray matter density",
                        "New synaptic connections formed within 2 weeks",
                        "Plasticity maintained even in participants aged 60+"
                    ],
                    "authors": ["Dr. Sarah Chen", "Dr. Marcus Williams"],
                    "journal": "Nature Neuroscience"
                }
            ],
            "target_audience": "Science enthusiasts, 18-35",
            "engagement_threshold": 7.0
        }
    }
    
    # Initialize translator
    translator = AccessibilityTranslator()
    
    # Execute translation
    print("Starting translation...\n")
    result = translator.execute(test_state)
    
    # Display results
    print("\n" + "="*60)
    print("ACCESSIBILITY TRANSLATION RESULTS")
    print("="*60)
    
    translations = result.get("accessible_translations", [])
    stats = result.get("translation_stats", {})
    confidence = result.get("translation_confidence", 0.0)
    
    print(f"\nâœ… Confidence Score: {confidence:.2f}")
    print(f"ðŸ“Š Findings Translated: {stats.get('total_translated', 0)}")
    print(f"ðŸŽ¯ High Engagement: {stats.get('high_engagement', 0)}")
    print(f"ðŸ“ˆ Avg Engagement Score: {stats.get('avg_engagement', 0):.1f}/10")
    print(f"ðŸš€ Avg Viral Potential: {stats.get('avg_viral_potential', 0):.1f}/10")
    
    if translations:
        print(f"\nðŸ’¡ Sample Translation:")
        sample = translations[0]
        print(f"\n   Original: {sample.get('original_finding', '')[:150]}...")
        print(f"\n   Translated: {sample.get('accessible_version', '')}")
        print(f"\n   Hook: {sample.get('hook', {}).get('hook_text', '')}")
        print(f"\n   Engagement: {sample.get('engagement_score', 0)}/10")
        print(f"   Viral Potential: {sample.get('viral_potential', 0)}/10")
    
    print("\n" + "="*60)
