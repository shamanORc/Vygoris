"""Custom Business Rule Engine"""

from typing import Dict, Any, List

class BusinessRuleEngine:
    """Custom business rule engine for detecting logic flaws"""
    
    def __init__(self):
        self.rules = {}
        self.violations = []
    
    async def load_rules(self, rules_file: str) -> Dict[str, Any]:
        """Load custom business rules"""
        
        # Simulate loading rules
        rules = {
            "admin_only_access": "Only admin role can access /admin endpoints",
            "user_isolation": "Users can only access their own data",
            "state_consistency": "Order state must follow: pending -> processing -> completed",
            "rate_limit": "Max 100 requests per minute per user"
        }
        
        self.rules = rules
        return rules
    
    async def check_rules(self, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check if business rules are violated"""
        
        violations = []
        
        for rule_name, rule_desc in self.rules.items():
            if await self._check_rule(rule_name, context):
                violations.append({
                    "rule": rule_name,
                    "description": rule_desc,
                    "violated": True,
                    "severity": "HIGH"
                })
        
        self.violations = violations
        return violations
    
    async def _check_rule(self, rule_name: str, context: Dict[str, Any]) -> bool:
        """Check a specific rule"""
        
        # Simulate rule checking
        if rule_name == "admin_only_access":
            return context.get("role") != "admin" and context.get("endpoint", "").startswith("/admin")
        
        return False
