#!/usr/bin/env python3
"""
Google Sheets Setup Helper for Barbershop Website

This script helps you create and configure the Google Sheet for appointment scheduling.
"""

import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_sheet_structure():
    """Create the basic structure for the scheduling sheet"""
    print("📊 Google Sheets Setup Instructions")
    print("=" * 50)
    
    # Get service account email
    try:
        creds_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON')
        if creds_json:
            creds = json.loads(creds_json)
            service_email = creds.get('client_email')
            print(f"✅ Service Account Email: {service_email}")
        else:
            print("❌ No credentials found in environment")
            return
    except Exception as e:
        print(f"❌ Error parsing credentials: {e}")
        return
    
    print("\n📋 Steps to set up your Google Sheet:")
    print("1. Go to https://sheets.google.com")
    print("2. Create a new spreadsheet")
    print("3. Name it 'Barbershop Schedule'")
    
    print("\n📅 Sheet Structure:")
    print("Set up your sheet with this structure:")
    
    # Generate dates for the next week
    today = datetime.now()
    dates = []
    for i in range(7):
        date = today + timedelta(days=i)
        dates.append(date.strftime("%d/%m"))
    
    print("\nRow 1 (Dates):")
    print("A1: (empty)  ", end="")
    for i, date in enumerate(dates, 1):
        print(f"  {chr(65+i)}1: {date}", end="")
    print()
    
    print("\nRow 2 (Start Times):")
    print("A2: Start    ", end="")
    for i in range(7):
        print(f"  {chr(66+i)}2: 09:30", end="")
    print()
    
    print("\nRow 3 (End Times):")
    print("A3: End      ", end="")
    for i in range(7):
        print(f"  {chr(66+i)}3: 17:45", end="")
    print()
    
    print("\nRows 4+ (Time Slots):")
    print("A4: 09:30, A5: 09:45, A6: 10:00, etc. (every 15 minutes)")
    print("Leave other columns empty for bookings")
    
    print(f"\n🔐 Share Settings:")
    print(f"4. Click 'Share' button")
    print(f"5. Add this email with 'Editor' permission:")
    print(f"   {service_email}")
    print("6. Make sure 'Notify people' is unchecked")
    
    print(f"\n🔗 Get Sheet ID:")
    print("7. Copy the URL of your sheet")
    print("8. Extract the Sheet ID from the URL:")
    print("   https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit")
    print("9. Update your .env file with:")
    print("   GOOGLE_SHEET_ID=your_actual_sheet_id")
    
    print(f"\n✅ Test Connection:")
    print("10. Run: python -c \"from services.scheduler import SchedulerService; SchedulerService()\"")
    
    print(f"\n📧 Email Setup:")
    print("For email functionality, you need to set up Gmail:")
    print("- Enable 2-Factor Authentication on your Gmail")
    print("- Generate an App Password (Google Account > Security > App passwords)")
    print("- Update .env with your email and app password")

if __name__ == "__main__":
    create_sheet_structure()
