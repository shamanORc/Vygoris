"""Configuration management for Vigorys"""

from dataclasses import dataclass
from typing import Optional
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """Vigorys configuration"""
    
    target_url: str
    mode: str = "normal"
    llm_provider: str = "grok"
    custom_rules: Optional[str] = None
    timeout: int = 300
    workers: int = 4
    demo_mode: bool = False
    
    # LLM Configuration
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "grok-2")
    
    # Crawling Configuration
    max_pages: int = 100
    max_forms: int = 50
    user_agent: str = "Vigorys/2.0"
    
    # Output Configuration
    verbose: bool = False
    log_file: Optional[str] = None
    
    def __post_init__(self):
        """Validate configuration"""
        if not self.target_url and not self.demo_mode:
            raise ValueError("target_url is required unless demo_mode is True")
        
        if self.mode not in ["quick", "normal", "ultra", "nuclear"]:
            raise ValueError(f"Invalid mode: {self.mode}")
        
        if self.llm_provider not in ["grok", "claude", "openai"]:
            raise ValueError(f"Invalid LLM provider: {self.llm_provider}")
