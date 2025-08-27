# Elite Barbershop Website

A modern, bilingual (English/Hebrew) barbershop website with appointment scheduling system.

## Features

- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Bilingual Support**: Full Hebrew and English language support
- **Appointment Scheduling**: Integration with Google Sheets for schedule management
- **Email Confirmation**: Secure appointment confirmation via email
- **Professional UI**: Clean, modern design with smooth animations
- **Service Management**: Easy-to-modify service types and durations

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Scheduling**: Google Sheets API
- **Email**: Gmail SMTP
- **Styling**: Custom CSS with professional design

## Quick Setup

### 1. Run Setup Script (Windows)
```powershell
.\setup.ps1
```

### 2. Manual Setup

#### Create Virtual Environment
```bash
python -m venv .venv
```

#### Activate Virtual Environment
**Windows:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `env_example.txt` to `.env` and fill in your credentials:

```env
# Google Sheets API
GOOGLE_SHEETS_CREDENTIALS_JSON=path/to/your/credentials.json
GOOGLE_SHEET_ID=your_google_sheet_id

# Email Configuration  
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Application Settings
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### 4. Google Sheets Setup

✅ **API Credentials are already configured!**

**Create Schedule Spreadsheet:**

1. **Go to [Google Sheets](https://sheets.google.com) and create a new spreadsheet**
2. **Name it "Barbershop Schedule"**
3. **Set up this structure:**
   ```
   Row 1: (empty) | 20/08 | 21/08 | 22/08 | 23/08 | 24/08 | 25/08 | 26/08
   Row 2: Start   | 09:30 | 09:30 | 09:30 | 09:30 | 09:30 | 09:30 | 09:30
   Row 3: End     | 17:45 | 17:45 | 17:45 | 17:45 | 17:45 | 17:45 | 17:45
   Row 4: 09:30   | (empty cells for bookings)
   Row 5: 09:45   | (empty cells for bookings)
   Row 6: 10:00   | (empty cells for bookings)
   ... (continue every 15 minutes until 17:45)
   ```

4. **Share the spreadsheet:**
   - Click "Share" button
   - Add this email with "Editor" permission:
     ```
     backend-spreadsheets-bot@barbershop-spreadheets-gmail.iam.gserviceaccount.com
     ```
   - Uncheck "Notify people"

5. **Get Sheet ID from URL:**
   ```
   https://docs.google.com/spreadsheets/d/[COPY_THIS_PART]/edit
   ```

6. **Update .env file:**
   ```env
   GOOGLE_SHEET_ID=your_copied_sheet_id
   ```

### 5. Email Setup

For Gmail:
1. Enable 2-factor authentication
2. Generate app password
3. Use app password in `.env` file

## Running the Application

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start the server
python main.py
```

The application will be available at `http://localhost:8000`

## Project Structure

```
barber_website/
├── main.py                 # FastAPI application
├── constants.py           # Services, shop info, and constants
├── languages.py           # Bilingual text content
├── requirements.txt       # Python dependencies
├── services/
│   ├── scheduler.py       # Google Sheets integration
│   └── email_service.py   # Email functionality
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── products.html      # Products page
│   ├── contact.html       # Contact page
│   └── confirm.html       # Appointment confirmation
└── static/
    ├── css/style.css      # Main stylesheet
    ├── js/main.js         # JavaScript functionality
    └── images/            # Static images
```

## Customization

### Services
Edit `constants.py` to modify services:
```python
SERVICES = {
    "haircut": {
        "name_en": "Hair Cut",
        "name_he": "תספורת", 
        "duration": 30
    }
}
```

### Shop Information
Update shop details in `constants.py`:
```python
SHOP_INFO = {
    "name_en": "Your Barbershop",
    "owner_name": "Owner Name",
    "address": {...},
    "contact": {...}
}
```

### Languages
Modify text content in `languages.py`:
```python
TEXTS = {
    "en": {"nav_home": "Home", ...},
    "he": {"nav_home": "בית", ...}
}
```

## API Endpoints

- `GET /` - Home page
- `GET /products` - Products page  
- `GET /contact` - Contact page
- `GET /confirm` - Confirmation page
- `GET /api/available-slots` - Get available time slots
- `POST /api/book-appointment` - Book appointment
- `POST /api/confirm-appointment` - Confirm appointment

## Language Support

The website automatically detects language from URL parameter:
- English: `http://localhost:8000/?lang=en`
- Hebrew: `http://localhost:8000/?lang=he`

Language toggle is available in the navigation bar.

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use a production WSGI server like Gunicorn
3. Set up proper SSL certificates
4. Configure domain and DNS
5. Set up proper backup for Google Sheets

## Support

For questions or issues, contact the shop owner or check the documentation.

## License

Private project for Elite Barbershop.
