"""Multi-Agent Orchestrator - Coordinates all agents in ReAct framework"""

import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import json

class AgentState(Enum):
    """Agent execution states"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class AgentTask:
    """Task for agents to execute"""
    id: str
    name: str
    description: str
    agent_type: str
    params: Dict[str, Any]
    dependencies: List[str] = None

class MultiAgentOrchestrator:
    """Orchestrates multi-agent system with ReAct framework"""
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.agents = {}
        self.task_queue = []
        self.results = {}
        self.state = AgentState.IDLE
    
    def register_agent(self, agent_type: str, agent_instance):
        """Register an agent"""
        self.agents[agent_type] = agent_instance
        print(f"[ORCHESTRATOR] Registered agent: {agent_type}")
    
    def create_task(self, name: str, agent_type: str, params: Dict[str, Any], 
                   dependencies: List[str] = None) -> AgentTask:
        """Create a task for an agent"""
        task_id = f"task_{len(self.task_queue)}"
        task = AgentTask(
            id=task_id,
            name=name,
            description=f"Execute {agent_type} with params {params}",
            agent_type=agent_type,
            params=params,
            dependencies=dependencies or []
        )
        self.task_queue.append(task)
        return task
    
    async def execute_workflow(self, target_url: str, mode: str = "nuclear") -> Dict[str, Any]:
        """Execute complete scanning workflow"""
        print(f"\n[ORCHESTRATOR] Starting {mode.upper()} workflow")
        print(f"[ORCHESTRATOR] Target: {target_url}\n")
        
        # Phase 1: Reconnaissance
        print("[ORCHESTRATOR] Phase 1: Reconnaissance")
        recon_task = self.create_task(
            "Reconnaissance",
            "recon",
            {"url": target_url, "max_pages": 100}
        )
        recon_results = await self._execute_task(recon_task)
        
        # Phase 2: Role Simulation
        print("\n[ORCHESTRATOR] Phase 2: Role Simulation")
        role_task = self.create_task(
            "Role Simulation",
            "role_simulator",
            {"url": target_url, "roles": ["user", "admin", "guest"]},
            dependencies=[recon_task.id]
        )
        role_results = await self._execute_task(role_task)
        
        # Phase 3: Logic Reasoning
        print("\n[ORCHESTRATOR] Phase 3: Logic Reasoning")
        reasoning_task = self.create_task(
            "Logic Reasoning",
            "logic_reasoner",
            {"crawl_data": recon_results, "role_data": role_results},
            dependencies=[recon_task.id, role_task.id]
        )
        reasoning_results = await self._execute_task(reasoning_task)
        
        # Phase 4: Validation & Exploitation
        print("\n[ORCHESTRATOR] Phase 4: Validation & Exploitation")
        validation_task = self.create_task(
            "Validation & Exploitation",
            "validator_exploiter",
            {"findings": reasoning_results},
            dependencies=[reasoning_task.id]
        )
        validation_results = await self._execute_task(validation_task)
        
        # Phase 5: Triage & Reporting
        print("\n[ORCHESTRATOR] Phase 5: Triage & Reporting")
        triage_task = self.create_task(
            "Triage & Reporting",
            "triage_reporter",
            {"findings": validation_results},
            dependencies=[validation_task.id]
        )
        final_results = await self._execute_task(triage_task)
        
        print("\n[ORCHESTRATOR] Workflow completed!")
        return final_results
    
    async def _execute_task(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a single task"""
        agent = self.agents.get(task.agent_type)
        if not agent:
            raise ValueError(f"Agent {task.agent_type} not registered")
        
        print(f"[{task.agent_type.upper()}] Executing: {task.name}")
        
        # Execute agent
        result = await agent.execute(task.params)
        self.results[task.id] = result
        
        print(f"[{task.agent_type.upper()}] Completed: {task.name}")
        return result
    
    def get_results(self) -> Dict[str, Any]:
        """Get all results"""
        return self.results
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate final report from all agent results"""
        return {
            "status": "completed",
            "agents_executed": len(self.results),
            "findings": self.results.get("triage_reporter", {}).get("findings", []),
            "summary": self._generate_summary()
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate summary of findings"""
        findings = self.results.get("triage_reporter", {}).get("findings", [])
        
        severity_count = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }
        
        for finding in findings:
            severity = finding.get("severity", "LOW")
            if severity in severity_count:
                severity_count[severity] += 1
        
        return {
            "total_findings": len(findings),
            "by_severity": severity_count,
            "critical_count": severity_count["CRITICAL"],
            "high_count": severity_count["HIGH"]
        }
