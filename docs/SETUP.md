# Setup Guide

This guide will walk you through setting up WordPress Claude Code Tools for your blog.

## Prerequisites

- Python 3.8 or higher
- WordPress site (self-hosted or WordPress.com Business plan)
- WordPress admin access

## Step 1: Enable WordPress REST API

The REST API is enabled by default in WordPress 4.7+. To verify:

1. Visit: `https://your-site.com/wp-json/`
2. You should see JSON data about your site

If you see a 404 error, check your permalinks settings in WordPress admin.

## Step 2: Create Application Password

Application passwords provide a secure way to authenticate with the REST API without using your main password.

### For WordPress 5.6+:

1. Go to WordPress Admin → Users → Your Profile
2. Scroll to "Application Passwords" section
3. Enter a name (e.g., "Claude Code Tools")
4. Click "Add New Application Password"
5. **Important**: Copy the generated password immediately (it won't be shown again)

### For Earlier Versions:

Install the [Application Passwords plugin](https://wordpress.org/plugins/application-passwords/) first.

## Step 3: Install Python Dependencies

```bash
# Clone the repository
git clone https://github.com/alanops/wordpress-claude-code-tools.git
cd wordpress-claude-code-tools

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Configure Credentials

### Method 1: Using config.json (Recommended for Development)

```bash
cp examples/config.example.json config.json
```

Edit `config.json`:
```json
{
  "site_url": "https://your-wordpress-site.com",
  "username": "your-username",
  "app_password": "xxxx xxxx xxxx xxxx xxxx xxxx"
}
```

### Method 2: Using Environment Variables (Recommended for Production)

```bash
export WP_SITE_URL="https://your-wordpress-site.com"
export WP_USERNAME="your-username"
export WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
```

Add to your `.bashrc` or `.zshrc` to persist.

## Step 5: Test Your Setup

```bash
# Test the connection
python scripts/wordpress_publisher.py
```

You should see:
```
✅ Connected to WordPress successfully!
```

## Step 6: Try Publishing

```bash
# Run the example
python examples/publish_article.py
```

## Troubleshooting

### "401 Unauthorized" Error

- Verify your username is correct (use email if that's how you log in)
- Check that the application password is copied correctly (including spaces)
- Ensure your user has publishing permissions

### "404 Not Found" on API Endpoints

- Check permalink settings (Settings → Permalinks)
- Try saving permalinks again (just click Save Changes)
- Verify `.htaccess` file exists and is writable

### SSL Certificate Errors

If you're testing with a local/development site:

```python
# In your script, add:
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# When making requests:
response = requests.post(url, verify=False)
```

**Note**: Never disable SSL verification in production!

### Connection Timeouts

- Check if your hosting provider limits API requests
- Some hosts block external API access on cheaper plans
- Try increasing the timeout value in the scripts

## Security Best Practices

1. **Never commit credentials**
   - Add `config.json` to `.gitignore`
   - Use environment variables in production

2. **Use HTTPS**
   - Always use `https://` URLs
   - Enable SSL on your WordPress site

3. **Limit permissions**
   - Create a dedicated user for API access
   - Give minimum required permissions

4. **Rotate passwords**
   - Regularly update application passwords
   - Delete unused application passwords

## Next Steps

- Read the [API Guide](API_GUIDE.md) for advanced usage
- Check out more [examples](../examples/)
- Learn about [Claude Code integration](CLAUDE_CODE.md)