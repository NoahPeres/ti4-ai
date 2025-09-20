#!/usr/bin/env python3
"""
GitHub PR Review Fetcher

This script fetches the latest review content for a given pull request number
using the GitHub API. Useful for iterating on codebase based on review feedback.

Usage:
    python scripts/fetch_pr_review.py <pr_number> [--repo owner/repo] [--token TOKEN]
    
Environment Variables:
    GITHUB_TOKEN: GitHub personal access token (recommended)
    GITHUB_REPO: Repository in format "owner/repo" (optional)
"""

import argparse
import json
import os
import sys
from typing import Dict, List, Optional, Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class GitHubPRReviewFetcher:
    """Fetches GitHub PR review content using the GitHub API."""
    
    def __init__(self, repo: str, token: Optional[str] = None):
        """
        Initialize the PR review fetcher.
        
        Args:
            repo: Repository in format "owner/repo"
            token: GitHub personal access token (optional but recommended)
        """
        self.repo = repo
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.base_url = "https://api.github.com"
        
    def _make_request(self, url: str) -> Any:
        """Make a request to the GitHub API."""
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'TI4-AI-PR-Review-Fetcher/1.0'
        }
        
        if self.token:
            headers['Authorization'] = f'token {self.token}'
            
        try:
            request = Request(url, headers=headers)
            with urlopen(request, timeout=15) as response:
                return json.loads(response.read().decode('utf-8'))
        except HTTPError as e:
            if e.code == 404:
                raise ValueError(f"PR not found or repository not accessible: {url}")
            elif e.code == 403:
                raise ValueError("API rate limit exceeded or insufficient permissions. Consider using a GitHub token.")
            else:
                raise ValueError(f"HTTP error {e.code}: {e.reason}")
        except URLError as e:
            raise ValueError(f"Network error: {e.reason}")
    
    def get_pr_reviews(self, pr_number: int) -> List[Dict[str, Any]]:
        """
        Fetch all reviews for a given PR number.
        
        Args:
            pr_number: Pull request number
            
        Returns:
            List of review objects from GitHub API
        """
        url = f"{self.base_url}/repos/{self.repo}/pulls/{pr_number}/reviews?per_page=100"
        return self._make_request(url)
    
    def get_latest_review(self, pr_number: int) -> Optional[Dict[str, Any]]:
        """
        Get the most recent review for a PR.
        
        Args:
            pr_number: Pull request number
            
        Returns:
            Latest review object or None if no reviews exist
        """
        reviews = self.get_pr_reviews(pr_number)
        if not reviews:
            return None
            
        # Sort by submitted_at timestamp to get the latest
        reviews.sort(
            key=lambda x: x.get('submitted_at') or x.get('created_at') or '',
            reverse=True
        )
        return reviews[0]
    
    def get_review_comments(self, pr_number: int, review_id: int) -> List[Dict[str, Any]]:
        """
        Get detailed comments for a specific review.
        
        Args:
            pr_number: Pull request number
            review_id: Review ID
            
        Returns:
            List of review comment objects
        """
        url = f"{self.base_url}/repos/{self.repo}/pulls/{pr_number}/reviews/{review_id}/comments"
        return self._make_request(url)
    
    def format_review_summary(self, review: Dict[str, Any], include_comments: bool = True) -> str:
        """
        Format a review into a readable summary.
        
        Args:
            review: Review object from GitHub API
            include_comments: Whether to include detailed comments
            
        Returns:
            Formatted review summary
        """
        summary = []
        summary.append("=" * 60)
        summary.append(f"GITHUB PR REVIEW SUMMARY")
        summary.append("=" * 60)
        summary.append(f"Reviewer: {review.get('user', {}).get('login', 'Unknown')}")
        summary.append(f"State: {review.get('state', 'Unknown')}")
        summary.append(f"Submitted: {review.get('submitted_at', 'Unknown')}")
        summary.append(f"Review ID: {review.get('id', 'Unknown')}")
        summary.append("")
        
        # Main review body
        body = review.get('body', '').strip()
        if body:
            summary.append("REVIEW BODY:")
            summary.append("-" * 40)
            summary.append(body)
            summary.append("")
        
        # Include detailed comments if requested
        if include_comments and review.get('id'):
            try:
                pr_number = self._extract_pr_number_from_review(review)
                if pr_number:
                    comments = self.get_review_comments(pr_number, review['id'])
                    if comments:
                        summary.append("DETAILED COMMENTS:")
                        summary.append("-" * 40)
                        for i, comment in enumerate(comments, 1):
                            summary.append(f"Comment {i}:")
                            summary.append(f"  File: {comment.get('path', 'Unknown')}")
                            summary.append(f"  Line: {comment.get('line', 'Unknown')}")
                            summary.append(f"  Body: {comment.get('body', 'No content')}")
                            summary.append("")
            except Exception as e:
                summary.append(f"Note: Could not fetch detailed comments: {e}")
                summary.append("")
        
        summary.append("=" * 60)
        return "\n".join(summary)
    
    def _extract_pr_number_from_review(self, review: Dict[str, Any]) -> Optional[int]:
        """Extract PR number from review object."""
        pull_request_url = review.get('pull_request_url', '')
        if pull_request_url:
            try:
                return int(pull_request_url.split('/')[-1])
            except (ValueError, IndexError):
                pass
        return None


