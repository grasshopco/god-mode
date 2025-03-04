# Multi-Tag Feature Documentation

This document explains how to use the new multi-tag feature in God Mode to efficiently route content to multiple files without duplication.

## Overview

The multi-tag feature allows you to specify multiple destinations for a single piece of content. This is particularly useful when you want to add the same information to several memory or documentation files without repeating the same text multiple times.

## Basic Usage

The syntax for using the multi-tag feature is:

```
[MULTI_TAG: TAG1, TAG2, TAG3, ...]
Your content goes here. This content will be routed to all specified tags.
```

Where:
- `TAG1, TAG2, TAG3, ...` is a comma-separated list of tags
- The content that follows will be routed to all the specified tags

## Supported Tags

The multi-tag feature supports all standard memory tags, as well as feature logs and documentation updates:

### Standard Memory Tags
- LOG_SUMMARY
- LOG_DETAIL
- MEMORY_UPDATE
- MEMORY_LEARNINGS
- MEMORY_UPDATES
- MEMORY_REQUIREMENTS
- MEMORY_ROADMAP
- MEMORY_ARCHITECTURE
- MEMORY_CONVENTIONS
- MEMORY_DEPENDENCIES
- MEMORY_GLOSSARY
- MEMORY_TESTING
- MEMORY_SECURITY
- MEMORY_PERFORMANCE
- MEMORY_ACCESSIBILITY

### Parameterized Tags
- FEATURE_LOG:FeatureName
- DOC_UPDATE:DocumentType

## Examples

### Example 1: Route to Multiple Memory Files

```
[MULTI_TAG: MEMORY_UPDATE, MEMORY_ARCHITECTURE, MEMORY_CONVENTIONS]
The project now uses a modular architecture with clear separation of concerns.
Each module follows the repository pattern with standard naming conventions.
```

This will route the content to:
- MEMORY_CURSOR.md
- memory_architecture.md
- memory_conventions.md

### Example 2: Route to Logs and Features

```
[MULTI_TAG: LOG_SUMMARY, LOG_DETAIL, FEATURE_LOG:Authentication]
Implemented JWT authentication with refresh token rotation.
The system now supports secure authentication using JWT tokens with automatic refresh.
```

This will route the content to:
- memory_logs_all.md
- memory_logs_detailed.md
- memory_log_feature_authentication.md

### Example 3: Combining with Standard Tags

You can use multi-tags alongside standard tags in the same message:

```
[MULTI_TAG: LOG_SUMMARY, MEMORY_UPDATE]
Added multi-tag feature to the message router

[LOG_DETAIL]
Implemented a new multi-tag feature that allows routing content to multiple files without duplication.
The feature supports all standard memory tags as well as feature logs and documentation updates.

[FEATURE_LOG: GodMode]
Enhanced message router with multi-tag support
```

## Best Practices

1. **Group Related Tags**: Group tags that should contain similar content. For example, logs and feature updates often contain similar information.

2. **Be Specific with Parameterized Tags**: When using FEATURE_LOG: or DOC_UPDATE:, be specific about the feature or document type.

3. **Format Appropriately**: The content will be formatted consistently for all destinations, so ensure it's suitable for all target files.

4. **Limit Tag Count**: While you can include as many tags as needed, consider readability. If the list becomes too long, it might be better to use separate tags with more specific content.

5. **Include Context**: Since the same content goes to multiple destinations, ensure it contains sufficient context to make sense on its own.

## Technical Details

The multi-tag feature works by:
1. Parsing the tag list into individual tags
2. Matching each tag to its corresponding file path
3. Appending the content to each file with appropriate formatting

Each file still receives the content with proper timestamps and formatting, just as if it had been routed with individual tags.

---

*This feature helps make the God Mode system more efficient by reducing redundancy in AI responses while maintaining comprehensive documentation.* 