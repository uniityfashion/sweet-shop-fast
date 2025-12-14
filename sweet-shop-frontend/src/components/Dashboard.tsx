/* eslint-disable @typescript-eslint/no-unused-vars */
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api'
import '../styles/Dashboard.css'

interface User {
  id: number
  username: string
  role: 'admin' | 'user'
}

interface Sweet {
  id: number
  name: string
  description: string
  price: number
  stock: number
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null)
  const [sweets, setSweets] = useState<Sweet[]>([])
  const [activeTab, setActiveTab] = useState('dashboard')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    fetchUserData()
  }, [])

  const fetchUserData = async () => {
    try {
      const userResponse = await api.get('/auth/me')
      setUser(userResponse.data)
      
      const inventoryResponse = await api.get('/inventory')
      setSweets(inventoryResponse.data)
    } catch (err) {
      setError('Failed to load data')
      navigate('/login')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('username')
    navigate('/login')
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  return (
    <div className="dashboard">
      <nav className="navbar">
        <div className="navbar-brand">
          <h1>🍰 Sweet Shop</h1>
        </div>
        <div className="navbar-info">
          <span>Welcome, {user?.username}! ({user?.role?.toUpperCase()})</span>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </nav>

      <div className="tabs">
        <button
          className={`tab-button ${activeTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setActiveTab('dashboard')}
        >
          Dashboard
        </button>
        <button
          className={`tab-button ${activeTab === 'sweets' ? 'active' : ''}`}
          onClick={() => setActiveTab('sweets')}
        >
          Products
        </button>
        <button
          className={`tab-button ${activeTab === 'inventory' ? 'active' : ''}`}
          onClick={() => setActiveTab('inventory')}
        >
          Inventory
        </button>
        {user?.role === 'admin' && (
          <button
            className={`tab-button ${activeTab === 'admin' ? 'active' : ''}`}
            onClick={() => setActiveTab('admin')}
          >
            Admin Panel
          </button>
        )}
      </div>

      <div className="content">
        {error && <div className="error-message">{error}</div>}

        {activeTab === 'dashboard' && (
          <div className="dashboard-view">
            <h2>Dashboard</h2>
            <div className="stats-grid">
              <div className="stat-card">
                <h3>{sweets.length}</h3>
                <p>Total Products</p>
              </div>
              <div className="stat-card">
                <h3>{sweets.reduce((sum, s) => sum + s.stock, 0)}</h3>
                <p>Total Stock</p>
              </div>
              <div className="stat-card">
                <h3>${sweets.reduce((sum, s) => sum + (s.price * s.stock), 0).toFixed(2)}</h3>
                <p>Inventory Value</p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'sweets' && (
          <SweetsView user={user} onUpdate={fetchUserData} />
        )}

        {activeTab === 'inventory' && (
          <InventoryView sweets={sweets} user={user} onUpdate={fetchUserData} />
        )}

        {activeTab === 'admin' && user?.role === 'admin' && (
          <AdminPanel user={user} onUpdate={fetchUserData} />
        )}
      </div>
    </div>
  )
}

function SweetsView({ user, onUpdate }: { user: User | null; onUpdate: () => void }) {
  const [sweets, setSweets] = useState<Sweet[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    handleSearch()
  }, [])

  const handleSearch = async () => {
    setLoading(true)
    try {
      const response = await api.get('/sweets/search', {
        params: { q: searchQuery },
      })
      setSweets(response.data)
    } catch (err) {
      console.error('Search failed:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleEdit = async (sweetId: number) => {
    const newPrice = prompt('Enter new price:')
    if (newPrice) {
      try {
        await api.put(`/sweets/${sweetId}`, {
          name: 'Updated',
          description: 'Updated',
          price: parseFloat(newPrice),
          stock: 0,
        })
        onUpdate()
      } catch (err) {
        alert('Failed to update sweet')
      }
    }
  }

  const handleDelete = async (sweetId: number) => {
    if (window.confirm('Are you sure you want to delete this sweet?')) {
      try {
        await api.delete(`/sweets/${sweetId}`)
        onUpdate()
      } catch (err) {
        alert('Failed to delete sweet')
      }
    }
  }

  return (
    <div className="sweets-view">
      <h2>Products</h2>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search by name or description..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>

      <div className="sweets-grid">
        {sweets.map((sweet) => (
          <div key={sweet.id} className="sweet-card">
            <h3>{sweet.name}</h3>
            <p>{sweet.description}</p>
            <p className="price">${sweet.price.toFixed(2)}</p>
            {user?.role === 'admin' && (
              <div className="admin-actions">
                <button onClick={() => handleEdit(sweet.id)}>Edit</button>
                <button onClick={() => handleDelete(sweet.id)} className="delete-btn">Delete</button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function InventoryView({ sweets, user, onUpdate }: { sweets: Sweet[]; user: User | null; onUpdate: () => void }) {
  const handlePurchase = async (sweetId: number) => {
    const quantity = prompt('Enter quantity to purchase:')
    if (quantity) {
      try {
        await api.post(`/inventory/${sweetId}/purchase`, {
          quantity: parseInt(quantity),
        })
        alert('Purchase successful!')
        onUpdate()
      } catch (err: unknown) {
        alert(err.response?.data?.detail || 'Purchase failed')
      }
    }
  }

  const handleRestock = async (sweetId: number) => {
    if (user?.role !== 'admin') {
      alert('Only admins can restock')
      return
    }

    const quantity = prompt('Enter quantity to restock:')
    if (quantity) {
      try {
        await api.post(`/inventory/${sweetId}/restock`, {
          quantity: parseInt(quantity),
        })
        alert('Restocked successfully!')
        onUpdate()
      } catch (err) {
        alert('Restock failed')
      }
    }
  }

  return (
    <div className="inventory-view">
      <h2>Inventory Management</h2>
      <table className="inventory-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Stock</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {sweets.map((sweet) => (
            <tr key={sweet.id}>
              <td>{sweet.name}</td>
              <td>{sweet.stock}</td>
              <td>${sweet.price.toFixed(2)}</td>
              <td>
                <button onClick={() => handlePurchase(sweet.id)} className="action-btn">
                  Purchase
                </button>
                {user?.role === 'admin' && (
                  <button onClick={() => handleRestock(sweet.id)} className="action-btn">
                    Restock
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function AdminPanel({ user, onUpdate }: { user: User | null; onUpdate: () => void }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [price, setPrice] = useState('')
  const [loading, setLoading] = useState(false)

  const handleCreateSweet = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    try {
      await api.post('/sweets', {
        name,
        description,
        price: parseFloat(price),
        stock: 0,
      })
      alert('Sweet created successfully!')
      setName('')
      setDescription('')
      setPrice('')
      onUpdate()
    } catch (err) {
      alert('Failed to create sweet')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="admin-panel">
      <h2>Admin Panel</h2>
      <div className="admin-section">
        <h3>Create New Sweet</h3>
        <form onSubmit={handleCreateSweet}>
          <div className="form-group">
            <label>Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
              disabled={loading}
            />
          </div>
          <div className="form-group">
            <label>Price</label>
            <input
              type="number"
              step="0.01"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              required
              disabled={loading}
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Sweet'}
          </button>
        </form>
      </div>
    </div>
  )
}
