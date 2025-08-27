import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from datetime import datetime, timedelta
from typing import List, Dict
import json
from constants import TIME_SLOT_INTERVAL, WORKING_DAYS, MAX_BOOKING_DAYS, SHOP_INFO, SHEET_CONFIG

class SchedulerService:
    def __init__(self):
        self.gc = None
        self.sheet = None
        self._initialize_google_sheets()
    
    def _initialize_google_sheets(self):
        """Initialize Google Sheets connection"""
        try:
            # Set up credentials
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            credentials_json = os.getenv('GOOGLE_SHEETS_CREDENTIALS_JSON')
            if credentials_json:
                # Try to parse as JSON string first
                try:
                    credentials_dict = json.loads(credentials_json)
                    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
                except json.JSONDecodeError:
                    # If it's not JSON, treat as file path (backward compatibility)
                    if os.path.exists(credentials_json):
                        creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_json, scope)
                    else:
                        raise Exception("Invalid credentials format")
                
                self.gc = gspread.authorize(creds)
                
                # Open the spreadsheet
                sheet_id = os.getenv('GOOGLE_SHEET_ID')
                if sheet_id:
                    self.sheet = self.gc.open_by_key(sheet_id).sheet1
                    print("Google Sheets connection established successfully!")
                else:
                    print("Warning: GOOGLE_SHEET_ID not found in environment variables.")
            else:
                print("Warning: Google Sheets credentials not found. Using mock data.")
                
        except Exception as e:
            print(f"Error initializing Google Sheets: {e}")
            print("Using mock data for development.")
    
    async def get_available_slots(self, date_str: str, duration_minutes: int) -> List[str]:
        """Get available time slots for a specific date"""
        try:
            # Parse date
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Check if date is within booking range
            today = datetime.now().date()
            if date < today or date > today + timedelta(days=MAX_BOOKING_DAYS):
                return []
            
            # Check if it's a working day
            if date.weekday() not in WORKING_DAYS:
                return []
            
            if self.sheet:
                return await self._get_slots_from_sheet(date, duration_minutes)
            else:
                # Mock data for development
                return self._get_mock_slots(date, duration_minutes)
                
        except Exception as e:
            print(f"Error getting available slots: {e}")
            return []
    
    async def _get_slots_from_sheet(self, date, duration_minutes: int) -> List[str]:
        """Get available slots from Google Sheets"""
        try:
            # Find the date column
            date_str = date.strftime("%d/%m")
            all_values = self.sheet.get_all_values()
            
            date_col = None
            for col_idx, cell in enumerate(all_values[0]):
                if cell == date_str:
                    date_col = col_idx
                    break
            
            if date_col is None:
                return []
            
            # Get start and end times from configured rows
            start_time = all_values[SHEET_CONFIG["start_time_row"]-1][date_col] if len(all_values) > SHEET_CONFIG["start_time_row"]-1 else SHOP_INFO["working_hours"]["start"]
            end_time = all_values[SHEET_CONFIG["end_time_row"]-1][date_col] if len(all_values) > SHEET_CONFIG["end_time_row"]-1 else SHOP_INFO["working_hours"]["end"]
            
            # Generate time slots
            available_slots = []
            current_time = datetime.strptime(start_time, "%H:%M")
            end_datetime = datetime.strptime(end_time, "%H:%M")
            
            while current_time + timedelta(minutes=duration_minutes) <= end_datetime:
                time_str = current_time.strftime("%H:%M")
                
                # Check if slot is available (empty in sheet)
                # Find the row for this time
                time_row = None
                for row_idx, row in enumerate(all_values[SHEET_CONFIG["first_time_slot_row"]-1:], start=SHEET_CONFIG["first_time_slot_row"]):
                    if len(row) > SHEET_CONFIG["time_column"] and row[SHEET_CONFIG["time_column"]] == time_str:
                        time_row = row_idx
                        break
                
                if time_row is None or len(all_values[time_row]) <= date_col or not all_values[time_row][date_col]:
                    # Check if we have enough consecutive slots
                    slots_needed = duration_minutes // TIME_SLOT_INTERVAL
                    available = True
                    
                    for i in range(slots_needed):
                        check_time = current_time + timedelta(minutes=i * TIME_SLOT_INTERVAL)
                        check_time_str = check_time.strftime("%H:%M")
                        
                        check_row = None
                        for row_idx, row in enumerate(all_values[3:], start=3):
                            if len(row) > 0 and row[0] == check_time_str:
                                check_row = row_idx
                                break
                        
                        if check_row and len(all_values[check_row]) > date_col and all_values[check_row][date_col]:
                            available = False
                            break
                    
                    if available:
                        available_slots.append(time_str)
                
                current_time += timedelta(minutes=TIME_SLOT_INTERVAL)
            
            return available_slots
            
        except Exception as e:
            print(f"Error getting slots from sheet: {e}")
            return []
    
    def _get_mock_slots(self, date, duration_minutes: int) -> List[str]:
        """Generate mock available slots for development"""
        available_slots = []
        
        # Generate slots from 10:00 to 16:00 with some random unavailable slots
        current_time = datetime.strptime("10:00", "%H:%M")
        end_time = datetime.strptime("16:00", "%H:%M")
        
        # Mock some unavailable slots
        unavailable = ["11:30", "14:00", "15:15"]
        
        while current_time + timedelta(minutes=duration_minutes) <= end_time:
            time_str = current_time.strftime("%H:%M")
            
            if time_str not in unavailable:
                available_slots.append(time_str)
            
            current_time += timedelta(minutes=TIME_SLOT_INTERVAL)
        
        return available_slots
    
    async def book_appointment(self, date_str: str, time_str: str, duration_minutes: int, 
                             customer_name: str, customer_phone: str):
        """Book an appointment in Google Sheets"""
        try:
            if not self.sheet:
                print(f"Mock booking: {customer_name} on {date_str} at {time_str}")
                return True
            
            # Find the date column
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            date_display = date.strftime(SHEET_CONFIG["date_format"])
            
            all_values = self.sheet.get_all_values()
            date_col = None
            
            for col_idx, cell in enumerate(all_values[0]):
                if cell == date_display:
                    date_col = col_idx
                    break
            
            if date_col is None:
                raise Exception("Date column not found")
            
            # Find time rows and mark as booked
            slots_needed = duration_minutes // TIME_SLOT_INTERVAL
            current_time = datetime.strptime(time_str, "%H:%M")
            
            booking_info = f"{customer_name} ({customer_phone})"
            
            for i in range(slots_needed):
                slot_time = current_time + timedelta(minutes=i * TIME_SLOT_INTERVAL)
                slot_time_str = slot_time.strftime("%H:%M")
                
                # Find the row for this time slot
                for row_idx, row in enumerate(all_values[3:], start=4):  # Start from row 4 (index 3)
                    if len(row) > 0 and row[0] == slot_time_str:
                        # Update the cell
                        self.sheet.update_cell(row_idx, date_col + 1, booking_info)
                        break
            
            return True
            
        except Exception as e:
            print(f"Error booking appointment: {e}")
            raise Exception("Failed to book appointment")
