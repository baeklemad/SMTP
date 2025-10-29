#!/usr/bin/env python3
"""
Professional Email Sender with HTML/CSS Template
Sends templated emails using Gmail SMTP with a sleek Cursor-inspired design.
Uses name-to-email mapping from config.json for certificate distribution.
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import make_msgid
import json
from datetime import datetime
from typing import Optional, Dict, Any
import urllib.request

class EmailSender:
    def __init__(self, config_file: str = "config.json"):
        """Initialize the email sender with configuration."""
        self.config = self._load_config(config_file)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuration file '{config_file}' not found.")
            print("Please create a config.json file with your email settings.")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in configuration file '{config_file}'.")
            return {}
    
    def _create_html_template(self, recipient_name: str = "Valued Customer", 
                            subject: str = "Important Update", 
                            content: str = "This is a professional email template.",
                            certificate_url: str = "#",
                            logo_cid: Optional[str] = None) -> str:
        """Create a clean HTML email template with Cursor-inspired minimal design."""
        
        # Generate unique content to prevent Gmail clipping
        import random
        unique_id = f"msg_{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{random.randint(1000, 9999)}"

        logo_markup = ""
        header_content = "ICPEP.se Meneses Campus"
        if logo_cid:
            # Use table layout for proper alignment without expanding header height
            logo_markup = f"""
<table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
<tr>
<td style="vertical-align:middle;">
<span style="font-size: 20px; font-weight: 600; color: #f36b3e; letter-spacing: -0.3px;">{header_content}</span>
</td>
<td align="right" style="vertical-align:middle; width:60px;">
<img src="cid:{logo_cid}" alt="ICPEP.se Meneses Campus Logo" loading="lazy" style="height:80px; width:auto; display:block;" />
</td>
</tr>
</table>"""
        else:
            logo_markup = header_content
        
        html_template = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{subject}</title>
<style type="text/css">
.download-button:hover {{
    background-color: #2a2a2a !important;
    border-color: #888888 !important;
}}
.download-button span {{
    color: #888888;
}}
.download-button:hover span {{
    color: #ffffff !important;
}}
@media only screen and (max-width: 600px) {{
    .email-container {{
        width: 100% !important;
        max-width: 100% !important;
    }}
    .content-padding {{
        padding: 24px !important;
    }}
}}
</style>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
<table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
<tr>
<td align="center" style="padding: 20px 0;">
<table border="0" cellpadding="0" cellspacing="0" width="600" class="email-container" style="max-width: 600px; background-color: #1e1e1e; border: 1px solid #333333; border-radius: 8px;" role="presentation">
<tr>
<td style="padding: 28px 36px; border-bottom: 1px solid #333333; background-color: #1a1a1a; border-radius: 8px 8px 0 0; height: 28px;">
{logo_markup}
</td>
</tr>
<tr>
<td class="content-padding" style="padding: 36px 36px 32px 36px;">
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">Dear {recipient_name},</p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">We invite you to join our Google Meet session to guide attendees on how to claim their courses. Please find the meeting details below:</p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">Topic: Machine Learning Principle and Overview
Date: Thursday, October 30, 2025
Time: 8:00 PM – 9:00 PM (Asia/Manila)
Google Meet Link: <a href="https://meet.google.com/uyv-vemw-ohy" target="_blank">https://meet.google.com/uyv-vemw-ohy</a></p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">We encourage you to join on time to ensure a smooth and informative session.</p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">We appreciate your participation and look forward to your continued engagement with ICPEP.se Meneses Campus.</p>
<p style="margin: 0 0 28px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">Best regards,<br/><span style="color: #b8b8b8;">ICPEP.se Meneses Campus Team</span></p>
<table border="0" cellpadding="0" cellspacing="0" style="margin: 0 0 16px 0;" role="presentation">
<tr>
<td align="left" style="padding-top: 8px;">
<a href="{certificate_url}" target="_blank" class="download-button" style="display: inline-block; padding: 12px 24px; background-color: transparent; border: 1px solid #666666; border-radius: 6px; color: #888888; text-decoration: none; font-size: 14px; font-weight: 500;">
<span style="color: #888888;">Download Certificate</span>
</a>
</td>
</tr>
</table>
<p style="margin: 0; font-size: 13px; color: #d4d4d4; line-height: 1.6;">Your certificate is available via the download link<br/>Save it for your professional records<br/>Share it on LinkedIn and other platforms</p>
</td>
</tr>
<tr>
<td style="padding: 28px 36px; border-top: 1px solid #333333; background-color: #1a1a1a; text-align: center; border-radius: 0 0 8px 8px;">
<p style="margin: 0 0 12px 0; font-size: 13px; color: #999999; line-height: 1.6;">Join our community of professionals and stay updated with the latest news and events.</p>
<p style="margin: 0; font-size: 12px; color: #666666;"><a href="https://www.facebook.com/ICPEP.SEBulSUMC" target="_blank">{datetime.now().year} ICPEP.se Meneses Campus.</a> All rights reserved.</p>
</td>
</tr>
</table>
</td>
</tr>
</table>
<div style="display:none;white-space:nowrap;font-size:15px;line-height:0;">&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; {unique_id}</div>
</body>
</html>"""
        return html_template
    
    def send_email(self, recipient_email: str, subject: str, 
                   content: str = None, recipient_name: str = None,
                   certificate_url: Optional[str] = None) -> bool:
        """
        Send a professional HTML email.
        
        Args:
            recipient_email: Email address of the recipient
            subject: Email subject line
            content: Email content (optional, uses default if not provided)
            recipient_name: Name of the recipient (optional)
            certificate_url: URL to the recipient's certificate (optional)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        
        if not self.config:
            print("Error: No configuration loaded.")
            return False
            
        # Use default content if not provided
        if content is None:
            content = """
            We hope this message finds you well. This is a professional email template 
            designed to communicate important information in a clear and engaging manner.
            
            Our team is committed to providing excellent service and maintaining the 
            highest standards in all our communications.
            """
        
        # Use recipient email as name if not provided
        if recipient_name is None:
            recipient_name = recipient_email.split('@')[0].title()
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["From"] = self.config['sender_email']
            message["To"] = recipient_email
            message["Subject"] = subject
            
            # Create HTML content
            logo_cid_value: Optional[str] = None
            logo_url = self.config.get("logo_url", "https://image2url.com/images/1761016319003-4de73802-a864-45e4-a4a7-155fc5c9967d.png")

            if logo_url:
                try:
                    logo_msg_id = make_msgid(domain="icpepse")
                    with urllib.request.urlopen(logo_url) as response:
                        logo_data = response.read()
                    logo_part = MIMEImage(logo_data)
                    logo_part.add_header("Content-ID", logo_msg_id)
                    logo_part.add_header("Content-Disposition", "inline", filename="logo.png")
                    message.attach(logo_part)
                    logo_cid_value = logo_msg_id.strip("<>")
                except Exception as e:
                    print(f"⚠️ Failed to load logo from URL '{logo_url}': {e}. Skipping inline logo attachment.")

            html_content = self._create_html_template(
                recipient_name,
                subject,
                content,
                certificate_url=certificate_url or "#",
                logo_cid=logo_cid_value,
            )
            
            # Create plain text version
            text_content = f"""
