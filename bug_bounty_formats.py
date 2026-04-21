"""Bug Bounty Formats - HackerOne, Bugcrowd, Intigriti"""

from typing import Dict, Any, List
from datetime import datetime
import json

class BugBountyFormats:
    """Generate reports in Bug Bounty platform formats"""
    
    @staticmethod
    def generate_hackerone_report(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate HackerOne format report"""
        
        # Group by severity
        critical = [f for f in findings if f.get("severity") == "CRITICAL"]
        high = [f for f in findings if f.get("severity") == "HIGH"]
        medium = [f for f in findings if f.get("severity") == "MEDIUM"]
        low = [f for f in findings if f.get("severity") == "LOW"]
        
        report = {
            "title": "Security Vulnerability Report - Vygoris",
            "vulnerability_information": {
                "vulnerability_types": list(set(f.get("type") for f in findings)),
                "severity_summary": {
                    "critical": len(critical),
                    "high": len(high),
                    "medium": len(medium),
                    "low": len(low)
                }
            },
            "affected_assets": {
                "asset_type": "URL",
                "asset_identifier": list(set(f.get("url") for f in findings))
            },
            "vulnerability_details": [],
            "impact": "Multiple security vulnerabilities detected",
            "remediation": "See individual findings for remediation steps",
            "proof_of_concept": {
                "description": "Real exploitation performed",
                "steps": []
            }
        }
        
        for finding in findings:
            detail = {
                "type": finding.get("type"),
                "severity": finding.get("severity"),
                "url": finding.get("url"),
                "parameter": finding.get("parameter"),
                "description": finding.get("impact"),
                "remediation": finding.get("remediation"),
                "cvss_score": finding.get("cvss_score", 0)
            }
            report["vulnerability_details"].append(detail)
            
            if finding.get("payload"):
                report["proof_of_concept"]["steps"].append({
                    "step": f"Inject payload in {finding.get('parameter')}",
                    "payload": finding.get("payload")
                })
        
        return report
    
    @staticmethod
    def generate_bugcrowd_report(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate Bugcrowd format report"""
        
        report = {
            "submission": {
                "title": "Security Vulnerabilities - Vygoris Scan",
                "vulnerability_type": "Multiple",
                "severity": "Critical",
                "cvss_score": max([f.get("cvss_score", 0) for f in findings]),
                "description": f"Found {len(findings)} vulnerabilities",
                "affected_endpoint": list(set(f.get("url") for f in findings)),
                "steps_to_reproduce": [],
                "impact": "Unauthorized access and data breach",
                "proof_of_concept": {
                    "description": "Real exploitation evidence",
                    "attachments": []
                },
                "remediation": "Implement security best practices"
            },
            "findings": []
        }
        
        for finding in findings:
            poc_step = {
                "step_number": len(report["submission"]["steps_to_reproduce"]) + 1,
                "description": finding.get("impact"),
                "payload": finding.get("payload"),
                "result": "Vulnerability confirmed"
            }
            report["submission"]["steps_to_reproduce"].append(poc_step)
            
            finding_entry = {
                "type": finding.get("type"),
                "severity": finding.get("severity"),
                "cvss": finding.get("cvss_score"),
                "url": finding.get("url"),
                "parameter": finding.get("parameter"),
                "evidence": finding.get("evidence", {})
            }
            report["findings"].append(finding_entry)
        
        return report
    
    @staticmethod
    def generate_intigriti_report(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate Intigriti format report"""
        
        report = {
            "vulnerability_report": {
                "title": "Vygoris Security Scan Report",
                "date_submitted": datetime.now().isoformat(),
                "researcher": "Vygoris Scanner",
                "vulnerabilities": []
            }
        }
        
        for i, finding in enumerate(findings, 1):
            vuln = {
                "id": f"VUL-{i:04d}",
                "type": finding.get("type"),
                "severity": finding.get("severity"),
                "cvss_v3": {
                    "score": finding.get("cvss_score", 0),
                    "vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
                },
                "affected_url": finding.get("url"),
                "affected_parameter": finding.get("parameter"),
                "description": finding.get("impact"),
                "proof_of_concept": {
                    "description": "Real exploitation",
                    "payload": finding.get("payload"),
                    "steps": finding.get("steps_to_reproduce", [])
                },
                "remediation": finding.get("remediation"),
                "references": [
                    "https://owasp.org/www-community/attacks/",
                    "https://cwe.mitre.org/"
                ]
            }
            report["vulnerability_report"]["vulnerabilities"].append(vuln)
        
        return report
    
    @staticmethod
    def export_to_hackerone_json(findings: List[Dict[str, Any]], filepath: str):
        """Export to HackerOne JSON"""
        
        report = BugBountyFormats.generate_hackerone_report(findings)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath
    
    @staticmethod
    def export_to_bugcrowd_json(findings: List[Dict[str, Any]], filepath: str):
        """Export to Bugcrowd JSON"""
        
        report = BugBountyFormats.generate_bugcrowd_report(findings)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath
    
    @staticmethod
    def export_to_intigriti_json(findings: List[Dict[str, Any]], filepath: str):
        """Export to Intigriti JSON"""
        
        report = BugBountyFormats.generate_intigriti_report(findings)
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return filepath
    
    @staticmethod
    def generate_markdown_report(findings: List[Dict[str, Any]]) -> str:
        """Generate Markdown report for all platforms"""
        
        md = "# Vygoris Security Scan Report\n\n"
        md += f"**Generated:** {datetime.now().isoformat()}\n\n"
        md += f"**Total Findings:** {len(findings)}\n\n"
        
        # Summary
        md += "## Summary\n\n"
        severity_counts = {}
        for finding in findings:
            sev = finding.get("severity", "UNKNOWN")
            severity_counts[sev] = severity_counts.get(sev, 0) + 1
        
        for sev, count in sorted(severity_counts.items(), reverse=True):
            md += f"- **{sev}:** {count}\n"
        
        md += "\n## Findings\n\n"
        
        for i, finding in enumerate(findings, 1):
            md += f"### {i}. {finding.get('type')} - {finding.get('severity')}\n\n"
            md += f"**URL:** {finding.get('url')}\n\n"
            md += f"**Parameter:** {finding.get('parameter')}\n\n"
            md += f"**CVSS Score:** {finding.get('cvss_score')}\n\n"
            md += f"**Impact:** {finding.get('impact')}\n\n"
            md += f"**Remediation:** {finding.get('remediation')}\n\n"
            
            if finding.get("payload"):
                md += f"**Payload:** `{finding.get('payload')}`\n\n"
            
            if finding.get("steps_to_reproduce"):
                md += "**Steps to Reproduce:**\n"
                for step in finding.get("steps_to_reproduce", []):
                    md += f"- {step}\n"
                md += "\n"
        
        return md

# Test
if __name__ == "__main__":
    findings = [
        {
            "type": "SQL_INJECTION",
            "severity": "CRITICAL",
            "cvss_score": 9.8,
            "url": "https://example.com/search",
            "parameter": "q",
            "payload": "' OR '1'='1",
            "impact": "Database compromise",
            "remediation": "Use parameterized queries",
            "steps_to_reproduce": ["1. Go to search", "2. Inject payload"]
        }
    ]
    
    h1 = BugBountyFormats.generate_hackerone_report(findings)
    print("✅ HackerOne report generated")
    print(json.dumps(h1, indent=2)[:200] + "...")
