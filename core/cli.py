"""CLI handler for Vigorys"""

from typing import Dict, Any
from .config import Config
from .logger import setup_logger
import json

logger = setup_logger(__name__)

class CLI:
    """CLI interface for Vigorys"""
    
    def __init__(self, config: Config):
        self.config = config
        logger.debug(f"Initialized CLI with config: {config}")
    
    def run_scan(self) -> Dict[str, Any]:
        """Run a scan"""
        logger.info(f"Starting scan on {self.config.target_url}")
        
        # Placeholder for actual scan implementation
        return {
            "status": "success",
            "target": self.config.target_url,
            "mode": self.config.mode,
            "findings": []
        }
    
    def run_demo(self) -> Dict[str, Any]:
        """Run demo scan"""
        logger.info("Running demo scan")
        
        return {
            "status": "success",
            "target": "demo.vulnerable-app.local",
            "mode": "nuclear",
            "findings": [
                {
                    "type": "authorization_bypass",
                    "severity": "CRITICAL",
                    "description": "Admin panel accessible without authentication"
                }
            ]
        }
    
    def display_results(self, results: Dict[str, Any]):
        """Display scan results in terminal"""
        print(f"\n{'='*60}")
        print(f"Scan Results: {results['status'].upper()}")
        print(f"{'='*60}\n")
        
        for finding in results.get('findings', []):
            print(f"[{finding.get('severity', 'UNKNOWN')}] {finding.get('type', 'Unknown')}")
            print(f"  {finding.get('description', 'No description')}\n")
    
    def export_report(self, results: Dict[str, Any], output_file: str, format: str):
        """Export results to file"""
        if format == "json":
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
        else:
            # Placeholder for other formats
            pass
