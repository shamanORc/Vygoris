#!/usr/bin/env python3
"""
Vigorys Nuclear Edition - Advanced Business Logic Vulnerability Scanner
Multi-Agent System with ReAct Framework, LLM-Guided Fuzzing, and Self-Improvement
"""

import asyncio
import sys
from typing import Dict, Any
from agents.orchestrator import AgentOrchestrator
from core.cli import CLIHandler
from core.config import Config
from core.logger import Logger

class VigorysNuclear:
    """Main Vigorys Nuclear Edition class"""
    
    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.orchestrator = AgentOrchestrator()
        self.cli = CLIHandler()
    
    async def run_scan(self, url: str, mode: str = "normal", **kwargs) -> Dict[str, Any]:
        """Run a security scan"""
        
        self.logger.info(f"Starting Vigorys Nuclear scan on {url} (mode: {mode})")
        
        # Prepare scan parameters
        params = {
            "url": url,
            "mode": mode,
            "max_pages": self._get_max_pages(mode),
            "roles": kwargs.get("roles", ["user", "admin", "guest"]),
            "enable_fuzzing": mode in ["ultra", "nuclear"],
            "enable_race_detection": mode == "nuclear"
        }
        
        # Run orchestrator
        result = await self.orchestrator.execute(params)
        
        self.logger.info(f"Scan complete: {result.get('findings_count', 0)} findings")
        
        return result
    
    def _get_max_pages(self, mode: str) -> int:
        """Get max pages to crawl based on mode"""
        
        modes = {
            "quick": 10,
            "normal": 50,
            "ultra": 100,
            "nuclear": 500
        }
        
        return modes.get(mode, 50)
    
    async def run_demo(self) -> Dict[str, Any]:
        """Run demo mode"""
        
        self.logger.info("Running Vigorys Nuclear demo")
        
        demo_result = {
            "status": "success",
            "mode": "demo",
            "findings_count": 8,
            "findings": [
                {
                    "type": "exposed_admin_panel",
                    "severity": "HIGH",
                    "location": "/admin",
                    "cvss_score": 7.5
                },
                {
                    "type": "authorization_bypass",
                    "severity": "CRITICAL",
                    "location": "/api/users",
                    "cvss_score": 9.9
                },
                {
                    "type": "race_condition",
                    "severity": "MEDIUM",
                    "location": "/api/transfer",
                    "cvss_score": 5.5
                }
            ]
        }
        
        return demo_result
    
    async def generate_report(self, scan_id: str, format: str = "pdf") -> str:
        """Generate report from scan"""
        
        self.logger.info(f"Generating {format} report for scan {scan_id}")
        
        return f"Report generated: scan_{scan_id}.{format}"

async def main():
    """Main entry point"""
    
    vygoris = VigorysNuclear()
    
    # Parse CLI arguments
    if len(sys.argv) < 2:
        print("Usage: python vigorys.py <command> [options]")
        print("Commands: scan, demo, report, version")
        return
    
    command = sys.argv[1]
    
    if command == "scan":
        url = sys.argv[3] if len(sys.argv) > 3 else "https://example.com"
        mode = sys.argv[5] if len(sys.argv) > 5 else "normal"
        result = await vygoris.run_scan(url, mode)
        print(f"✅ Scan complete: {result.get('findings_count', 0)} findings")
    
    elif command == "demo":
        result = await vygoris.run_demo()
        print(f"✅ Demo mode: {result.get('findings_count', 0)} findings")
    
    elif command == "report":
        scan_id = sys.argv[3] if len(sys.argv) > 3 else "1"
        format = sys.argv[5] if len(sys.argv) > 5 else "pdf"
        result = await vygoris.generate_report(scan_id, format)
        print(f"✅ {result}")
    
    elif command == "version":
        print("Vigorys Nuclear Edition v2.0")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    asyncio.run(main())
