# UI Quality Checklist

Use this checklist to review the interface. Apply items that fit the requested feature; do not add complexity just to satisfy every item.

## Product and visual design

- The page makes its purpose and primary action clear.
- Content follows a useful hierarchy. Spacing, typography, color, and component shapes feel consistent.
- The visual direction fits the product and request. Do not default to generic cards, gradients, or decoration without a reason.
- Existing design tokens and components are reused where they fit.

## Interaction and states

- Interactive elements respond to pointer and keyboard input.
- Forms explain required fields, validation failures, and submission results.
- Loading, empty, error, success, and disabled states appear where relevant.
- Navigation and dialogs have a clear way to continue or dismiss.
- Data mutations use the project's existing data flow. If only a local demonstration is possible, make that boundary clear.

## Responsive behavior

- Content remains readable at narrow and wide viewport sizes.
- Navigation, columns, controls, and tables adapt to available space.
- No important content or action is hidden behind hover-only behavior.

## Accessibility

- Use semantic landmarks, headings, buttons, links, and form controls.
- Associate labels and descriptions with inputs.
- Keep keyboard focus visible and interaction order predictable.
- Provide text alternatives for meaningful images and non-color cues for important status.
- Respect reduced-motion preferences when adding animation.
