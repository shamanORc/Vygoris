"""Real PoC Generator - Captura de dados e evidências"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import base64
from pathlib import Path

class PoC Generator:
    """Generate real Proof of Concept with evidence"""
    
    def __init__(self):
        self.pocs: List[Dict[str, Any]] = []
        self.evidence_dir = Path("/tmp/vygoris_evidence")
        self.evidence_dir.mkdir(exist_ok=True)
    
    def generate_sql_injection_poc(self, 
                                   url: str, 
                                   parameter: str, 
                                   payload: str,
                                   response: str,
                                   response_time: float) -> Dict[str, Any]:
        """Generate SQL Injection PoC"""
        
        poc = {
            "type": "SQL_INJECTION",
            "severity": "CRITICAL",
            "cvss_score": 9.8,
            "url": url,
            "parameter": parameter,
            "payload": payload,
            "evidence": {
                "response_contains_error": "SQL error" in response or "syntax error" in response,
                "response_time_anomaly": response_time > 5,
                "response_length": len(response),
                "response_preview": response[:200]
            },
            "steps_to_reproduce": [
                f"1. Navigate to {url}",
                f"2. Find parameter: {parameter}",
                f"3. Inject payload: {payload}",
                f"4. Observe SQL error or time delay",
                f"5. Confirm data extraction possible"
            ],
            "impact": "Attacker can extract, modify, or delete database records",
            "remediation": "Use parameterized queries and input validation",
            "timestamp": datetime.now().isoformat()
        }
        
        self.pocs.append(poc)
        return poc
    
    def generate_xss_poc(self,
                        url: str,
                        parameter: str,
                        payload: str,
                        response: str,
                        screenshot_path: Optional[str] = None) -> Dict[str, Any]:
        """Generate XSS PoC"""
        
        poc = {
            "type": "XSS",
            "severity": "HIGH",
            "cvss_score": 7.1,
            "url": url,
            "parameter": parameter,
            "payload": payload,
            "evidence": {
                "payload_reflected": payload in response,
                "script_tag_present": "<script>" in response,
                "event_handler_present": "onerror=" in response or "onload=" in response,
                "screenshot": screenshot_path
            },
            "steps_to_reproduce": [
                f"1. Navigate to {url}",
                f"2. Find parameter: {parameter}",
                f"3. Inject payload: {payload}",
                f"4. Observe JavaScript execution",
                f"5. Confirm session hijacking possible"
            ],
            "impact": "Attacker can steal cookies, sessions, or perform actions as user",
            "remediation": "Implement output encoding and Content Security Policy",
            "timestamp": datetime.now().isoformat()
        }
        
        self.pocs.append(poc)
        return poc
    
    def generate_idor_poc(self,
                         url: str,
                         original_id: str,
                         test_id: str,
                         original_response: str,
                         test_response: str,
                         original_status: int,
                         test_status: int) -> Dict[str, Any]:
        """Generate IDOR PoC"""
        
        poc = {
            "type": "IDOR",
            "severity": "HIGH",
            "cvss_score": 7.5,
            "url": url,
            "evidence": {
                "original_id": original_id,
                "test_id": test_id,
                "original_status": original_status,
                "test_status": test_status,
                "unauthorized_access": test_status == 200 and original_status == 403,
                "data_exposed": len(test_response) > 100
            },
            "steps_to_reproduce": [
                f"1. Authenticate as user A",
                f"2. Access resource with ID: {original_id}",
                f"3. Change ID to: {test_id}",
                f"4. Observe access to user B's data",
                f"5. Confirm no authorization checks"
            ],
            "impact": "Attacker can access other users' private data",
            "remediation": "Implement proper authorization checks on all resources",
            "timestamp": datetime.now().isoformat()
        }
        
        self.pocs.append(poc)
        return poc
    
    def generate_auth_bypass_poc(self,
                                url: str,
                                username: str,
                                password: str,
                                response: str,
                                cookies: Dict[str, str]) -> Dict[str, Any]:
        """Generate Authentication Bypass PoC"""
        
        poc = {
            "type": "AUTH_BYPASS",
            "severity": "CRITICAL",
            "cvss_score": 9.9,
            "url": url,
            "evidence": {
                "username": username,
                "password": password,
                "login_successful": "dashboard" in response.lower() or "logout" in response.lower(),
                "session_cookie_obtained": len(cookies) > 0,
                "cookies": {k: v[:20] + "..." for k, v in cookies.items()}
            },
            "steps_to_reproduce": [
                f"1. Navigate to {url}",
                f"2. Enter username: {username}",
                f"3. Enter password: {password}",
                f"4. Observe successful login",
                f"5. Confirm weak credentials accepted"
            ],
            "impact": "Attacker can gain unauthorized access to user accounts",
            "remediation": "Enforce strong password policies and rate limiting",
            "timestamp": datetime.now().isoformat()
        }
        
        self.pocs.append(poc)
        return poc
    
    def generate_race_condition_poc(self,
                                   url: str,
                                   action: str,
                                   concurrent_requests: int,
                                   results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate Race Condition PoC"""
        
        poc = {
            "type": "RACE_CONDITION",
            "severity": "MEDIUM",
            "cvss_score": 5.3,
            "url": url,
            "action": action,
            "evidence": {
                "concurrent_requests": concurrent_requests,
                "inconsistent_results": len(set(str(r) for r in results)) > 1,
                "duplicate_processing": sum(1 for r in results if r.get("processed")) > 1,
                "results_sample": results[:3]
            },
            "steps_to_reproduce": [
                f"1. Prepare {concurrent_requests} identical requests",
                f"2. Send them simultaneously to {url}",
                f"3. Action: {action}",
                f"4. Observe inconsistent state",
                f"5. Confirm race condition vulnerability"
            ],
            "impact": "Attacker can bypass limits, duplicate transactions, or corrupt data",
            "remediation": "Implement proper locking mechanisms and atomic operations",
            "timestamp": datetime.now().isoformat()
        }
        
        self.pocs.append(poc)
        return poc
    
    def save_evidence(self, name: str, data: Any) -> str:
        """Save evidence file"""
        
        filepath = self.evidence_dir / f"{name}_{datetime.now().timestamp()}.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return str(filepath)
    
    def export_all_pocs(self, format: str = "json") -> str:
        """Export all PoCs"""
        
        if format == "json":
            filepath = self.evidence_dir / "all_pocs.json"
            with open(filepath, 'w') as f:
                json.dump(self.pocs, f, indent=2)
        
        elif format == "html":
            filepath = self.evidence_dir / "all_pocs.html"
            html = self._generate_html_report()
            with open(filepath, 'w') as f:
                f.write(html)
        
        return str(filepath)
    
    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        
        html = """
        <html>
        <head>
            <title>Vygoris PoC Report</title>
            <style>
                body { font-family: monospace; background: #0f1419; color: #00ff00; padding: 20px; }
                .poc { border: 1px solid #00ff00; margin: 10px 0; padding: 10px; }
                .critical { border-color: #ff0000; }
                .high { border-color: #ff9900; }
                .medium { border-color: #ffff00; }
                h2 { color: #00ffff; }
                code { background: #1a1f2e; padding: 5px; }
            </style>
        </head>
        <body>
            <h1>🔐 Vygoris PoC Report</h1>
        """
        
        for poc in self.pocs:
            severity_class = poc["severity"].lower()
            html += f"""
            <div class="poc {severity_class}">
                <h2>{poc['type']} - {poc['severity']} (CVSS {poc['cvss_score']})</h2>
                <p><strong>URL:</strong> {poc.get('url', 'N/A')}</p>
                <p><strong>Impact:</strong> {poc.get('impact', 'N/A')}</p>
                <p><strong>Remediation:</strong> {poc.get('remediation', 'N/A')}</p>
            </div>
            """
        
        html += "</body></html>"
        return html
    
    def get_pocs(self) -> List[Dict[str, Any]]:
        """Get all PoCs"""
        return self.pocs

# Test
if __name__ == "__main__":
    gen = PoC Generator()
    
    poc = gen.generate_sql_injection_poc(
        url="https://example.com/search",
        parameter="q",
        payload="' OR '1'='1",
        response="SQL error: syntax error",
        response_time=6.5
    )
    
    print("✅ PoC generated:")
    print(json.dumps(poc, indent=2))
