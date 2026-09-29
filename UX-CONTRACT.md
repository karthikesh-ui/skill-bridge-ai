# Skill Bridge-AI interaction contract

Career discovery saves answers locally and opens filtered results. A career card opens its details and sets the selected career. The details page links to pathway route choices; the selected route persists locally. Roadmap statuses, skill checks and profile fields persist only in the same browser. Returning to a career can change the selection without deleting prior progress. Every screen keeps the shared header and footer.

An API failure should show a readable next action. Empty search results ask the student to try another term. Guidance shows a busy state and returns either Gemini text or built-in text; the source is labeled. Eligibility and exam text are illustrative and direct the student to official sources. Selection controls use native buttons and select elements with keyboard operation. The profile's native select popup is intentionally operating-system owned.

## Canonical UI Map

| Capability | Canonical owner | Source of truth | Allowed variants | Verification |
|---|---|---|---|---|
| Select/Listbox | Native select | Profile and roadmap markup | Native OS popup | Keyboard selection and change event |
| Form | Profile form and shared input styles | `templates/profile.html`, `static/js/app.js` | Profile | Local save and reload |
| Scrollbar | Global stylesheet | `static/css/styles.css` | Browser-owned geometry | Stylesheet audit |
| Career navigation | Shared selected career helper | `static/js/app.js` | Explore and choose | API and page tests |
| Feedback | Inline status region | Page templates and scripts | Loading, success, error | Browser flow |
