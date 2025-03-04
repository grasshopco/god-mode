# UI Guidelines

This document outlines the UI principles, component patterns, and styling guidelines for the project. Reference this document when implementing frontend components to ensure consistency.

## Design Principles

- **Clarity**: UI should be intuitive and minimize cognitive load
- **Consistency**: Similar elements should behave similarly
- **Feedback**: Actions should provide clear visual feedback
- **Efficiency**: Minimize steps needed to accomplish tasks
- **Accessibility**: Design for users with different abilities and preferences
- **Responsiveness**: Design should adapt gracefully across devices

## Color System

The project uses a custom theming system with these base colors:

- **Primary**: [Your primary color]
- **Secondary**: [Your secondary color]
- **Accent**: [Your accent color]
- **Background**: [Your background color]
- **Surface**: [Your surface color]
- **Error**: [Your error color]
- **Text**: [Your text colors]
  - Primary: [Your primary text color]
  - Secondary: [Your secondary text color]
  - Disabled: [Your disabled text color]

## Typography

- **Primary Font**: Inter, system-ui, sans-serif
- **Heading Sizes**:
  - H1: 2.5rem
  - H2: 2rem
  - H3: 1.75rem
  - H4: 1.5rem
  - H5: 1.25rem
  - H6: 1rem
- **Body Text**: 1rem
- **Small Text**: 0.875rem
- **Line Height**: 1.5 for body, 1.2 for headings

## Components

### Buttons

- **Primary**: Filled with primary color, white text
- **Secondary**: Outlined with primary color
- **Text**: No background, primary color text
- **Danger**: Filled with error color
- **Icon**: Icon only, can be filled or outlined

Buttons should have:
- Padding: 0.5rem 1rem (horizontal), 0.25rem 0.5rem (icon)
- Border-radius: 0.25rem
- Clear hover and active states
- Disabled state should be visually distinct

### Cards

- Slight elevation effect (box-shadow)
- Border-radius: 0.5rem
- Padding: 1rem
- Clear header, content, and actions sections
- Consistent spacing between elements

### Forms

- Labels should be clear and positioned above inputs
- Input fields should have:
  - Consistent height (2.5rem)
  - Clear focus states
  - Appropriate validation feedback
  - Helpful error messages
- Group related fields together
- Required fields should be marked

### Navigation

- Clear current section indicator
- Consistent hover/focus states
- Mobile navigation should collapse to a hamburger menu
- Navigation items should have adequate touch targets (min 44px)

## Layout Patterns

- Use a 12-column grid system for layout
- Maintain consistent spacing using a spacing scale
- Spacing scale: 0.25rem, 0.5rem, 1rem, 1.5rem, 2rem, 3rem, 4rem, 6rem
- Content should have max-width constraints for readability on large screens
- Breakpoints:
  - Mobile: < 768px
  - Tablet: 768px - 1024px
  - Desktop: > 1024px

## Accessibility Guidelines

- Maintain contrast ratio of at least 4.5:1 for text
- Ensure all interactive elements are keyboard navigable
- Provide alternative text for images
- Use semantic HTML elements
- Test with screen readers

## Animation and Transitions

- Keep animations subtle and purposeful
- Standard transition duration: 150ms - 300ms
- Use ease-in-out timing function for most transitions
- Avoid animations that could trigger motion sickness

## Icons

- Use consistent icon set throughout the application
- Icons should be clear and recognizable
- Provide text labels or tooltips for icons when their meaning may be ambiguous

---

*This document serves as a reference for UI implementation. Always consider the context and user needs when applying these guidelines.* 