def detect_repo_from_git() -> Optional[str]:
    """Try to detect the GitHub repository from git remote."""
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        if result.returncode == 0:
            url = result.stdout.strip()
            # Parse GitHub URL formats
            if 'github.com' in url:
                if url.startswith('git@github.com:'):
                    repo = url.replace('git@github.com:', '').replace('.git', '')
                elif 'github.com/' in url:
                    repo = url.split('github.com/')[-1].replace('.git', '')
                else:
                    return None
                return repo
    except Exception:
        pass
    return None


def main():
    """Main function to handle command line arguments and fetch PR review."""
    parser = argparse.ArgumentParser(
        description="Fetch GitHub PR review content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python scripts/fetch_pr_review.py 123
    python scripts/fetch_pr_review.py 123 --repo owner/repo
    python scripts/fetch_pr_review.py 123 --token ghp_xxxx
    
Environment Variables:
    GITHUB_TOKEN: GitHub personal access token
    GITHUB_REPO: Repository in format "owner/repo"
        """
    )
    
    parser.add_argument('pr_number', type=int, help='Pull request number')
    parser.add_argument('--repo', help='Repository in format "owner/repo"')
    parser.add_argument('--token', help='GitHub personal access token')
    parser.add_argument('--all-reviews', action='store_true', 
                       help='Show all reviews instead of just the latest')
    parser.add_argument('--no-comments', action='store_true',
                       help='Skip fetching detailed review comments')
    
    args = parser.parse_args()
    
    # Determine repository
    repo = args.repo or os.getenv('GITHUB_REPO') or detect_repo_from_git()
    if not repo:
        print("Error: Repository not specified. Use --repo, set GITHUB_REPO env var, or run from a git repository.")
        sys.exit(1)
    
    # Initialize fetcher
    token = args.token or os.getenv('GITHUB_TOKEN')
    if not token:
        print("Warning: No GitHub token provided. API rate limits may apply.")
        print("Consider setting GITHUB_TOKEN environment variable or using --token")
        print()
    
    try:
        fetcher = GitHubPRReviewFetcher(repo, token)
        
        if args.all_reviews:
            # Fetch all reviews
            reviews = fetcher.get_pr_reviews(args.pr_number)
            if not reviews:
                print(f"No reviews found for PR #{args.pr_number} in {repo}")
                sys.exit(0)
            
            print(f"Found {len(reviews)} review(s) for PR #{args.pr_number} in {repo}")
            print()
            
            for i, review in enumerate(reviews, 1):
                print(f"REVIEW {i}/{len(reviews)}")
                print(fetcher.format_review_summary(review, not args.no_comments))
                if i < len(reviews):
                    print("\n" + "="*60 + "\n")
        else:
            # Fetch latest review only
            review = fetcher.get_latest_review(args.pr_number)
            if not review:
                print(f"No reviews found for PR #{args.pr_number} in {repo}")
                sys.exit(0)
            
            print(f"Latest review for PR #{args.pr_number} in {repo}:")
            print()
            print(fetcher.format_review_summary(review, not args.no_comments))
            
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()