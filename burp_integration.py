"""Burp Suite Integration - XML export and API"""

from typing import Dict, Any, List
from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime
import json

class BurpIntegration:
    """Export findings to Burp Suite format"""
    
    @staticmethod
    def generate_burp_xml(findings: List[Dict[str, Any]]) -> str:
        """Generate Burp Suite XML format"""
        
        root = Element("issues")
        
        for finding in findings:
            issue = SubElement(root, "issue")
            
            # Issue details
            SubElement(issue, "type").text = finding.get("type", "Unknown")
            SubElement(issue, "name").text = finding.get("type", "Unknown")
            SubElement(issue, "severity").text = finding.get("severity", "Medium")
            SubElement(issue, "confidence").text = "Certain"
            SubElement(issue, "host").text = finding.get("url", "").split("/")[2]
            SubElement(issue, "port").text = "443"
            SubElement(issue, "protocol").text = "https"
            SubElement(issue, "url").text = finding.get("url", "")
            
            # Description
            description = SubElement(issue, "description")
            SubElement(description, "text").text = finding.get("impact", "")
            
            # Remediation
            remediation = SubElement(issue, "remediation")
            SubElement(remediation, "text").text = finding.get("remediation", "")
            
            # Evidence
            evidence = SubElement(issue, "evidence")
            for key, value in finding.get("evidence", {}).items():
                SubElement(evidence, key).text = str(value)
            
            # Request/Response
            if "payload" in finding:
                request = SubElement(issue, "request")
                SubElement(request, "payload").text = finding.get("payload", "")
        
        xml_str = tostring(root, encoding='unicode')
        return f'<?xml version="1.0" encoding="UTF-8"?>\n{xml_str}'
    
    @staticmethod
    def export_to_burp_xml(findings: List[Dict[str, Any]], filepath: str):
        """Export findings to Burp XML file"""
        
        xml_content = BurpIntegration.generate_burp_xml(findings)
        
        with open(filepath, 'w') as f:
            f.write(xml_content)
        
        return filepath
    
    @staticmethod
    def generate_burp_api_payload(findings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate payload for Burp Suite API"""
        
        payload = {
            "issues": [],
            "metadata": {
                "tool": "Vygoris",
                "version": "2.0",
                "timestamp": datetime.now().isoformat(),
                "total_findings": len(findings)
            }
        }
        
        for finding in findings:
            issue = {
                "type": finding.get("type"),
                "name": finding.get("type"),
                "severity": finding.get("severity"),
                "confidence": "Certain",
                "url": finding.get("url"),
                "parameter": finding.get("parameter"),
                "payload": finding.get("payload"),
                "evidence": finding.get("evidence", {}),
                "impact": finding.get("impact"),
                "remediation": finding.get("remediation"),
                "steps": finding.get("steps_to_reproduce", [])
            }
            payload["issues"].append(issue)
        
        return payload
    
    @staticmethod
    def send_to_burp_api(findings: List[Dict[str, Any]], 
                        burp_url: str = "http://localhost:8080") -> Dict[str, Any]:
        """Send findings to Burp Suite API"""
        
        import requests
        
        payload = BurpIntegration.generate_burp_api_payload(findings)
        
        try:
            response = requests.post(
                f"{burp_url}/api/v1/issues",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response": response.json() if response.text else {}
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Test
if __name__ == "__main__":
    findings = [
        {
            "type": "SQL_INJECTION",
            "severity": "CRITICAL",
            "url": "https://example.com/search",
            "parameter": "q",
            "payload": "' OR '1'='1",
            "evidence": {"sql_error": True},
            "impact": "Database compromise",
            "remediation": "Use parameterized queries"
        }
    ]
    
    xml = BurpIntegration.generate_burp_xml(findings)
    print("✅ Burp XML generated:")
    print(xml[:200] + "...")
