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

- **Font Family**: Inter, system-ui, sans-serif
- **Font Weights**:
  - Regular: 400
  - Medium: 500
  - Bold: 700
- **Font Sizes**:
  - Heading 1: 2.5rem
  - Heading 2: 2rem
  - Heading 3: 1.75rem
  - Heading 4: 1.5rem
  - Heading 5: 1.25rem
  - Heading 6: 1rem
  - Body: 1rem
  - Small: 0.875rem
  - Caption: 0.75rem

## Spacing

The spacing system uses a base unit of 4px:

- **Extra Small**: 4px (0.25rem)
- **Small**: 8px (0.5rem)
- **Medium**: 16px (1rem)
- **Large**: 24px (1.5rem)
- **Extra Large**: 32px (2rem)
- **2x Extra Large**: 48px (3rem)
- **3x Extra Large**: 64px (4rem)

## Component Guidelines

### Buttons

- **Primary Button**: Used for main actions
  - Background: Primary color
  - Text: White
  - Padding: 0.5rem 1rem
  - Border-radius: 0.25rem
  - Hover state: 10% darker than primary color
  - Active state: 15% darker than primary color
  - Disabled state: 50% opacity
  
- **Secondary Button**: Used for secondary actions
  - Background: Transparent
  - Border: 1px solid primary color
  - Text: Primary color
  - Padding: 0.5rem 1rem
  - Border-radius: 0.25rem
  - Hover state: 10% primary color background
  - Active state: 15% primary color background
  - Disabled state: 50% opacity

- **Text Button**: Used for tertiary actions
  - Background: Transparent
  - Text: Primary color
  - Padding: 0.5rem 1rem
  - Hover state: 10% primary color background
  - Active state: 15% primary color background
  - Disabled state: 50% opacity

- **Icon Button**: Used for compact actions
  - Size: 2.5rem x 2.5rem
  - Border-radius: 50% (circular) or 0.25rem (square)
  - Padding: 0.5rem
  - Center icon within button
  - Same hover/active/disabled states as other buttons

### Forms

- **Text Input**:
  - Height: 2.5rem
  - Border: 1px solid (light gray)
  - Border-radius: 0.25rem
  - Padding: 0.5rem
  - Focus state: Primary color border
  - Error state: Error color border
  - Disabled state: Light gray background, 50% opacity text

- **Text Area**:
  - Min-height: 5rem
  - Border: 1px solid (light gray)
  - Border-radius: 0.25rem
  - Padding: 0.5rem
  - Focus state: Primary color border
  - Error state: Error color border
  - Disabled state: Light gray background, 50% opacity text

- **Select**:
  - Height: 2.5rem
  - Border: 1px solid (light gray)
  - Border-radius: 0.25rem
  - Padding: 0.5rem
  - Custom dropdown icon
  - Focus state: Primary color border
  - Error state: Error color border
  - Disabled state: Light gray background, 50% opacity text

- **Checkbox and Radio**:
  - Custom styling with SVG icons
  - Size: 1rem x 1rem
  - Border-radius for checkbox: 0.125rem
  - Border-radius for radio: 50%
  - Focus state: Primary color border
  - Selected state: Primary color fill
  - Disabled state: 50% opacity

- **Form Labels**:
  - Position: Above input
  - Font-weight: Medium (500)
  - Margin-bottom: 0.25rem
  - Required field indicator: Red asterisk (*)

- **Form Validation**:
  - Error messages: Below input, error color
  - Success indicator: Green checkmark or border
  - Validation on: Blur or submit (form-dependent)

### Cards

- **Standard Card**:
  - Background: White or surface color
  - Border-radius: 0.5rem
  - Box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1)
  - Padding: 1rem
  - Sections: Header, content, footer

- **Action Card**:
  - Same as standard card
  - Hover state: Slight elevation increase
  - Cursor: pointer
  - Optional border: 1px solid (light gray)

- **Media Card**:
  - Same as standard card
  - Image container: Aspect ratio 16:9 or 4:3
  - Image border-radius-top: 0.5rem

### Navigation

- **Top Navigation**:
  - Height: 4rem
  - Background: White or primary color
  - Box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1)
  - Links: Horizontal layout with consistent spacing
  - Active state: Underline or color change
  - Mobile: Collapses to hamburger menu

- **Side Navigation**:
  - Width: 16rem
  - Background: White or light gray
  - Links: Vertical layout with consistent spacing
  - Active state: Highlight background, left border or color change
  - Mobile: Collapsible or slide-in menu

