"""Race Condition Detector - Detects timing-based vulnerabilities"""

from typing import Dict, Any, List
import asyncio

class RaceConditionDetector:
    """Detects race conditions and timing attacks"""
    
    def __init__(self):
        self.race_conditions = []
    
    async def detect_race_conditions(self, endpoint: str, concurrent_requests: int = 10) -> List[Dict[str, Any]]:
        """Detect race conditions through concurrent requests"""
        
        tasks = []
        
        for i in range(concurrent_requests):
            task = asyncio.create_task(self._make_request(endpoint, i))
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks)
        
        # Analyze responses for inconsistencies
        race_conditions = await self._analyze_responses(responses)
        
        self.race_conditions.extend(race_conditions)
        
        return race_conditions
    
    async def _make_request(self, endpoint: str, request_id: int) -> Dict[str, Any]:
        """Make a request"""
        
        # Simulate request
        await asyncio.sleep(0.01)
        
        return {
            "request_id": request_id,
            "endpoint": endpoint,
            "status": 200,
            "response_time": 50 + (request_id * 10)
        }
    
    async def _analyze_responses(self, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze responses for race conditions"""
        
        race_conditions = []
        
        # Check for timing inconsistencies
        response_times = [r.get("response_time", 0) for r in responses]
        avg_time = sum(response_times) / len(response_times) if response_times else 0
        
        for response in responses:
            time_diff = abs(response.get("response_time", 0) - avg_time)
            
            if time_diff > avg_time * 0.5:  # 50% variance
                race_conditions.append({
                    "type": "timing_variance",
                    "severity": "MEDIUM",
                    "request_id": response.get("request_id"),
                    "response_time": response.get("response_time"),
                    "avg_time": avg_time
                })
        
        return race_conditions
