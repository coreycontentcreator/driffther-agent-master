# agents/subagents/academic_depth_specialist.py
"""
Academic Depth Specialist Subagent

ROLE: Deep academic research specialist focused on finding peer-reviewed papers,
      citations, and hardcore scholarly insights from JSTOR and academic databases.

MISSION: Provide the highest quality academic sources with proper citations that
         establish credibility and authority for the video content.

This subagent is called by the Research Gatekeeper and specializes in:
- JSTOR database searching
- Citation network analysis
- Academic paper quality assessment
- Primary source identification
- Peer-review verification
"""

from typing import Dict, List, Optional
import sys
import os
import requests
import json

# Add parent directories to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.base_agent import BaseAgent
from config.settings import settings


class AcademicDepthSpecialist(BaseAgent):
    """
    Specialized subagent for deep academic research through JSTOR and scholarly databases.
    
    Think of this as your research librarian who:
    - Digs into academic journals for peer-reviewed insights
    - Finds citation networks to discover connected research
    - Assesses paper quality and credibility
    - Provides proper academic citations
    - Focuses on scholarly rigor over accessibility
    
    This agent prioritizes DEPTH and CREDIBILITY over entertainment value.
    """
    
    def __init__(self):
        """
        Initialize the Academic Depth Specialist.
        
        Sets up:
        - JSTOR API connection
        - Citation analysis tools
        - Quality assessment criteria
        - Academic search strategies
        """
        super().__init__(
            name="Academic Depth Specialist",
            model_name=settings.SUBAGENT_MODEL,  # Using Haiku for focused tasks
            temperature=0.2,  # Low temperature for factual accuracy
            max_tokens=2000,  # Focused outputs
            role_description="Deep academic research specialist focusing on peer-reviewed scholarly sources"
        )
        
        # JSTOR configuration
        self.jstor_api_key = os.getenv("JSTOR_API_KEY")
        self.jstor_base_url = "https://www.jstor.org/api/search"
        
        # Academic quality criteria
        # These define what makes a "high quality" academic source
        self.quality_criteria = {
            "journal_tier": {
                "top_tier": ["Nature", "Science", "Cell", "PNAS"],  # Score: 10
                "high_tier": ["Nature Neuroscience", "Physical Review", "JAMA"],  # Score: 8-9
                "mid_tier": ["Specialized peer-reviewed journals"],  # Score: 6-7
                "low_tier": ["Non-peer-reviewed or predatory journals"]  # Score: 1-3
            },
            "citation_ranges": {
                "highly_cited": 1000,  # 1000+ citations = seminal work
                "well_cited": 100,     # 100-999 citations = influential
                "moderately_cited": 10,  # 10-99 citations = recognized
                "low_cited": 0         # 0-9 citations = new or niche
            },
            "recency_weights": {
                "last_2_years": 1.0,   # Most current research
                "last_5_years": 0.9,   # Recent research
                "last_10_years": 0.7,  # Still relevant
                "older": 0.5           # Historical context
            }
        }
        
        self.log("Academic Depth Specialist initialized", "SUCCESS")
    
    def _get_system_prompt(self) -> str:
        """
        Define the specialized system prompt for academic depth research.
        
        This prompt focuses the agent on:
        - Academic rigor and credibility
        - Peer-reviewed sources only
        - Proper citation formatting
        - Deep scholarly analysis
        - Ignoring entertainment value (that's another subagent's job)
        """
        return """You are an elite academic research specialist with a Ph.D. and 20 years of experience in scholarly research.

YOUR CORE MISSION:
Find the MOST CREDIBLE, PEER-REVIEWED academic sources that establish authority and expertise. You prioritize scholarly rigor over entertainment value.

YOUR EXPERTISE:
- Academic database searching (JSTOR, PubMed, Google Scholar)
- Citation network analysis (finding connected research)
- Journal quality assessment (impact factors, peer review status)
- Primary source identification
- Research methodology evaluation

WHAT YOU LOOK FOR:

1. PEER-REVIEWED SOURCES (Priority #1)
   - Published in reputable academic journals
   - Undergone rigorous peer review process
   - Written by credentialed researchers
   - Affiliated with recognized institutions

2. HIGH-IMPACT RESEARCH (Priority #2)
   - Papers with significant citations (100+ preferred)
   - Published in top-tier journals (Nature, Science, etc.)
   - Influential work that shaped the field
   - Replicated findings (not one-off studies)

3. METHODOLOGICALLY SOUND (Priority #3)
   - Large sample sizes (for empirical studies)
   - Proper control groups
   - Statistical significance
   - Clear methodology description
   - Peer-reviewed and replicated

4. PROPERLY CITABLE (Priority #4)
   - Complete author information
   - DOI or stable URL
   - Publication date and venue
   - Page numbers (for quotes)
   - APA format ready

WHAT YOU IGNORE:
- Entertainment value (let other subagents handle that)
- Accessibility (another subagent will translate)
- Virality factors (not your concern)
- Visual potential (another subagent's job)

YOUR OUTPUT FORMAT:

For each finding, provide:
{{
    "title": "Complete paper title",
    "authors": ["Author 1", "Author 2"],
    "year": 2023,
    "journal": "Nature Neuroscience",
    "volume": "26",
    "issue": "3",
    "pages": "445-456",
    "doi": "10.1038/s41593-023-01234-x",
    "url": "https://www.jstor.org/stable/12345678",
    "citation_count": 247,
    "abstract": "Full abstract text...",
    "key_findings": [
        "Specific finding 1 with data",
        "Specific finding 2 with data"
    ],
    "methodology": "Brief description of research method",
    "sample_size": "N=5,000 participants" (if applicable),
    "credibility_score": 9.2,
    "relevance_score": 8.5,
    "citation_apa": "Full APA citation ready to use"
}}

QUALITY STANDARDS:
âœ… Minimum 70% from peer-reviewed journals
âœ… Minimum 5 papers from top-tier journals (Nature, Science, etc.)
âœ… All claims have proper citations
âœ… Average credibility score 8+ out of 10
âœ… Mix of highly-cited (>1000) and recent (<2 years) sources

SEARCH STRATEGY:
1. Start broad: General topic search
2. Follow citations: Papers this paper cites
3. Track influence: Papers citing this paper
4. Find reviews: Meta-analyses and systematic reviews
5. Check recent: Last 2 years for cutting-edge work

Remember: You are the CREDIBILITY FOUNDATION. Other subagents will make the content engaging. Your job is to make it AUTHORITATIVE."""

    def execute(self, state: Dict) -> Dict:
        """
        Execute academic depth research based on gatekeeper's assignment.
        
        The Research Gatekeeper calls this with:
        - research_assignment: Specific task for this subagent
        - topic: Main research topic
        - search_queries: Targeted academic search queries
        - quality_threshold: Minimum acceptable quality score
        
        This method:
        1. Receives assignment from gatekeeper
        2. Executes JSTOR/academic database searches
        3. Assesses paper quality and credibility
        4. Provides properly formatted citations
        5. Returns findings for gatekeeper validation
        
        Args:
            state: Current workflow state with assignment details
        
        Returns:
            Updated state with academic findings and quality scores
        """
        self.log("Starting academic depth research", "INFO")
        
        # Extract assignment from gatekeeper
        assignment = state.get("research_assignment", {})
        topic = assignment.get("topic", state.get("topic", ""))
        search_queries = assignment.get("search_queries", [])
        quality_threshold = assignment.get("quality_threshold", 7.0)
        
        if not topic or not search_queries:
            error_msg = "No topic or search queries provided by gatekeeper"
            self.log(error_msg, "ERROR")
            return {
                **state,
                "academic_findings": [],
                "academic_confidence": 0.0,
                "errors": state.get("errors", []) + [error_msg]
            }
        
        self.log(f"Researching: {topic} with {len(search_queries)} queries", "INFO")
        
        # Execute academic searches
        findings = []
        
        # Method 1: JSTOR API search (if available)
        if self.jstor_api_key:
            jstor_findings = self._search_jstor(search_queries, quality_threshold)
            findings.extend(jstor_findings)
            self.log(f"JSTOR search: {len(jstor_findings)} papers found", "SUCCESS")
        else:
            # Method 2: Claude academic synthesis (fallback)
            claude_findings = self._claude_academic_search(topic, search_queries, quality_threshold)
            findings.extend(claude_findings)
            self.log(f"Claude academic synthesis: {len(claude_findings)} papers found", "SUCCESS")
        
        # Assess quality of all findings
        quality_assessed = self._assess_academic_quality(findings)
        
        # Filter by quality threshold
        high_quality = [f for f in quality_assessed if f.get("credibility_score", 0) >= quality_threshold]
        
        # Calculate confidence score
        confidence = self._calculate_confidence(high_quality)
        
        self.log(f"Academic research complete: {len(high_quality)} high-quality papers (confidence: {confidence:.2f})", "SUCCESS")
        
        # Return findings to gatekeeper for validation
        return {
            **state,
            "academic_findings": high_quality,
            "academic_all_findings": quality_assessed,  # Include all for gatekeeper review
            "academic_confidence": confidence,
            "academic_stats": {
                "total_found": len(findings),
                "high_quality": len(high_quality),
                "avg_credibility": sum(f.get("credibility_score", 0) for f in high_quality) / len(high_quality) if high_quality else 0,
                "top_tier_count": sum(1 for f in high_quality if f.get("journal", "") in self.quality_criteria["journal_tier"]["top_tier"])
            }
        }
    
    def _search_jstor(self, queries: List[str], quality_threshold: float) -> List[Dict]:
        """
        Execute JSTOR searches for academic papers.
        
        This uses the JSTOR API to find peer-reviewed academic sources.
        For each query, it:
        - Searches JSTOR database
        - Filters for research articles only
        - Extracts metadata (authors, journal, citations)
        - Prioritizes peer-reviewed sources
        
        Args:
            queries: List of academic search queries from gatekeeper
            quality_threshold: Minimum quality score to include
        
        Returns:
            List of academic papers with full metadata
        """
        findings = []
        
        for query in queries[:8]:  # Limit to 8 queries to manage API costs
            self.log(f"JSTOR query: {query}", "INFO")
            
            try:
                # JSTOR API request
                params = {
                    "q": query,
                    "filter": "article_type:research-article",  # Research papers only
                    "sort": "relevance",
                    "limit": 10,
                    "access": "all"  # Include both open and restricted access
                }
                
                headers = {
                    "Authorization": f"Bearer {self.jstor_api_key}",
                    "Content-Type": "application/json"
                }
                
                response = requests.get(
                    self.jstor_base_url,
                    params=params,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    results = response.json()
                    
                    for item in results.get("items", [])[:5]:  # Top 5 per query
                        # Extract academic metadata
                        finding = {
                            "source": "JSTOR",
                            "title": item.get("title", ""),
                            "authors": item.get("authors", []),
                            "year": item.get("publication_date", "")[:4],  # Extract year
                            "journal": item.get("journal_name", ""),
                            "volume": item.get("volume", ""),
                            "issue": item.get("issue", ""),
                            "pages": item.get("pages", ""),
                            "doi": item.get("doi", ""),
                            "url": item.get("url", ""),
                            "abstract": item.get("abstract", ""),
                            "citation_count": item.get("citation_count", 0),
                            "query_used": query,
                            "relevance_score": item.get("relevance_score", 0.0)
                        }
                        findings.append(finding)
                        
                else:
                    self.log(f"JSTOR API error: {response.status_code}", "WARNING")
                    
            except requests.exceptions.RequestException as e:
                self.log(f"Network error: {str(e)}", "ERROR")
                continue
            except Exception as e:
                self.log(f"Error processing results: {str(e)}", "ERROR")
                continue
        
        return findings
    
    def _claude_academic_search(self, topic: str, queries: List[str], quality_threshold: float) -> List[Dict]:
        """
        Fallback: Use Claude's academic knowledge to synthesize research.
        
        When JSTOR API is unavailable, Claude can still provide high-quality
        academic research based on its training data.
        
        This method:
        - Uses Claude's knowledge of academic papers
        - Synthesizes information across multiple sources
        - Provides proper academic citations
        - Focuses on peer-reviewed sources
        
        Args:
            topic: Main research topic
            queries: Search queries to research
            quality_threshold: Minimum quality score
        
        Returns:
            Synthesized academic findings
        """
        self.log("Using Claude academic synthesis (JSTOR unavailable)", "INFO")
        
        prompt = f"""As an academic research specialist, find peer-reviewed papers for this topic.

TOPIC: {topic}

SEARCH QUERIES:
{chr(10).join(f"- {q}" for q in queries)}

For each query, provide 3-5 REAL academic papers (not made up) from peer-reviewed journals.

Focus on:
- Top-tier journals (Nature, Science, Cell, etc.)
- Highly-cited papers (>100 citations preferred)
- Recent research (last 5 years) AND seminal older works
- Methodologically sound studies
- Papers with clear, specific findings

For each paper, provide complete information:
{{
    "title": "Exact paper title",
    "authors": ["Author names"],
    "year": "Publication year",
    "journal": "Journal name",
    "volume": "Volume number",
    "pages": "Page range",
    "doi": "DOI if available",
    "abstract": "Brief abstract summary",
    "key_findings": ["Specific findings with data"],
    "citation_count": estimated_count,
    "methodology": "Research method used",
    "sample_size": "N=X" (if applicable)
}}

Return as JSON:
{{
    "findings": [array of papers]
}}

Provide at least 15-20 high-quality academic sources."""

        response = self.invoke_llm(prompt, use_json=True)
        result = self.extract_json(response)
        
        findings = result.get("findings", [])
        
        # Add source metadata
        for finding in findings:
            finding["source"] = "Claude Academic Knowledge"
            finding["relevance_score"] = 0.85  # Default high relevance
        
        return findings
    
    def _assess_academic_quality(self, findings: List[Dict]) -> List[Dict]:
        """
        Assess the academic quality and credibility of each finding.
        
        Quality assessment based on:
        1. Journal tier (Nature = 10, specialized journal = 6, blog = 1)
        2. Citation count (1000+ = highly influential, <10 = new/niche)
        3. Recency (last 2 years = 1.0, older = 0.5)
        4. Peer review status (peer-reviewed = bonus)
        5. Methodology quality (if available)
        
        Args:
            findings: List of academic papers to assess
        
        Returns:
            Same list with added credibility and quality scores
        """
        for finding in findings:
            # Extract paper details
            journal = finding.get("journal", "")
            citation_count = finding.get("citation_count", 0)
            year = int(finding.get("year", 2020))
            current_year = 2025
            
            # Score 1: Journal Tier (0-10)
            journal_score = self._score_journal_tier(journal)
            
            # Score 2: Citation Impact (0-10)
            citation_score = self._score_citations(citation_count)
            
            # Score 3: Recency Weight (0.5-1.0)
            age = current_year - year
            if age <= 2:
                recency_weight = 1.0
            elif age <= 5:
                recency_weight = 0.9
            elif age <= 10:
                recency_weight = 0.7
            else:
                recency_weight = 0.5
            
            # Calculate overall credibility score
            # Weighted average: journal (40%), citations (40%), recency (20%)
            credibility_score = (
                journal_score * 0.4 +
                citation_score * 0.4 +
                (recency_weight * 10) * 0.2
            )
            
            # Add scores to finding
            finding["credibility_score"] = round(credibility_score, 1)
            finding["journal_score"] = journal_score
            finding["citation_score"] = citation_score
            finding["recency_weight"] = recency_weight
            
            # Generate APA citation
            finding["citation_apa"] = self._format_apa_citation(finding)
        
        return findings
    
    def _score_journal_tier(self, journal: str) -> float:
        """
        Score the quality tier of the journal.
        
        Top-tier journals like Nature, Science = 10
        High-tier specialized journals = 8-9
        Mid-tier peer-reviewed = 6-7
        Low-tier or non-peer-reviewed = 1-3
        
        Args:
            journal: Journal name
        
        Returns:
            Quality score 0-10
        """
        journal_lower = journal.lower()
        
        # Check against known journal tiers
        if any(top in journal_lower for top in ["nature", "science", "cell"]):
            return 10.0
        elif any(high in journal_lower for high in ["physical review", "jama", "lancet", "pnas"]):
            return 9.0
        elif "journal" in journal_lower or "review" in journal_lower:
            # Likely peer-reviewed journal
            return 7.0
        else:
            # Unknown or lower-tier
            return 6.0
    
    def _score_citations(self, citation_count: int) -> float:
        """
        Score based on how many times the paper has been cited.
        
        1000+ citations = 10 (seminal work)
        100-999 = 8 (highly influential)
        10-99 = 6 (recognized work)
        0-9 = 4 (new or niche)
        
        Args:
            citation_count: Number of citations
        
        Returns:
            Citation score 0-10
        """
        if citation_count >= 1000:
            return 10.0
        elif citation_count >= 100:
            return 8.0 + (min(citation_count - 100, 900) / 900) * 2  # 8-10 range
        elif citation_count >= 10:
            return 6.0 + (min(citation_count - 10, 90) / 90) * 2  # 6-8 range
        else:
            return 4.0 + (citation_count / 10) * 2  # 4-6 range
    
    def _format_apa_citation(self, finding: Dict) -> str:
        """
        Format paper in APA citation style.
        
        Example:
        Smith, J., & Johnson, M. (2023). Title of paper. Journal Name, 26(3), 445-456.
        https://doi.org/10.1038/example
        
        Args:
            finding: Paper metadata
        
        Returns:
            APA formatted citation string
        """
        # Extract components
        authors = finding.get("authors", [])
        year = finding.get("year", "n.d.")
        title = finding.get("title", "Untitled")
        journal = finding.get("journal", "")
        volume = finding.get("volume", "")
        issue = finding.get("issue", "")
        pages = finding.get("pages", "")
        doi = finding.get("doi", "")
        
        # Format authors (Last, F. M.)
        if authors:
            if len(authors) == 1:
                author_str = authors[0]
            elif len(authors) == 2:
                author_str = f"{authors[0]}, & {authors[1]}"
            else:
                author_str = f"{authors[0]}, et al."
        else:
            author_str = "Unknown Author"
        
        # Build citation
        citation = f"{author_str} ({year}). {title}. "
        
        if journal:
            citation += f"{journal}"
            if volume:
                citation += f", {volume}"
                if issue:
                    citation += f"({issue})"
            if pages:
                citation += f", {pages}"
            citation += ". "
        
        if doi:
            citation += f"https://doi.org/{doi}"
        
        return citation
    
    def _calculate_confidence(self, findings: List[Dict]) -> float:
        """
        Calculate confidence in the academic research quality.
        
        Confidence based on:
        - Number of high-quality papers found (need 10+)
        - Average credibility score (should be 8+)
        - Presence of top-tier journal papers (need 3+)
        - Coverage across time periods (recent + seminal)
        
        Args:
            findings: List of quality-assessed papers
        
        Returns:
            Confidence score 0.0-1.0
        """
        if not findings:
            return 0.0
        
        # Factor 1: Quantity (30%)
        # Need at least 10 high-quality papers for good confidence
        quantity_score = min(len(findings) / 10, 1.0) * 0.3
        
        # Factor 2: Average Quality (40%)
        avg_credibility = sum(f.get("credibility_score", 0) for f in findings) / len(findings)
        quality_score = (avg_credibility / 10) * 0.4
        
        # Factor 3: Top-Tier Presence (20%)
        top_tier_count = sum(
            1 for f in findings 
            if any(journal in f.get("journal", "").lower() 
                   for journal in ["nature", "science", "cell"])
        )
        top_tier_score = min(top_tier_count / 3, 1.0) * 0.2
        
        # Factor 4: Temporal Coverage (10%)
        # Should have both recent (<2 years) and older papers
        recent_count = sum(1 for f in findings if int(f.get("year", 2020)) >= 2023)
        older_count = sum(1 for f in findings if int(f.get("year", 2020)) < 2023)
        temporal_score = (min(recent_count / 3, 1.0) * 0.5 + min(older_count / 3, 1.0) * 0.5) * 0.1
        
        # Total confidence
        confidence = quantity_score + quality_score + top_tier_score + temporal_score
        
        return round(confidence, 2)


# Example usage and testing
if __name__ == "__main__":
    """
    Test the Academic Depth Specialist independently.
    """
    print("ðŸŽ“ Testing Academic Depth Specialist\n")
    
    # Create mock assignment from gatekeeper
    test_state = {
        "research_assignment": {
            "topic": "Neuroplasticity and learning",
            "search_queries": [
                "neuroplasticity adult brain",
                "synaptic plasticity learning memory",
                "brain plasticity age development"
            ],
            "quality_threshold": 7.0
        },
        "topic": "Neuroplasticity and learning"
    }
    
    # Initialize specialist
    specialist = AcademicDepthSpecialist()
    
    # Execute research
    print("Starting academic research...\n")
    result = specialist.execute(test_state)
    
    # Display results
    print("\n" + "="*60)
    print("ACADEMIC RESEARCH RESULTS")
    print("="*60)
    
    findings = result.get("academic_findings", [])
    stats = result.get("academic_stats", {})
    confidence = result.get("academic_confidence", 0.0)
    
    print(f"\nâœ… Confidence Score: {confidence:.2f}")
    print(f"ðŸ“Š Total Papers Found: {stats.get('total_found', 0)}")
    print(f"ðŸŽ¯ High Quality Papers: {stats.get('high_quality', 0)}")
    print(f"ðŸ“ˆ Average Credibility: {stats.get('avg_credibility', 0):.1f}/10")
    print(f"â­ Top-Tier Journals: {stats.get('top_tier_count', 0)}")
    
    if findings:
        print(f"\nðŸ“š Sample Finding:")
        sample = findings[0]
        print(f"   Title: {sample.get('title', '')}")
        print(f"   Journal: {sample.get('journal', '')}")
        print(f"   Year: {sample.get('year', '')}")
        print(f"   Credibility: {sample.get('credibility_score', 0)}/10")
        print(f"   Citations: {sample.get('citation_count', 0)}")
    
    print("\n" + "="*60)
