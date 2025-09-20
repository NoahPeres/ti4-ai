# GitHub PR Review Fetcher - Usage Examples

This script fetches GitHub PR review content using the GitHub API, which is useful for iterating on your codebase based on review feedback.

## Setup

### 1. GitHub Token (Recommended)
Create a GitHub personal access token for better rate limits and private repo access:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` scope
3. Set it as an environment variable:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### 2. Repository Detection
The script can auto-detect your repository from git remotes, or you can specify it manually.

## Usage Examples

### Basic Usage
```bash
# Fetch latest review for PR #123 (auto-detects repo from git)
python scripts/fetch_pr_review.py 123

# Specify repository manually
python scripts/fetch_pr_review.py 123 --repo owner/repo-name
```

### Advanced Options
```bash
# Show all reviews instead of just the latest
python scripts/fetch_pr_review.py 123 --all-reviews

# Skip detailed comments (faster)
python scripts/fetch_pr_review.py 123 --no-comments

# Use specific token
python scripts/fetch_pr_review.py 123 --token ghp_your_token
```

### Environment Variables
```bash
# Set repository and token via environment
export GITHUB_REPO="owner/repo-name"
export GITHUB_TOKEN="ghp_your_token"

python scripts/fetch_pr_review.py 123
```

## Sample Output

```
============================================================
GITHUB PR REVIEW SUMMARY
============================================================
Reviewer: code-reviewer
State: APPROVED
Submitted: 2024-01-15T10:30:00Z
Review ID: 123456789

REVIEW BODY:
--------------------------------------------
Great work on implementing the space combat mechanics! 
The code looks solid and follows TDD practices well.

A few minor suggestions:
- Consider adding more edge case tests
- The combat resolution could be optimized

DETAILED COMMENTS:
--------------------------------------------
Comment 1:
  File: src/ti4/rules/space_combat.py
  Line: 45
  Body: This method could benefit from type hints

Comment 2:
  File: tests/test_rule_78_space_combat.py
  Line: 120
  Body: Add a test case for empty fleet combat

============================================================
```

## Integration with Development Workflow

### 1. After Receiving Review Feedback
```bash
# Fetch the latest review to see what needs to be addressed
python scripts/fetch_pr_review.py 456

# Make your changes based on the feedback
# Then push updates to the PR
```

### 2. Monitoring Multiple Reviews
```bash
# See all reviews to track the conversation
python scripts/fetch_pr_review.py 456 --all-reviews
```

### 3. Quick Check Without Comments
```bash
# Fast overview of review status
python scripts/fetch_pr_review.py 456 --no-comments
```

## Error Handling

The script handles common scenarios:
- **404 errors**: PR not found or repository not accessible
- **403 errors**: Rate limit exceeded or insufficient permissions
- **Network errors**: Connection issues
- **No reviews**: Gracefully handles PRs without reviews

## Rate Limits

- **Without token**: 60 requests/hour per IP
- **With token**: 5,000 requests/hour per user

For regular use, a GitHub token is highly recommended.