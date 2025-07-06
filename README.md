# WordPress Claude Code Tools 🚀

A collection of open-source tools for automating WordPress content management using Claude Code and DevOps principles. Transform your WordPress blog into a frictionless publishing platform directly from your terminal.

## 🎯 Overview

This repository contains sanitized, production-ready scripts that demonstrate how to:
- Publish WordPress posts via REST API from the terminal
- Automate content management with Python scripts
- Check and fix broken links programmatically
- Integrate AI-assisted content creation with WordPress
- Implement GitOps workflows for blog management

## 📁 Repository Structure

```
wordpress-claude-code-tools/
├── scripts/                    # Core automation scripts
│   ├── wordpress_publisher.py  # Main publishing script
│   ├── check_broken_links.py   # Broken links scanner
│   ├── fix_broken_links.py     # Automated link fixer
│   └── update_post.py          # Post update utility
├── examples/                   # Example implementations
│   ├── publish_article.py      # Example article publisher
│   └── config.example.json     # Configuration template
├── workflows/                  # GitHub Actions templates
│   └── deploy.yml             # Example deployment workflow
├── docs/                      # Documentation
│   ├── SETUP.md              # Setup instructions
│   ├── API_GUIDE.md          # WordPress REST API guide
│   └── CLAUDE_CODE.md        # Claude Code integration guide
└── tests/                     # Test scripts
    └── test_api_connection.py # API connection tester
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- WordPress site with REST API enabled
- WordPress Application Password (for authentication)
- Claude Code (optional, for AI-assisted content)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/alanops/wordpress-claude-code-tools.git
cd wordpress-claude-code-tools
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your WordPress credentials:
```bash
cp examples/config.example.json config.json
# Edit config.json with your WordPress details
```

### Basic Usage

#### Publishing a Post
```python
from scripts.wordpress_publisher import WordPressPublisher

publisher = WordPressPublisher(
    site_url="https://yoursite.com",
    username="your_username",
    app_password="your_app_password"
)

publisher.publish_post(
    title="My DevOps Article",
    content="<p>Content goes here...</p>",
    status="publish"
)
```

#### Checking Broken Links
```bash
python scripts/check_broken_links.py --site https://yoursite.com
```

## 🛠️ Core Features

### WordPress Publisher
- Authenticate using Application Passwords
- Create, update, and delete posts
- Manage categories and tags
- Handle featured images
- Support for custom post types

### Broken Links Manager
- Scan all published posts for broken links
- Generate detailed reports
- Automatically fix common link issues
- Batch update multiple posts
- Smart link replacement strategies

### AI Integration Support
- Templates for Claude Code integration
- Content generation helpers
- Automated proofreading workflows
- SEO optimization suggestions

## 📚 Documentation

Detailed documentation is available in the `docs/` directory:

- **[Setup Guide](docs/SETUP.md)**: Complete setup instructions
- **[API Guide](docs/API_GUIDE.md)**: WordPress REST API reference
- **[Claude Code Integration](docs/CLAUDE_CODE.md)**: AI-assisted content workflows
- **[Examples](examples/)**: Ready-to-use script examples

## 🔧 Advanced Usage

### GitOps Workflow

Integrate with GitHub Actions for automated deployment:

```yaml
name: Publish Blog Post
on:
  push:
    paths:
      - 'content/*.md'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish to WordPress
        run: python scripts/publish_from_markdown.py
```

### Custom Scripts

Extend the base functionality:

```python
from scripts.wordpress_publisher import WordPressPublisher

class CustomPublisher(WordPressPublisher):
    def publish_with_seo(self, title, content, meta_description):
        # Add your custom logic here
        pass
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Ways to Contribute
- Add new automation scripts
- Improve documentation
- Share your workflow examples
- Report bugs or suggest features
- Add test coverage

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- WordPress REST API team for excellent documentation
- Claude Code by Anthropic for AI assistance
- The DevOps community for inspiration

## 🚨 Security Notes

- **Never commit credentials**: Use environment variables or config files
- **Use Application Passwords**: More secure than regular passwords
- **Enable HTTPS**: Always use SSL for API communication
- **Validate inputs**: Sanitize all user inputs before API calls

## 📈 Roadmap

- [ ] WordPress multisite support
- [ ] Scheduled post automation
- [ ] Media library management
- [ ] Backup and restore utilities
- [ ] Performance monitoring tools
- [ ] Integration with more AI platforms

## 💬 Support

- Open an issue for bug reports
- Start a discussion for feature requests
- Check existing issues before creating new ones

## 🌟 Show Your Support

If you find these tools helpful, please consider:
- ⭐ Starring this repository
- 🐦 Sharing on social media
- 📝 Writing about your experience
- 🤝 Contributing improvements

---

Built with ❤️ by [AlanOps](https://alanops.com) - Automating the tedious, one script at a time.