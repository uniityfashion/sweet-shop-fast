# 🍰 Sweet Shop Management System

A complete full-stack web application for managing a sweet shop, featuring user authentication, product catalog, and inventory management.

## 📋 Project Overview

The Sweet Shop Management System is a comprehensive solution built with:
- **Backend**: FastAPI with SQLAlchemy ORM and JWT authentication
- **Frontend**: React with TypeScript and modern UI
- **Database**: SQLite for development
- **Testing**: Comprehensive test suite with 25+ tests (100% passing)

## ✨ Features

### 🔐 User Authentication
- User registration with validation
- Secure JWT-based login
- Password hashing with SHA256
- Role-based access control (Admin/User)
- Automatic token refresh and logout

### 🍬 Product Management
- Search products by name or description
- View detailed product information
- Create new products (admin only)
- Edit product details (admin only)
- Delete products (admin only)
- Real-time inventory visibility

### 📦 Inventory Management
- View current stock levels
- Purchase products (reduces stock)
- Restock inventory (admin only)
- Stock validation (prevent overselling)
- Inventory value calculation

### 📊 Dashboard
- Real-time statistics
- Total product count
- Total stock overview
- Inventory value tracking
- Responsive design for all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 16+
- npm or yarn

### Backend Setup (5 minutes)

```bash
# Navigate to backend directory
cd sweet-shop-fast/sweet-shop-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\Activate.ps1
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Start backend server
python -m uvicorn app.main:app --reload
```

Backend runs on: **http://localhost:8000**

### Frontend Setup (5 minutes)

```bash
# In a new terminal, navigate to frontend directory
cd sweet-shop-fast/sweet-shop-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on: **http://localhost:5173**

## 📁 Project Structure

```
sweet-shop-fast/
│
├── sweet-shop-backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── database.py          # SQLAlchemy config
│   │   ├── models.py            # ORM models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── auth.py              # Auth logic
│   │   └── routers/
│   │       ├── auth.py          # Auth endpoints
│   │       ├── sweets.py        # Products endpoints
│   │       └── inventory.py     # Inventory endpoints
│   │
│   ├── tests/
│   │   ├── test_auth.py         # 9 auth tests
│   │   ├── test_sweets.py       # 9 product tests
│   │   └── test_inventory.py    # 7 inventory tests
│   │
│   ├── conftest.py              # Pytest configuration
│   ├── pytest.ini               # Pytest settings
│   ├── requirements.txt         # Python dependencies
│   └── PROJECT_COMPLETION.md    # Backend summary
│
├── sweet-shop-frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Login.tsx        # Login form
│   │   │   ├── Register.tsx     # Registration form
│   │   │   ├── Dashboard.tsx    # Main dashboard
│   │   │   └── ProtectedRoute.tsx # Route protection
│   │   │
│   │   ├── styles/
│   │   │   ├── Auth.css         # Auth pages styling
│   │   │   └── Dashboard.css    # Dashboard styling
│   │   │
│   │   ├── api.ts               # Axios client
│   │   ├── App.tsx              # Main app component
│   │   └── main.tsx             # Entry point
│   │
│   ├── package.json
│   └── README.md
│
├── SETUP_AND_RUN_GUIDE.md       # Complete setup instructions
└── README.md                    # This file
```

## 🧪 Testing

The backend includes comprehensive test coverage:

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage report
pytest --cov=app tests/
```

### Test Coverage
- ✅ **9 Authentication Tests**: Registration, login, token validation
- ✅ **9 Product Tests**: Search, CRUD with role-based access
- ✅ **7 Inventory Tests**: Stock management, purchase, restock

**Total: 25 tests - 100% passing**

## 🔌 API Endpoints

### Authentication
```
POST   /auth/register              Register new user
POST   /auth/login                 Login and get token
GET    /auth/me                    Get current user
```

### Products
```
GET    /sweets/search?q={query}   Search products
POST   /sweets                     Create product (admin)
GET    /sweets/{id}                Get product details
PUT    /sweets/{id}                Update product (admin)
DELETE /sweets/{id}                Delete product (admin)
```

### Inventory
```
GET    /inventory                  Get all products
POST   /inventory/{id}/purchase   Purchase product
POST   /inventory/{id}/restock    Restock (admin)
```

