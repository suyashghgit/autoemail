import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  Users, 
  Mail
} from 'lucide-react';
import EmailForm from './EmailForm';
import AuthStatus from './AuthStatus';

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

const ContactsSection = () => (
  <div>
    <h2 className="text-3xl font-bold mb-6">Recent Contacts</h2>
    <div className="bg-white shadow rounded-lg p-6">
      <table className="w-full">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-3 text-left">Email</th>
            <th className="p-3 text-left">Subject</th>
            <th className="p-3 text-left">Article Link</th>
            <th className="p-3 text-left">Date Sent</th>
          </tr>
        </thead>
        <tbody>
          {[
            { 
              email: 'john@example.com', 
              subject: 'Article Review Request', 
              article: 'https://usobserver.com/article-1', 
              date: '2024-02-10' 
            },
            { 
              email: 'jane@example.com', 
              subject: 'Follow-up on Article', 
              article: 'https://usobserver.com/article-2', 
              date: '2024-01-15' 
            }
          ].map(contact => (
            <tr key={contact.email} className="border-b hover:bg-gray-50">
              <td className="p-3">{contact.email}</td>
              <td className="p-3">{contact.subject}</td>
              <td className="p-3">
                <a href={contact.article} className="text-blue-600 hover:underline">
                  View Article
                </a>
              </td>
              <td className="p-3">{contact.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

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