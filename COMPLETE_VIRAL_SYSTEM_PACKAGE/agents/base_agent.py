"""
Base Agent Class - Foundation for All Agents

This file provides the base functionality that ALL agents in the system inherit from.
Think of this as the "parent class" that defines common behaviors all agents need.

EXPLANATION FOR BEGINNERS:
- This is an "abstract base class" - it's never used directly
- All other agents (Research Gatekeeper, Academic Specialist, etc.) inherit from this
- It provides common functionality: logging, API calls, error handling
- This avoids code duplication - write common code once, use everywhere

INHERITANCE EXAMPLE:
    class AcademicDepthSpecialist(BaseAgent):  # ← Inherits from BaseAgent
        # Now has access to all BaseAgent methods!
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
import os
from anthropic import Anthropic

# Configure logging
# This sets up colored console output so you can see what's happening
logging.basicConfig(
    level=logging.INFO,  # Show INFO level and above (INFO, WARNING, ERROR)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)


class BaseAgent:
    """
    Base class for all agents in the Viral Documentary System.
    
    This class provides:
    1. Anthropic API client setup
    2. Logging utilities
    3. Common helper methods
    4. Error handling patterns
    
    All specialized agents (Research Gatekeeper, Academic Specialist, etc.)
    inherit from this class to get these capabilities automatically.
    """
    
    def __init__(
        self,
        name: str = "BaseAgent",  # Agent's name for logging
        model: str = "claude-sonnet-4-20250514",  # Which Claude model to use
        max_tokens: int = 4000,  # Maximum response length
        temperature: float = 0.7  # Creativity level (0=focused, 1=creative)
    ):
        """
        Initialize the base agent.
        
        PARAMETERS EXPLAINED:
        - name: Used for logging (e.g., "Academic Depth Specialist")
        - model: Which Claude model to use
          * claude-sonnet-4-20250514 = Intelligent, balanced
          * claude-opus-4-20250514 = Most capable, slower/expensive
          * claude-haiku-4-5-20250514 = Fastest, cheapest
        - max_tokens: Maximum length of Claude's response
          * 1 token ≈ 0.75 words, so 4000 tokens ≈ 3000 words
        - temperature: Controls randomness
          * 0.0 = Deterministic (same input → same output)
          * 1.0 = Creative (same input → varied outputs)
          * 0.7 = Balanced (default for most tasks)
        
        Args:
            name: Agent's display name
            model: Claude model identifier
            max_tokens: Maximum response length
            temperature: Response creativity (0.0-1.0)
        """
        self.name = name
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
        # Set up logger specific to this agent
        # Each agent gets its own logger so we can track which agent did what
        self.logger = logging.getLogger(name)
        
        # Initialize Anthropic client
        # This connects to Claude API using your API key from environment variables
        self._init_anthropic_client()
        
        self.log(f"Initialized {name}", "INFO")
    
    def _init_anthropic_client(self):
        """
        Initialize the Anthropic API client.
        
        This method:
        1. Gets your API key from environment variables
        2. Creates an Anthropic client object
        3. Handles errors if API key is missing
        
        SECURITY NOTE: Never hardcode API keys in your code!
        Always use environment variables (.env file) to store secrets.
        """
        try:
            # Get API key from environment variable
            # os.getenv() reads from .env file (loaded by python-dotenv)
            api_key = os.getenv("ANTHROPIC_API_KEY")
            
            if not api_key:
                # No API key found - this will cause problems
                self.log("WARNING: ANTHROPIC_API_KEY not found in environment variables", "WARNING")
                self.log("Set it in .env file or agent will fail on API calls", "WARNING")
                self.client = None
            else:
                # Create Anthropic client with your API key
                self.client = Anthropic(api_key=api_key)
                self.log("Anthropic client initialized successfully", "DEBUG")
                
        except Exception as e:
            # Something went wrong during initialization
            self.log(f"Failed to initialize Anthropic client: {str(e)}", "ERROR")
            self.client = None
    
    def log(self, message: str, level: str = "INFO"):
        """
        Log a message with timestamp and agent name.
        
        This is a convenience method that makes logging easier.
        Instead of:
            self.logger.info("My message")
        You can write:
            self.log("My message", "INFO")
        
        LOGGING LEVELS EXPLAINED:
        - DEBUG: Detailed info for debugging (most verbose)
        - INFO: General information about what's happening
        - WARNING: Something unexpected but not critical
        - ERROR: Something went wrong but agent can continue
        - CRITICAL: Serious error, agent cannot continue
        
        Args:
            message: The message to log
            level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        # Convert level string to appropriate logger method
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        
        # Log the message with agent name prefix
        log_method(f"[{self.name}] {message}")
    
    def call_claude(
        self,
        system_prompt: str,  # System instructions for Claude
        user_message: str,  # The user's query/request
        override_model: Optional[str] = None,  # Optional: use different model
        override_max_tokens: Optional[int] = None,  # Optional: different token limit
        override_temperature: Optional[float] = None  # Optional: different creativity
    ) -> str:
        """
        Make an API call to Claude and return the response.
        
        This is the core method that communicates with Claude API.
        It handles:
        - Setting up the request
        - Making the API call
        - Error handling
        - Extracting the response text
        
        HOW IT WORKS:
        1. Prepare system prompt (tells Claude its role and behavior)
        2. Prepare user message (the actual query)
        3. Send to Claude API
        4. Get response
        5. Extract text from response
        6. Return to caller
        
        Args:
            system_prompt: Instructions defining Claude's role and behavior
            user_message: The actual query or request
            override_model: Optional different model to use (defaults to self.model)
            override_max_tokens: Optional different token limit
            override_temperature: Optional different creativity level
        
        Returns:
            Claude's response as a string
            
        Raises:
            Exception: If API call fails or client not initialized
        """
        # Check if client is initialized
        if not self.client:
            error_msg = "Anthropic client not initialized. Check API key in .env file."
            self.log(error_msg, "ERROR")
            raise Exception(error_msg)
        
        # Use provided values or fall back to instance defaults
        model = override_model or self.model
        max_tokens = override_max_tokens or self.max_tokens
        temperature = override_temperature or self.temperature
        
        try:
            self.log(f"Calling Claude API ({model})...", "DEBUG")
            
            # Make the API call
            # This sends your request to Claude and waits for response
            message = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,  # System instructions
                messages=[
                    {
                        "role": "user",  # Who is sending the message
                        "content": user_message  # The actual message
                    }
                ]
            )
            
            # Extract text from response
            # Claude's response is in message.content[0].text
            response_text = message.content[0].text
            
            # Log success (truncate long responses for readability)
            preview = response_text[:100] + "..." if len(response_text) > 100 else response_text
            self.log(f"API call successful. Response preview: {preview}", "DEBUG")
            
            return response_text
            
        except Exception as e:
            # Something went wrong with the API call
            error_msg = f"Claude API call failed: {str(e)}"
            self.log(error_msg, "ERROR")
            raise Exception(error_msg)
    
    def execute(self, state: Dict) -> Dict:
        """
        Execute the agent's main task.
        
        This is an "abstract method" - it MUST be overridden by child classes.
        Each agent (Academic Specialist, Accessibility Translator, etc.) 
        implements its own execute() method with specialized logic.
        
        PATTERN EXPLANATION:
        BaseAgent defines the interface: execute(state) → state
        Each child agent implements the actual logic differently
        
        Example:
            class AcademicDepthSpecialist(BaseAgent):
                def execute(self, state):
                    # Do academic research here
                    return updated_state
        
        Args:
            state: Current workflow state (dictionary with all data)
        
        Returns:
            Updated state dictionary with agent's results added
        
        Raises:
            NotImplementedError: If child class doesn't override this
        """
        raise NotImplementedError(
            f"{self.name} must implement execute() method. "
            "This is an abstract base class - child agents must override execute()."
        )
    
    def validate_state(self, state: Dict, required_keys: List[str]) -> bool:
        """
        Validate that state contains all required keys.
        
        This is a helper method for checking if the state dictionary
        has all the data the agent needs to do its work.
        
        EXAMPLE USAGE:
            required = ["topic", "search_queries", "quality_threshold"]
            if not self.validate_state(state, required):
                return error_state
        
        Args:
            state: State dictionary to validate
            required_keys: List of keys that must be present
        
        Returns:
            True if all keys present, False otherwise
        """
        missing_keys = [key for key in required_keys if key not in state]
        
        if missing_keys:
            self.log(f"State validation failed. Missing keys: {missing_keys}", "ERROR")
            return False
        
        self.log("State validation passed", "DEBUG")
        return True
    
    def safe_get(self, dictionary: Dict, key: str, default: Any = None) -> Any:
        """
        Safely get a value from a dictionary with a default fallback.
        
        This prevents KeyError exceptions when accessing dictionaries.
        
        EXAMPLE:
            # Instead of:
            value = state["maybe_missing_key"]  # ← Crashes if key missing
            
            # Use:
            value = self.safe_get(state, "maybe_missing_key", default="")
        
        Args:
            dictionary: Dictionary to get value from
            key: Key to look up
            default: Value to return if key not found
        
        Returns:
            Value from dictionary or default
        """
        return dictionary.get(key, default)
    
    def merge_state(self, state: Dict, updates: Dict) -> Dict:
        """
        Merge updates into state and return new state.
        
        This creates a new state dictionary with updates applied,
        without modifying the original state dictionary.
        
        WHY? Immutability prevents bugs where one agent's changes
        accidentally affect another agent's state.
        
        Args:
            state: Original state
            updates: Dictionary of values to update/add
        
        Returns:
            New state dictionary with updates applied
        """
        # Create a copy of the original state
        new_state = state.copy()
        
        # Apply updates
        new_state.update(updates)
        
        self.log(f"Merged {len(updates)} updates into state", "DEBUG")
        return new_state


# =================================================================
# USAGE EXAMPLE
# =================================================================
"""
Example of creating a custom agent that inherits from BaseAgent:

from agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="My Custom Agent",
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.5
        )
    
    def execute(self, state: Dict) -> Dict:
        # Validate required data
        if not self.validate_state(state, ["topic"]):
            return self.merge_state(state, {"error": "Missing topic"})
        
        # Get topic from state
        topic = self.safe_get(state, "topic", "")
        
        # Call Claude
        system_prompt = "You are a helpful research assistant."
        user_message = f"Tell me about {topic}"
        
        response = self.call_claude(system_prompt, user_message)
        
        # Return updated state
        return self.merge_state(state, {
            "my_agent_response": response,
            "my_agent_confidence": 0.95
        })

# Usage:
agent = MyCustomAgent()
result = agent.execute({"topic": "Black Holes"})
print(result["my_agent_response"])
"""
