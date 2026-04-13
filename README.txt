IRIS DENTAL MEDICAL — WEBSITE
==============================

FOLDER STRUCTURE
----------------
iris-site/
├── index.html          ← Main homepage
├── blog.html           ← Blog index (list of posts)
├── README.txt          ← This file
├── images/             ← Put all images here
│   ├── logo.png        ← Your logo (extract from current site or re-upload)
│   ├── favicon.png     ← Small icon for browser tab
│   └── dr-kaneshima.jpg  ← Dr. Kaneshima's photo
└── posts/              ← One HTML file per blog post
    └── post-template.html  ← COPY THIS for every new post


HOW TO ADD A BLOG POST
-----------------------
1. Copy posts/post-template.html
2. Rename it: posts/your-post-title.html
3. Open it and find all the "CHANGE:" comments — update:
   - <title> tag
   - Post tag (e.g. "Preventive Care")
   - Post title (h1)
   - Date and author
   - Post body content
4. Open blog.html and add a new .blog-card block
   (copy the sample card already there and update the fields)
5. Upload the whole folder to Netlify


HOW TO DEPLOY TO NETLIFY
-------------------------
1. Go to netlify.com → sign up free
2. Drag and drop this entire "iris-site" folder onto the Netlify dashboard
3. Your site goes live instantly at a random URL (e.g. sunny-dental-123.netlify.app)
4. Go to Domain Settings → add your custom domain
5. To update the site: just drag and drop the folder again


IMAGES
------
- logo.png: The Iris Dental logo. Currently embedded as base64 in the old code.
  Extract it by opening the old Squarespace page, right-click the logo → Save image.
- dr-kaneshima.jpg: Same — right-click the photo on the existing site → Save image.
- favicon.png: A small square version of your logo (32x32 or 64x64 px).
  If you don't have one, just delete the favicon line in <head> for now.
- Post images: Any JPG/PNG works. Put them in images/ and reference as
  ../images/your-file.jpg from inside the posts/ folder.


NEED HELP?
----------
Just describe what you want to Claude:
- "Add a blog post about spring dental tips"
- "Add an insurance section to the homepage"
- "Update the hours to include Sunday"
Claude will generate the code and you paste/replace.
