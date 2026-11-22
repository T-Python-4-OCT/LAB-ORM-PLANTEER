# CSS structure

`style.css` is the only stylesheet linked by `templates/base.html`. It imports the files below in the original cascade order. Keep this order unless intentionally changing precedence.

```text
css/
├── style.css                 Entry point and ordered imports
├── base/
│   └── foundation.css        Variables, reset, typography, container
├── layout/
│   ├── header.css            Announcement, branding, navigation
│   ├── sections.css          Shared section headings and spacing
│   └── footer.css            Footer columns and copyright
├── components/
│   ├── buttons.css           Buttons and variants
│   ├── forms.css             Inputs, labels, validation, actions
│   ├── notices.css           Feedback messages
│   ├── plant-card.css        Plant grids and reusable cards
│   └── ticker.css            Marquee appearance
├── pages/
│   ├── home/
│   │   ├── hero.css          Homepage introduction
│   │   └── sections.css      Categories, story, closing section
│   ├── collection.css        Search, filters, results, empty state
│   ├── plant-detail.css      Plant information, care, comments
│   ├── plant-form.css        Add/edit page layout
│   ├── plant-delete.css      Deletion confirmation
│   ├── contact.css           Contact page layout
│   └── messages.css          Community message board
├── responsive/
│   └── breakpoints.css       Existing viewport overrides
└── motion/
    ├── ticker.css            Seamless marquee and reduced motion
    └── accents.css           Reveal, hover, hero, back-to-top effects
```

Edit the file responsible for the feature. Shared controls belong in `components`; page-specific composition belongs in `pages`. Colors and fonts are defined in `base/foundation.css`. Existing responsive overrides stay together in `responsive/breakpoints.css`; motion-specific viewport and accessibility overrides stay with their effects.

Rules and declarations are expanded onto separate lines for readability. This is an organization change: selectors, values, and rule order are retained. The former `polish.css` is now `motion/accents.css`.
