import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  Users, 
  Mail
} from 'lucide-react';
import EmailForm from './EmailForm';
import AuthStatus from './AuthStatus';
import { getContacts } from '../services/api';
import axios from 'axios';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch(activeTab) {
      case 'dashboard':
        return <DashboardContent />;
      case 'contacts':
        return <ContactsSection />;
      case 'sequences':
        return <EmailSequencesSection />;
      default:
        return <DashboardContent />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-md">
        <div className="p-5 border-b">
          <h1 className="text-2xl font-bold text-[#c41e3a]">US Observer</h1>
        </div>
        <nav className="p-4">
          {[
            { icon: <LayoutDashboard />, label: 'Dashboard', key: 'dashboard' },
            { icon: <Users />, label: 'Contacts', key: 'contacts' },
            { icon: <Mail />, label: 'Email Sequences', key: 'sequences' }
          ].map(item => (
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
              {item.icon}
              <span className="ml-3">{item.label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Main Content Area */}
      <div className="flex-1 p-10 overflow-y-auto">
        <AuthStatus />
        {renderContent()}
      </div>
    </div>
  );
};

const DashboardContent = () => (
  <div>
    <h2 className="text-3xl font-bold mb-6">Dashboard Overview</h2>
    <div className="grid grid-cols-4 gap-4">
      {[
        { label: 'Total Emails Sent', value: '245', color: 'bg-red-100' },
        { label: 'Successful Deliveries', value: '236', color: 'bg-green-100' },
        { label: 'Failed Deliveries', value: '9', color: 'bg-yellow-100' },
        { label: 'Open Rate', value: '42.3%', color: 'bg-blue-100' }
      ].map(card => (
        <div key={card.label} className={`p-5 rounded-lg ${card.color}`}>
          <h3 className="text-sm font-medium">{card.label}</h3>
          <p className="text-2xl font-bold">{card.value}</p>
        </div>
      ))}
    </div>
  </div>
);

const ContactsSection = () => {
  const [contacts, setContacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  if (loading) return <div className="p-4">Loading contacts...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Contacts</h2>
      <div className="bg-white shadow rounded-lg p-6">
        <table className="w-full">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-3 text-left">User ID</th>
              <th className="p-3 text-left">Name</th>
              <th className="p-3 text-left">Email</th>
              <th className="p-3 text-left">Sequence</th>
              <th className="p-3 text-left">Join Date</th>
              <th className="p-3 text-left">Last Email Sent</th>
            </tr>
          </thead>
          <tbody>
            {contacts.map(contact => (
              <tr key={contact.user_id} className="border-b hover:bg-gray-50">
                <td className="p-3">{contact.user_id}</td>
                <td className="p-3">{`${contact.first_name} ${contact.last_name}`}</td>
                <td className="p-3">{contact.email_address}</td>
                <td className="p-3">{contact.email_sequence}</td>
                <td className="p-3">{new Date(contact.join_date).toLocaleDateString()}</td>
                <td className="p-3">{new Date(contact.last_email_sent_at).toLocaleDateString()}</td>
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

  useEffect(() => {
    const fetchSequences = async () => {
      try {
        const response = await axios.get('http://localhost:8000/sequences');
        setSequences(response.data);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchSequences();
  }, []);

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
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sequences.map((sequence) => (
          <div 
            key={sequence.sequence_id} 
            className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition-shadow"
          >
            <h3 className="text-xl font-semibold mb-3">
              {getSequenceLabel(sequence.sequence_id)}
            </h3>
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
              <p className="line-clamp-3">{sequence.email_body}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard; 