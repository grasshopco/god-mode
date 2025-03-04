# Message Router Usage Guide

This document explains how to use the Message Router system effectively and ensure the AI consistently includes the correct markers in its responses for automated documentation.

## Overview

The Message Router system automatically processes AI outputs containing special markers and routes content to the appropriate files. This maintains organized documentation and memory without manual copying and pasting.

## Available Tags

The message router processes several types of tags:

- `[LOG_SUMMARY]` - Routes to memory_logs_all.md
- `[LOG_DETAIL]` - Routes to memory_logs_detailed.md
- `[MEMORY_UPDATE]` - Routes to MEMORY_CURSOR.md
- `[FEATURE: FeatureName]` - Routes to feature-specific logs in `memory_feature_*.md`

### Memory Update Markers
- `[MEMORY_LEARNINGS]` - Routes to `memory_learnings.md`
- `[MEMORY_UPDATES]` - Routes to `memory_updates.md`
- `[MEMORY_REQUIREMENTS]` - Routes to `memory_requirements.md`
- `[MEMORY_ROADMAP]` - Routes to `memory_roadmap.md`
- `[MEMORY_ARCHITECTURE]` - Routes to `memory_architecture.md`
- `[MEMORY_CONVENTIONS]` - Routes to `memory_conventions.md`
- `[MEMORY_DEPENDENCIES]` - Routes to `memory_dependencies.md`
- `[MEMORY_GLOSSARY]` - Routes to `memory_glossary.md`
- `[MEMORY_TESTING]` - Routes to `memory_testing.md`
- `[MEMORY_SECURITY]` - Routes to `memory_security.md`
- `[MEMORY_PERFORMANCE]` - Routes to `memory_performance.md`
- `[MEMORY_ACCESSIBILITY]` - Routes to `memory_accessibility.md`

### Special Markers
- `[DOC_UPDATE: Type]` - Routes to documentation files based on type (project, feature, design, data)

### Multi-Tag Marker (New!)
- `[MULTI_TAG: TAG1, TAG2, ...]` - Routes the same content to multiple destinations

The multi-tag feature allows you to route the same content to multiple files without duplication. For more information, see [Multi-Tag Feature Documentation](documentation_multi_tag_feature.md).

## Training the AI to Use Markers

To ensure the AI consistently includes markers in its responses:

### 1. Add a Rule to the Cursor Rules File

Edit `.cursor/.cursorrules` to add the following instruction:

```
All comprehensive responses that contain significant code changes, design decisions, 
or insights must include markup with appropriate markers for the message router:

1. Include a [LOG_SUMMARY] with a brief description of the changes.
2. Include a [LOG_DETAIL] with comprehensive explanation of the changes.
3. Include a [MEMORY_UPDATE] for relevant project context updates.
4. Use [FEATURE: FeatureName] for specific feature updates.
5. Use [DOC_UPDATE: Type] for documentation updates.
6. Use specific memory markers like [MEMORY_ARCHITECTURE] when updating specialized memory files.
7. For content that should go to multiple files, use the [MULTI_TAG: TAG1, TAG2, ...] format.

This markup enables automatic documentation and persistent memory.
```

### 2. Create a Structured Response Template

Ask the AI to follow this structured response template for significant changes:

```
<Response to user's question/implementation>

---

[MULTI_TAG: LOG_SUMMARY, FEATURE: FeatureName]
Brief one-line summary of the changes made

[LOG_DETAIL]
Detailed explanation of:
- What was implemented
- Why it was done this way
- Any alternatives considered
- Future considerations

[MEMORY_UPDATE]
Key architectural decisions or context that should be remembered for future sessions

[DOC_UPDATE: project]
Any documentation that should be added to the project documentation
```

### 3. Prompt the AI Explicitly

Include prompts to the AI to include markers in your requests:

- "Please include the appropriate message router markers in your response."
- "Make sure to add [LOG_SUMMARY] and [LOG_DETAIL] markers to your response."
- "Remember to update the relevant memory files with the appropriate markers."
- "Use the multi-tag feature for content that should go to multiple destinations."

### 4. Provide Feedback and Reinforcement

If the AI forgets to include markers:

- Remind it about the message router system
- Ask it to add markers to its previous response
- Refer it to this documentation

## Best Practices for Using Markers

### When to Use Each Marker

- **LOG_SUMMARY**: For brief summaries of changes (1-2 sentences)
- **LOG_DETAIL**: For comprehensive explanations of implementations
- **MEMORY_UPDATE**: For architectural decisions and important context
- **MEMORY_LEARNINGS**: For insights gained during development
- **FEATURE: FeatureName**: For feature-specific implementation details
- **DOC_UPDATE**: For updates to official documentation
- **MULTI_TAG**: For content that should be routed to multiple destinations

### Format Recommendations

