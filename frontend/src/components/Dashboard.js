import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  Users, 
  Mail
} from 'lucide-react';
import EmailForm from './EmailForm';
import AuthStatus from './AuthStatus';
import { getContacts } from '../services/api';

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
  return (
    <div>
      <h2 className="text-3xl font-bold mb-6">Send Email</h2>
      <div className="bg-white shadow rounded-lg">
        <EmailForm />
      </div>
    </div>
  );
};

export default Dashboard; 