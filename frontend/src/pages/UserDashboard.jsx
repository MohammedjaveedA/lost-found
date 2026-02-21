import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import API from '../services/api';
import toast from 'react-hot-toast';
import { PlusIcon, CheckCircleIcon, XMarkIcon, PhoneIcon } from '@heroicons/react/24/outline';

export default function UserDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [filter, setFilter] = useState('all'); // Keep filter but only 'all' and 'lost' will work
  const [formData, setFormData] = useState({
    type: 'lost', // Default to lost, remove found option
    title: '',
    description: '',
    category: '',
    location: '',
    date: new Date().toISOString().split('T')[0],
    phone_number: ''
  });

  const categories = [
    'Electronics', 'Keys', 'Wallet', 'Phone', 'Books',
    'Accessories', 'Clothing', 'ID Card', 'Water Bottle', 'Other'
  ];

  useEffect(() => {
    console.log('UserDashboard - Current user:', user);
    
    if (user?.role === 'regular' && !user?.organization) {
      console.log('No organization, redirecting to home');
      navigate('/');
      return;
    }
    
    if (user?.organization) {
      console.log('Fetching items for organization:', user.organization.id);
      fetchItems();
    }
  }, [user, filter, navigate]);

  const fetchItems = async () => {
    try {
      setLoading(true);
      // Always fetch only lost items
      const url = '/items/?type=lost';
      const response = await API.get(url);
      console.log('Items fetched:', response.data);
      setItems(response.data.items);
    } catch (error) {
      console.error('Error fetching items:', error);
      toast.error('Failed to load items');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate phone number
    if (!formData.phone_number || formData.phone_number.length < 10) {
      toast.error('Please enter a valid 10-digit phone number');
      return;
    }

    try {
      // Always set type as 'lost'
      const itemData = { ...formData, type: 'lost' };
      await API.post('/items/', itemData);
      toast.success('Lost item posted successfully!');
      setShowForm(false);
      setFormData({
        type: 'lost',
        title: '',
        description: '',
        category: '',
        location: '',
        date: new Date().toISOString().split('T')[0],
        phone_number: ''
      });
      fetchItems();
    } catch (error) {
      console.error('Error posting item:', error);
      toast.error('Failed to post item');
    }
  };

  const handleResolve = async (itemId) => {
    try {
      await API.put(`/items/${itemId}/resolve`);
      toast.success('Item marked as resolved!');
      fetchItems();
    } catch (error) {
      console.error('Error resolving item:', error);
      toast.error('Failed to mark item as resolved');
    }
  };

  const handleDelete = async (itemId) => {
    if (!window.confirm('Are you sure you want to delete this item?')) return;
    try {
      await API.delete(`/items/${itemId}`);
      toast.success('Item deleted successfully!');
      fetchItems();
    } catch (error) {
      console.error('Error deleting item:', error);
      toast.error('Failed to delete item');
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  if (!user?.organization) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading your organization...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Lost Items Feed
              </h1>
              <p className="text-gray-600 mt-2">
                Organization: <span className="font-semibold text-blue-600">{user.organization.name}</span>
              </p>
            </div>
            <button
              onClick={() => setShowForm(!showForm)}
              className="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
            >
              <PlusIcon className="h-5 w-5 mr-1" />
              Report Lost Item
            </button>
          </div>
        </div>

        {/* Post Form */}
        {showForm && (
          <div className="bg-white rounded-lg border border-gray-200 p-6 mb-8 shadow-sm">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Report Lost Item</h2>
              <button
                onClick={() => setShowForm(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <XMarkIcon className="h-6 w-6" />
              </button>
            </div>
            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Removed type selection - always lost */}

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Title
                </label>
                <input
                  type="text"
                  name="title"
                  required
                  value={formData.title}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                  placeholder="e.g., Blue Water Bottle"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  name="description"
                  required
                  value={formData.description}
                  onChange={handleChange}
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                  placeholder="Describe the item in detail..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Category
                </label>
                <select
                  name="category"
                  required
                  value={formData.category}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                >
                  <option value="">Select category</option>
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Location where it was lost
                </label>
                <input
                  type="text"
                  name="location"
                  required
                  value={formData.location}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                  placeholder="e.g., Library, 2nd Floor"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date lost
                </label>
                <input
                  type="date"
                  name="date"
                  required
                  value={formData.date}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                />
              </div>

              {/* Phone Number Field - Mandatory */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Your Phone Number <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <PhoneIcon className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="tel"
                    name="phone_number"
                    required
                    value={formData.phone_number}
                    onChange={handleChange}
                    className="w-full pl-10 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-gray-900"
                    placeholder="e.g., 9876543210"
                    pattern="[0-9]{10}"
                    title="Please enter a valid 10-digit phone number"
                  />
                </div>
                <p className="mt-1 text-xs text-gray-500">
                  Others will call this number if they find your item
                </p>
              </div>

              <div className="flex space-x-3 pt-2">
                <button
                  type="submit"
                  className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                >
                  Report Lost Item
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="bg-gray-500 text-white px-6 py-2 rounded-lg font-medium hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

      

        {/* Items List */}
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p className="text-gray-500">Loading lost items...</p>
          </div>
        ) : items.length === 0 ? (
          <div className="bg-white rounded-lg border border-gray-200 p-12 text-center">
            <div className="text-gray-400 mb-4">
              <svg className="h-16 w-16 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No lost items reported</h3>
            <p className="text-gray-500 mb-4">
              Be the first to report a lost item in your organization
            </p>
            <button
              onClick={() => setShowForm(true)}
              className="inline-flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              <PlusIcon className="h-5 w-5 mr-1" />
              Report Lost Item
            </button>
          </div>
        ) : (
          <div className="space-y-4">
            {items.map((item) => (
              <div
                key={item.id}
                className={`bg-white rounded-lg border border-gray-200 p-6 shadow-sm hover:shadow-md transition ${
                  item.status === 'resolved' ? 'opacity-75 bg-gray-50' : ''
                }`}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-3">
                      <span className="px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-800">
                        LOST
                      </span>
                      {item.status === 'resolved' && (
                        <span className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-xs font-semibold">
                          RESOLVED
                        </span>
                      )}
                      {item.user.id === user?.id && (
                        <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-xs font-semibold">
                          YOUR POST
                        </span>
                      )}
                    </div>
                    
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">{item.title}</h3>
                    <p className="text-gray-600 mb-4">{item.description}</p>
                    
                    <div className="grid grid-cols-2 gap-2 text-sm text-gray-500 mb-3">
                      <div>
                        <span className="font-medium">Category:</span> {item.category}
                      </div>
                      <div>
                        <span className="font-medium">Location:</span> {item.location}
                      </div>
                      <div>
                        <span className="font-medium">Date:</span> {item.date}
                      </div>
                      <div>
                        <span className="font-medium">Posted by:</span> {item.user.name}
                      </div>
                    </div>

                    {/* Phone Number Display */}
                    {item.phone_number && (
                      <div className="mt-4 pt-3 border-t border-gray-100">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center text-gray-700">
                            <PhoneIcon className="h-5 w-5 text-green-600 mr-2" />
                            <span className="font-medium">Contact:</span>
                            <span className="ml-2 text-gray-900">{item.phone_number}</span>
                          </div>
                          <a
                            href={`tel:${item.phone_number}`}
                            className="inline-flex items-center bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition text-sm font-medium"
                          >
                            <PhoneIcon className="h-4 w-4 mr-2" />
                            Call Now
                          </a>
                        </div>
                        <p className="text-xs text-gray-500 mt-2">
                          {item.user.id === user?.id 
                            ? 'This is your contact number' 
                            : 'Call this number if you found this item'}
                        </p>
                      </div>
                    )}
                  </div>
                  
                  {/* Delete button for all users? Or only for post owner? */}
                  {item.user.id === user?.id && (
                    <div className="flex space-x-2 ml-4">
                      {item.status === 'open' && (
                        <button
                          onClick={() => handleResolve(item.id)}
                          className="text-green-600 hover:text-green-800 p-2 hover:bg-green-50 rounded-lg transition"
                          title="Mark as resolved"
                        >
                          <CheckCircleIcon className="h-6 w-6" />
                        </button>
                      )}
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="text-red-600 hover:text-red-800 p-2 hover:bg-red-50 rounded-lg transition"
                        title="Delete"
                      >
                        <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}