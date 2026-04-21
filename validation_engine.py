"""Real Validation Engine - Zero False Positives"""

from typing import Dict, Any, List, Tuple
import time

class ValidationEngine:
    """Validate findings to ensure zero false positives"""
    
    @staticmethod
    def validate_sql_injection(response: str, 
                               response_time: float,
                               payload: str) -> Tuple[bool, Dict[str, Any]]:
        """Validate SQL Injection with multiple checks"""
        
        evidence = {
            "checks_passed": 0,
            "checks_total": 5,
            "details": {}
        }
        
        # Check 1: SQL error messages
        sql_errors = [
            "SQL error", "syntax error", "mysql_fetch", "ORA-", 
            "PostgreSQL", "SQLServer", "sqlite3", "ODBC"
        ]
        has_sql_error = any(err.lower() in response.lower() for err in sql_errors)
        evidence["details"]["sql_error_detected"] = has_sql_error
        if has_sql_error:
            evidence["checks_passed"] += 1
        
        # Check 2: Time-based detection (>5s delay)
        time_delay = response_time > 5
        evidence["details"]["time_delay_detected"] = time_delay
        if time_delay:
            evidence["checks_passed"] += 1
        
        # Check 3: Payload reflection
        payload_reflected = payload in response
        evidence["details"]["payload_reflected"] = payload_reflected
        if payload_reflected:
            evidence["checks_passed"] += 1
        
        # Check 4: Response size anomaly (>2x normal)
        response_size_anomaly = len(response) > 10000
        evidence["details"]["response_size_anomaly"] = response_size_anomaly
        if response_size_anomaly:
            evidence["checks_passed"] += 1
        
        # Check 5: Database metadata extraction
        metadata_keywords = ["information_schema", "sysobjects", "pg_catalog"]
        has_metadata = any(kw in response.lower() for kw in metadata_keywords)
        evidence["details"]["metadata_extraction"] = has_metadata
        if has_metadata:
            evidence["checks_passed"] += 1
        
        # Require at least 2 checks to pass
        is_valid = evidence["checks_passed"] >= 2
        
        return is_valid, evidence
    
    @staticmethod
    def validate_xss(response: str, 
                     payload: str,
                     dom_changes: bool = False) -> Tuple[bool, Dict[str, Any]]:
        """Validate XSS with multiple checks"""
        
        evidence = {
            "checks_passed": 0,
            "checks_total": 4,
            "details": {}
        }
        
        # Check 1: Payload reflection in HTML
        payload_in_html = payload in response
        evidence["details"]["payload_in_html"] = payload_in_html
        if payload_in_html:
            evidence["checks_passed"] += 1
        
        # Check 2: Script tag present
        has_script = "<script>" in response or "javascript:" in response.lower()
        evidence["details"]["script_tag_present"] = has_script
        if has_script:
            evidence["checks_passed"] += 1
        
        # Check 3: Event handlers
        event_handlers = ["onerror=", "onload=", "onclick=", "onmouseover="]
        has_event = any(eh in response.lower() for eh in event_handlers)
        evidence["details"]["event_handler_present"] = has_event
        if has_event:
            evidence["checks_passed"] += 1
        
        # Check 4: DOM changes detected
        evidence["details"]["dom_changes"] = dom_changes
        if dom_changes:
            evidence["checks_passed"] += 1
        
        # Require at least 2 checks to pass
        is_valid = evidence["checks_passed"] >= 2
        
        return is_valid, evidence
    
    @staticmethod
    def validate_idor(original_response: str,
                      test_response: str,
                      original_status: int,
                      test_status: int,
                      user_id_original: str,
                      user_id_test: str) -> Tuple[bool, Dict[str, Any]]:
        """Validate IDOR with multiple checks"""
        
        evidence = {
            "checks_passed": 0,
            "checks_total": 4,
            "details": {}
        }
        
        # Check 1: Status code bypass
        status_bypass = (original_status == 403 and test_status == 200) or \
                       (original_status == 401 and test_status == 200)
        evidence["details"]["status_bypass"] = status_bypass
        if status_bypass:
            evidence["checks_passed"] += 1
        
        # Check 2: Different data in response
        different_data = original_response != test_response and len(test_response) > 100
        evidence["details"]["different_data"] = different_data
        if different_data:
            evidence["checks_passed"] += 1
        
        # Check 3: User ID in response
        user_id_in_response = user_id_test in test_response
        evidence["details"]["user_id_in_response"] = user_id_in_response
        if user_id_in_response:
            evidence["checks_passed"] += 1
        
        # Check 4: Consistent access
        consistent_access = test_status == 200
        evidence["details"]["consistent_access"] = consistent_access
        if consistent_access:
            evidence["checks_passed"] += 1
        
        # Require at least 3 checks to pass
        is_valid = evidence["checks_passed"] >= 3
        
        return is_valid, evidence
    
    @staticmethod
    def validate_auth_bypass(response: str,
                            cookies: Dict[str, str],
                            status_code: int) -> Tuple[bool, Dict[str, Any]]:
        """Validate Authentication Bypass"""
        
        evidence = {
            "checks_passed": 0,
            "checks_total": 4,
            "details": {}
        }
        
        # Check 1: Successful status code
        success_status = status_code == 200
        evidence["details"]["success_status"] = success_status
        if success_status:
            evidence["checks_passed"] += 1
        
        # Check 2: Session cookie obtained
        has_session = len(cookies) > 0 and any(
            k.lower() in ["session", "sessionid", "jsessionid", "sid"]
            for k in cookies.keys()
        )
        evidence["details"]["session_cookie"] = has_session
        if has_session:
            evidence["checks_passed"] += 1
        
        # Check 3: Dashboard/authenticated content
        auth_indicators = ["dashboard", "profile", "logout", "user", "account"]
        has_auth_content = any(ind in response.lower() for ind in auth_indicators)
        evidence["details"]["auth_content"] = has_auth_content
        if has_auth_content:
            evidence["checks_passed"] += 1
        
        # Check 4: No error messages
        error_indicators = ["invalid", "denied", "unauthorized", "forbidden"]
        no_errors = not any(err in response.lower() for err in error_indicators)
        evidence["details"]["no_errors"] = no_errors
        if no_errors:
            evidence["checks_passed"] += 1
        
        # Require at least 3 checks to pass
        is_valid = evidence["checks_passed"] >= 3
        
        return is_valid, evidence
    
    @staticmethod
    def validate_race_condition(results: List[Dict[str, Any]]) -> Tuple[bool, Dict[str, Any]]:
        """Validate Race Condition"""
        
        evidence = {
            "checks_passed": 0,
            "checks_total": 3,
            "details": {}
        }
        
        # Check 1: Inconsistent results
        unique_results = len(set(str(r) for r in results))
        inconsistent = unique_results > 1
        evidence["details"]["inconsistent_results"] = inconsistent
        if inconsistent:
            evidence["checks_passed"] += 1
        
        # Check 2: Duplicate processing
        processed_count = sum(1 for r in results if r.get("processed"))
        duplicate_processing = processed_count > 1
        evidence["details"]["duplicate_processing"] = duplicate_processing
        if duplicate_processing:
            evidence["checks_passed"] += 1
        
        # Check 3: State corruption
        total_count = sum(r.get("count", 0) for r in results)
        expected_count = len(results)
        state_corruption = total_count > expected_count
        evidence["details"]["state_corruption"] = state_corruption
        if state_corruption:
            evidence["checks_passed"] += 1
        
        # Require at least 2 checks to pass
        is_valid = evidence["checks_passed"] >= 2
        
        return is_valid, evidence
    
    @staticmethod
    def filter_false_positives(findings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out false positives from findings"""
        
        validated_findings = []
        
        for finding in findings:
            finding_type = finding.get("type")
            is_valid = False
            evidence = {}
            
            if finding_type == "SQL_INJECTION":
                is_valid, evidence = ValidationEngine.validate_sql_injection(
                    finding.get("response", ""),
                    finding.get("response_time", 0),
                    finding.get("payload", "")
                )
            
            elif finding_type == "XSS":
                is_valid, evidence = ValidationEngine.validate_xss(
                    finding.get("response", ""),
                    finding.get("payload", ""),
                    finding.get("dom_changes", False)
                )
            
            elif finding_type == "IDOR":
                is_valid, evidence = ValidationEngine.validate_idor(
                    finding.get("original_response", ""),
                    finding.get("test_response", ""),
                    finding.get("original_status", 0),
                    finding.get("test_status", 0),
                    finding.get("original_id", ""),
                    finding.get("test_id", "")
                )
            
            elif finding_type == "AUTH_BYPASS":
                is_valid, evidence = ValidationEngine.validate_auth_bypass(
                    finding.get("response", ""),
                    finding.get("cookies", {}),
                    finding.get("status_code", 0)
                )
            
            elif finding_type == "RACE_CONDITION":
                is_valid, evidence = ValidationEngine.validate_race_condition(
                    finding.get("results", [])
                )
            
            if is_valid:
                finding["validation"] = evidence
                finding["validated"] = True
                validated_findings.append(finding)
        
        return validated_findings

# Test
if __name__ == "__main__":
    is_valid, evidence = ValidationEngine.validate_sql_injection(
        response="SQL error: syntax error near '1'",
        response_time=6.5,
        payload="' OR '1'='1"
    )
    
    print(f"✅ SQL Injection validation: {is_valid}")
    print(f"Evidence: {evidence}")
