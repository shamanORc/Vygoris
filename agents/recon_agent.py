"""Reconnaissance Agent - Crawls target and discovers pages/forms/endpoints"""

import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class Page:
    url: str
    title: str
    forms: List[Dict[str, Any]]
    links: List[str]
    endpoints: List[str]

class ReconAgent:
    """Reconnaissance agent for crawling and discovery"""
    
    def __init__(self):
        self.discovered_pages = []
        self.discovered_forms = []
        self.discovered_endpoints = []
    
    async def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute reconnaissance"""
        url = params.get("url")
        max_pages = params.get("max_pages", 100)
        
        print(f"[RECON] Crawling {url}")
        print(f"[RECON] Max pages: {max_pages}")
        
        # Simulate crawling
        pages = await self._crawl_target(url, max_pages)
        
        return {
            "status": "success",
            "pages_discovered": len(pages),
            "pages": pages,
            "forms_found": len(self.discovered_forms),
            "endpoints_found": len(self.discovered_endpoints)
        }
    
    async def _crawl_target(self, url: str, max_pages: int) -> List[Page]:
        """Crawl target website"""
        pages = []
        
        # Simulate discovering pages
        discovered_urls = [
            url,
            f"{url}/dashboard",
            f"{url}/admin",
            f"{url}/api/users",
            f"{url}/api/products",
            f"{url}/settings",
            f"{url}/profile"
        ]
        
        for page_url in discovered_urls[:max_pages]:
            page = Page(
                url=page_url,
                title=f"Page: {page_url}",
                forms=await self._extract_forms(page_url),
                links=await self._extract_links(page_url),
                endpoints=await self._extract_endpoints(page_url)
            )
            pages.append(page)
            self.discovered_pages.append(page)
        
        return pages
    
    async def _extract_forms(self, url: str) -> List[Dict[str, Any]]:
        """Extract forms from page"""
        forms = []
        
        if "login" in url or "admin" in url:
            forms.append({
                "method": "POST",
                "action": "/login",
                "fields": ["username", "password"]
            })
        
        if "api" in url:
            forms.append({
                "method": "POST",
                "action": "/api/create",
                "fields": ["data", "user_id"]
            })
        
        self.discovered_forms.extend(forms)
        return forms
    
    async def _extract_links(self, url: str) -> List[str]:
        """Extract links from page"""
        return [
            f"{url}/page1",
            f"{url}/page2",
            f"{url}/page3"
        ]
    
    async def _extract_endpoints(self, url: str) -> List[str]:
        """Extract API endpoints"""
        endpoints = [
            "/api/users",
            "/api/products",
            "/api/orders",
            "/api/admin/settings"
        ]
        self.discovered_endpoints.extend(endpoints)
        return endpoints