Dear {recipient_name},

{content}

Best regards,
ICPEP.se Meneses Campus

Thank you for your participation
            """
            
            # Attach parts
            text_part = MIMEText(text_content, "plain")
            html_part = MIMEText(html_content, "html")

            message.attach(text_part)
            message.attach(html_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.config['sender_email'], self.config['app_password'])
                server.sendmail(
                    self.config['sender_email'], 
                    recipient_email, 
                    message.as_string()
                )
            
            print(f"✅ Email sent successfully to {recipient_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Authentication failed. Please check your email and app password.")
            return False
        except smtplib.SMTPRecipientsRefused:
            print("❌ Recipient email address is invalid.")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP error occurred: {e}")
            return False
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            return False
    
    def send_bulk_certificates(self) -> Dict[str, bool]:
        """
        Send certificates to all recipients listed in config.json.
        Uses name-to-details mapping from config to match certificate links.
            
        Returns:
            dict: Results for each recipient (email -> success status)
        """
        if not self.config or 'recipients' not in self.config:
            print("❌ No recipients found in configuration.")
            return {}
        
        if not isinstance(self.config['recipients'], dict):
            print("❌ Recipients must be a dictionary with name-to-email mapping.")
            print("Expected format: {\"Name\": \"email@example.com\"}")
            return {}
        
        results = {}
        
        for name, details in self.config['recipients'].items():
            email = None
            certificate_url = None

            if isinstance(details, dict):
                email = details.get('email')
                certificate_url = details.get('certificate_url')
            else:
                email = details

            if not email:
                print(f"⚠️  No email configured for: {name}")
                continue

            if not certificate_url:
                print(f"⚠️  No certificate link configured for: {name}")
                results[email] = False
                continue

            print(f"📄 Processing: {name}")
            
            # Create certificate-specific content
            certificate_content = f"""
