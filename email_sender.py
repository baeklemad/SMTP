#!/usr/bin/env python3
"""
Professional Email Sender with HTML/CSS Template
Now supports sending both certificate emails and Google Meet invitations.
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
        self._logo_data = None
        self._logo_msg_id = None
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Configuration file '{config_file}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in configuration file '{config_file}'.")
            return {}
    
    def _get_logo_data(self):
        """Fetch and cache the logo data."""
        if self._logo_data:
            return self._logo_data, self._logo_msg_id

        logo_url = self.config.get("logo_url", "")
        if not logo_url:
            return None, None

        try:
            logo_msg_id = make_msgid(domain="icpepse")
            with urllib.request.urlopen(logo_url) as response:
                self._logo_data = response.read()
            self._logo_msg_id = logo_msg_id
            return self._logo_data, self._logo_msg_id
        except Exception as e:
            print(f"⚠️ Failed to download logo: {e}")
            return None, None

    def _create_html_template(self, recipient_name: str, subject: str,
                              mode: str = "certificate",
                              certificate_url: str = "#",
                              meet_info: Optional[Dict[str, str]] = None,
                              logo_cid: Optional[str] = None) -> str:
        """Create an HTML template for either certificates or Google Meet invites."""
        import random
        unique_id = f"msg_{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{random.randint(1000, 9999)}"

        # Header with logo
        header_content = "ICPEP.se Meneses Campus"
        if logo_cid:
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
            logo_markup = f'<span style="font-size: 20px; font-weight: 600; color: #f36b3e; letter-spacing: -0.3px;">{header_content}</span>'

        # Body content based on mode
        if mode == "meet" and meet_info:
            main_paragraphs = f"""
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">Dear {recipient_name},</p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">We invite you to join our <strong>Google Meet session</strong> to guide attendees on how to claim their courses. Please find the meeting details below:</p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">
<strong>Topic:</strong> {meet_info.get('topic')}<br/>
<strong>Date:</strong> {meet_info.get('date')}<br/>
<strong>Time:</strong> {meet_info.get('time')}<br/>
<strong>Google Meet Link:</strong> <a href="{meet_info.get('link')}" target="_blank" style="color: #4aa3ff; text-decoration: underline;">{meet_info.get('link')}</a>
</p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">Congratulations! We are pleased to present you with your participation certificate.</p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">You can download your certificate using the button below. Please save it for your records and feel free to share it on your professional profiles.</p>
<p style="margin: 0 0 28px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">Best regards,<br/><span style="color: #b8b8b8;">ICPEP.se Meneses Campus Team</span></p>
"""
        else:
            main_paragraphs = f"""
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">Dear {recipient_name},</p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">Congratulations! We are pleased to present you with your participation certificate.</p>
<p style="margin: 0 0 18px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">You can download your certificate using the button below. Please save it for your records and feel free to share it on your professional profiles.</p>
<table border="0" cellpadding="0" cellspacing="0" style="margin: 0 0 16px 0;" role="presentation">
<tr>
<td align="left" style="padding-top: 8px;">
<a href="{certificate_url}" target="_blank" class="download-button" style="display: inline-block; padding: 12px 24px; background-color: transparent; border: 1px solid #666666; border-radius: 6px; color: #888888; text-decoration: none; font-size: 14px; font-weight: 500;">
<span style="color: #888888;">Download Certificate</span>
</a>
</td>
</tr>
</table>
<p style="margin: 0 0 18px 0; font-size: 13px; color: #d4d4d4; line-height: 1.6;">Your certificate is available via the download link<br/>Save it for your professional records<br/>Share it on LinkedIn and other platforms</p>
<p style="margin: 0 0 28px 0; font-size: 15px; line-height: 1.7; color: #d4d4d4;">Best regards,<br/><span style="color: #b8b8b8;">ICPEP.se Meneses Campus Team</span></p>
"""

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
<td style="padding: 28px 36px; border-bottom: 1px solid #333333; background-color: #1a1a1a; border-radius: 8px 8px 0 0;">
{logo_markup}
</td>
</tr>
<tr>
<td class="content-padding" style="padding: 36px 36px 32px 36px;">
{main_paragraphs}
</td>
</tr>
<tr>
<td style="padding: 28px 36px; border-top: 1px solid #333333; background-color: #1a1a1a; text-align: center; border-radius: 0 0 8px 8px;">
<p style="margin: 0 0 12px 0; font-size: 13px; color: #999999; line-height: 1.6;">Join our community of professionals and stay updated with the latest news and events.</p>
<p style="margin: 0; font-size: 12px; color: #666666;">&copy; {datetime.now().year} ICPEP.se Meneses Campus. All rights reserved.</p>
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

    def send_email(self, recipient_email: str, subject: str, recipient_name: str,
                   mode: str = "certificate",
                   certificate_url: Optional[str] = None,
                   meet_info: Optional[Dict[str, str]] = None,
                   server: Optional[smtplib.SMTP] = None) -> bool:
        """
        Send an HTML email for certificate or meet invite.
        If 'server' is provided, it uses the existing connection.
        Otherwise, it creates a new connection (and closes it after sending).
        """
        if not self.config:
            print("❌ No configuration loaded.")
            return False
        
        try:
            message = MIMEMultipart("alternative")
            message["From"] = self.config['sender_email']
            message["To"] = recipient_email
            message["Subject"] = subject

            logo_cid_value = None
            logo_data, logo_msg_id = self._get_logo_data()
            
            if logo_data and logo_msg_id:
                logo_part = MIMEImage(logo_data)
                logo_part.add_header("Content-ID", logo_msg_id)
                logo_part.add_header("Content-Disposition", "inline", filename="logo.png")
                message.attach(logo_part)
                logo_cid_value = logo_msg_id.strip("<>")

            html_content = self._create_html_template(
                recipient_name, subject,
                mode=mode,
                certificate_url=certificate_url,
                meet_info=meet_info,
                logo_cid=logo_cid_value,
            )

            text_content = f"Dear {recipient_name},\n\nThis message contains HTML content.\nPlease view it in an email client that supports HTML."

            message.attach(MIMEText(text_content, "plain"))
            message.attach(MIMEText(html_content, "html"))

            if server:
                # Use existing connection
                server.sendmail(self.config['sender_email'], recipient_email, message.as_string())
            else:
                # Create new connection
                context = ssl.create_default_context()
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as new_server:
                    new_server.starttls(context=context)
                    new_server.login(self.config['sender_email'], self.config['app_password'])
                    new_server.sendmail(self.config['sender_email'], recipient_email, message.as_string())

            print(f"✅ Sent to {recipient_email}")
            return True

        except Exception as e:
            print(f"❌ Failed to send to {recipient_email}: {e}")
            return False

    def send_bulk_meet_invites(self):
        """Send Google Meet invites to all recipients."""
        if 'recipients' not in self.config:
            print("❌ No recipients found in config.json.")
            return {}

        print("\n📧 Let's set up your Google Meet invitation:")
        subject = input("Enter email subject: ").strip() or "ICPEP.se Google Meet Invitation"
        topic = input("Enter event topic: ").strip()
        date = input("Enter event date (e.g. Thursday, October 30, 2025): ").strip()
        time = input("Enter time (e.g. 8:00 PM – 9:00 PM (Asia/Manila)): ").strip()
        link = input("Enter Google Meet link: ").strip()

        meet_info = {
            "topic": topic,
            "date": date,
            "time": time,
            "link": link
        }

        # Trial Phase: Test Email
        print("\n🔎 Test Phase:")
        if input("Send a test email first? (y/n): ").strip().lower() == 'y':
            test_email = input("Enter test recipient email: ").strip()
            if test_email:
                # Get sample data from first recipient
                first_recipient_key = next(iter(self.config['recipients']))
                
                print(f"📨 Sending test email to {test_email} (using data from {first_recipient_key})...")
                test_success = self.send_email(
                    recipient_email=test_email,
                    recipient_name=first_recipient_key,
                    subject=subject,
                    mode="meet",
                    meet_info=meet_info
                )
                
                if test_success:
                    print("✅ Test email sent successfully.")
                    if input("Proceed with bulk sending? (y/n): ").strip().lower() != 'y':
                        print("🚫 Bulk sending aborted.")
                        return {}
                else:
                    print("❌ Test email failed. Aborting.")
                    return {}

        results = {}
        
        # Establish connection once
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.config['sender_email'], self.config['app_password'])
                
                for name, details in self.config['recipients'].items():
                    email = details.get('email') if isinstance(details, dict) else details
                    if not email:
                        print(f"⚠️ Missing email for {name}")
                        continue
                    print(f"📨 Sending to: {name} ({email})")
                    success = self.send_email(
                        recipient_email=email,
                        recipient_name=name,
                        subject=subject,
                        mode="meet",
                        meet_info=meet_info,
                        server=server # Pass the active connection
                    )
                    results[email] = success
        except Exception as e:
            print(f"❌ Connection error: {e}")
            
        return results

def main():
    print("🚀 Professional Email Sender (Certificates + Meet Invites)")
    print("=" * 60)
    
    sender = EmailSender()
    if not sender.config:
        print("Missing config.json — please create it.")
        return

    print("\n📧 Menu Options:")
    print("1. Send single email (manual)")
    print("2. Send bulk certificate emails")
    print("3. Send custom certificate email")
    print("4. Send Google Meet invitations")

    choice = input("\nSelect option (1–4): ").strip()

    if choice == "1":
        # Manual single email
        email = input("Recipient email: ").strip()
        name = input("Recipient name: ").strip()
        subject = input("Email subject: ").strip()
        cert_url = input("Certificate URL: ").strip()
        sender.send_email(email, subject, name, mode="certificate", certificate_url=cert_url)
        
    elif choice == "2":
        # Bulk certificate emails from config
        if 'recipients' not in sender.config:
            print("❌ No recipients found in config.json.")
            return
        
        subject = input("Enter email subject (default: 'Your Certificate of Participation'): ").strip()
        if not subject:
            subject = "Your Certificate of Participation"

        # Trial Phase: Test Email
        print("\n🔎 Test Phase:")
        if input("Send a test email first? (y/n): ").strip().lower() == 'y':
            test_email = input("Enter test recipient email: ").strip()
            if test_email:
                # Get sample data from first recipient
                first_recipient_key = next(iter(sender.config['recipients']))
                first_recipient_data = sender.config['recipients'][first_recipient_key]
                
                sample_name = first_recipient_key
                sample_cert_url = '#'
                if isinstance(first_recipient_data, dict):
                    sample_cert_url = first_recipient_data.get('certificate_url', '#')
                
                print(f"📨 Sending test email to {test_email} (using data from {sample_name})...")
                test_success = sender.send_email(
                    recipient_email=test_email,
                    recipient_name=sample_name,
                    subject=subject,
                    mode="certificate",
                    certificate_url=sample_cert_url
                )
                
                if test_success:
                    print("✅ Test email sent successfully.")
                    if input("Proceed with bulk sending? (y/n): ").strip().lower() != 'y':
                        print("🚫 Bulk sending aborted.")
                        return
                else:
                    print("❌ Test email failed. Aborting.")
                    return
            
        results = {}
        
        # Establish connection once
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(sender.smtp_server, sender.smtp_port) as server:
                server.starttls(context=context)
                server.login(sender.config['sender_email'], sender.config['app_password'])

                for name, details in sender.config['recipients'].items():
                    if isinstance(details, dict):
                        email = details.get('email')
                        cert_url = details.get('certificate_url', '#')
                    else:
                        email = details
                        cert_url = '#'
                        
                    if not email:
                        print(f"⚠️ Missing email for {name}")
                        continue
                        
                    print(f"📨 Sending to: {name} ({email})")
                    success = sender.send_email(
                        recipient_email=email,
                        recipient_name=name,
                        subject=subject,
                        mode="certificate",
                        certificate_url=cert_url,
                        server=server # Pass the active connection
                    )
                    results[email] = success
        except Exception as e:
            print(f"❌ Connection error: {e}")
            
        success_count = sum(1 for r in results.values() if r)
        print(f"\n📊 Done! {success_count}/{len(results)} certificates sent successfully.")
        
    elif choice == "3":
        # Custom certificate email
        email = input("Recipient email: ").strip()
        name = input("Recipient name: ").strip()
        subject = input("Email subject: ").strip() or "Your Certificate of Participation"
        cert_url = input("Certificate URL: ").strip()
        
        success = sender.send_email(
            recipient_email=email,
            recipient_name=name,
            subject=subject,
            mode="certificate",
            certificate_url=cert_url
        )
        if success:
            print("\n✅ Certificate email sent successfully!")
        else:
            print("\n❌ Failed to send certificate email.")
            
    elif choice == "4":
        # Google Meet invitations
        print("\n📨 Sending Google Meet invites...\n")
        results = sender.send_bulk_meet_invites()
        success = sum(1 for r in results.values() if r)
        total = len(results)
        print(f"\n📊 Done! {success}/{total} invites sent successfully.")
        
    else:
        print("❌ Invalid option selected.")

if __name__ == "__main__":
    main()