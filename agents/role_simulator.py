"""Role Simulator Agent - Simulates multiple user roles and compares behaviors"""

import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class RoleSession:
    role: str
    session_id: str
    actions: List[Dict[str, Any]]
    responses: List[Dict[str, Any]]

class RoleSimulator:
    """Simulates different user roles and detects authorization issues"""
    
    def __init__(self):
        self.sessions = {}
        self.role_behaviors = {}
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute role simulation"""
        url = params.get("url")
        roles = params.get("roles", ["user", "admin", "guest"])
        
        print(f"[ROLE_SIMULATOR] Simulating roles: {roles}")
        
        # Create sessions for each role
        sessions = await self._create_role_sessions(url, roles)
        
        # Compare behaviors
        comparisons = await self._compare_role_behaviors(sessions)
        
        return {
            "status": "success",
            "roles_simulated": len(roles),
            "sessions": sessions,
            "comparisons": comparisons,
            "anomalies": await self._detect_anomalies(comparisons)
        }
    
    async def _create_role_sessions(self, url: str, roles: List[str]) -> Dict[str, RoleSession]:
        """Create isolated sessions for each role"""
        sessions = {}
        
        for role in roles:
            session_id = f"session_{role}_{id(self)}"
            
            print(f"[ROLE_SIMULATOR] Creating session for role: {role}")
            
            session = RoleSession(
                role=role,
                session_id=session_id,
                actions=[],
                responses=[]
            )
            
            # Simulate actions for each role
            actions = await self._simulate_role_actions(url, role)
            session.actions = actions
            
            # Get responses
            responses = await self._get_role_responses(url, role, actions)
            session.responses = responses
            
            sessions[role] = session
        
        return sessions
    
    async def _simulate_role_actions(self, url: str, role: str) -> List[Dict[str, Any]]:
        """Simulate actions for a specific role"""
        actions = [
            {"action": "view_dashboard", "endpoint": "/dashboard"},
            {"action": "view_users", "endpoint": "/api/users"},
            {"action": "delete_user", "endpoint": "/api/users/1", "method": "DELETE"},
            {"action": "modify_settings", "endpoint": "/api/settings", "method": "POST"},
            {"action": "access_admin", "endpoint": "/admin", "method": "GET"}
        ]
        
        # Filter actions based on role
        if role == "admin":
            return actions  # Admin can do everything
        elif role == "user":
            return actions[:2]  # User can only view
        else:  # guest
            return actions[:1]  # Guest can only view dashboard
    
    async def _get_role_responses(self, url: str, role: str, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get responses for role actions"""
        responses = []
        
        for action in actions:
            endpoint = action.get("endpoint")
            
            # Simulate response based on role and endpoint
            if role == "admin":
                status = 200
                data = {"success": True, "data": "Admin access granted"}
            elif role == "user":
                if "admin" in endpoint or "delete" in action.get("action", ""):
                    status = 403
                    data = {"error": "Forbidden"}
                else:
                    status = 200
                    data = {"success": True, "data": "User data"}
            else:  # guest
                status = 401
                data = {"error": "Unauthorized"}
            
            responses.append({
                "action": action.get("action"),
                "endpoint": endpoint,
                "status": status,
                "data": data
            })
        
        return responses
    
    async def _compare_role_behaviors(self, sessions: Dict[str, RoleSession]) -> List[Dict[str, Any]]:
        """Compare behaviors across roles"""
        comparisons = []
        
        # Get all unique endpoints
        all_endpoints = set()
        for session in sessions.values():
            for response in session.responses:
                all_endpoints.add(response.get("endpoint"))
        
        # Compare access for each endpoint
        for endpoint in all_endpoints:
            comparison = {
                "endpoint": endpoint,
                "access_by_role": {}
            }
            
            for role, session in sessions.items():
                for response in session.responses:
                    if response.get("endpoint") == endpoint:
                        comparison["access_by_role"][role] = response.get("status")
            
            comparisons.append(comparison)
        
        return comparisons
    
    async def _detect_anomalies(self, comparisons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect authorization anomalies"""
        anomalies = []
        
        for comparison in comparisons:
            endpoint = comparison.get("endpoint")
            access = comparison.get("access_by_role", {})
            
            # Check for inconsistent access
            statuses = list(access.values())
            
            # If guest has same access as admin, it's an anomaly
            if access.get("guest") == 200 and access.get("admin") == 200:
                anomalies.append({
                    "type": "excessive_guest_access",
                    "endpoint": endpoint,
                    "severity": "HIGH",
                    "description": f"Guest can access {endpoint} like an admin"
                })
            
            # If user can delete but admin cannot (unlikely)
            if access.get("user") == 200 and "delete" in endpoint and access.get("admin") != 200:
                anomalies.append({
                    "type": "privilege_escalation",
                    "endpoint": endpoint,
                    "severity": "CRITICAL",
                    "description": f"User can access {endpoint} but admin cannot"
                })
        
        return anomalies
