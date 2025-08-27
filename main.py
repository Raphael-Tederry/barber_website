from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import os
from dotenv import load_dotenv
import uvicorn
from datetime import datetime, timedelta
import secrets
import string
from typing import Optional, List, Dict
import json
import signal
import sys

from services.scheduler import SchedulerService
from services.email_service import EmailService
from constants import SERVICES, SHOP_INFO
from languages import TEXTS

# Load environment variables
load_dotenv()

app = FastAPI(title="Elite Barbershop", description="Professional barbershop scheduling system")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Services
scheduler_service = SchedulerService()
email_service = EmailService()

# In-memory storage for pending confirmations (in production, use Redis or database)
pending_confirmations = {}

# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\n🔄 Shutting down gracefully...")
    print("✅ Barbershop website stopped.")
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, lang: str = "en"):
    """Main page with shop info and scheduling option"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "lang": lang,
        "texts": TEXTS[lang],
        "services": SERVICES,
        "shop_info": SHOP_INFO
    })

@app.get("/products", response_class=HTMLResponse) 
async def products(request: Request, lang: str = "en"):
    """Products page"""
    return templates.TemplateResponse("products.html", {
        "request": request,
        "lang": lang,
        "texts": TEXTS[lang],
        "shop_info": SHOP_INFO
    })

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request, lang: str = "en"):
    """Contact and location page"""
    return templates.TemplateResponse("contact.html", {
        "request": request, 
        "lang": lang,
        "texts": TEXTS[lang],
        "shop_info": SHOP_INFO
    })

@app.get("/api/available-slots")
async def get_available_slots(date: str, services: str):
    """Get available time slots for a specific date and services"""
    try:
        # Parse services
        selected_services = services.split(",")
        total_duration = sum(SERVICES[service]["duration"] for service in selected_services)
        
        # Get available slots from scheduler
        slots = await scheduler_service.get_available_slots(date, total_duration)
        
        return {"slots": slots}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/book-appointment")
async def book_appointment(
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    customer_phone: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    services: str = Form(...),
    lang: str = Form(default="en")
):
    """Book an appointment"""
    try:
        # Parse services
        selected_services = services.split(",")
        total_duration = sum(SERVICES[service]["duration"] for service in selected_services)
        
        # Generate confirmation code
        confirmation_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        
        # Store pending confirmation
        booking_id = secrets.token_urlsafe(16)
        pending_confirmations[booking_id] = {
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": customer_phone,
            "date": date,
            "time": time,
            "services": selected_services,
            "duration": total_duration,
            "confirmation_code": confirmation_code,
            "created_at": datetime.now(),
            "lang": lang
        }
        
        # Send confirmation email
        await email_service.send_confirmation_email(
            customer_email, customer_name, date, time, 
            selected_services, confirmation_code, lang
        )
        
        return {"success": True, "booking_id": booking_id, "message": "Confirmation email sent"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/confirm-appointment")
async def confirm_appointment(
    booking_id: str = Form(...),
    confirmation_code: str = Form(...)
):
    """Confirm appointment with code from email"""
    try:
        if booking_id not in pending_confirmations:
            raise HTTPException(status_code=404, detail="Booking not found")
            
        booking = pending_confirmations[booking_id]
        
        # Check if code matches
        if booking["confirmation_code"] != confirmation_code.upper():
            raise HTTPException(status_code=400, detail="Invalid confirmation code")
            
        # Check if not expired (30 minutes)
        if datetime.now() - booking["created_at"] > timedelta(minutes=30):
            del pending_confirmations[booking_id]
            raise HTTPException(status_code=400, detail="Confirmation code expired")
            
        # Book the appointment in Google Sheets
        await scheduler_service.book_appointment(
            booking["date"], booking["time"], booking["duration"],
            booking["customer_name"], booking["customer_phone"]
        )
        
        # Remove from pending
        del pending_confirmations[booking_id]
        
        return {"success": True, "message": "Appointment confirmed successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/confirm", response_class=HTMLResponse)
async def confirm_page(request: Request, booking_id: str, lang: str = "en"):
    """Confirmation page"""
    return templates.TemplateResponse("confirm.html", {
        "request": request,
        "booking_id": booking_id,
        "lang": lang,
        "texts": TEXTS[lang],
        "shop_info": SHOP_INFO
    })

if __name__ == "__main__":
    try:
        print("🚀 Starting Elite Barbershop website...")
        print("📍 Server: http://localhost:8000")
        print("⌨️  Press Ctrl+C to stop")
        print("-" * 40)
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    except KeyboardInterrupt:
        print("\n🔄 Shutting down gracefully...")
        print("✅ Barbershop website stopped.")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)