## 🛠 Technology Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.104.1 | Web framework |
| SQLAlchemy | 2.0.23 | ORM |
| Pydantic | 2.5.0 | Data validation |
| Pytest | 7.4.3 | Testing |
| Python-Jose | 3.3.0 | JWT handling |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 18 | UI library |
| TypeScript | Latest | Type safety |
| Vite | 7.2 | Build tool |
| Axios | Latest | HTTP client |
| React Router | 6 | Navigation |

### Database
- **SQLite** for development
- In-memory database for testing
- Easy migration to PostgreSQL/MySQL for production

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ SHA256 password hashing with salt
- ✅ Role-based access control (RBAC)
- ✅ Protected routes
- ✅ CORS middleware configured
- ✅ Input validation with Pydantic
- ✅ Secure token storage in localStorage
- ✅ Automatic logout on token expiration

## 📱 Responsive Design

The frontend is fully responsive and works on:
- ✅ Desktop browsers
- ✅ Tablets
- ✅ Mobile phones

Features CSS Grid and Flexbox for adaptive layouts.

## 🎯 User Roles

### Admin
- Full product management (create, read, update, delete)
- Inventory management (restock)
- View all products and inventory

### User
- Search and browse products
- Purchase products
- View inventory levels
- Access personal dashboard

## 📊 Database Schema

### Users Table
```
- id (Primary Key)
- username (Unique)
- hashed_password
- role (ADMIN | USER)
```

### Sweets Table
```
- id (Primary Key)
- name
- description
- price
- stock
```

## 🚀 Deployment

### Backend Deployment
```bash
# Using Uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Environment variables needed:
# - DATABASE_URL (for production DB)
# - TESTING (set to false)
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Deploy dist/ folder to:
# - Vercel
# - Netlify  
# - AWS S3
# - Any static hosting service
```
## 🖼️ User Interface Screenshots

This section documents the primary user-facing screens for authentication in the Sweet Shop Management System frontend.

### 1. Login Page

This is the entry point for all users (Admin and regular Users). It captures the `Username` and `Password` credentials required for JWT-based authentication.

| Screenshot | Description |
| :---: | :--- |
| <img width="810" height="540" alt="Screenshot (614)" src="https://github.com/user-attachments/assets/7e7a2d14-5c01-4280-ad03-7001bd1fbd0e" /> |The primary login interface, allowing users to enter credentials or navigate to the registration page via the "Register here" link. |

### 2. Registration Page

This screen is used by new customers or staff to create an account by providing a username and matching passwords.

| Screenshot | Description |
| :---: | :--- |
| <img width="810" height="540" alt="Screenshot (617)" src="https://github.com/user-attachments/assets/3220e199-8cc3-42ee-901e-84617dd8a9c5" /> | The user registration form. The system enforces password matching and security rules upon submission. |

### 3. Registration Failure

This screenshot illustrates the system's feedback mechanism when a registration attempt fails, often due to an existing username or a password validation error.

| Screenshot | Description |
| :---: | :--- |
|  <img width="810" height="540" alt="Screenshot (616)" src="https://github.com/user-attachments/assets/f83f6454-f62f-46a8-a2cc-b3bc53cb89ef" /> | Error feedback indicating that the registration request, possibly for the username '22bcs12324', was rejected by the backend. |

### 4. Login Failure

This shows the user experience when invalid credentials (username or password) are provided during a login attempt, protecting the system from unauthorized access.

| Screenshot | Description |
| :---: | :--- |
| <img width="810" height="540" alt="Screenshot (615)" src="https://github.com/user-attachments/assets/5663ba40-93b1-4898-97f5-32db6c2cc027" /> | Error feedback indicating an unsuccessful login attempt for the user '22bcs12324', confirming the security mechanism is active. |

## 🐛 Troubleshooting

