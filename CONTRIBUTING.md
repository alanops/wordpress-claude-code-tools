# Contributing to WordPress Claude Code Tools

Thank you for your interest in contributing to WordPress Claude Code Tools! This project aims to make WordPress content management frictionless for developers through automation and AI integration.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Contribution Guidelines](#contribution-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

## Code of Conduct

This project follows a simple code of conduct:

- **Be respectful**: Treat all contributors with respect
- **Be constructive**: Provide helpful feedback and suggestions
- **Be collaborative**: Work together to improve the project
- **Be inclusive**: Welcome contributors of all skill levels

## How to Contribute

There are many ways to contribute to this project:

### 🐛 Bug Reports
- Found a bug? Open an issue with steps to reproduce
- Include your Python version, WordPress version, and OS
- Provide error messages and logs when possible

### 💡 Feature Requests
- Have an idea for improvement? Create a feature request issue
- Explain the use case and expected behavior
- Consider implementation complexity and maintenance impact

### 📝 Documentation
- Improve existing documentation
- Add examples and tutorials
- Fix typos and clarify instructions
- Translate documentation to other languages

### 🔧 Code Contributions
- Fix bugs and implement features
- Add new automation scripts
- Improve error handling and user experience
- Add tests and improve code coverage

### 🎨 Examples and Templates
- Share your automation workflows
- Create example integrations
- Add templates for common use cases
- Document real-world implementations

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- WordPress site for testing (recommended: local development environment)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/YOUR_USERNAME/wordpress-claude-code-tools.git
cd wordpress-claude-code-tools
```

3. Add the upstream repository:

```bash
git remote add upstream https://github.com/alanops/wordpress-claude-code-tools.git
```

### Set Up Development Environment

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available
```

3. Set up pre-commit hooks (optional but recommended):

```bash
pip install pre-commit
pre-commit install
```

### Configuration for Testing

1. Copy the example configuration:

```bash
cp examples/config.example.json config.json
```

2. Update with your test WordPress site details:

```json
{
  "site_url": "https://your-test-site.com",
  "username": "test-user",
  "app_password": "your-test-app-password"
}
```

⚠️ **Important**: Never commit real credentials! Use a test site for development.

## Contribution Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Include docstrings for functions and classes
- Keep functions focused and modular

Example:

```python
def publish_post(self, 
                title: str, 
                content: str, 
                status: str = "publish") -> Optional[Dict[str, Any]]:
    """
    Publish a new post to WordPress
    
    Args:
        title: Post title
        content: Post content (HTML)
        status: Post status (publish, draft, private)
        
    Returns:
        Post data if successful, None otherwise
        
    Raises:
        ValueError: If title or content is empty
    """
```

### Error Handling

- Use try/except blocks for external API calls
- Provide meaningful error messages
- Log errors appropriately
- Fail gracefully with helpful feedback

```python
try:
    response = requests.post(url, json=data, timeout=30)
    response.raise_for_status()
    return response.json()
except requests.exceptions.Timeout:
    print("❌ Request timed out. Check your internet connection.")
    return None
except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP error: {e}")
    return None
```

### Security

- Never hardcode credentials or API keys
- Use environment variables or config files
- Validate all user inputs
- Use HTTPS for all API communications
- Document security considerations

### Testing

While we don't have a comprehensive test suite yet, please:

- Test your changes with a real WordPress site
- Verify error handling with invalid inputs
- Check edge cases and boundary conditions
- Document any manual testing steps

### Documentation

- Update relevant documentation for your changes
- Add docstrings to new functions
- Include usage examples
- Update the README if adding new features

## Pull Request Process

### Before Submitting

1. **Update your fork**:

```bash
git fetch upstream
git checkout main
git merge upstream/main
```

2. **Create a feature branch**:

```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes** following the guidelines above

4. **Test your changes** thoroughly

5. **Commit with descriptive messages**:

```bash
git commit -m "Add feature: intelligent content categorization

- Implement AI-based category suggestion
- Add confidence scoring for suggestions
- Include fallback for manual categorization
- Update documentation with examples"
```

### Submitting the Pull Request

1. **Push your branch**:

```bash
git push origin feature/your-feature-name
```

2. **Create a pull request** on GitHub with:
   - Clear title describing the change
   - Detailed description of what and why
   - Reference to related issues (if any)
   - Screenshots or examples (if applicable)

3. **Respond to feedback** promptly and professionally

### Pull Request Template

When creating a PR, please include:

```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Testing
- [ ] Tested with WordPress 6.x
- [ ] Tested error handling
- [ ] Verified security considerations
- [ ] Updated documentation

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No credentials committed
```

## Issue Guidelines

### Bug Reports

Use this template for bug reports:

```markdown
**Describe the Bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Run command '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9.0]
- WordPress version: [e.g., 6.3]
- Plugin versions: [if relevant]

**Additional Context**
Error messages, logs, screenshots, etc.
```

### Feature Requests

Use this template for feature requests:

```markdown
**Feature Description**
Clear description of the feature you'd like to see.

**Use Case**
Explain why this feature would be useful.

**Proposed Solution**
If you have ideas for implementation.

**Alternatives Considered**
Other approaches you've thought about.

**Additional Context**
Mockups, examples, related issues, etc.
```

## Development Areas

We especially welcome contributions in these areas:

### High Priority
- **Error handling improvements**
- **Additional WordPress REST API features**
- **Performance optimizations**
- **Security enhancements**

### Medium Priority
- **Plugin compatibility testing**
- **Multisite support**
- **Media management features**
- **Bulk operations**

### Nice to Have
- **Web interface for non-technical users**
- **Integration with other CMS platforms**
- **Advanced AI features**
- **Monitoring and analytics**

## Code Architecture

### Project Structure

```
wordpress-claude-code-tools/
├── scripts/           # Core functionality
│   ├── __init__.py
│   ├── wordpress_publisher.py
│   └── check_broken_links.py
├── examples/          # Usage examples
├── docs/             # Documentation
├── tests/            # Test scripts (future)
└── workflows/        # CI/CD templates
```

### Design Principles

- **Modularity**: Each script should be independently useful
- **Composability**: Scripts should work well together
- **Configurability**: Support multiple configuration methods
- **Extensibility**: Easy to add new features and integrations
- **Reliability**: Robust error handling and logging

## Community

### Communication

- **GitHub Issues**: For bugs, features, and questions
- **Discussions**: For general questions and community chat
- **Pull Requests**: For code review and collaboration

### Recognition

Contributors will be:
- Listed in the project's contributors section
- Mentioned in release notes for significant contributions
- Invited to become maintainers for sustained contributions

### Mentorship

New contributors are welcome! If you're new to:
- **Python**: We can help with code style and best practices
- **WordPress APIs**: We can guide you through the REST API
- **Open Source**: We can help you learn the contribution process

Don't hesitate to ask questions in issues or discussions.

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Test with multiple WordPress versions
4. Update documentation
5. Create GitHub release
6. Announce in community channels

## Legal

By contributing to this project, you agree that:

- Your contributions will be licensed under the MIT License
- You have the right to contribute the code/documentation
- You understand this is an open source project

## Questions?

- Check existing [issues](https://github.com/alanops/wordpress-claude-code-tools/issues)
- Start a [discussion](https://github.com/alanops/wordpress-claude-code-tools/discussions)
- Read the [documentation](docs/)

Thank you for contributing to WordPress Claude Code Tools! 🚀

---

*This contributing guide is inspired by best practices from the open source community and is itself open to improvement through contributions.*