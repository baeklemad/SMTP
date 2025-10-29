# Professional Email Sender

A Python script for sending professional HTML/CSS templated emails using Gmail SMTP with a sleek black, white, and orange color scheme.

## Features

- 🎨 **Professional Design**: Sleek black/white/orange color scheme
- 📧 **Gmail SMTP Integration**: Secure email sending via Gmail
- 📱 **Responsive Template**: Mobile-friendly HTML email template
- 🔧 **Easy Configuration**: JSON-based configuration system
- 📎 **Attachment Support**: Send files with your emails
- 🌙 **Dark Mode Support**: Automatic dark mode detection
- ♿ **Accessibility**: Clean, readable design

## Quick Start

### 1. Setup Gmail App Password

1. Enable 2-Factor Authentication on your Gmail account
2. Go to [Google Account Settings](https://myaccount.google.com/)
3. Navigate to Security → 2-Step Verification → App passwords
4. Generate a new app password for "Mail"
5. Save the 16-character password

### 2. Configure the Script

Edit `config.json` with your email settings:

```json
{
    "sender_email": "your-email@gmail.com",
    "app_password": "your-16-character-app-password",
    "recipients": [
        "recipient1@example.com",
        "recipient2@example.com"
    ],
    "company_info": {
        "name": "Your Company Name",
        "phone": "+1 (555) 123-4567",
        "website": "www.yourcompany.com",
        "address": "123 Business St, City, State 12345"
    }
}
```

### 3. Run the Script

```bash
python email_sender.py
```

## Usage Examples

### Basic Usage

```python
from email_sender import EmailSender

# Initialize sender
sender = EmailSender()

# Send a simple email
sender.send_email(
    recipient_email="customer@example.com",
    subject="Welcome to Our Service",
    content="Thank you for choosing our professional services!"
)
```

### Advanced Usage

```python
# Send email with custom content and attachment
sender.send_email(
    recipient_email="client@company.com",
    subject="Monthly Report",
    content="Please find attached your monthly report with detailed analytics.",
    recipient_name="John Smith",
    attachment_path="monthly_report.pdf"
)
```

## Email Template Features

### Design Elements
- **Header**: Professional gradient header with company branding
- **Orange Accent**: Vibrant orange accent line for visual appeal
- **Typography**: Clean, modern font stack (Segoe UI)
- **Responsive**: Mobile-optimized layout
- **Call-to-Action**: Professional orange button styling

### Color Scheme
- **Primary**: Black (#000000) and White (#ffffff)
- **Accent**: Orange gradient (#ff6b35 to #ff8c42)
- **Text**: Dark gray (#333333) for readability
- **Background**: Light gray (#f8f9fa) for contrast

### Responsive Design
- Mobile-first approach
- Flexible layout for all screen sizes
- Optimized typography scaling
- Touch-friendly button sizes

## Configuration Options

### Email Settings
- `sender_email`: Your Gmail address
- `app_password`: Gmail app password (16 characters)
- `recipients`: List of default recipients

### Company Information
- `company_info.name`: Your company name
- `company_info.phone`: Contact phone number
- `company_info.website`: Company website
- `company_info.address`: Business address

## Security Notes

- ⚠️ **Never commit your `config.json` with real credentials**
- 🔒 Use Gmail App Passwords, not your regular password
- 🛡️ Keep your app password secure and private
- 📝 Consider using environment variables for production

## Troubleshooting

### Common Issues

1. **Authentication Error**
   - Verify your Gmail app password is correct
   - Ensure 2FA is enabled on your Gmail account
   - Check that "Less secure app access" is disabled

2. **SMTP Connection Error**
   - Verify internet connection
   - Check Gmail SMTP settings (smtp.gmail.com:587)
   - Ensure firewall isn't blocking the connection

3. **Recipient Refused**
   - Verify recipient email address is valid
   - Check for typos in email addresses
   - Ensure recipient email exists

### Debug Mode

Enable debug output by modifying the script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## File Structure

```
email-sender/
├── email_sender.py      # Main script
├── config.json          # Configuration file
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## Dependencies

This script uses only Python standard library modules:
- `smtplib` - SMTP email sending
- `email` - Email message construction
- `ssl` - Secure connections
- `json` - Configuration loading
- `os` - File system operations

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Verify your Gmail settings and app password
3. Test with a simple email first
4. Check Python version compatibility (3.6+)

---

**Happy Emailing! 📧✨**