- Keep markers on separate lines
- Include clear section breaks between marker sections
- Use proper Markdown formatting within sections
- Keep LOG_SUMMARY concise (1-2 sentences)
- Make LOG_DETAIL comprehensive with proper subsections
- For repeated content, prefer MULTI_TAG over duplicate sections

### Example of Well-Formatted Response with Multi-Tag

```
I've implemented the authentication system using JWT tokens with refresh token rotation.

---

[MULTI_TAG: LOG_SUMMARY, FEATURE: Authentication]
Implemented JWT authentication with refresh token rotation, role-based access control, and secure storage.

[LOG_DETAIL]
# Authentication Implementation

The authentication system has been implemented with the following components:

## JWT Token Strategy
- Access tokens with 15-minute expiration
- Refresh tokens with 7-day expiration and rotation
- Secure HttpOnly cookies for token storage

## Security Considerations
- CSRF protection with double-submit pattern
- Token revocation capabilities
- Rate limiting on auth endpoints

## Role-Based Access Control
- Implemented middleware for role verification
- Created user, admin, and super-admin roles
- Added permission checks in protected routes

Testing has been completed with unit tests covering the token generation,
validation, and refresh flows.

[MULTI_TAG: MEMORY_UPDATE, MEMORY_SECURITY]
The project now uses JWT-based authentication with the following architecture decisions:
- Token-based auth with access/refresh token pattern
- Tokens stored in HttpOnly cookies
- Role-based permission system
- CSRF protection implemented

[DOC_UPDATE: project]
## Authentication

The project uses JWT-based authentication with the following features:
- **Access tokens**: Short-lived (15m) for API authorization
- **Refresh tokens**: Long-lived (7d) with automatic rotation
- **Storage**: HttpOnly cookies with Secure flag
- **Protection**: CSRF tokens, rate limiting
```

## Processing AI Responses

After receiving a response with markers from the AI:

1. Copy the entire response to your clipboard
2. Run the message router script to process the markers:
   ```bash
   cd god_mode/scripts
   ./route --clipboard
   ```
3. The script will automatically extract content from each marker and route it to the appropriate files

## Automating the Process

For greater automation:

1. Run the script in watch mode to automatically process clipboard changes:
   ```bash
   cd god_mode/scripts
   ./route --watch
   ```
2. Copy AI responses to your clipboard when received
3. The script will detect the change and process the markers automatically

## Troubleshooting

If content is not being properly routed:

- Check that markers are properly formatted with square brackets
- Ensure there's a space after the marker name and colon (for parameterized markers)
- For multi-tags, ensure the tag list is comma-separated
- Verify the script is running with proper permissions
- Check if the target files and directories exist and are writable
- Look for error messages in the script output

## Tag Formats

The message router supports two tag formats:

### 1. Bracket-Style Tags (Legacy)

```
[TAG]content
```

These are the original tag format where content follows the tag marker.

### 2. XML-Style Tags (Recommended)

```
<TAG>content</TAG>
```

XML-style tags provide clear boundaries for content and are preferred for several reasons:

- Content boundaries are explicitly defined
- Content is copied verbatim to memory files
- Same content can be tagged with multiple tags
- Complex formatting is preserved exactly as written

The message router will process both formats, but XML-style tags are recommended for all new content.

## Examples with XML-Style Tags

### Basic Usage

```
<LOG_SUMMARY>
Added user profile editing functionality to the account settings page.
</LOG_SUMMARY>

<LOG_DETAIL>
Implemented user profile editing with the following features:
- Field validation for email, username, and phone
- Image upload for profile photos with drag-and-drop
- Automatic saving with visual feedback
- Responsive design for mobile and desktop interfaces

This required changes to:
1. `UserProfile.tsx` component
2. `userAPI.ts` for backend communication
3. `validation.ts` for field validation logic
</LOG_DETAIL>

<MEMORY_UPDATE>
The user profile system now supports inline editing and image uploads. Field validation follows the same pattern as the registration form, reusing the validation utilities.
</MEMORY_UPDATE>

### Feature-Specific Updates

```
<FEATURE: Authentication>
Added password reset functionality with email verification. The system now sends a time-limited token to the user's registered email address, which can be used to reset their password. The token expires after 30 minutes for security reasons.
</FEATURE: Authentication>
```

### Multiple Tags for Same Content

With XML-style tags, you can apply multiple tags to the same content when it fits multiple categories:

```
<MEMORY_SECURITY>
All API endpoints now require authentication tokens. Anonymous access has been disabled except for the login and registration endpoints.
</MEMORY_SECURITY>

<MEMORY_UPDATE>
All API endpoints now require authentication tokens. Anonymous access has been disabled except for the login and registration endpoints.
</MEMORY_UPDATE>
```

This is more explicit than the previous multi-tag system and ensures content is preserved exactly as written.

---

By consistently using these markers in AI responses, you'll maintain comprehensive documentation and memory that evolves with your project, enabling more effective AI assistance. 