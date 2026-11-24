# Makueni Pamoja Funeral Home: new website

```
funeral-site/
├── frontend/                 static site (HTML, CSS, JS), no build step
│   ├── index.html  about.html  services.html  gallery.html  contact.html
│   ├── admin/index.html      owner login: upload/delete photos, read messages
│   ├── css/styles.css
│   ├── js/config.js          phone, WhatsApp, API URL, image URLs: edit here
│   ├── js/main.js            header/footer, gallery, contact form
│   ├── .htaccess             301 redirects from old WordPress URLs (cPanel)
│   └── robots.txt
└── backend/                  FastAPI
    ├── main.py  config.py  database.py  models.py  schemas.py
    ├── auth.py  cloudinary_service.py
    ├── routers/ auth.py  gallery.py  contact.py
    ├── scripts/ migrate_wp_media.py  wp_media_urls.txt (70 files from the old site)
    ├── requirements.txt
    └── .env.example
```

## 1. Run the backend locally
```bash
cd backend
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then fill in Cloudinary keys, ADMIN_PASSWORD, JWT_SECRET
uvicorn main:app --reload     # API docs at http://localhost:8000/docs
```
The app refuses admin login until ADMIN_PASSWORD and JWT_SECRET are set.

## 2. Run the frontend locally
```bash
cd frontend
python -m http.server 5500    # open http://localhost:5500
```

## 3. Move the old photos and videos into Cloudinary
With `.env` filled in, from `backend/`:
```bash
python -m scripts.migrate_wp_media
```
Cloudinary downloads each file straight from the live old site, so run this
**before** the WordPress site is switched off. Logos and icons are skipped.
Everything lands in the gallery (visible on gallery.html and in /admin).
Then, in `frontend/js/config.js`, swap the `img` URLs for the Cloudinary ones
(copy them from your Cloudinary dashboard). Compress the two WhatsApp videos
first if you want them to load fast on mobile data.

## 4. Deploy
- **Backend:** Render, Railway or Fly.io (or cPanel "Setup Python App" if available).
  Set the same variables as `.env` in the host's settings. SQLite is wiped on
  free hosts that have no persistent disk; use their free Postgres and set
  DATABASE_URL (also `pip install psycopg2-binary`).
- **Frontend:** upload the contents of `frontend/` to `public_html` in cPanel
  (after taking a full backup). Set `api` in `js/config.js` to the backend URL
  and add the site's domain to `CORS_ORIGINS`.
- **Redirects:** `.htaccess` keeps the old WordPress URLs working (301).

## To confirm with the client
- WhatsApp number and opening hours (config.js)
- Exact map location (contact.html currently centres on Wote)
- Text for coffins, body transfer and exhumation: the old site had none, so
  those sections are short placeholders written from the homepage list
- Whether to keep "Leading World Facility", and a professional email address
- Optional later: obituaries / condolence pages

## Production checklist (frontend)
- `js/config.js`: set `api` to the deployed backend URL, confirm WhatsApp and hours.
- Domain: `sitemap.xml`, `robots.txt`, canonical tags and the structured data in `index.html`
  use https://www.makuenipamojafuneralhome.co.ke. Change it everywhere if the domain differs.
- `.htaccess` forces HTTPS; remove those three lines if the host has no SSL certificate yet.
- `404.html` is served by `.htaccess` for missing pages. `admin/` still uses `css/styles.css`;
  the public pages use `css/site.css`.
- Submit the sitemap in Google Search Console after launch.

## Images and videos (bundled)
All photos and videos from the old WordPress site are now in `frontend/img/` (videos in
`frontend/img/video/`, compressed to 720p). `js/config.js` points to them, so the site no longer
depends on the old WordPress server. The gallery shows these files until the backend is live;
once it is, the Cloudinary migration (section 3) is optional.
