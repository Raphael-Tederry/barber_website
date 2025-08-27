# Services and their durations (in minutes)
SERVICES = {
    "haircut": {
        "name_en": "Hair Cut",
        "name_he": "תספורת",
        "duration": 30
    },
    "beard_trim": {
        "name_en": "Beard Trim", 
        "name_he": "עיצוב זקן",
        "duration": 15
    },
    "waxing": {
        "name_en": "Facial Waxing",
        "name_he": "שעווה לפנים", 
        "duration": 10
    }
}

# Shop Information
SHOP_INFO = {
    "name_en": "Elite Barbershop",
    "name_he": "ברברשופ עלית",
    "owner_name": "David Cohen",
    "address": {
        "street": "Dizengoff Street",
        "house_number": "125",
        "city": "Tel Aviv",
        "extra_specification": "First door to the left in the basement",
        "address_en": "125 Dizengoff Street, Tel Aviv - First door to the left in the basement",
        "address_he": "רחוב דיזנגוף 125, תל אביב - דלת ראשונה משמאל במרתף"
    },
    "contact": {
        "phone": "+972-50-123-4567",
        "email": "info@elitebarbershop.com"
    },
    "working_hours": {
        "start": "09:00",
        "end": "15:00"
    }
}

# Time slot interval in minutes
TIME_SLOT_INTERVAL = 15

# Days of the week the shop is open (0 = Monday, 6 = Sunday)
WORKING_DAYS = [0, 1, 2, 3, 4, 6]  # Monday to Friday + Sunday

# Maximum days ahead for booking
MAX_BOOKING_DAYS = 7

# Google Sheets Configuration
SHEET_CONFIG = {
    "date_row": 1,          # Row containing dates (20/08, 21/08, etc.)
    "start_time_row": 2,    # Row containing start times (09:00, 09:00, etc.)
    "end_time_row": 3,      # Row containing end times (15:00, 15:00, etc.)
    "first_time_slot_row": 4,  # First row with time slots (starts at row 4)
    "time_column": 0,       # Column A (index 0) contains time slots
    "first_date_column": 1, # Column B (index 1) is first date column
    "date_format": "%d/%m", # Format for dates in sheet (20/08)
    "time_format": "%H:%M"  # Format for times in sheet (09:00)
}
