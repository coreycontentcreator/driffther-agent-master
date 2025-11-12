# agents/subagents/historical_context_miner.py
"""
Historical Context Miner Subagent

ROLE: Discovers the timeline, evolution, and dramatic story arc of scientific/historical discoveries.
MISSION: Turn facts into compelling narratives through historical context and human drama.
"""

from typing import Dict, List
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent
from config.settings import settings

class HistoricalContextMiner(BaseAgent):
    """Specialized subagent for mining historical context, timelines, and narrative arcs."""
    
    def __init__(self):
        super().__init__(
            name="Historical Context Miner",
            model_name=settings.SUBAGENT_MODEL,
            temperature=0.6,
            max_tokens=2000,
            role_description="Discovers historical evolution and narrative arcs of discoveries"
        )
        self.log("Historical Context Miner initialized", "SUCCESS")
    
    def _get_system_prompt(self) -> str:
        return """You are a historian and storyteller specializing in the history of science and ideas.

YOUR MISSION: Find the STORY behind the facts - the timeline, drama, key figures, and evolution.

WHAT YOU SEARCH FOR:
1. KEY MILESTONES - Specific dates, breakthrough moments
2. KEY FIGURES - Researchers and their personal stories  
3. CONTROVERSIES - Debates, rejected theories, conflicts
4. MISTAKES - Wrong ideas that seemed right at the time
5. TURNING POINTS - Moments that changed everything
6. CULTURAL CONTEXT - How society viewed this topic over time

OUTPUT FORMAT:
{
    "historical_timeline": [{
        "year": "1915",
        "event": "What happened",
        "significance": "Why it mattered",
        "key_figures": ["Names"],
        "drama_factor": 9,
        "storytelling_potential": "How to present in video"
    }],
    "evolution_narrative": "Overall story arc of discovery",
    "surprising_facts": ["Facts that surprise modern audience"]
}

Focus on DRAMA and STORYTELLING VALUE - find the human stories behind discoveries."""
    
    def execute(self, state: Dict) -> Dict:
        assignment = state.get("historical_assignment", {})
        topic = assignment.get("topic", state.get("topic", ""))
        
        if not topic:
            self.log("No topic provided", "ERROR")
            return {**state, "historical_findings": [], "historical_confidence": 0.0}
        
        self.log(f"Mining historical context for: {topic}", "INFO")
        findings = self._research_history(topic)
        confidence = self._calculate_confidence(findings)
        
        self.log(f"Historical mining complete (confidence: {confidence:.2f})", "SUCCESS")
        return {
            **state,
            "historical_findings": findings,
            "historical_confidence": confidence
        }
    
    def _research_history(self, topic: str) -> Dict:
        prompt = f"""Research the historical evolution of: {topic}

Find:
1. Timeline of key discoveries (with specific dates)
2. Key researchers and their personal stories
3. Controversies and debates
4. Wrong theories and corrections
5. Turning points that changed understanding

Return comprehensive JSON with historical_timeline, evolution_narrative, and surprising_facts."""
        
        response = self.invoke_llm(prompt, use_json=True)
        return self.extract_json(response)
    
    def _calculate_confidence(self, findings: Dict) -> float:
        timeline = findings.get("historical_timeline", [])
        narrative = findings.get("evolution_narrative", "")
        
        if not timeline: return 0.0
        
        # Score based on timeline completeness and narrative quality
        timeline_score = min(len(timeline) / 8, 1.0) * 0.6  # Want 8+ milestones
        narrative_score = (len(narrative) / 500) * 0.4 if narrative else 0.0
        
        return round(min(timeline_score + narrative_score, 1.0), 2)

if __name__ == "__main__":
    print("ðŸ“œ Testing Historical Context Miner")
    test_state = {
        "historical_assignment": {"topic": "Quantum mechanics development"},
        "topic": "Quantum mechanics"
    }
    miner = HistoricalContextMiner()
    result = miner.execute(test_state)
    print(f"Confidence: {result.get('historical_confidence', 0):.2f}")
