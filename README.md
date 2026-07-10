Keja Go is a student housing platform focused on **Embu, Kenya** — specifically areas around University of Embu.

---

## Features

- **Area-based browsing** — Pick a neighbourhood (Gakwegori, Kangaru, Njukiri, etc.)
- **Search & filter** — Filter by price range, room type, or keyword search
- **Listing detail** — Full info, amenities, photos, and landlord contact
- **Contact landlords** — Send an enquiry directly from a listing
- **List your room** — Landlords can submit rooms with photos
- **User accounts** — Register and log in as a student or landlord
- **Favorites** — Students can save and manage favourite listings
- **Landlord dashboard** — Landlords can view, edit, and delete their own listings
- **Admin panel** — Password-protected admin dashboard at `#/jadmin` to verify/manage all listings and areas
- **Safety tips** — Help and guidance for students

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript (SPA with hash routing) |
| Backend | Python 3.10+, FastAPI |
| Database | SQLite (dev, via `aiosqlite`) / PostgreSQL (prod, via `asyncpg`) |
| Auth | JWT (`python-jose[cryptography]`) + bcrypt (`passlib[bcrypt]`) |
| ORM | SQLAlchemy 2.x (async) |
| Image storage | Local filesystem (`backend/uploads/`) |

## Getting Started (Local Development)

### 1. Create and activate a Python virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Seed the database

```bash
python -m backend.seed
```

### 4. Run the server

```bash
uvicorn backend.main:app --reload --port 8000
```

Open http://localhost:8000 in your browser.

> Locally, the app uses SQLite (zero-config, file stored at `backend/keja-go.db`).
> In production (Render), it uses PostgreSQL via the `DATABASE_URL` environment variable.
> To re-seed on PostgreSQL: `python -m backend.seed --force`

## Areas Covered

| Area | Description |
|------|-------------|
| Gakwegori | Near University of Embu Gate A |
| Kangaru | Market area, affordable rooms |
| Njukiri | Quiet residential |
| Iveche | Near the university |
| Kamiu | Student-friendly estate |
| Koimugo | Residential compound area |
| Town | Embu Town centre |
| Karurumo | Nearby residential |
| Kanyakumu | Growing student area |
| Kianjokoma | Mixed residential |

## Project Structure

```
housing/
├── README.md
├── AGENTS.md
├── requirements.txt
├── Procfile
├── runtime.txt
├── backend/
│   ├── main.py              # FastAPI app + static file serving
│   ├── database.py           # Async SQLAlchemy engine + session
│   ├── models.py             # SQLAlchemy ORM models (Listing, Area, User, Favorite)
│   ├── schemas.py            # Pydantic request/response schemas
│   ├── seed.py               # Database seeder (sample data)
│   ├── uploads/              # Uploaded images (gitignored)
│   └── routers/
│       ├── listings.py       # CRUD + search/filter for listings (ownership enforced)
│       ├── areas.py          # CRUD for areas (with lat/lng coordinates)
│       ├── contact.py        # Contact-landlord endpoint
│       ├── auth.py           # JWT auth: register, login, me, dependencies
│       └── favorites.py      # Favorites: add, remove, list
├── frontend/
│   ├── index.html            # SPA shell with dynamic auth nav
│   ├── css/
│   │   └── style.css         # All styles (responsive, admin, auth forms)
│   └── js/
│       ├── api.js            # API fetch wrappers (all endpoints)
│       ├── state.js          # App state object + filters + auth
│       ├── render.js         # HTML render functions per page
│       ├── router.js         # Hash-based SPA router + all event handlers
│       └── app.js            # Entry point
└── images/                   # Static placeholder images
```

## API Endpoints

### Listings
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/listings` | List listings (query: `city`, `area`, `min_price`, `max_price`, `listing_type`, `search`, `verified`, `owner_id`) |
| GET | `/api/listings/:id` | Get a single listing |
| POST | `/api/listings` | Create a listing (multipart form with optional images) |
| PUT | `/api/listings/:id` | Update a listing (ownership enforced) |
| DELETE | `/api/listings/:id` | Delete a listing (ownership enforced) |

### Auth
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Register a new user (student or landlord) |
| POST | `/api/auth/login` | Login, returns JWT + user data |
| GET | `/api/auth/me` | Get current user from token |

### Favorites
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/favorites` | List current user's favorites (with listing data) |
| POST | `/api/favorites/:id` | Add a listing to favorites |
| DELETE | `/api/favorites/:id` | Remove a listing from favorites |

### Other
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/areas` | List areas within Embu with lat/lng coordinates |
| POST | `/api/areas` | Create a new area (admin) |
| DELETE | `/api/areas/:id` | Delete an area (admin, blocked if listings reference it) |
| POST | `/api/contact/:id` | Submit a contact enquiry for a listing |
| GET | `/api/images/:filename` | Serve uploaded images |

## Frontend Routes

| Route | Page |
|-------|------|
| `#/` | Home (hero + area grid + featured listings) |
| `#/browse` | Browse / filter all listings |
| `#/listing/:id` | Listing detail with contact form |
| `#/add` | Add a new listing |
| `#/login` | Sign in |
| `#/register` | Create account (student or landlord) |
| `#/logout` | Log out |
| `#/my-listings` | Landlord dashboard (edit/delete own listings) |
| `#/favorites` | Student saved listings |
| `#/about` | Safety tips & about |
| `#/jadmin` | Admin dashboard (password-protected) |

## License

MIT
