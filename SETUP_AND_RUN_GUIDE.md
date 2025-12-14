# Sweet Shop Full Stack Application - Setup & Run Guide

## Project Structure

```
sweet-shop-fast/
├── sweet-shop-backend/       # FastAPI backend
│   ├── app/
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── routers/
│   │       ├── auth.py
│   │       ├── sweets.py
│   │       └── inventory.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_sweets.py
│   │   └── test_inventory.py
│   ├── conftest.py
│   └── requirements.txt
│
└── sweet-shop-frontend/      # React TypeScript frontend
    ├── src/
    │   ├── components/
    │   ├── styles/
    │   ├── api.ts
    │   ├── App.tsx
    │   └── main.tsx
    └── package.json
```

## System Requirements

- Python 3.11+
- Node.js 16+
- npm or yarn
- Git

## Part 1: Backend Setup & Run

### 1.1 Navigate to Backend Directory

```bash
cd sweet-shop-fast/sweet-shop-backend
```

### 1.2 Create Python Virtual Environment

```bash
python -m venv venv
```

### 1.3 Activate Virtual Environment

**Windows (PowerShell):**
```bash
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 1.4 Install Dependencies

```bash
pip install -r requirements.txt
```

### 1.5 Run Tests (Optional but Recommended)

```bash
pytest tests/ -v
```

Expected output: **25 passed in X.XXs**

### 1.6 Start Backend Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server should start on `http://localhost:8000`

### 1.7 Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Part 2: Frontend Setup & Run

### 2.1 Open New Terminal/PowerShell

Keep the backend running in the current terminal.

### 2.2 Navigate to Frontend Directory

```bash
cd sweet-shop-fast/sweet-shop-frontend
```

### 2.3 Install Dependencies

```bash
npm install
```

### 2.4 Start Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Part 3: Testing the Application

### 3.1 Access the Frontend

Open your browser and go to `http://localhost:5173`

### 3.2 Test User Registration

1. Click "Register here" link
2. Create a new account with:
   - Username: `testuser`
   - Password: `password123`
3. You'll be automatically logged in and redirected to dashboard

### 3.3 Test User Login

1. Click "Login here" link
2. Login with created credentials
3. You should see the dashboard with user info

### 3.4 Test Product Features

1. **Search Products**: Use the search bar on Products tab
2. **View Inventory**: Check the Inventory tab for stock levels
3. **Purchase**: Click Purchase on any product (reduces stock)

### 3.5 Test Admin Features

**Note**: Only admin users can access admin features.

To test admin features, you need to manually create an admin user in the database or modify a test user's role.

Admin capabilities:
- Create new sweets
- Edit product details
- Delete products
- Restock inventory

## API Endpoints Reference

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Products
- `GET /sweets/search?q=query` - Search products
- `POST /sweets` - Create product (admin only)
- `GET /sweets/{id}` - Get product details
- `PUT /sweets/{id}` - Update product (admin only)
- `DELETE /sweets/{id}` - Delete product (admin only)

### Inventory
- `GET /inventory` - Get all products with stock
- `POST /inventory/{id}/purchase` - Purchase product
- `POST /inventory/{id}/restock` - Restock product (admin only)

## Common Issues & Solutions

### Issue: Backend won't start
**Solution:**
- Check if port 8000 is already in use
- Run: `lsof -i :8000` (macOS/Linux) or `netstat -ano | findstr :8000` (Windows)
- Kill process or use different port: `python -m uvicorn app.main:app --port 8001`

### Issue: Frontend can't connect to backend
**Solution:**
- Verify backend is running on http://localhost:8000
- Check `api.ts` for correct API_BASE_URL
- Check browser console (F12) for CORS errors
- Ensure backend CORS middleware is enabled

### Issue: Tests fail
**Solution:**
- Ensure SQLite and all dependencies are installed
- Check Python version is 3.11+
- Try: `pip install --upgrade -r requirements.txt`
- Run: `pytest --version` to verify pytest installation

### Issue: "Port 5173 already in use"
**Solution:**
- Kill existing process or use: `npm run dev -- --port 5174`

### Issue: Login fails with "No such table: users"
**Solution:**
- This shouldn't happen, but restart backend to reinitialize test database
- Check backend logs for database errors

## Development Workflow

### Backend Development
1. Make changes to Python files
2. Server auto-reloads (if using `--reload`)
3. Tests run with: `pytest tests/ -v`
4. Check API at: http://localhost:8000/docs

### Frontend Development
1. Make changes to React/TypeScript files
2. Hot Module Replacement (HMR) auto-updates browser
3. Check console (F12) for errors
4. Build for production: `npm run build`

## Deployment

### Backend Deployment
```bash
# Using Uvicorn in production
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Or using Gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Frontend Deployment
```bash
# Build production version
npm run build

# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - Any static hosting
```

## Database

The application uses **SQLite** for development:
- Backend creates `sweet_shop.db` automatically
- Tests use in-memory SQLite (no file)
- Data persists between runs

### Reset Database (Backend)
Simply delete `sweet_shop.db` file and restart the server.

## Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: SQLAlchemy 2.0.23 + SQLite
- **Authentication**: JWT + SHA256
- **Testing**: Pytest 7.4.3
- **Validation**: Pydantic 2.5.0

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **Routing**: React Router v6
- **Styling**: CSS Grid + Flexbox

## Additional Commands

### Backend
```bash
# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=app tests/

# Format code
black app/

# Lint code
flake8 app/
```

### Frontend
```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Run ESLint
npm run lint
```

## Troubleshooting Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Python 3.11+ installed
- [ ] Node.js 16+ installed
- [ ] Virtual environment activated (backend)
- [ ] All dependencies installed
- [ ] No firewall blocking ports 8000/5173
- [ ] `access_token` stored in localStorage after login
- [ ] Browser console clear of errors (F12)

## Support

For issues or questions:
1. Check browser console (F12) for frontend errors
2. Check backend terminal for server errors
3. Review API logs at http://localhost:8000/docs
4. Check project README files for detailed documentation

---

**Application Status**: ✅ Ready for Development & Testing
**Total Tests**: 25 (All Passing)
**Frontend Components**: 5
**Backend Endpoints**: 11
