import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  Users, 
  Mail,
  UserPlus,
  ToggleLeft
} from 'lucide-react';
import EmailForm from './EmailForm';
import AuthStatus from './AuthStatus';
import { getContacts } from '../services/api';
import axios from 'axios';
import EmailGroups from './EmailGroups';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { toast } from 'react-hot-toast';
import WeekSelector from './WeekSelector';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', key: 'dashboard' },
    { icon: Users, label: 'Contacts', key: 'contacts' },
    { icon: Mail, label: 'Email Sequences', key: 'sequences' },
    { icon: UserPlus, label: 'Email Groups', key: 'groups' },
    { icon: ToggleLeft, label: 'Week Selector', key: 'selector' }
  ];

  const renderContent = () => {
    switch(activeTab) {
      case 'dashboard':
        return <DashboardContent />;
      case 'contacts':
        return <ContactsSection />;
      case 'sequences':
        return <EmailSequencesSection />;
      case 'groups':
        return <EmailGroups />;
      case 'selector':
        return <WeekSelector />;
      default:
        return <DashboardContent />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-100 pt-24">
      {/* Sidebar */}
      <div className="fixed left-0 top-24 h-[calc(100vh-6rem)] w-64 bg-white shadow-md">
        <div className="p-5 border-b">
          <h1 className="text-2xl font-bold text-[#c41e3a]">US Observer</h1>
        </div>
        <nav className="p-4">
          {navItems.map(item => {
            const Icon = item.icon;
            return (
              <button 
                key={item.key}
                onClick={() => setActiveTab(item.key)}
                className={`
                  flex items-center w-full p-3 mb-2 rounded 
                  ${activeTab === item.key 
                    ? 'bg-red-100 text-[#c41e3a]' 
                    : 'hover:bg-gray-100'}
                `}
              >
                <Icon />
                <span className="ml-3">{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="ml-64 flex-1 p-10 overflow-y-auto">
        <AuthStatus />
        {renderContent()}
      </div>
    </div>
  );
};

const DashboardContent = () => {
  const [sequenceStats, setSequenceStats] = useState([
    // Updated default stats structure
    { sequence_id: 1, sequence_name: 'Week 1', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 2, sequence_name: 'Week 2', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 3, sequence_name: 'Week 3', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 4, sequence_name: 'Week 4', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 5, sequence_name: 'Week 5', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 6, sequence_name: 'Week 6', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 7, sequence_name: 'Week 7', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 8, sequence_name: 'Week 8', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 9, sequence_name: 'Week 9', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 10, sequence_name: 'Week 10', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 15, sequence_name: 'Monthly', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 }
  ]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [emailMetrics, setEmailMetrics] = useState([]);

  useEffect(() => {
    const fetchSequenceStats = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL}/dashboard_stats`);
        setSequenceStats(response.data);
        setLoading(false);
      } catch (err) {
        console.error('Failed to fetch sequence stats:', err);
        setError('Unable to load sequence statistics. Please try again later.');
        setLoading(false);
      }
    };

    const fetchEmailMetrics = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/email_metrics`);
        // Sort metrics by sequence_id to maintain consistent order
        const sortedMetrics = response.data.sort((a, b) => a.sequence_id - b.sequence_id);
        setEmailMetrics(sortedMetrics);
      } catch (err) {
        console.error('Failed to fetch email metrics:', err);
        // Set empty array instead of undefined
        setEmailMetrics([]);
      }
    };

    fetchSequenceStats();
    fetchEmailMetrics();
  }, []);

  if (loading) return <div className="text-center p-4">Loading stats...</div>;
  if (error) return (
    <div className="bg-red-50 text-red-500 p-4 rounded-lg">
      <p>{error}</p>
      <p className="text-sm mt-2">Using default values for demonstration.</p>
    </div>
  );

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Dashboard Overview</h2>
      
      {/* Sequence Distribution Cards - Updated */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        {[
          { label: 'Week 1', sequence_id: 1, color: 'bg-blue-100' },
          { label: 'Week 2', sequence_id: 2, color: 'bg-green-100' },
          { label: 'Week 3', sequence_id: 3, color: 'bg-yellow-100' },
          { label: 'Week 4', sequence_id: 4, color: 'bg-purple-100' },
          { label: 'Week 5', sequence_id: 5, color: 'bg-pink-100' },
          { label: 'Week 6', sequence_id: 6, color: 'bg-indigo-100' },
          { label: 'Week 7', sequence_id: 7, color: 'bg-orange-100' },
          { label: 'Week 8', sequence_id: 8, color: 'bg-teal-100' },
          { label: 'Week 9', sequence_id: 9, color: 'bg-cyan-100' },
          { label: 'Week 10', sequence_id: 10, color: 'bg-lime-100' },
          { label: 'Monthly', sequence_id: 15, color: 'bg-red-100' },
          { label: 'Total Subscribers', sequence_id: 'total', color: 'bg-gray-100' }
        ].map(card => {
          const stat = sequenceStats.find(s => s.sequence_id === card.sequence_id) || { total_contacts: 0 };
          const count = card.sequence_id === 'total' 
            ? sequenceStats.reduce((acc, curr) => acc + curr.total_contacts, 0)
            : stat.total_contacts;

          return (
            <div key={card.label} className={`p-5 rounded-lg ${card.color}`}>
              <h3 className="text-sm font-medium">{card.label}</h3>
              <p className="text-2xl font-bold">{count}</p>
              {card.sequence_id !== 'total' && (
                <p className="text-sm text-gray-600">
                  {((count / sequenceStats.reduce((acc, curr) => acc + curr.total_contacts, 0)) * 100).toFixed(1)}%
                </p>
              )}
            </div>
          );
        })}
      </div>

      {/* Visual Distribution Bar */}
      <div className="bg-white p-6 rounded-lg shadow">
        <h3 className="text-xl font-semibold mb-4">Sequence Distribution</h3>
        <div className="space-y-3">
          {sequenceStats
            .filter(stat => stat.sequence_id !== 'total')
            .map(stat => {
              const percentage = (stat.total_contacts / sequenceStats.reduce((acc, curr) => acc + curr.total_contacts, 0)) * 100;
              return (
                <div key={stat.sequence_id} className="flex items-center">
                  <span className="w-24">
                    {stat.sequence_name}
                  </span>
                  <div className="flex-1 bg-gray-200 rounded-full h-4">
                    <div 
                      className="bg-red-500 h-4 rounded-full transition-all duration-500"
                      style={{ width: `${percentage}%` }}
                    ></div>
                  </div>
                  <span className="ml-3 w-32">
                    {stat.total_contacts} ({percentage.toFixed(1)}%)
                  </span>
                </div>
              );
            })}
        </div>
      </div>

      {/* Email Metrics Section */}
      <div className="mt-8 bg-white p-6 rounded-lg shadow">
        <h3 className="text-xl font-semibold mb-4">Email Performance (Last 30 Days)</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="bg-gray-50">
                <th className="px-6 py-3 text-left">Sequence</th>
                <th className="px-6 py-3 text-left">Sent</th>
                <th className="px-6 py-3 text-left">Delivery Rate</th>
                <th className="px-6 py-3 text-left">Details</th>
              </tr>
            </thead>
            <tbody>
              {emailMetrics.length > 0 ? (
                emailMetrics.map((metric) => (
                  <React.Fragment key={metric.sequence_id}>
                    <tr className="border-b">
                      <td className="px-6 py-4">{metric.sequence_name}</td>
                      <td className="px-6 py-4">{metric.total_sent}</td>
                      <td className="px-6 py-4">
                        <div className="flex items-center">
                          <div className="w-24 bg-gray-200 rounded-full h-2.5 mr-2">
                            <div
                              className="bg-green-600 h-2.5 rounded-full"
                              style={{ width: `${metric.delivery_rate}%` }}
                            ></div>
                          </div>
                          {metric.delivery_rate}%
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <button
                          onClick={() => {
                            const row = document.getElementById(`details-${metric.sequence_id}`);
                            if (row) {
                              row.classList.toggle('hidden');
                            }
                          }}
                          className="text-blue-600 hover:text-blue-800"
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                    <tr id={`details-${metric.sequence_id}`} className="hidden bg-gray-50">
                      <td colSpan="4" className="px-6 py-4">
                        <div className="space-y-4">
                          {/* Successful Deliveries */}
                          <div>
                            <h4 className="font-semibold text-green-700 mb-2">
                              Successful Deliveries ({metric.successful_deliveries?.length || 0})
                            </h4>
                            {metric.successful_deliveries?.length > 0 ? (
                              <div className="grid grid-cols-2 gap-4">
                                {metric.successful_deliveries.map((delivery, index) => (
                                  <div key={index} className="bg-green-50 p-3 rounded">
                                    <p className="text-sm">
                                      <span className="font-medium">To:</span> {delivery.recipient}
                                    </p>
                                    <p className="text-sm text-gray-600">
                                      <span className="font-medium">Sent:</span> {new Date(delivery.sent_at).toLocaleString()}
                                    </p>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <p className="text-sm text-gray-600">No successful deliveries</p>
                            )}
                          </div>

                          {/* Failed Deliveries */}
                          <div>
                            <h4 className="font-semibold text-red-700 mb-2">
                              Failed Deliveries ({metric.failed_deliveries?.length || 0})
                            </h4>
                            {metric.failed_deliveries?.length > 0 ? (
                              <div className="grid grid-cols-2 gap-4">
                                {metric.failed_deliveries.map((delivery, index) => (
                                  <div key={index} className="bg-red-50 p-3 rounded">
                                    <p className="text-sm">
                                      <span className="font-medium">To:</span> {delivery.recipient}
                                    </p>
                                    <p className="text-sm text-gray-600">
                                      <span className="font-medium">Attempted:</span> {new Date(delivery.attempted_at).toLocaleString()}
                                    </p>
                                    <p className="text-sm text-red-600">
                                      <span className="font-medium">Error:</span> {delivery.error_message}
                                    </p>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <p className="text-sm text-gray-600">No failed deliveries</p>
                            )}
                          </div>
                        </div>
                      </td>
                    </tr>
                  </React.Fragment>
                ))
              ) : (
                <tr>
                  <td colSpan="4" className="px-6 py-4 text-center text-gray-500">
                    No email metrics available for the last 30 days
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

const ContactsSection = () => {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email_address: '',
    company_name: '',
    phone_number: '',
    linkedin_url: ''
  });
  const [formError, setFormError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [editingNotes, setEditingNotes] = useState(null);
  const [noteText, setNoteText] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortField, setSortField] = useState('user_id');
  const [sortDirection, setSortDirection] = useState('asc');
  const [sequenceFilter, setSequenceFilter] = useState('all');

  useEffect(() => {
    const fetchContacts = async () => {
      try {
        const data = await getContacts();
        setContacts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchContacts();
  }, []);

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setFormError(null); // Clear error when user types
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError(null);
    setSuccessMessage(null);

    try {
      // Create contact
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/contacts`,
        formData
      );
      
      // Add new contact to the list
      setContacts([...contacts, response.data]);
      
      // Send initial welcome email using Week 1 sequence
      try {
        // Get Week 1 sequence data
        const sequencesResponse = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/sequences`);
        const week1Sequence = sequencesResponse.data.find(seq => seq.sequence_id === 1);
        
        if (week1Sequence) {
          await axios.post(
            `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/send`,
            {
              recipient: formData.email_address,
              subject: week1Sequence.email_subject,
              body: `Dear ${formData.first_name},\n\n${week1Sequence.email_body}`,
              article_link: week1Sequence.article_link,
              contact_id: response.data.user_id,
              sequence_id: 1  // Week 1
            }
          );
          setSuccessMessage('Contact added successfully and welcome email sent!');
        } else {
          setSuccessMessage('Contact added successfully, but Week 1 sequence not found.');
        }
      } catch (emailErr) {
        console.error('Failed to send welcome email:', emailErr);
        setSuccessMessage('Contact added successfully, but welcome email failed to send.');
      }
      
      // Reset form
      setFormData({
        first_name: '',
        last_name: '',
        email_address: '',
        company_name: '',
        phone_number: '',
        linkedin_url: ''
      });
      setShowForm(false);
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(null), 3000);
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Failed to add contact');
    }
  };

  const formatSequence = (sequence) => {
    if (sequence >= 1 && sequence <= 10) {
      return `Week ${sequence}`;
    }
    return 'Monthly';
  };

  const handleNotesUpdate = async (contactId, notes) => {
    try {
      await axios.patch(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/contacts/${contactId}`,
        { notes }
      );
      
      // Update the contacts list with new notes
      setContacts(contacts.map(contact => 
        contact.user_id === contactId 
          ? { ...contact, notes } 
          : contact
      ));
      
      setEditingNotes(null);
      toast.success('Notes updated successfully');
    } catch (err) {
      toast.error('Failed to update notes');
      console.error('Failed to update notes:', err);
    }
  };

  // Filter and sort contacts
  const filteredContacts = contacts
    .filter(contact => {
      // Search filter
      const searchLower = searchTerm.toLowerCase();
      const matchesSearch = 
        contact.first_name.toLowerCase().includes(searchLower) ||
        contact.last_name.toLowerCase().includes(searchLower) ||
        contact.email_address.toLowerCase().includes(searchLower) ||
        (contact.company_name || '').toLowerCase().includes(searchLower);

      // Sequence filter
      const matchesSequence = 
        sequenceFilter === 'all' || 
        contact.email_sequence.toString() === sequenceFilter;

      return matchesSearch && matchesSequence;
    })
    .sort((a, b) => {
      let aValue = a[sortField];
      let bValue = b[sortField];

      // Handle special cases for combined fields
      if (sortField === 'full_name') {
        aValue = `${a.first_name} ${a.last_name}`;
        bValue = `${b.first_name} ${b.last_name}`;
      }

      // Handle date fields
      if (sortField === 'join_date' || sortField === 'last_email_sent_at') {
        aValue = new Date(aValue);
        bValue = new Date(bValue);
      }

      if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1;
      return 0;
    });

  // Add this before the return statement
  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  // Add this new function to handle CSV export
  const exportToCSV = () => {
    // Headers matching Gmail's template (only including fields we have)
    const headers = [
      'First Name',
      'Last Name',
      'E-mail 1 - Value',
      'Phone 1 - Value',
      'Organization Name',
      'Website 1 - Value', // For LinkedIn URL
      'Notes',
      'Labels'
    ].join(',');

    // Convert contacts to CSV rows
    const csvRows = contacts.map(contact => {
      // Escape fields that might contain commas
      const escapeCsvField = (field) => {
        if (!field) return '';
        // If field contains comma or newline, wrap in quotes
        if (field.includes(',') || field.includes('\n') || field.includes('"')) {
          return `"${field.replace(/"/g, '""')}"`;
        }
        return field;
      };

      const row = [
        escapeCsvField(contact.first_name),
        escapeCsvField(contact.last_name),
        escapeCsvField(contact.email_address),
        escapeCsvField(contact.phone_number),
        escapeCsvField(contact.company_name),
        escapeCsvField(contact.linkedin_url),
        escapeCsvField(contact.notes),
        'US Observer Contact' // Label all contacts with this
      ].join(',');

      return row;
    });

    // Combine headers and rows
    const csvContent = [headers, ...csvRows].join('\n');

    // Create and trigger download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    if (link.download !== undefined) {
      const url = URL.createObjectURL(blob);
      link.setAttribute('href', url);
      link.setAttribute('download', 'us_observer_contacts.csv');
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  if (loading) return <div className="p-4">Loading contacts...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-3xl font-bold">Contacts</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-[#c41e3a] text-white px-4 py-2 rounded hover:bg-red-700"
        >
          {showForm ? 'Cancel' : 'Add Contact'}
        </button>
      </div>

      {/* Success Message */}
      {successMessage && (
        <div className="mb-4 p-3 bg-green-100 text-green-700 rounded">
          {successMessage}
        </div>
      )}

      {/* Add Contact Form */}
      {showForm && (
        <div className="bg-white shadow rounded-lg p-6 mb-6">
          <h3 className="text-xl font-semibold mb-4">Add New Contact</h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  First Name
                </label>
                <input
                  type="text"
                  name="first_name"
                  value={formData.first_name}
                  onChange={handleInputChange}
                  required
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Last Name
                </label>
                <input
                  type="text"
                  name="last_name"
                  value={formData.last_name}
                  onChange={handleInputChange}
                  required
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <input
                type="email"
                name="email_address"
                value={formData.email_address}
                onChange={handleInputChange}
                required
                className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Company Name
              </label>
              <input
                type="text"
                name="company_name"
                value={formData.company_name}
                onChange={handleInputChange}
                className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
              />
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Phone Number
                </label>
                <input
                  type="tel"
                  name="phone_number"
                  value={formData.phone_number}
                  onChange={handleInputChange}
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  LinkedIn Profile
                </label>
                <input
                  type="url"
                  name="linkedin_url"
                  value={formData.linkedin_url}
                  onChange={handleInputChange}
                  placeholder="https://linkedin.com/in/..."
                  className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
                />
              </div>
            </div>
            {formError && (
              <div className="text-red-500 text-sm">{formError}</div>
            )}
            <button
              type="submit"
              className="bg-[#c41e3a] text-white px-4 py-2 rounded hover:bg-red-700"
            >
              Add Contact
            </button>
          </form>
        </div>
      )}

      {/* Search and Filter Controls - Updated */}
      <div className="bg-white shadow rounded-lg p-4 mb-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Search Contacts
            </label>
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search by name, email, or company..."
              className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
            />
          </div>

          {/* Sequence Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Filter by Sequence
            </label>
            <select
              value={sequenceFilter}
              onChange={(e) => setSequenceFilter(e.target.value)}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-red-500"
            >
              <option value="all">All Sequences</option>
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15].map((seq) => (
                <option key={seq} value={seq.toString()}>
                  {seq === 15 ? 'Monthly' : `Week ${seq}`}
                </option>
              ))}
            </select>
          </div>

          {/* Export Button */}
          <div className="flex items-end">
            <button
              onClick={exportToCSV}
              className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
              Export to CSV
            </button>
          </div>

          {/* Results Count */}
          <div className="flex items-end">
            <p className="text-gray-600">
              Showing {filteredContacts.length} of {contacts.length} contacts
            </p>
          </div>
        </div>
      </div>

      {/* Updated Table Headers */}
      <div className="bg-white shadow rounded-lg p-6">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th 
                className="p-3 text-left cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('user_id')}
              >
                <div className="flex items-center">
                  User ID
                  {sortField === 'user_id' && (
                    <span className="ml-1">
                      {sortDirection === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </div>
              </th>
              <th 
                className="p-3 text-left cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('full_name')}
              >
                <div className="flex items-center">
                  Name
                  {sortField === 'full_name' && (
                    <span className="ml-1">
                      {sortDirection === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </div>
              </th>
              <th 
                className="p-3 text-left cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('email_address')}
              >
                <div className="flex items-center">
                  Email
                  {sortField === 'email_address' && (
                    <span className="ml-1">
                      {sortDirection === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </div>
              </th>
              <th 
                className="p-3 text-left cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('company_name')}
              >
                <div className="flex items-center">
                  Company
                  {sortField === 'company_name' && (
                    <span className="ml-1">
                      {sortDirection === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </div>
              </th>
              <th 
                className="p-3 text-left cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('email_sequence')}
              >
                <div className="flex items-center">
                  Sequence
                  {sortField === 'email_sequence' && (
                    <span className="ml-1">
                      {sortDirection === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </div>
              </th>
              <th 
                className="p-3 text-left cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('join_date')}
              >
                <div className="flex items-center">
                  Join Date
                  {sortField === 'join_date' && (
                    <span className="ml-1">
                      {sortDirection === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </div>
              </th>
              <th 
                className="p-3 text-left cursor-pointer hover:bg-gray-200"
                onClick={() => handleSort('last_email_sent_at')}
              >
                <div className="flex items-center">
                  Last Email
                  {sortField === 'last_email_sent_at' && (
                    <span className="ml-1">
                      {sortDirection === 'asc' ? '↑' : '↓'}
                    </span>
                  )}
                </div>
              </th>
              <th className="p-3 text-left">Notes</th>
            </tr>
          </thead>
          <tbody>
            {filteredContacts.map(contact => (
              <tr key={contact.user_id} className="border-b hover:bg-gray-50">
                <td className="p-3">{contact.user_id}</td>
                <td className="p-3">{`${contact.first_name} ${contact.last_name}`}</td>
                <td className="p-3">{contact.email_address}</td>
                <td className="p-3">{contact.company_name || '-'}</td>
                <td className="p-3">{formatSequence(contact.email_sequence)}</td>
                <td className="p-3">
                  {contact.join_date ? new Date(contact.join_date).toLocaleDateString() : '-'}
                </td>
                <td className="p-3">
                  {contact.last_email_sent_at ? new Date(contact.last_email_sent_at).toLocaleDateString() : '-'}
                </td>
                <td className="p-3">
                  {editingNotes === contact.user_id ? (
                    <div className="flex flex-col space-y-2">
                      <textarea
                        className="w-full p-2 border rounded-md focus:ring-2 focus:ring-red-500 min-h-[100px]"
                        value={noteText}
                        onChange={(e) => setNoteText(e.target.value)}
                        placeholder="Enter notes here..."
                      />
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleNotesUpdate(contact.user_id, noteText)}
                          className="bg-green-500 text-white px-3 py-1 rounded-md hover:bg-green-600"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => {
                            setEditingNotes(null);
                            setNoteText('');
                          }}
                          className="bg-gray-500 text-white px-3 py-1 rounded-md hover:bg-gray-600"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div 
                      className="group relative cursor-pointer"
                      onClick={() => {
                        setEditingNotes(contact.user_id);
                        setNoteText(contact.notes || '');
                      }}
                    >
                      <div className="min-h-[1.5rem] max-h-[4.5rem] overflow-hidden">
                        {contact.notes ? (
                          <p className="whitespace-pre-wrap">{contact.notes}</p>
                        ) : (
                          <p className="text-gray-400 italic">Click to add notes</p>
                        )}
                      </div>
                      <div className="absolute inset-0 bg-gray-100 opacity-0 group-hover:opacity-10 transition-opacity" />
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

const EmailSequencesSection = () => {
  const [sequences, setSequences] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingId, setEditingId] = useState(null);
  const [formErrors, setFormErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');
  const [editForm, setEditForm] = useState({
    email_body: '',
    article_link: '',
    email_subject: ''
  });

  useEffect(() => {
    fetchSequences();
  }, []);

  const fetchSequences = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/sequences`);
      // Sort sequences by sequence_id to maintain order
      const sortedSequences = response.data.sort((a, b) => a.sequence_id - b.sequence_id);
      setSequences(sortedSequences);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleEdit = (sequence) => {
    setEditingId(sequence.sequence_id);
    setEditForm({
      email_body: sequence.email_body,
      article_link: sequence.article_link,
      email_subject: sequence.email_subject || ''
    });
  };

  const validateForm = () => {
    const errors = {};
    
    // Validate email subject
    if (!editForm.email_subject?.trim()) {
      errors.email_subject = 'Email subject is required';
    }
    
    // Validate email body
    if (!editForm.email_body?.trim()) {
      errors.email_body = 'Email body is required';
    }

    // Validate article link
    if (!editForm.article_link?.trim()) {
      errors.article_link = 'Article link is required';
    } else {
      try {
        new URL(editForm.article_link);
      } catch (e) {
        errors.article_link = 'Please enter a valid URL (e.g., https://example.com)';
      }
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSave = async (sequenceId) => {
    // Clear previous messages
    setError(null);
    setSuccessMessage('');

    if (!validateForm()) {
      return;
    }

    try {
      await axios.put(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/sequences/${sequenceId}`, 
        editForm
      );
      setEditingId(null);
      setFormErrors({});
      fetchSequences();
      setSuccessMessage('Sequence updated successfully!');
      
      setTimeout(() => {
        setSuccessMessage('');
      }, 3000);
    } catch (err) {
      // Handle backend validation errors
      if (err.response?.data) {
        const backendErrors = Array.isArray(err.response.data) ? err.response.data : [err.response.data];
        const newFormErrors = {};
        
        backendErrors.forEach(error => {
          if (error.loc && error.loc[1]) {
            const field = error.loc[1];
            newFormErrors[field] = error.msg;
          }
        });
        
        if (Object.keys(newFormErrors).length > 0) {
          setFormErrors(newFormErrors);
        } else {
          setError('An error occurred while saving');
        }
      } else {
        setError('An error occurred while saving');
      }
    }
  };

  const handleChange = (e) => {
    setEditForm({
      ...editForm,
      [e.target.name]: e.target.value
    });
    // Clear error for this field when user starts typing
    if (formErrors[e.target.name]) {
      setFormErrors({
        ...formErrors,
        [e.target.name]: null
      });
    }
  };

  const modules = {
    toolbar: [
      [{ 'header': [1, 2, 3, false] }],
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      [{ 'color': [] }, { 'background': [] }],
      ['link'],
      ['clean']
    ],
  };

  const formats = [
    'header',
    'bold', 'italic', 'underline', 'strike',
    'list', 'bullet',
    'link',
    'color', 'background'
  ];

  const getSequenceLabel = (sequenceId) => {
    if (sequenceId >= 1 && sequenceId <= 10) {
      return `Week ${sequenceId}`;
    }
    return 'Monthly';
  };

  if (loading) return <div>Loading sequences...</div>;
  if (error) return <div className="text-red-500">Error: {error}</div>;

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Email Sequences</h2>
      
      {/* Notification Messages */}
      {successMessage && (
        <div className="mb-4 p-3 bg-green-100 text-green-700 rounded-md">
          {successMessage}
        </div>
      )}
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sequences.map((sequence) => (
          <div 
            key={sequence.sequence_id} 
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow"
          >
            <h3 className="text-xl font-semibold mb-3">
              {getSequenceLabel(sequence.sequence_id)}
            </h3>
            {editingId === sequence.sequence_id ? (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email Subject
                  </label>
                  <input
                    type="text"
                    name="email_subject"
                    value={editForm.email_subject}
                    onChange={handleChange}
                    className={`w-full p-2 border rounded focus:ring-2 focus:ring-red-500 ${
                      formErrors.email_subject ? 'border-red-500' : ''
                    }`}
                  />
                  {formErrors.email_subject && (
                    <p className="text-red-500 text-sm mt-1">{formErrors.email_subject}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Article Link
                  </label>
                  <input
                    type="url"
                    name="article_link"
                    value={editForm.article_link}
                    onChange={handleChange}
                    className={`w-full p-2 border rounded focus:ring-2 focus:ring-red-500 ${
                      formErrors.article_link ? 'border-red-500' : ''
                    }`}
                  />
                  {formErrors.article_link && (
                    <p className="text-red-500 text-sm mt-1">{formErrors.article_link}</p>
                  )}
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email Body
                  </label>
                  <div className={`h-64 ${formErrors.email_body ? 'border border-red-500 rounded' : ''}`}>
                    <ReactQuill
                      theme="snow"
                      value={editForm.email_body}
                      onChange={(content) => {
                        setEditForm({
                          ...editForm,
                          email_body: content
                        });
                        // Clear error when user starts typing
                        if (formErrors.email_body) {
                          setFormErrors({
                            ...formErrors,
                            email_body: null
                          });
                        }
                      }}
                      modules={modules}
                      formats={formats}
                      className="h-48"
                    />
                  </div>
                  {formErrors.email_body && (
                    <p className="text-red-500 text-sm mt-1">{formErrors.email_body}</p>
                  )}
                </div>
                <button
                  onClick={() => handleSave(sequence.sequence_id)}
                  className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
                >
                  Save
                </button>
              </div>
            ) : (
              <>
                <div className="mb-4 space-y-2">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Subject:</label>
                    <p className="text-gray-800">{sequence.email_subject || 'No subject set'}</p>
                  </div>
                  <div>
                    <a 
                      href={sequence.article_link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-800 underline"
                    >
                      View Article
                    </a>
                  </div>
                </div>
                <div className="text-gray-600">
                  <div 
                    className="line-clamp-3"
                    dangerouslySetInnerHTML={{ __html: sequence.email_body }}
                  />
                </div>
                <button
                  onClick={() => handleEdit(sequence)}
                  className="mt-4 text-red-600 hover:text-red-800"
                >
                  Edit
                </button>
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard; 