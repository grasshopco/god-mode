# 🏷️ God Mode Tags System

God Mode uses special tags to organize and route information to the right places in your project. This guide explains how to use these tags effectively.

## ✨ What Are Tags?

Tags are special markers in square brackets like `[LOG_SUMMARY]` or `[MEMORY_UPDATE]` that tell God Mode where to store different types of information. When the AI assistant includes these tags in its responses, the Message Router automatically extracts and saves this content to the appropriate files.

## 📋 Available Tags

### Basic Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `[LOG_SUMMARY]` | Brief, high-level summary of key decisions or insights | [LOG_SUMMARY] Implemented JWT authentication system |
| `[LOG_DETAIL]` | Detailed technical discussions or explorations | [LOG_DETAIL] The authentication flow works by... |
| `[MEMORY_UPDATE]` | Important facts to remember for future discussions | [MEMORY_UPDATE] The database schema uses UUID as primary keys |
| `[REFERENCE: Name]` | Technical details saved for reference | [REFERENCE: API Endpoints] The user API has the following endpoints... |
| `[FEATURE_LOG: Name]` | Notes about a specific feature's implementation | [FEATURE_LOG: Authentication] Added password reset functionality |
| `[DOCUMENTATION: Path]` | Documentation for a specific component | [DOCUMENTATION: components/Button] The Button component supports... |

### Specialized Memory Tags

| Tag | Purpose |
|-----|---------|
| `[MEMORY_LEARNINGS]` | Insights and lessons learned |
| `[MEMORY_ARCHITECTURE]` | Architecture changes |
| `[MEMORY_REQUIREMENTS]` | Requirement changes |
| `[MEMORY_ROADMAP]` | Roadmap updates |
| `[MEMORY_CONVENTIONS]` | Convention changes |
| `[MEMORY_DEPENDENCIES]` | Dependency changes |
| `[MEMORY_GLOSSARY]` | Terminology updates |
| `[MEMORY_TESTING]` | Testing updates |
| `[MEMORY_SECURITY]` | Security updates |
| `[MEMORY_PERFORMANCE]` | Performance updates |
| `[MEMORY_ACCESSIBILITY]` | Accessibility updates |

### Multi-tag System

You can route the same content to multiple destinations without repeating yourself:

```
[MULTI_TAG: LOG_SUMMARY, FEATURE_LOG: Authentication]
Implemented JWT authentication with refresh token rotation.
```

## 🧠 How Tags Work

1. **The AI includes tags**: When the AI assistant responds to you in Cursor, it includes appropriate tags in its response.

2. **Message Router processes tags**: The Message Router (running in the background) watches for these tags and extracts the content.

3. **Content is saved**: The content is automatically saved to the appropriate files in the `god_mode/memory` directory.

4. **Notification appears**: You'll see a desktop notification confirming that the content was saved.

## 📚 Example Usage

Here's how tags might appear in an AI response:

```
I've analyzed your authentication system and here are my findings:

[LOG_SUMMARY]
Reviewed the authentication system and found potential security issues with the token storage approach.

[LOG_DETAIL]
The current implementation stores JWT tokens in localStorage, which makes them vulnerable to XSS attacks. A more secure approach would be to store the access token in memory and the refresh token in an HttpOnly cookie.

Here's how you could implement this change:

```javascript
// Instead of this:
localStorage.setItem('token', accessToken);

// Do this:
// 1. Keep access token in memory
this.accessToken = accessToken;
// 2. Refresh token comes from HttpOnly cookie set by the server
```

This approach protects against most common XSS attacks while maintaining functionality.

[MEMORY_SECURITY]
The authentication system should use HttpOnly cookies for refresh tokens and in-memory storage for access tokens to mitigate XSS vulnerabilities.
```

## 🛠️ Troubleshooting

- **Tags not being processed?** Make sure God Mode is running (check with `./god_mode_remote.sh` option 3)
- **AI not adding tags?** Update the Cursor rules (option 7 in the remote control menu)
- **No notifications?** Make sure the `plyer` package is installed: `pip install plyer`

## 📑 Where to Find Saved Content

All tagged content is saved in the `god_mode/memory` directory:

- `memory_logs_summary.md` - Contains all [LOG_SUMMARY] entries
- `memory_logs_detail.md` - Contains all [LOG_DETAIL] entries
- `memory_general.md` - Contains all [MEMORY_UPDATE] entries
- `memory_features/feature_name.md` - Contains feature-specific logs
- etc.

You can browse these files to review past discussions and decisions. 