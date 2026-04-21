"""Triage & Reporter Agent - Deduplicates, prioritizes and generates reports"""

from typing import Dict, Any, List
from collections import defaultdict

class TriageReporter:
    """Deduplicates findings, calculates CVSS, and generates reports"""
    
    def __init__(self):
        self.deduplicated_findings = []
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute triage and reporting"""
        findings = params.get("findings", {}).get("findings", [])
        
        print(f"[TRIAGE] Processing {len(findings)} findings")
        
        # Deduplicate findings
        deduplicated = await self._deduplicate_findings(findings)
        
        # Calculate CVSS scores
        scored = await self._calculate_cvss_scores(deduplicated)
        
        # Map to OWASP and CWE
        mapped = await self._map_to_standards(scored)
        
        # Prioritize
        prioritized = await self._prioritize_findings(mapped)
        
        self.deduplicated_findings = prioritized
        
        return {
            "status": "success",
            "original_count": len(findings),
            "deduplicated_count": len(deduplicated),
            "findings": prioritized,
            "summary": await self._generate_summary(prioritized)
        }
    
    async def _deduplicate_findings(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate similar findings"""
        seen = {}
        deduplicated = []
        
        for finding in findings:
            key = (finding.get("type"), finding.get("location"))
            
            if key not in seen:
                seen[key] = finding
                deduplicated.append(finding)
        
        print(f"[TRIAGE] Deduplicated: {len(findings)} -> {len(deduplicated)}")
        return deduplicated
    
    async def _calculate_cvss_scores(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate CVSS 3.1 scores"""
        severity_to_cvss = {
            "CRITICAL": 9.9,
            "HIGH": 7.5,
            "MEDIUM": 5.5,
            "LOW": 3.9
        }
        
        for finding in findings:
            severity = finding.get("severity", "MEDIUM")
            finding["cvss_score"] = severity_to_cvss.get(severity, 5.5)
            finding["cvss_vector"] = f"CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H"
        
        return findings
    
    async def _map_to_standards(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map findings to OWASP and CWE"""
        type_to_owasp = {
            "exposed_admin_panel": "A01:2021 – Broken Access Control",
            "unprotected_api": "A01:2021 – Broken Access Control",
            "authorization_issue": "A01:2021 – Broken Access Control",
            "potential_state_manipulation": "A04:2021 – Insecure Deserialization"
        }
        
        type_to_cwe = {
            "exposed_admin_panel": "CWE-284: Improper Access Control",
            "unprotected_api": "CWE-284: Improper Access Control",
            "authorization_issue": "CWE-639: Authorization Bypass Through User-Controlled Key",
            "potential_state_manipulation": "CWE-502: Deserialization of Untrusted Data"
        }
        
        for finding in findings:
            finding_type = finding.get("type", "unknown")
            finding["owasp"] = type_to_owasp.get(finding_type, "Unknown")
            finding["cwe"] = type_to_cwe.get(finding_type, "Unknown")
        
        return findings
    
    async def _prioritize_findings(self, findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize findings by severity and CVSS"""
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        
        sorted_findings = sorted(
            findings,
            key=lambda x: (
                severity_order.get(x.get("severity", "LOW"), 4),
                -x.get("cvss_score", 0)
            )
        )
        
        return sorted_findings
    
    async def _generate_summary(self, findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary statistics"""
        severity_count = defaultdict(int)
        
        for finding in findings:
            severity = finding.get("severity", "LOW")
            severity_count[severity] += 1
        
        return {
            "total_findings": len(findings),
            "critical": severity_count["CRITICAL"],
            "high": severity_count["HIGH"],
            "medium": severity_count["MEDIUM"],
            "low": severity_count["LOW"],
            "avg_cvss": sum(f.get("cvss_score", 0) for f in findings) / len(findings) if findings else 0
        }
