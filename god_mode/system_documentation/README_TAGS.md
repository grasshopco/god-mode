# 🏷️ God Mode Tags System

God Mode uses special tags to organize and route information to the right places in your project. This guide explains how to use these tags effectively.

## ✨ What Are Tags?

Tags are special markers that tell God Mode where to store different types of information. God Mode supports two tag formats:

1. **Bracket-style tags** like `[LOG_SUMMARY]` or `[MEMORY_UPDATE]` (Legacy format)
2. **XML-style tags** like `<LOG_SUMMARY>...</LOG_SUMMARY>` (New improved format)

When the AI assistant includes these tags in its responses, the Message Router automatically extracts and saves this content to the appropriate files.

## 📋 Available Tags

### Basic Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `[LOG_SUMMARY]` | High-level implementation notes | [LOG_SUMMARY] Fixed bug in authentication flow |
| `[LOG_DETAIL]` | Detailed technical implementation | [LOG_DETAIL] Corrected the JWT token validation by adding proper expiration check |
| `[MEMORY_UPDATE]` | Important context information | [MEMORY_UPDATE] The system uses a Redis cache for session storage |
| `[REFERENCE: Name]` | Technical details saved for reference | [REFERENCE: API Endpoints] The user API has the following endpoints... |
| `[FEATURE: Name]` | Notes about a specific feature's implementation | [FEATURE: Authentication] Added password reset functionality |
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

## 🔄 Tag Formats

### Bracket Style (Legacy)

The original tag format uses square brackets:

```
[LOG_SUMMARY]
Brief summary of changes.

[MEMORY_UPDATE]
Important context information.
```

### XML Style (Recommended)

The new XML-style tags provide clearer boundaries for content and better support for multiple tagging:

```
<LOG_SUMMARY>
Brief summary of changes.
</LOG_SUMMARY>

<MEMORY_UPDATE>
Important context information.
</MEMORY_UPDATE>
```

### Advantages of XML-Style Tags

- **Clear boundaries**: Explicitly shows where tagged content begins and ends
- **Verbatim content**: Content is copied exactly as written, preserving formatting
- **Multiple tagging**: Same content can be tagged with multiple different tags
- **Semantic clarity**: Makes it obvious which tags apply to which content

## 🧠 How XML-Style Tags Work

1. **The AI includes XML tags**: The AI assistant wraps relevant content in opening and closing tags.
2. **Message Router identifies tags**: The router finds all XML-style tags in the response.
3. **Content is extracted**: The exact content between tags is extracted.
4. **Files are updated**: Content is saved to the appropriate files based on tag types.

## 📚 Example With XML-Style Tags

Here's how the XML-style tags appear in an AI response:

```
I've analyzed your authentication system and here are my findings:

<LOG_SUMMARY>
Reviewed the authentication system and found potential security issues with the token storage approach.
</LOG_SUMMARY>

<LOG_DETAIL>
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
</LOG_DETAIL>

<MEMORY_SECURITY>
The authentication system should use HttpOnly cookies for refresh tokens and in-memory storage for access tokens to mitigate XSS vulnerabilities.
</MEMORY_SECURITY>
```

## 🔀 Multiple Tags for the Same Content

With XML-style tags, you can apply multiple different tags to the same content when relevant to multiple categories:

```
<MEMORY_UPDATE>
Authentication tokens are now stored in HttpOnly cookies instead of localStorage to prevent XSS attacks.
</MEMORY_UPDATE>

<MEMORY_SECURITY>
Authentication tokens are now stored in HttpOnly cookies instead of localStorage to prevent XSS attacks.
</MEMORY_SECURITY>
```

This replaces the multi-tag format and is much more explicit and clear.

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