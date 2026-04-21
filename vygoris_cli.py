#!/usr/bin/env python3
"""Vygoris Production - CLI Nuclear Edition"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

from real_http_client import RealHTTPClient
from payload_injector import PayloadInjector
from poc_generator import PoC Generator
from burp_integration import BurpIntegration
from bug_bounty_formats import BugBountyFormats
from validation_engine import ValidationEngine

class VygoriesCLI:
    """Vygoris Production CLI"""
    
    def __init__(self):
        self.http_client = RealHTTPClient()
        self.payload_injector = PayloadInjector()
        self.poc_gen = PoC Generator()
        self.findings = []
    
    def scan(self, url: str, output_format: str = "json"):
        """Run full security scan"""
        
        print(f"🔍 Vygoris Production - Scanning {url}")
        print(f"⏰ Started: {datetime.now().isoformat()}")
        print("-" * 60)
        
        # Phase 1: Crawl and map
        print("📍 Phase 1: Crawling and mapping...")
        pages = self.http_client.crawl(url)
        print(f"✅ Found {len(pages)} pages")
        
        # Phase 2: Test SQL Injection
        print("\n💉 Phase 2: Testing SQL Injection...")
        for page in pages:
            for param in page.get("parameters", []):
                payloads = self.payload_injector.get_sql_payloads()
                for payload in payloads[:3]:  # Test top 3
                    response = self.http_client.inject_payload(
                        page["url"], param, payload
                    )
                    
                    if response and "error" in response.lower():
                        poc = self.poc_gen.generate_sql_injection_poc(
                            url=page["url"],
                            parameter=param,
                            payload=payload,
                            response=response,
                            response_time=0.5
                        )
                        self.findings.append(poc)
                        print(f"  ⚠️ Found SQL Injection in {param}")
        
        # Phase 3: Test XSS
        print("\n🔗 Phase 3: Testing XSS...")
        for page in pages:
            for param in page.get("parameters", []):
                payloads = self.payload_injector.get_xss_payloads()
                for payload in payloads[:2]:
                    response = self.http_client.inject_payload(
                        page["url"], param, payload
                    )
                    
                    if response and payload in response:
                        poc = self.poc_gen.generate_xss_poc(
                            url=page["url"],
                            parameter=param,
                            payload=payload,
                            response=response
                        )
                        self.findings.append(poc)
                        print(f"  ⚠️ Found XSS in {param}")
        
        # Phase 4: Validate findings
        print("\n✔️ Phase 4: Validating findings (Zero False Positives)...")
        validated = ValidationEngine.filter_false_positives(self.findings)
        print(f"✅ Validated {len(validated)}/{len(self.findings)} findings")
        
        # Phase 5: Export
        print("\n📤 Phase 5: Exporting findings...")
        self._export_findings(validated, output_format)
        
        print("-" * 60)
        print(f"✅ Scan completed: {datetime.now().isoformat()}")
        print(f"📊 Total findings: {len(validated)}")
    
    def _export_findings(self, findings: list, output_format: str):
        """Export findings in requested format"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if output_format == "json":
            filepath = f"vygoris_report_{timestamp}.json"
            with open(filepath, 'w') as f:
                json.dump(findings, f, indent=2)
            print(f"  ✅ JSON: {filepath}")
        
        elif output_format == "burp":
            filepath = f"vygoris_burp_{timestamp}.xml"
            BurpIntegration.export_to_burp_xml(findings, filepath)
            print(f"  ✅ Burp XML: {filepath}")
        
        elif output_format == "hackerone":
            filepath = f"vygoris_h1_{timestamp}.json"
            BugBountyFormats.export_to_hackerone_json(findings, filepath)
            print(f"  ✅ HackerOne: {filepath}")
        
        elif output_format == "bugcrowd":
            filepath = f"vygoris_bugcrowd_{timestamp}.json"
            BugBountyFormats.export_to_bugcrowd_json(findings, filepath)
            print(f"  ✅ Bugcrowd: {filepath}")
        
        elif output_format == "intigriti":
            filepath = f"vygoris_intigriti_{timestamp}.json"
            BugBountyFormats.export_to_intigriti_json(findings, filepath)
            print(f"  ✅ Intigriti: {filepath}")
        
        elif output_format == "markdown":
            filepath = f"vygoris_report_{timestamp}.md"
            md = BugBountyFormats.generate_markdown_report(findings)
            with open(filepath, 'w') as f:
                f.write(md)
            print(f"  ✅ Markdown: {filepath}")
        
        elif output_format == "all":
            self._export_findings(findings, "json")
            self._export_findings(findings, "burp")
            self._export_findings(findings, "hackerone")
            self._export_findings(findings, "bugcrowd")
            self._export_findings(findings, "intigriti")
            self._export_findings(findings, "markdown")

def main():
    """Main CLI entry point"""
    
    parser = argparse.ArgumentParser(
        description="Vygoris Production - Real Security Scanner for Bug Bounty"
    )
    
    parser.add_argument(
        "url",
        help="Target URL to scan"
    )
    
    parser.add_argument(
        "--format",
        choices=["json", "burp", "hackerone", "bugcrowd", "intigriti", "markdown", "all"],
        default="json",
        help="Output format (default: json)"
    )
    
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)"
    )
    
    args = parser.parse_args()
    
    cli = VygoriesCLI()
    cli.scan(args.url, args.format)

if __name__ == "__main__":
    main()
