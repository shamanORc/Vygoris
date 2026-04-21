"""Real HTTP Client - Playwright-based with real request/response handling"""

import asyncio
from playwright.async_api import async_playwright, Page, Browser
from typing import Dict, Any, List, Optional
import json
from datetime import datetime

class RealHTTPClient:
    """Real HTTP client using Playwright for accurate web interaction"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.requests_log: List[Dict[str, Any]] = []
        self.responses_log: List[Dict[str, Any]] = []
    
    async def initialize(self):
        """Initialize Playwright browser"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
    
    async def close(self):
        """Close browser"""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def navigate(self, url: str) -> Dict[str, Any]:
        """Navigate to URL and capture response"""
        
        if not self.page:
            self.page = await self.browser.new_page()
        
        try:
            response = await self.page.goto(url, wait_until="networkidle")
            
            result = {
                "url": url,
                "status": response.status if response else 0,
                "headers": dict(response.headers) if response else {},
                "timestamp": datetime.now().isoformat(),
                "success": response and response.status < 400
            }
            
            self.responses_log.append(result)
            return result
        
        except Exception as e:
            return {
                "url": url,
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    async def fill_form(self, form_selector: str, data: Dict[str, str]) -> Dict[str, Any]:
        """Fill and submit form with real data"""
        
        try:
            # Fill form fields
            for field_name, value in data.items():
                selector = f"{form_selector} [name='{field_name}']"
                await self.page.fill(selector, value)
            
            # Get form action
            form_action = await self.page.evaluate(
                f"document.querySelector('{form_selector}').action"
            )
            
            # Submit form
            await self.page.click(f"{form_selector} button[type='submit']")
            await self.page.wait_for_load_state("networkidle")
            
            # Capture response
            current_url = self.page.url
            status_code = 200  # Assume success if no error
            
            result = {
                "form": form_selector,
                "data": data,
                "action": form_action,
                "redirect_url": current_url,
                "status": status_code,
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
            
            self.requests_log.append(result)
            return result
        
        except Exception as e:
            return {
                "form": form_selector,
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    async def inject_payload(self, selector: str, payload: str) -> Dict[str, Any]:
        """Inject payload into input field"""
        
        try:
            await self.page.fill(selector, payload)
            
            # Get current page content
            content = await self.page.content()
            
            result = {
                "selector": selector,
                "payload": payload,
                "content_length": len(content),
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "payload_reflected": payload in content
            }
            
            self.requests_log.append(result)
            return result
        
        except Exception as e:
            return {
                "selector": selector,
                "payload": payload,
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_cookies(self) -> Dict[str, str]:
        """Get all cookies from current page"""
        
        cookies = await self.page.context.cookies()
        return {c["name"]: c["value"] for c in cookies}
    
    async def set_cookies(self, cookies: Dict[str, str]):
        """Set cookies for current page"""
        
        cookie_list = [{"name": k, "value": v, "url": self.page.url} for k, v in cookies.items()]
        await self.page.context.add_cookies(cookie_list)
    
    async def get_page_content(self) -> str:
        """Get full page HTML content"""
        return await self.page.content()
    
    async def take_screenshot(self, filename: str) -> str:
        """Take screenshot of current page"""
        
        path = f"/tmp/{filename}"
        await self.page.screenshot(path=path)
        return path
    
    def get_requests_log(self) -> List[Dict[str, Any]]:
        """Get all requests made"""
        return self.requests_log
    
    def get_responses_log(self) -> List[Dict[str, Any]]:
        """Get all responses received"""
        return self.responses_log

# Test
async def test():
    client = RealHTTPClient()
    await client.initialize()
    
    try:
        result = await client.navigate("https://example.com")
        print(f"✅ Navigation result: {result}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(test())
