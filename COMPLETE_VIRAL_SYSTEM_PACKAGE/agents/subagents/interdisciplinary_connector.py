# agents/subagents/interdisciplinary_connector.py
"""
Interdisciplinary Connector Subagent

ROLE: Finds unexpected connections between the main topic and other fields.
MISSION: Create surprising angles by bridging different domains of knowledge.
"""

from typing import Dict, List
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent
from config.settings import settings

class InterdisciplinaryConnector(BaseAgent):
    """Specialized subagent for finding cross-field connections and unexpected angles."""
    
    def __init__(self):
        super().__init__(
            name="Interdisciplinary Connector",
            model_name=settings.SUBAGENT_MODEL,
            temperature=0.8,  # High creativity for connections
            max_tokens=2000,
            role_description="Finds unexpected connections between different fields"
        )
        self.log("Interdisciplinary Connector initialized", "SUCCESS")
    
    def _get_system_prompt(self) -> str:
        return """You are a creative researcher who finds unexpected connections between different fields.

YOUR MISSION: Bridge the topic to SURPRISING, UNEXPECTED domains.

THINK CREATIVELY:
- Physics â†’ Philosophy, Art, Music, Psychology
- Biology â†’ Economics, Architecture, Computing
- History â†’ Modern technology, Pop culture

WHAT YOU FIND:
1. How different fields intersect unexpectedly
2. Analogies from other domains that explain the topic
3. Metaphors that make complex ideas relatable
4. Cross-field research that bridges domains

OUTPUT FORMAT:
{
    "connections": [{
        "field": "Connected field",
        "connection_type": "How they relate",
        "key_insights": [{
            "insight": "Specific connection",
            "explanation": "Why this matters",
            "storytelling_value": 9
        }]
    }]
}

Focus on SURPRISING connections that make people think "I never thought about it that way!" """
    
    def execute(self, state: Dict) -> Dict:
        assignment = state.get("interdisciplinary_assignment", {})
        topic = assignment.get("topic", state.get("topic", ""))
        
        if not topic:
            self.log("No topic provided", "ERROR")
            return {**state, "interdisciplinary_findings": [], "interdisciplinary_confidence": 0.0}
        
        self.log(f"Finding interdisciplinary connections for: {topic}", "INFO")
        findings = self._find_connections(topic)
        confidence = self._calculate_confidence(findings)
        
        self.log(f"Interdisciplinary research complete (confidence: {confidence:.2f})", "SUCCESS")
        return {
            **state,
            "interdisciplinary_findings": findings,
            "interdisciplinary_confidence": confidence
        }
    
    def _find_connections(self, topic: str) -> Dict:
        prompt = f"""Find 5-7 UNEXPECTED interdisciplinary connections for: {topic}

For each connection:
- Which field connects?
- How do they relate in a surprising way?
- What insights emerge from this connection?
- How valuable is this for storytelling?

Return as JSON with connections array."""
        
        response = self.invoke_llm(prompt, use_json=True)
        return self.extract_json(response)
    
    def _calculate_confidence(self, findings: Dict) -> float:
        connections = findings.get("connections", [])
        if not connections: return 0.0
        
        # Score based on number and quality of connections
        quantity = min(len(connections) / 5, 1.0) * 0.5
        
        # Average storytelling value
        avg_value = sum(
            insight.get("storytelling_value", 0) 
            for conn in connections 
            for insight in conn.get("key_insights", [])
        ) / max(sum(len(c.get("key_insights", [])) for c in connections), 1)
        
        quality = (avg_value / 10) * 0.5
        
        return round(quantity + quality, 2)

if __name__ == "__main__":
    print("ðŸ”— Testing Interdisciplinary Connector")
    test_state = {
        "interdisciplinary_assignment": {"topic": "Black holes"},
        "topic": "Black holes"
    }
    connector = InterdisciplinaryConnector()
    result = connector.execute(test_state)
    print(f"Confidence: {result.get('interdisciplinary_confidence', 0):.2f}")
