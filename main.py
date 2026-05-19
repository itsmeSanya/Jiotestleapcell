import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from playwright.sync_api import sync_playwright

app = FastAPI()

# Force immediate log output
os.environ["PYTHONUNBUFFERED"] = "1"

@app.get("/")
def home():
    return HTMLResponse("<h3>Cloud Bot Testing Endpoint</h3><p>Go to <code>/test</code> to trigger Playwright blindly.</p>")

@app.get("/test")
def test_bot():
    print("⚡ Incoming test request received. Initiating Playwright...")
    try:
        with sync_playwright() as p:
            print("🔧 Launching Chromium...")
            # Using the cloud-container friendly arguments we discovered
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--no-zygote"
                ]
            )
            
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            
            page = context.new_page()
            
            print("🌐 Navigating to JioMart Cart...")
            # 60 second explicit timeout fallback
            page.goto("https://www.jiomart.com/cart/bag", timeout=60000, wait_until="domcontentloaded")
            
            print("📑 Page loaded successfully. Extracting source HTML...")
            page_content = page.content()
            
            browser.close()
            print("✅ Test complete. Sending HTML response.")
            
            # Returns the raw text/HTML source directly to your web browser window
            return PlainTextResponse(page_content)
            
    except Exception as e:
        error_message = f"❌ CRITICAL SCRAPE ERROR: {str(e)}"
        print(error_message)
        return PlainTextResponse(error_message, status_code=500)
      
