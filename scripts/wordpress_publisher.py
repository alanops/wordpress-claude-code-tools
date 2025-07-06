#!/usr/bin/env python3
"""
WordPress Publisher - Core publishing functionality for WordPress REST API
"""

import requests
import json
import base64
from typing import Optional, Dict, Any
import os
from datetime import datetime


class WordPressPublisher:
    """Main class for interacting with WordPress REST API"""
    
    def __init__(self, site_url: str, username: str, app_password: str):
        """
        Initialize WordPress Publisher
        
        Args:
            site_url: WordPress site URL (e.g., https://example.com)
            username: WordPress username or email
            app_password: WordPress application password
        """
        self.site_url = site_url.rstrip('/')
        self.username = username
        self.app_password = app_password
        self.headers = self._create_auth_headers()
        
    def _create_auth_headers(self) -> Dict[str, str]:
        """Create authentication headers for API requests"""
        credentials = f"{self.username}:{self.app_password}"
        token = base64.b64encode(credentials.encode()).decode()
        
        return {
            'Authorization': f'Basic {token}',
            'Content-Type': 'application/json',
        }
    
    def test_connection(self) -> bool:
        """Test the API connection and authentication"""
        try:
            response = requests.get(
                f"{self.site_url}/wp-json/wp/v2/users/me",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def publish_post(self, 
                    title: str, 
                    content: str, 
                    status: str = "publish",
                    categories: Optional[list] = None,
                    tags: Optional[list] = None,
                    excerpt: Optional[str] = None,
                    featured_media: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """
        Publish a new post to WordPress
        
        Args:
            title: Post title
            content: Post content (HTML)
            status: Post status (publish, draft, private)
            categories: List of category IDs
            tags: List of tag IDs
            excerpt: Post excerpt
            featured_media: Featured image ID
            
        Returns:
            Post data if successful, None otherwise
        """
        post_data = {
            'title': title,
            'content': content,
            'status': status,
            'format': 'standard'
        }
        
        if categories:
            post_data['categories'] = categories
        if tags:
            post_data['tags'] = tags
        if excerpt:
            post_data['excerpt'] = excerpt
        if featured_media:
            post_data['featured_media'] = featured_media
        
        try:
            response = requests.post(
                f"{self.site_url}/wp-json/wp/v2/posts",
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                post_info = response.json()
                print(f"✅ Post published successfully!")
                print(f"Post ID: {post_info['id']}")
                print(f"URL: {post_info['link']}")
                return post_info
            else:
                print(f"❌ Failed to publish post")
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error publishing post: {e}")
            return None
    
    def update_post(self, 
                   post_id: int,
                   title: Optional[str] = None,
                   content: Optional[str] = None,
                   status: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Update an existing post"""
        post_data = {}
        
        if title:
            post_data['title'] = title
        if content:
            post_data['content'] = content
        if status:
            post_data['status'] = status
        
        try:
            response = requests.post(
                f"{self.site_url}/wp-json/wp/v2/posts/{post_id}",
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Failed to update post {post_id}")
                return None
                
        except Exception as e:
            print(f"❌ Error updating post: {e}")
            return None
    
    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        """Get a single post by ID"""
        try:
            response = requests.get(
                f"{self.site_url}/wp-json/wp/v2/posts/{post_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error fetching post: {e}")
            return None
    
    def get_all_posts(self, per_page: int = 100, status: str = "publish") -> list:
        """Get all posts from WordPress"""
        all_posts = []
        page = 1
        
        while True:
            try:
                response = requests.get(
                    f"{self.site_url}/wp-json/wp/v2/posts",
                    headers=self.headers,
                    params={'per_page': per_page, 'page': page, 'status': status},
                    timeout=30
                )
                
                if response.status_code == 200:
                    posts = response.json()
                    if not posts:
                        break
                    all_posts.extend(posts)
                    page += 1
                else:
                    break
                    
            except Exception as e:
                print(f"❌ Error fetching posts: {e}")
                break
        
        return all_posts
    
    def delete_post(self, post_id: int, force: bool = False) -> bool:
        """
        Delete a post
        
        Args:
            post_id: Post ID to delete
            force: Skip trash and permanently delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            params = {'force': force} if force else {}
            
            response = requests.delete(
                f"{self.site_url}/wp-json/wp/v2/posts/{post_id}",
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Error deleting post: {e}")
            return False


def load_config(config_file: str = "config.json") -> Dict[str, str]:
    """Load configuration from JSON file"""
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        return {
            'site_url': os.getenv('WP_SITE_URL', ''),
            'username': os.getenv('WP_USERNAME', ''),
            'app_password': os.getenv('WP_APP_PASSWORD', '')
        }


def main():
    """Example usage"""
    config = load_config()
    
    if not all([config.get('site_url'), config.get('username'), config.get('app_password')]):
        print("❌ Missing configuration. Please set up config.json or environment variables.")
        return
    
    # Initialize publisher
    publisher = WordPressPublisher(
        site_url=config['site_url'],
        username=config['username'],
        app_password=config['app_password']
    )
    
    # Test connection
    if publisher.test_connection():
        print("✅ Connected to WordPress successfully!")
    else:
        print("❌ Failed to connect to WordPress")
        return
    
    # Example: Publish a test post
    test_post = publisher.publish_post(
        title=f"Test Post - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        content="<p>This is a test post created with WordPress Claude Code Tools.</p>",
        status="draft"
    )
    
    if test_post:
        print(f"Created test post with ID: {test_post['id']}")


if __name__ == "__main__":
    main()