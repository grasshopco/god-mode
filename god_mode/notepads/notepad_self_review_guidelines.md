# AI Self-Review Guidelines

This document outlines the process and criteria for AI self-review of generated code. Reference this document when conducting self-reviews to ensure thorough and consistent evaluation.

## Self-Review Process

1. **Initial Code Generation**: Generate code based on requirements
2. **Immediate Self-Review**: Review the generated code before presenting it
3. **Iterative Improvement**: Make necessary improvements based on the review
4. **Final Verification**: Verify that all issues have been addressed

## Review Criteria

### Correctness

- Does the code correctly implement the requested functionality?
- Are there any logical errors or edge cases not handled?
- Does the code handle all specified requirements?
- Are there any off-by-one errors or similar subtle bugs?

### Code Quality

- Is the code clean, readable, and well-organized?
- Are variable and function names descriptive and consistent?
- Is there appropriate commenting for complex logic?
- Is the code DRY (Don't Repeat Yourself)?
- Are functions focused on a single responsibility?
- Is error handling comprehensive and appropriate?

### Performance

- Are there any obvious performance issues?
- Are there more efficient algorithms or data structures that could be used?
- Are there any unnecessary computations or redundant operations?
- For frontend code, are there potential rendering performance issues?

### Security

- Are there any potential security vulnerabilities?
- Is user input properly validated and sanitized?
- Are there any potential injection attacks (SQL, XSS, etc.)?
- Is sensitive data properly protected?
- Are authentication and authorization properly implemented?

### Maintainability

- Is the code easy to understand and modify?
- Is the code structured in a way that makes future changes straightforward?
- Are there any "magic numbers" or hardcoded values that should be constants?
- Is the code modular and well-encapsulated?

### Compatibility

- Does the code work across all required browsers/platforms?
- Are there any browser-specific or platform-specific issues?
- Does the code handle different screen sizes and devices appropriately?

### Accessibility

- Does the UI code meet accessibility standards?
- Are there appropriate ARIA attributes where needed?
- Is the UI navigable via keyboard?
- Does the UI work well with screen readers?

### Testing

- Are there appropriate tests for the code?
- Do the tests cover edge cases and error scenarios?
- Are the tests clear and maintainable?

## Self-Review Checklist

Use this checklist for each self-review:

- [ ] Functionality is complete and correct
- [ ] Code follows project style guidelines
- [ ] Variable and function names are clear and descriptive
- [ ] Error handling is comprehensive
- [ ] Edge cases are considered and handled
- [ ] No obvious performance issues
- [ ] No security vulnerabilities
- [ ] Code is well-structured and maintainable
- [ ] Comments explain "why" not just "what"
- [ ] No unnecessary code or commented-out code
- [ ] Tests are included where appropriate

## Common Issues to Watch For

- Uncaught exceptions or unhandled errors
- Improper null/undefined checking
- Incorrect type handling
- Memory leaks (especially in frontend code)
- Race conditions in asynchronous code
- Hardcoded credentials or sensitive information
- Overly complex functions or components
- Inconsistent naming conventions
- Inadequate validation of inputs
- Missing error messages or unclear user feedback

## Improvement Process

When issues are identified during self-review:

1. Categorize the issue (correctness, quality, performance, etc.)
2. Determine the severity and priority
3. Make the necessary changes
4. Re-review the changes to ensure they don't introduce new issues
5. Document the changes and reasoning in the appropriate logs

---

*This document serves as a guide for AI self-review. The goal is to produce high-quality, maintainable, and correct code through systematic self-evaluation and improvement.* 