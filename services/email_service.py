import smtplib
import os
import json
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
from constants import SERVICES, SHOP_INFO

# Optional OAuth 2.0 imports (will fallback to SMTP if not available)
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from googleapiclient.discovery import build
    OAUTH_AVAILABLE = True
except ImportError:
    OAUTH_AVAILABLE = False

class EmailService:
    def __init__(self):
        self.email = os.getenv('EMAIL_ADDRESS')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.oauth_credentials = os.getenv('GMAIL_OAUTH_CREDENTIALS')
        self.use_oauth = OAUTH_AVAILABLE and self.oauth_credentials and not self.password
    
    async def send_confirmation_email(self, customer_email: str, customer_name: str, 
                                    date: str, time: str, services: List[str], 
                                    confirmation_code: str, lang: str = "en"):
        """Send confirmation email to customer"""
        try:
            if not self.email:
                print(f"Mock email to {customer_email}: Confirmation code {confirmation_code}")
                return True
            
            if not self.password and not self.oauth_credentials:
                print(f"Mock email to {customer_email}: Confirmation code {confirmation_code}")
                print("⚠️  No email credentials configured!")
                return True
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = customer_email
            
            if lang == "he":
                msg['Subject'] = f"אישור תור - {SHOP_INFO['name_he']}"
                body = self._get_hebrew_email_body(customer_name, date, time, services, confirmation_code)
            else:
                msg['Subject'] = f"Appointment Confirmation - {SHOP_INFO['name_en']}"
                body = self._get_english_email_body(customer_name, date, time, services, confirmation_code)
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            print(f"Mock email to {customer_email}: Confirmation code {confirmation_code}")
            return True  # Don't fail the booking if email fails
    
    def _get_english_email_body(self, customer_name: str, date: str, time: str, 
                               services: List[str], confirmation_code: str) -> str:
        """Generate English email body"""
        services_text = ", ".join([SERVICES[service]["name_en"] for service in services])
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Appointment Confirmation</h2>
                
                <p>Dear {customer_name},</p>
                
                <p>Thank you for booking an appointment with <strong>{SHOP_INFO['name_en']}</strong>!</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2c3e50;">Appointment Details:</h3>
                    <p><strong>Date:</strong> {date}</p>
                    <p><strong>Time:</strong> {time}</p>
                    <p><strong>Services:</strong> {services_text}</p>
                </div>
                
                <div style="background-color: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <h3 style="margin-top: 0; color: #27ae60;">Confirmation Required</h3>
                    <p>To confirm your appointment, please enter this code on our website:</p>
                    <h2 style="color: #27ae60; font-size: 32px; margin: 10px 0; letter-spacing: 4px;">{confirmation_code}</h2>
                    <p style="font-size: 14px; color: #666;">This code expires in 30 minutes</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #2c3e50;">Contact Information:</h3>
                    <p><strong>Address:</strong> {SHOP_INFO['address']['address_en']}</p>
                    <p><strong>Phone:</strong> {SHOP_INFO['contact']['phone']}</p>
                    <p><strong>Email:</strong> {SHOP_INFO['contact']['email']}</p>
                </div>
                
                <p style="margin-top: 30px;">We look forward to seeing you!</p>
                <p><strong>{SHOP_INFO['owner_name']}</strong><br>{SHOP_INFO['name_en']}</p>
            </div>
        </body>
        </html>
        """
    
    def _get_hebrew_email_body(self, customer_name: str, date: str, time: str, 
                              services: List[str], confirmation_code: str) -> str:
        """Generate Hebrew email body"""
        services_text = ", ".join([SERVICES[service]["name_he"] for service in services])
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; direction: rtl;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">אישור תור</h2>
                
                <p>{customer_name} היקר/ה,</p>
                
                <p>תודה על קביעת תור ב<strong>{SHOP_INFO['name_he']}</strong>!</p>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin-top: 0; color: #2c3e50;">פרטי התור:</h3>
                    <p><strong>תאריך:</strong> {date}</p>
                    <p><strong>שעה:</strong> {time}</p>
                    <p><strong>שירותים:</strong> {services_text}</p>
                </div>
                
                <div style="background-color: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: center;">
                    <h3 style="margin-top: 0; color: #27ae60;">נדרש אישור</h3>
                    <p>לאישור התור, אנא הזן קוד זה באתר שלנו:</p>
                    <h2 style="color: #27ae60; font-size: 32px; margin: 10px 0; letter-spacing: 4px;">{confirmation_code}</h2>
                    <p style="font-size: 14px; color: #666;">הקוד בתוקף למשך 30 דקות</p>
                </div>
                
                <div style="margin: 30px 0;">
                    <h3 style="color: #2c3e50;">פרטי קשר:</h3>
                    <p><strong>כתובת:</strong> {SHOP_INFO['address']['address_he']}</p>
                    <p><strong>טלפון:</strong> {SHOP_INFO['contact']['phone']}</p>
                    <p><strong>אימייל:</strong> {SHOP_INFO['contact']['email']}</p>
                </div>
                
                <p style="margin-top: 30px;">אנחנו מצפים לראותך!</p>
                <p><strong>{SHOP_INFO['owner_name']}</strong><br>{SHOP_INFO['name_he']}</p>
            </div>
        </body>
        </html>
        """
