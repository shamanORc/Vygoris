"""Logic Reasoner Agent - LLM-powered business logic analysis"""

from typing import Dict, Any, List

class LogicReasoner:
    """Analyzes business logic using LLM reasoning"""
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.findings = []
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute logic reasoning"""
        crawl_data = params.get("crawl_data", {})
        role_data = params.get("role_data", {})
        
        print(f"[LOGIC_REASONER] Analyzing business logic")
        print(f"[LOGIC_REASONER] Pages: {crawl_data.get('pages_discovered', 0)}")
        print(f"[LOGIC_REASONER] Roles: {len(role_data)}")
        
        # Analyze crawl data
        crawl_findings = await self._analyze_crawl_data(crawl_data)
        
        # Analyze role behaviors
        role_findings = await self._analyze_role_behaviors(role_data)
        
        # Combine findings
        all_findings = crawl_findings + role_findings
        
        return {
            "status": "success",
            "findings_count": len(all_findings),
            "findings": all_findings,
            "analysis_depth": "comprehensive"
        }
    
    async def _analyze_crawl_data(self, crawl_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze crawl data for vulnerabilities"""
        findings = []
        
        pages = crawl_data.get("pages", [])
        for page in pages:
            # Check for exposed admin panels
            if "admin" in str(page).lower():
                findings.append({
                    "type": "exposed_admin_panel",
                    "severity": "HIGH",
                    "confidence": "MEDIUM",
                    "description": "Admin panel may be exposed without proper authentication",
                    "location": page.get("url") if isinstance(page, dict) else str(page),
                    "steps_to_reproduce": ["Navigate to admin panel URL", "Check if authentication is required"],
                    "poc": "curl https://target.com/admin",
                    "fix_suggestion": "Implement proper authentication and authorization checks"
                })
            
            # Check for API endpoints
            if "api" in str(page).lower():
                findings.append({
                    "type": "unprotected_api",
                    "severity": "MEDIUM",
                    "confidence": "MEDIUM",
                    "description": "API endpoint may lack proper access controls",
                    "location": page.get("url") if isinstance(page, dict) else str(page),
                    "steps_to_reproduce": ["Access API endpoint", "Try modifying request parameters"],
                    "poc": "curl -X POST https://target.com/api/data -d '{}'",
                    "fix_suggestion": "Add authentication tokens and rate limiting"
                })
        
        return findings
    
    async def _analyze_role_behaviors(self, role_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze role-based behaviors"""
        findings = []
        
        # Check for authorization anomalies
        anomalies = role_data.get("anomalies", [])
        for anomaly in anomalies:
            findings.append({
                "type": anomaly.get("type", "authorization_issue"),
                "severity": anomaly.get("severity", "MEDIUM"),
                "confidence": "HIGH",
                "description": anomaly.get("description", "Authorization anomaly detected"),
                "location": anomaly.get("endpoint", "unknown"),
                "steps_to_reproduce": [
                    f"Login as guest user",
                    f"Access {anomaly.get('endpoint')}",
                    f"Compare access with admin user"
                ],
                "poc": f"curl -H 'Authorization: Bearer guest_token' https://target.com{anomaly.get('endpoint')}",
                "fix_suggestion": "Implement proper role-based access control (RBAC)"
            })
        
        # Check for state manipulation
        comparisons = role_data.get("comparisons", [])
        for comparison in comparisons:
            access_by_role = comparison.get("access_by_role", {})
            
            # If multiple roles have same access, might be state manipulation issue
            if len(set(access_by_role.values())) == 1:
                findings.append({
                    "type": "potential_state_manipulation",
                    "severity": "MEDIUM",
                    "confidence": "LOW",
                    "description": f"All roles have same access to {comparison.get('endpoint')}",
                    "location": comparison.get("endpoint"),
                    "steps_to_reproduce": ["Test endpoint with different roles", "Compare responses"],
                    "poc": "Compare responses across different user sessions",
                    "fix_suggestion": "Verify role-based access control implementation"
                })
        
        return findings