Congratulations! We are pleased to present you with your participation certificate.

Your certificate is available at the following link: {certificate_url}

We appreciate your participation and look forward to your continued engagement with ICPEP.se Meneses Campus.

Best regards,
ICPEP.se Meneses Campus Team
            """
            
            # Send email with certificate
            success = self.send_email(
                recipient_email=email,
                subject="Correction: Official Certificate Email for  Programming Month 2025 – Machine Learning: Principles and Overview ",
                content=certificate_content,
                recipient_name=name,
                certificate_url=certificate_url
            )
            
            results[email] = success
            
            if success:
                print(f"   ✅ Sent to {email}")
            else:
                print(f"   ❌ Failed to send to {email}")
        
        return results

def main():
    """Main function to demonstrate email sending."""
    print("🚀 Professional Email Sender with Certificate Support")
    print("=" * 55)
    
    # Initialize email sender
    email_sender = EmailSender()
    
    if not email_sender.config:
        print("\n📝 Please create a config.json file with your email settings.")
        print("\nExample config.json:")
        print("""
{
    "sender_email": "your-email@gmail.com",
    "app_password": "your-app-password",
    "recipients": {
        "Carl Jumel P. Mercado": {
            "email": "carljumel@example.com",
            "certificate_url": "https://example.com/certificate.pdf"
        },
        "Juan Dela Cruz": {
            "email": "juan@example.com",
            "certificate_url": "https://example.com/certificate.pdf"
        }
    }
}
        """)
        print("\n📌 Note: Certificate links must be configured in config.json:")
        print("   \"certificate_url\": \"https://example.com/certificate.pdf\"")
        return
    
    print("\n📧 Email Options:")
    print("1. Send single email")
    print("2. Send certificate emails to all recipients (from config.json)")
    print("3. Send custom certificate email")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        # Single email
        recipient = input("Enter recipient email: ").strip()
        subject = input("Enter email subject: ").strip()
        content = input("Enter email content (press Enter for default): ").strip()
        certificate_link = input("Enter certificate link (optional): ").strip()

        if not content:
            content = None
        if not certificate_link:
            certificate_link = None

        success = email_sender.send_email(
            recipient_email=recipient,
            subject=subject,
            content=content,
            certificate_url=certificate_link
        )
        
        if success:
            print("\n🎉 Email sent successfully!")
        else:
            print("\n💥 Failed to send email. Please check your configuration.")
    
    elif choice == "2":
        # Bulk certificate emails
        print("\n📧 Sending certificates using links configured in config.json...")
        print()

        results = email_sender.send_bulk_certificates()
        
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        print("=" * 55)
        print(f"📊 Results: {successful}/{total} certificates sent successfully")
        
        if successful == total and total > 0:
            print("🎉 All certificates sent successfully!")
        elif successful > 0:
            print("⚠️  Some certificates failed to send. Check the error messages above.")
        else:
            print("💥 No certificates were sent. Please check your configuration.")
    
    elif choice == "3":
        # Custom certificate email
        recipient = input("Enter recipient email: ").strip()
        recipient_name = input("Enter recipient name: ").strip()
        certificate_link = input("Enter certificate link: ").strip()
        
        if not recipient_name:
            recipient_name = recipient.split('@')[0].title()
        
        success = email_sender.send_email(
            recipient_email=recipient,
            subject="Your Participation Certificate for Programming Month 2025 – Machine Learning: Principles and Overview - ICPEP.se Meneses Campus",
            content=f"""
Congratulations! We are pleased to present you with your participation certificate.

Your certificate is available at the following link: {certificate_link}

Please save this certificate for your records and feel free to share it on your professional profiles.

We appreciate your participation and look forward to your continued engagement with ICPEP.se Meneses Campus.

Best regards,
ICPEP.se Meneses Campus Team
            """,
            recipient_name=recipient_name,
            certificate_url=certificate_link
        )
        
        if success:
            print("\n🎉 Certificate email sent successfully!")
        else:
            print("\n💥 Failed to send certificate email. Please check your configuration.")
    
    else:
        print("❌ Invalid option selected.")

if __name__ == "__main__":
    main()