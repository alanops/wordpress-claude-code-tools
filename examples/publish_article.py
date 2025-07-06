#!/usr/bin/env python3
"""
Example: Publishing an article with WordPress Claude Code Tools
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.wordpress_publisher import WordPressPublisher, load_config
from datetime import datetime


def publish_devops_article():
    """Example of publishing a DevOps article"""
    
    # Load configuration
    config = load_config()
    
    # Initialize publisher
    publisher = WordPressPublisher(
        site_url=config['site_url'],
        username=config['username'],
        app_password=config['app_password']
    )
    
    # Test connection
    if not publisher.test_connection():
        print("❌ Failed to connect to WordPress")
        return
    
    # Article content
    article_title = "5 DevOps Automation Tips That Will Save You Hours"
    
    article_content = """
<p>As DevOps engineers, we're always looking for ways to automate repetitive tasks and streamline our workflows. Here are five automation tips that have saved me countless hours.</p>

<h2>1. Automate Your Documentation</h2>
<p>Use tools like Terraform Docs or Ansible-doc to automatically generate documentation from your infrastructure code. This ensures your docs are always up-to-date.</p>

<h2>2. Set Up Intelligent Alerting</h2>
<p>Instead of getting bombarded with alerts, use tools like PagerDuty or Opsgenie to intelligently route and group alerts based on severity and context.</p>

<h2>3. Implement GitOps for Everything</h2>
<p>Not just for Kubernetes! Apply GitOps principles to all your infrastructure changes. Every change should go through version control.</p>

<h2>4. Create Reusable CI/CD Templates</h2>
<p>Build a library of reusable pipeline templates for common tasks. This makes setting up new projects much faster.</p>

<h2>5. Automate Security Scanning</h2>
<p>Integrate security scanning into your CI/CD pipeline. Tools like Trivy, Snyk, or SonarQube can catch vulnerabilities early.</p>

<p><strong>Remember:</strong> The time you invest in automation today will pay dividends in the future. Start small, iterate, and gradually build your automation toolkit.</p>
"""
    
    # Publish the article
    result = publisher.publish_post(
        title=article_title,
        content=article_content,
        status="draft",  # Start as draft for review
        excerpt="Five practical DevOps automation tips that will streamline your workflow and save hours of manual work."
    )
    
    if result:
        print("\n✅ Article published successfully!")
        print(f"📝 Title: {article_title}")
        print(f"🔗 URL: {result['link']}")
        print(f"📊 Status: Draft (ready for review)")
        print(f"🆔 Post ID: {result['id']}")
        
        # Example: Update the post to published status
        print("\n🔄 Publishing the article...")
        updated = publisher.update_post(
            post_id=result['id'],
            status="publish"
        )
        
        if updated:
            print("✅ Article is now live!")
    else:
        print("❌ Failed to publish article")


def publish_from_markdown():
    """Example of publishing from a Markdown file"""
    
    # This is a placeholder for markdown conversion
    # You would typically use a library like markdown2 or python-markdown
    
    markdown_content = """
# Infrastructure as Code Best Practices

Learn how to write maintainable and scalable infrastructure code.

## Key Principles

1. **Version Control Everything**
2. **Use Modules and Reusability**
3. **Implement Proper Testing**
4. **Document Your Decisions**

## Example

```hcl
module "web_server" {
  source = "./modules/ec2"
  
  instance_type = "t3.micro"
  ami_id        = var.web_ami_id
  
  tags = {
    Environment = "production"
    Team        = "platform"
  }
}
```
"""
    
    # Convert markdown to HTML (simplified example)
    html_content = markdown_content.replace('# ', '<h1>').replace('</h1>\n', '</h1>')
    html_content = html_content.replace('## ', '<h2>').replace('</h2>\n', '</h2>')
    html_content = html_content.replace('```hcl', '<pre><code class="language-hcl">')
    html_content = html_content.replace('```', '</code></pre>')
    html_content = html_content.replace('**', '<strong>').replace('</strong>', '</strong>')
    
    print("📝 Markdown converted to HTML (simplified)")
    # In practice, use a proper markdown library for conversion


if __name__ == "__main__":
    # Example 1: Publish a DevOps article
    publish_devops_article()
    
    # Example 2: Show markdown conversion concept
    # publish_from_markdown()