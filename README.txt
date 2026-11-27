IRIS DENTAL MEDICAL — WEBSITE
==============================

Design: "Style A · Feels like home" (warm, photo-led).
Plain HTML + one shared stylesheet. No build step: edit a file, upload, done.


FOLDER STRUCTURE
----------------
iris-dental-site/
├── index.html            ← Home
├── treatments.html       ← Treatments
├── about.html            ← About us & Dr. Kaneshima
├── access.html           ← Access & hours
├── faq.html              ← FAQ (booking, cancellations, U.S. insurance, payment, treatments, visit)
├── privacy.html          ← Privacy policy
├── 404.html              ← "Page not found" page (Netlify uses it automatically)
├── sitemap.xml, robots.txt ← For Google. Add new pages to sitemap.xml
├── _redirects            ← Netlify: hides docs/, tools/, CLAUDE.md, README.txt from the public site
├── CLAUDE.md             ← Rules and clinic facts for Claude (read this first)
├── README.txt            ← This file
├── docs/                 ← Internal: analytics plan, monthly reports, backlog, photo list
├── tools/check_site.py   ← Run before publishing: python3 tools/check_site.py
├── css/
│   └── site.css          ← ALL styling (colours, fonts, spacing) for every page
├── js/
│   └── site.js           ← Mobile menu + booking-click tracking
├── images/
│   ├── logo-mark.png             ← Logo mark used in header, hero and footer
│   ├── dr-kaneshima-portrait.jpg ← Dr. Kaneshima's photo (high resolution)
│   ├── og-image.jpg              ← Image shown when the site is shared (1200×630)
│   ├── favicon.png               ← Browser-tab icon
│   ├── apple-touch-icon.png      ← Icon when saved to an iPhone home screen
│   └── (logo.png, dr-kaneshima.jpg, partnership-banner.png: old design, no longer used)


THINGS THAT APPEAR ON SEVERAL PAGES
-----------------------------------
If one of these changes, search all .html files for it and update every copy:
- Booking link:  https://irisdental.intakeq.com/booking
- Phone:         046-244-5818  (links use tel:+81462445818)
- Email:         irisdentalcaregate4@gmail.com
- Hours:         "9:00–17:00" — index.html (Access & hours section),
                 access.html (hours table), faq.html, the footer of every page,
                 and the "openingHoursSpecification" block near the top of index.html
- Insurance list: index.html (U.S. insurance card), faq.html
- Full list of clinic facts: CLAUDE.md
- Header menu and footer: same block on every page


ANALYTICS
---------
Google Tag Manager (GTM-TZVKB3WL) is installed on every page (top of <head> +
the <noscript> block right after <body>). Copy both blocks into any new page.
js/site.js sends book_click, book_medical_click and phone_click to the dataLayer.
Setup steps for GA4 and the monthly report routine: docs/analytics/measurement-plan.md


HOW TO DEPLOY TO NETLIFY
------------------------
1. Go to netlify.com → sign up free
2. Drag and drop this entire folder onto the Netlify dashboard
   (or connect the GitHub repository so every push deploys automatically)
3. Your site goes live instantly at a random URL (e.g. sunny-dental-123.netlify.app)
4. Go to Domain Settings → add your custom domain
5. To update the site: drag and drop the folder again (or push to GitHub)


PREVIEWING LOCALLY
------------------
Double-click index.html to open it in a browser. Everything works offline except
the web fonts (Lora and Poppins load from Google Fonts).


NEED HELP?
----------
Just describe what you want to Claude:
- "Add a question to the FAQ"
- "Add an FAQ section to the treatments page"
- "Update the hours to include Sunday"
