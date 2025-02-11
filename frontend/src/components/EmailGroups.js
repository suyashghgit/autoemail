import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Mail, ChevronDown, ChevronUp } from 'lucide-react';
import toast from 'react-hot-toast';

const EmailGroups = () => {
  const [groups, setGroups] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedGroup, setExpandedGroup] = useState(null);
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

  const handleSendGroupEmail = async (group) => {
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/send-group`,
        {
          sequence_id: group.sequence_id,
          subject: "Test subject",
        }
      );

      // Show success toast
      toast.success(`Successfully sent ${response.data.successful_sends} emails`, {
        duration: 4000,
        position: 'top-right',
        style: {
          background: '#10B981',
          color: 'white',
        },
      });
      
      // Refresh groups data
      fetchGroups();
    } catch (err) {
      // Show error toast
      toast.error(err.response?.data?.detail || 'Failed to send group emails', {
        duration: 4000,
        position: 'top-right',
        style: {
          background: '#EF4444',
          color: 'white',
        },
      });
    }
  };

  const getGroupName = (sequenceId) => {
    if (sequenceId === 15) {
      return "Monthly Group";
    }
    return `Week ${sequenceId} Group`;
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
                  <h3 className="text-xl font-semibold">{getGroupName(group.sequence_id)}</h3>
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
    </div>
  );
};

export default EmailGroups; 