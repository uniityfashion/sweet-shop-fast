# Sweet Shop Frontend

A modern React TypeScript frontend for the Sweet Shop Management System built with Vite.

## Features

- **User Authentication**: Login and registration with JWT token-based auth
- **Product Catalog**: Search and browse sweet products
- **Inventory Management**: View stock levels and make purchases
- **Admin Panel**: Create, update, and delete products (admin only)
- **Responsive Design**: Works on desktop and mobile devices

## Prerequisites

- Node.js 16+ 
- npm or yarn
- Backend API running on http://localhost:8000

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Project Structure

```
src/
├── components/          # React components
│   ├── Login.tsx       # Login form component
│   ├── Register.tsx    # Registration form component
│   ├── Dashboard.tsx   # Main dashboard with tabs
│   └── ProtectedRoute.tsx # Route protection for authenticated users
├── styles/             # CSS stylesheets
│   ├── Auth.css       # Authentication page styles
│   └── Dashboard.css  # Dashboard styles
├── api.ts             # Axios API client configuration
├── App.tsx            # Main app component with routing
├── main.tsx           # Application entry point
└── index.css          # Global styles
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`. The API client:

- Automatically includes JWT token in Authorization header
- Handles token expiration and redirects to login
- Uses axios for HTTP requests

## Key Endpoints Used

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user
- `GET /sweets/search` - Search sweets
- `GET /inventory` - Get inventory
- `POST /sweets` - Create sweet (admin)
- `PUT /sweets/{id}` - Update sweet (admin)
- `DELETE /sweets/{id}` - Delete sweet (admin)
- `POST /inventory/{id}/purchase` - Purchase sweet
- `POST /inventory/{id}/restock` - Restock sweet (admin)

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Component Structure

Each major feature is organized into:
- **Login/Register**: Authentication views
- **Dashboard**: Main app container with tab navigation
- **SweetsView**: Product search and browsing
- **InventoryView**: Stock management
- **AdminPanel**: Product management (admin only)

## Styling

The application uses CSS Grid and Flexbox for responsive layouts with:
- Modern gradient backgrounds
- Smooth transitions and hover effects
- Mobile-first responsive design
- Consistent color scheme (purple gradient theme)

## Authentication Flow

1. User registers or logs in
2. Backend returns JWT access token
3. Token stored in localStorage
4. Token automatically included in all API requests
5. Protected routes require valid token
6. Expired tokens trigger automatic logout and redirect to login

## State Management

Uses React hooks (useState, useEffect) for:
- User authentication state
- Form input state
- Data fetching and caching
- UI state (active tabs, loading states)

## Error Handling

- API errors display user-friendly messages
- 401 responses trigger logout
- Form validation before submission
- Try-catch blocks for all async operations

## Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

---

**Status**: ✅ Complete
**Framework**: React 18 + TypeScript
**Build Tool**: Vite

The React Compiler is enabled on this template. See [this documentation](https://react.dev/learn/react-compiler) for more information.

Note: This will impact Vite dev & build performances.

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
