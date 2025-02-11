import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Mail, ChevronDown, ChevronUp, UserPlus } from 'lucide-react';

const EmailGroups = () => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedGroup, setExpandedGroup] = useState(null);
  const [selectedContacts, setSelectedContacts] = useState([]);
  const [showEmailForm, setShowEmailForm] = useState(false);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [emailForm, setEmailForm] = useState({
    subject: '',
    body: '',
    article_link: ''
  });
  const [sending, setSending] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    fetchGroups();
  }, []);

  const fetchGroups = async () => {
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/email_groups`
      );
      setGroups(response.data);
      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const handleGroupExpand = (sequenceId) => {
    setExpandedGroup(expandedGroup === sequenceId ? null : sequenceId);
  };

  const handleContactSelect = (contactId) => {
    setSelectedContacts(prev => 
      prev.includes(contactId)
        ? prev.filter(id => id !== contactId)
        : [...prev, contactId]
    );
  };

  const handleSendGroupEmail = async (group) => {
    setSelectedGroup(group);
    setShowEmailForm(true);
  };

  const handleEmailSubmit = async (e) => {
    e.preventDefault();
    setSending(true);

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/send-group`,
        {
          sequence_id: selectedGroup.sequence_id,
          ...emailForm
        }
      );

      // Show success message
      setSuccessMessage(`Successfully sent ${response.data.successful_sends} emails`);
      
      // Reset form and close modal
      setEmailForm({ subject: '', body: '', article_link: '' });
      setShowEmailForm(false);
      setSelectedGroup(null);
      
      // Refresh groups data
      fetchGroups();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send group emails');
    } finally {
      setSending(false);
    }
  };

  if (loading) return (
    <div className="flex justify-center items-center h-64">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-700"></div>
    </div>
  );

  if (error) return (
    <div className="text-red-500 p-4 bg-red-50 rounded-lg">
      Error loading email groups: {error}
    </div>
  );

  return (
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-6">Email Groups</h2>
      
      <div className="grid gap-6">
        {groups.map((group) => (
          <div key={group.sequence_id} className="bg-white rounded-lg shadow-md">
            <div className="p-4 flex items-center justify-between border-b">
              <div className="flex items-center space-x-4">
                <div className="bg-red-100 p-3 rounded-full">
                  <Mail className="h-6 w-6 text-red-700" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold">{group.group_name}</h3>
                  <p className="text-gray-600">{group.contact_count} contacts</p>
                </div>
              </div>
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => handleSendGroupEmail(group)}
                  className="bg-red-700 text-white px-4 py-2 rounded-lg hover:bg-red-800 transition-colors"
                >
                  Send Group Email
                </button>
                <button
                  onClick={() => handleGroupExpand(group.sequence_id)}
                  className="p-2 hover:bg-gray-100 rounded-full transition-colors"
                >
                  {expandedGroup === group.sequence_id ? (
                    <ChevronUp className="h-6 w-6" />
                  ) : (
                    <ChevronDown className="h-6 w-6" />
                  )}
                </button>
              </div>
            </div>
            
            {expandedGroup === group.sequence_id && (
              <div className="p-4">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="bg-gray-50">
                        <th className="p-3 text-left">Name</th>
                        <th className="p-3 text-left">Email</th>
                        <th className="p-3 text-left">Join Date</th>
                        <th className="p-3 text-left">Last Email</th>
                        <th className="p-3 text-left">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {group.contacts.map((contact) => (
                        <tr key={contact.user_id} className="border-t">
                          <td className="p-3">
                            {contact.first_name} {contact.last_name}
                          </td>
                          <td className="p-3">{contact.email_address}</td>
                          <td className="p-3">
                            {new Date(contact.join_date).toLocaleDateString()}
                          </td>
                          <td className="p-3">
                            {new Date(contact.last_email_sent_at).toLocaleDateString()}
                          </td>
                          <td className="p-3">
                            <button
                              onClick={() => handleContactSelect(contact.user_id)}
                              className={`p-2 rounded-full transition-colors ${
                                selectedContacts.includes(contact.user_id)
                                  ? 'bg-red-100 text-red-700'
                                  : 'hover:bg-gray-100'
                              }`}
                            >
                              <UserPlus className="h-5 w-5" />
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
      
      {/* Email Form Modal */}
      {showEmailForm && selectedGroup && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full">
            <h3 className="text-xl font-semibold mb-4">
              Send Email to {selectedGroup.group_name}
            </h3>
            <form onSubmit={handleEmailSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Subject
                </label>
                <input
                  type="text"
                  value={emailForm.subject}
                  onChange={(e) => setEmailForm({ ...emailForm, subject: e.target.value })}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Article Link
                </label>
                <input
                  type="url"
                  value={emailForm.article_link}
                  onChange={(e) => setEmailForm({ ...emailForm, article_link: e.target.value })}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Email Body
                </label>
                <textarea
                  value={emailForm.body}
                  onChange={(e) => setEmailForm({ ...emailForm, body: e.target.value })}
                  rows={6}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div className="flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => {
                    setShowEmailForm(false);
                    setSelectedGroup(null);
                  }}
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={sending}
                  className={`px-4 py-2 bg-red-700 text-white rounded hover:bg-red-800 ${
                    sending ? 'opacity-50 cursor-not-allowed' : ''
                  }`}
                >
                  {sending ? 'Sending...' : 'Send Email'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default EmailGroups; 