### Backend Won't Start
- Check if port 8000 is in use: `lsof -i :8000`
- Verify Python 3.11+ installed: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt --upgrade`

### Frontend Can't Connect to Backend
- Ensure backend running on http://localhost:8000
- Check `src/api.ts` for correct API_BASE_URL
- Look for CORS errors in browser console (F12)

### Tests Failing
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check pytest installed: `pytest --version`
- Verify Python version: `python --version`

### Port Already in Use
- Backend: `python -m uvicorn app.main:app --port 8001`
- Frontend: `npm run dev -- --port 5174`

## 📚 Documentation

- See [SETUP_AND_RUN_GUIDE.md](SETUP_AND_RUN_GUIDE.md) for detailed setup instructions
- See [sweet-shop-backend/PROJECT_COMPLETION.md](sweet-shop-backend/PROJECT_COMPLETION.md) for backend details
- See [sweet-shop-frontend/README.md](sweet-shop-frontend/README.md) for frontend details

## 🎓 Learning Resources

This project demonstrates:
- ✅ Full-stack web application development
- ✅ Test-Driven Development (TDD) methodology
- ✅ RESTful API design
- ✅ JWT authentication implementation
- ✅ Role-based access control
- ✅ React hooks and TypeScript
- ✅ Database design and ORM usage
- ✅ API documentation with Swagger

## 📈 Future Enhancements

- [ ] Order management system
- [ ] Customer ratings and reviews
- [ ] Email notifications
- [ ] Advanced inventory analytics
- [ ] Payment integration
- [ ] Admin dashboard with charts
- [ ] Product categories and filtering
- [ ] User profile management
- [ ] Real-time notifications
- [ ] API rate limiting


## 📄 License

This project is open source.

## ✅ Project Status

- **Backend**: ✅ Complete (Steps 1-5)
- **Frontend**: ✅ Complete
- **Tests**: ✅ 25/25 Passing
- **Documentation**: ✅ Complete
- **Production Ready**: ⚠️ Requires environment configuration

---

## 🎉 Getting Started

1. **Read** [SETUP_AND_RUN_GUIDE.md](SETUP_AND_RUN_GUIDE.md)
2. **Setup Backend**: Run backend installation and tests
3. **Setup Frontend**: Run frontend installation  
4. **Test**: Register a user and test all features
5. **Explore**: Check out the API docs at http://localhost:8000/docs

---

## My AI Usage

This project was developed with a strict commitment to transparency regarding the use of AI coding assistants, which significantly accelerated the development process while maintaining a strong focus on quality via Test-Driven Development (TDD).

### 7.1. Tools Used

* **GitHub Copilot (VS Code Extension):** Primary tool for real-time code suggestions, boilerplate generation, and accelerating the TDD cycle.
* **LLM (e.g., Gemini/ChatGPT):** Used for high-level architectural planning, complex configuration debugging, and generating high-quality documentation drafts.

### 7.2. How AI Was Leveraged

| Project Area | Task | Specific Contribution by AI |
| :--- | :--- | :--- |
| **Backend TDD** | **Test Writing** | Generated the initial structure for most of the **25+ tests** (in `test_auth.py`, `test_sweets.py`, etc.), including mock data setup and asserting API response status codes (e.g., asserting a `403 Forbidden` for non-admin attempts). |
| **Boilerplate** | **FastAPI Setup** | Scaffolded the initial `app/main.py` structure, including CORS middleware configuration and setting up the initial dependency injection for the SQLAlchemy database session. |
| **Data Models** | **Schema & ORM** | Suggested the Pydantic schemas (`schemas.py`) and SQLAlchemy ORM models (`models.py`) based on the table descriptions, ensuring correct type hints (e.g., `role: Literal['ADMIN', 'USER']` for the `Users` model). |
| **Frontend** | **Component Logic** | Assisted with the boilerplate for React functional components, state management using `useState` and `useEffect`, and the asynchronous Axios calls within `src/api.ts`. |
| **Debugging** | **Token Handling** | Helped identify and correct a subtle bug in the JWT token extraction process (the standard `Bearer ` prefix handling) during the implementation of the `oauth2_scheme` in `app/auth.py`. |

### 7.3. Co-Authorship & Reflection

* **Commit History:** All commits where Copilot provided substantial structural or logical suggestions were tagged using the required `Co-authored-by: GitHub Copilot <noreply@github.com>` trailer.
* **TDD Partnership:** AI was treated as a junior developer. I wrote the **Red** test first, allowed the AI to generate the first pass of the **Green** code, and then manually performed the **Refactor** step, often simplifying the AI's suggestions or enforcing role-based logic that the AI initially missed.
* **Conclusion:** AI assistance allowed the project to achieve a comprehensive feature set and **100% test coverage** within the planned timeline by automating syntax and repetitive tasks, thus letting me focus purely on the application's core business logic and security features.


---

**Created using FastAPI, React, and TypeScript**
