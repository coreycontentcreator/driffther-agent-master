# agents/subagents/contrarian_viewpoint_hunter.py
"""
Contrarian Viewpoint Hunter Subagent

ROLE: Identifies legitimate alternative perspectives and ongoing debates.
MISSION: Add depth and balance by finding well-supported minority viewpoints.
"""

from typing import Dict, List
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent
from config.settings import settings

class ContrarianViewpointHunter(BaseAgent):
    """Specialized subagent for finding legitimate alternative perspectives."""
    
    def __init__(self):
        super().__init__(
            name="Contrarian Viewpoint Hunter",
            model_name=settings.SUBAGENT_MODEL,
            temperature=0.5,
            max_tokens=2000,
            role_description="Finds legitimate alternative perspectives and debates"
        )
        self.log("Contrarian Viewpoint Hunter initialized", "SUCCESS")
    
    def _get_system_prompt(self) -> str:
        return """You are a research specialist who finds LEGITIMATE alternative viewpoints.

YOUR MISSION: Find well-supported minority opinions that add depth and nuance.

CRITICAL DISTINCTION:
âœ… GOOD: Legitimate scientific debate backed by evidence
âœ… GOOD: Minority opinions from credible researchers
âœ… GOOD: Ongoing controversies within the field
âŒ BAD: Conspiracy theories
âŒ BAD: Pseudoscience
âŒ BAD: Fringe theories without evidence

WHAT YOU FIND:
1. Alternative interpretations of data
2. Ongoing debates among experts
3. Minority positions with good evidence
4. Areas of scientific uncertainty

OUTPUT FORMAT:
{
    "contrarian_viewpoints": [{
        "viewpoint": "What the minority claims",
        "evidence": "Research supporting this view",
        "proponents": ["Credible researchers"],
        "credibility_score": 7,
        "why_minority": "Why this isn't mainstream",
        "value_for_narrative": "How this adds depth"
    }],
    "ongoing_debates": ["Open questions in the field"]
}

Focus on viewpoints that add DEPTH and NUANCE, not controversy for its own sake."""
    
    def execute(self, state: Dict) -> Dict:
        assignment = state.get("contrarian_assignment", {})
        topic = assignment.get("topic", state.get("topic", ""))
        mainstream_findings = assignment.get("mainstream_findings", [])
        
        if not topic:
            self.log("No topic provided", "ERROR")
            return {**state, "contrarian_findings": [], "contrarian_confidence": 0.0}
        
        self.log(f"Hunting contrarian viewpoints for: {topic}", "INFO")
        findings = self._find_viewpoints(topic, mainstream_findings)
        confidence = self._calculate_confidence(findings)
        
        self.log(f"Contrarian hunting complete (confidence: {confidence:.2f})", "SUCCESS")
        return {
            **state,
            "contrarian_findings": findings,
            "contrarian_confidence": confidence
        }
    
    def _find_viewpoints(self, topic: str, mainstream_findings: List) -> Dict:
        mainstream_summary = "\n".join([str(f)[:200] for f in mainstream_findings[:5]])
        
        prompt = f"""Find LEGITIMATE contrarian viewpoints about: {topic}

MAINSTREAM PERSPECTIVE:
{mainstream_summary}

Find 3-5 alternative perspectives that:
âœ“ Have credible research support
âœ“ Come from qualified experts
âœ“ Represent ongoing debates
âœ“ Add nuance without denying facts

Return as JSON with contrarian_viewpoints and ongoing_debates."""
        
        response = self.invoke_llm(prompt, use_json=True)
        return self.extract_json(response)
    
    def _calculate_confidence(self, findings: Dict) -> float:
        viewpoints = findings.get("contrarian_viewpoints", [])
        debates = findings.get("ongoing_debates", [])
        
        if not viewpoints: return 0.0
        
        # Score based on quantity and credibility
        quantity = min(len(viewpoints) / 3, 1.0) * 0.5
        avg_credibility = sum(v.get("credibility_score", 0) for v in viewpoints) / len(viewpoints)
        quality = (avg_credibility / 10) * 0.5
        
        return round(quantity + quality, 2)

if __name__ == "__main__":
    print("ðŸŽ¯ Testing Contrarian Viewpoint Hunter")
    test_state = {
        "contrarian_assignment": {
            "topic": "AI consciousness",
            "mainstream_findings": ["AI systems can't be conscious", "Consciousness requires biological substrate"]
        },
        "topic": "AI consciousness"
    }
    hunter = ContrarianViewpointHunter()
    result = hunter.execute(test_state)
    print(f"Confidence: {result.get('contrarian_confidence', 0):.2f}")
