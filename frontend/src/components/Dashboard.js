import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  Users, 
  Mail,
  UserPlus
} from 'lucide-react';
import EmailForm from './EmailForm';
import AuthStatus from './AuthStatus';
import { getContacts } from '../services/api';
import axios from 'axios';
import EmailGroups from './EmailGroups';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { toast } from 'react-hot-toast';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const navItems = [
    { icon: LayoutDashboard, label: 'Dashboard', key: 'dashboard' },
    { icon: Users, label: 'Contacts', key: 'contacts' },
    { icon: Mail, label: 'Email Sequences', key: 'sequences' },
    { icon: UserPlus, label: 'Email Groups', key: 'groups' }
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
    // Default stats structure to prevent errors if API fails
    { sequence_id: 1, sequence_name: 'Week 1', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 2, sequence_name: 'Week 2', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 3, sequence_name: 'Week 3', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 4, sequence_name: 'Week 4', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 5, sequence_name: 'Week 5', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 6, sequence_name: 'Week 6', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 },
    { sequence_id: 9, sequence_name: 'Monthly', total_contacts: 0, completed_contacts: 0, pending_contacts: 0, success_rate: 0 }
  ]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [emailMetrics, setEmailMetrics] = useState([]);

  useEffect(() => {
    const fetchSequenceStats = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/dashboard_stats`);
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
      
      {/* Sequence Distribution Cards */}
      <div className="grid grid-cols-4 gap-4 mb-6">
        {[
          { label: 'Week 1', sequence_id: 1, color: 'bg-blue-100' },
          { label: 'Week 2', sequence_id: 2, color: 'bg-green-100' },
          { label: 'Week 3', sequence_id: 3, color: 'bg-yellow-100' },
          { label: 'Week 4', sequence_id: 4, color: 'bg-purple-100' },
          { label: 'Week 5', sequence_id: 5, color: 'bg-pink-100' },
          { label: 'Week 6', sequence_id: 6, color: 'bg-indigo-100' },
          { label: 'Monthly', sequence_id: 9, color: 'bg-red-100' },
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
              </tr>
            </thead>
            <tbody>
              {emailMetrics.length > 0 ? (
                emailMetrics.map((metric) => (
                  <tr key={metric.sequence_id} className="border-b">
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
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan="3" className="px-6 py-4 text-center text-gray-500">
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
              subject: "Welcome to US Observer",
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
    if (sequence >= 1 && sequence <= 6) {
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

      <div className="bg-white shadow rounded-lg p-6">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-3 text-left">User ID</th>
              <th className="p-3 text-left">Name</th>
              <th className="p-3 text-left">Email</th>
              <th className="p-3 text-left">Company</th>
              <th className="p-3 text-left">Sequence</th>
              <th className="p-3 text-left">Join Date</th>
              <th className="p-3 text-left">Last Email</th>
              <th className="p-3 text-left">Notes</th>
            </tr>
          </thead>
          <tbody>
            {contacts.map(contact => (
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
    article_link: ''
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
      article_link: sequence.article_link
    });
  };

  const validateForm = () => {
    const errors = {};
    
    // Validate email body
    if (!editForm.email_body.trim()) {
      errors.email_body = 'Email body cannot be empty';
    }

    // Validate article link if it's not empty
    if (editForm.article_link.trim()) {
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
      
      // Clear success message after 3 seconds
      setTimeout(() => {
        setSuccessMessage('');
      }, 3000);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'An error occurred while saving');
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
    if (sequenceId >= 1 && sequenceId <= 6) {
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
          Error: {error}
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
                  <div className="h-64">
                    <ReactQuill
                      theme="snow"
                      value={editForm.email_body}
                      onChange={(content) => {
                        setEditForm({
                          ...editForm,
                          email_body: content
                        });
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
                <div className="mb-4">
                  <a 
                    href={sequence.article_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 underline"
                  >
                    View Article
                  </a>
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