- **Tab Navigation**:
  - Border-bottom: 1px solid (light gray)
  - Active tab: Primary color indicator
  - Hover state: Light gray background
  - Padding: 0.5rem 1rem
  - Spacing between tabs: 1rem

- **Breadcrumbs**:
  - Separator: Forward slash (/) or custom icon
  - Current page: Bold or non-clickable
  - Font-size: 0.875rem
  - Truncation on mobile if needed

### Modals and Dialogs

- **Modal Container**:
  - Background: White or surface color
  - Border-radius: 0.5rem
  - Box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2)
  - Max-width: 90% of viewport
  - Max-height: 90% of viewport
  - Sections: Header, content, footer

- **Modal Overlay**:
  - Background: Black at 50% opacity
  - Covers entire viewport
  - Z-index: Higher than all other elements

- **Modal Header**:
  - Padding: 1rem
  - Border-bottom: 1px solid (light gray)
  - Close button: Top right corner

- **Modal Footer**:
  - Padding: 1rem
  - Border-top: 1px solid (light gray)
  - Button alignment: Right-aligned or justified

### Feedback Components

- **Toast Notifications**:
  - Position: Bottom center or top right
  - Background: Dark color with high contrast text
  - Border-radius: 0.25rem
  - Padding: 0.75rem 1rem
  - Auto-dismiss: After 3-5 seconds
  - Animation: Fade in/out or slide

- **Alert Banners**:
  - Full width
  - Background color based on type (info, warning, error, success)
  - Border-radius: 0.25rem
  - Padding: 0.75rem 1rem
  - Icon: Left-aligned based on type
  - Dismissible: Optional close button

- **Progress Indicators**:
  - Linear: Height of 0.25rem, primary color
  - Circular: SVG-based, 1.5rem diameter
  - Color: Primary for standard, different colors for different states
  - Animation: Smooth transitions

- **Loading States**:
  - Skeleton screens for content loading
  - Loading spinner for actions (circular, primary color)
  - Button loading: Replace text with spinner
  - Page loading: Full-page overlay with centered spinner

## Responsive Design

- **Breakpoints**:
  - Mobile: < 768px
  - Tablet: 768px - 1024px
  - Desktop: > 1024px

- **Grid System**:
  - 12-column grid
  - Gutters: 1rem (0.5rem on each side)
  - Container padding: 1rem on mobile, 2rem on tablet/desktop
  - Max-width container: 1200px for larger screens

- **Responsive Patterns**:
  - Stack columns on mobile
  - Reduce font sizes on mobile (html font-size: 14px vs 16px)
  - Hide non-essential elements on smaller screens
  - Convert multi-column layouts to single column
  - Use collapsible sections for complex content

## Accessibility Guidelines

- **Color Contrast**:
  - Text: Minimum 4.5:1 ratio against background
  - Large text: Minimum 3:1 ratio against background
  - UI components: Minimum 3:1 ratio against adjacent colors

- **Keyboard Navigation**:
  - All interactive elements must be keyboard accessible
  - Focus states must be clearly visible
  - Tab order must follow logical flow
  - Skip links for navigation

- **Screen Readers**:
  - All images must have alt text
  - ARIA labels for custom controls
  - ARIA landmarks for screen reader navigation
  - Semantic HTML for proper structure

- **Text Sizing**:
  - All text must be resizable up to 200%
  - No fixed pixel sizes for text
  - Line heights should be at least 1.5 for readability

- **Reduced Motion**:
  - Honor prefers-reduced-motion media query
  - Provide alternative non-animated experience

## Animation Guidelines

- **Purpose**: Animations should have a clear purpose (feedback, transitions, etc.)
- **Duration**:
  - Micro-interactions: 100-300ms
  - Page transitions: 200-500ms
  - Complex animations: 500-1000ms
- **Easing**:
  - Standard: ease-in-out (0.4, 0, 0.2, 1)
  - Enter: ease-out (0, 0, 0.2, 1)
  - Exit: ease-in (0.4, 0, 1, 1)
- **Properties to Animate**:
  - Prefer opacity and transform for performance
  - Avoid animating layout properties (width, height, top, left)
- **Performance**:
  - Use will-change for complex animations
  - Keep animations to GPU-accelerated properties
  - Test performance on low-end devices

---

*This document serves as a reference for UI implementation. Always consider the context and user needs when applying these guidelines.* 