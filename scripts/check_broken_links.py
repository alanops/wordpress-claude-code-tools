#!/usr/bin/env python3
"""
Broken Links Checker - Scan WordPress posts for broken links
"""

import requests
import re
from urllib.parse import urlparse, urljoin
from typing import List, Tuple, Dict, Any
import concurrent.futures
import json
from wordpress_publisher import WordPressPublisher, load_config


class BrokenLinksChecker:
    """Check for broken links in WordPress posts"""
    
    def __init__(self, publisher: WordPressPublisher, site_url: str):
        """
        Initialize the broken links checker
        
        Args:
            publisher: WordPressPublisher instance
            site_url: Base site URL
        """
        self.publisher = publisher
        self.site_url = site_url.rstrip('/')
        self.checked_urls = {}  # Cache for already checked URLs
        
    def extract_links_from_content(self, content: str) -> List[str]:
        """Extract all links from HTML content"""
        # Pattern to match href attributes
        link_pattern = r'href=["\']([^"\']*)["\']'
        links = re.findall(link_pattern, content, re.IGNORECASE)
        
        # Pattern to match markdown-style links
        markdown_pattern = r'\[([^\]]*)\]\(([^)]*)\)'
        markdown_links = re.findall(markdown_pattern, content)
        
        # Combine all links
        all_links = links + [link[1] for link in markdown_links]
        
        # Convert relative URLs to absolute
        absolute_links = []
        for link in all_links:
            if link.startswith('/') and not link.startswith('//'):
                link = urljoin(self.site_url, link)
            absolute_links.append(link)
        
        return list(set(absolute_links))  # Remove duplicates
    
    def check_link_status(self, url: str) -> Tuple[str, str]:
        """
        Check if a link is working
        
        Returns:
            Tuple of (status, message)
        """
        # Check cache first
        if url in self.checked_urls:
            return self.checked_urls[url]
        
        # Skip certain URL types
        if any(url.startswith(prefix) for prefix in ['#', 'javascript:', 'mailto:', 'tel:']):
            result = ('SKIP', 'Special URL type')
            self.checked_urls[url] = result
            return result
        
        try:
            # Use HEAD request first (faster)
            response = requests.head(
                url, 
                timeout=10, 
                allow_redirects=True,
                headers={'User-Agent': 'WordPress Broken Links Checker'}
            )
            
            # Some servers don't support HEAD, try GET
            if response.status_code == 405:
                response = requests.get(
                    url, 
                    timeout=10, 
                    allow_redirects=True,
                    headers={'User-Agent': 'WordPress Broken Links Checker'},
                    stream=True  # Don't download full content
                )
            
            if response.status_code == 200:
                result = ('OK', f'HTTP {response.status_code}')
            elif response.status_code in [301, 302, 303, 307, 308]:
                result = ('REDIRECT', f'HTTP {response.status_code} -> {response.headers.get("Location", "Unknown")}')
            elif response.status_code == 404:
                result = ('BROKEN', f'HTTP {response.status_code} - Not Found')
            else:
                result = ('ERROR', f'HTTP {response.status_code}')
                
        except requests.exceptions.Timeout:
            result = ('TIMEOUT', 'Request timed out')
        except requests.exceptions.ConnectionError:
            result = ('CONNECTION_ERROR', 'Connection failed')
        except Exception as e:
            result = ('ERROR', str(e))
        
        self.checked_urls[url] = result
        return result
    
    def check_post_links(self, post: Dict[str, Any]) -> Dict[str, Any]:
        """Check all links in a single post"""
        post_id = post['id']
        post_title = post['title']['rendered']
        post_url = post['link']
        content = post['content']['rendered']
        
        links = self.extract_links_from_content(content)
        
        if not links:
            return None
        
        broken_links = []
        
        for link in links:
            status, message = self.check_link_status(link)
            
            if status in ['BROKEN', 'ERROR', 'TIMEOUT', 'CONNECTION_ERROR']:
                broken_links.append({
                    'url': link,
                    'status': status,
                    'message': message
                })
        
        if broken_links:
            return {
                'post_id': post_id,
                'post_title': post_title,
                'post_url': post_url,
                'total_links': len(links),
                'broken_links': broken_links
            }
        
        return None
    
    def scan_all_posts(self, max_workers: int = 5) -> List[Dict[str, Any]]:
        """
        Scan all published posts for broken links
        
        Args:
            max_workers: Number of concurrent workers for link checking
            
        Returns:
            List of posts with broken links
        """
        print("🔍 Fetching all posts...")
        posts = self.publisher.get_all_posts()
        print(f"📝 Found {len(posts)} published posts")
        
        broken_links_report = []
        
        # Use thread pool for concurrent link checking
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all posts for checking
            future_to_post = {
                executor.submit(self.check_post_links, post): post 
                for post in posts
            }
            
            # Process completed checks
            for i, future in enumerate(concurrent.futures.as_completed(future_to_post), 1):
                post = future_to_post[future]
                print(f"\r[{i}/{len(posts)}] Checking: {post['title']['rendered'][:50]}...", end='', flush=True)
                
                try:
                    result = future.result()
                    if result:
                        broken_links_report.append(result)
                except Exception as e:
                    print(f"\n❌ Error checking post {post['id']}: {e}")
        
        print("\n✅ Scan complete!")
        return broken_links_report
    
    def generate_report(self, broken_links_report: List[Dict[str, Any]], 
                       output_file: str = "broken_links_report.json") -> None:
        """Generate and save broken links report"""
        if not broken_links_report:
            print("🎉 No broken links found! Your site is in great shape.")
            return
        
        total_broken = sum(len(post['broken_links']) for post in broken_links_report)
        
        print("\n" + "="*80)
        print("🔧 BROKEN LINKS REPORT")
        print("="*80)
        print(f"📊 Summary: {len(broken_links_report)} posts with {total_broken} broken links\n")
        
        for post_info in broken_links_report:
            print(f"📄 POST: {post_info['post_title']}")
            print(f"🔗 URL: {post_info['post_url']}")
            print(f"🆔 ID: {post_info['post_id']}")
            print(f"📊 Total Links: {post_info['total_links']}")
            print(f"❌ Broken: {len(post_info['broken_links'])}")
            
            for link in post_info['broken_links'][:5]:  # Show first 5
                print(f"   • {link['url']}")
                print(f"     Status: {link['status']} - {link['message']}")
            
            if len(post_info['broken_links']) > 5:
                print(f"   ... and {len(post_info['broken_links']) - 5} more")
            print()
        
        # Save detailed report
        with open(output_file, 'w') as f:
            json.dump(broken_links_report, f, indent=2)
        
        print(f"💾 Detailed report saved to: {output_file}")


def main():
    """Main function"""
    config = load_config()
    
    if not all([config.get('site_url'), config.get('username'), config.get('app_password')]):
        print("❌ Missing configuration. Please set up config.json or environment variables.")
        return
    
    # Initialize publisher and checker
    publisher = WordPressPublisher(
        site_url=config['site_url'],
        username=config['username'],
        app_password=config['app_password']
    )
    
    checker = BrokenLinksChecker(publisher, config['site_url'])
    
    # Run the scan
    print("🚀 Starting broken links scan...")
    report = checker.scan_all_posts()
    
    # Generate report
    checker.generate_report(report)


if __name__ == "__main__":
    main()