import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';

const WeekSelector = () => {
  const [activeWeeks, setActiveWeeks] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchActiveWeeks();
  }, []);

  const fetchActiveWeeks = async () => {
    try {
      const { data } = await axios.get(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/active-weeks`
      );
      setActiveWeeks(data);
      setLoading(false);
    } catch (err) {
      console.error('Failed to fetch active weeks:', err);
      toast.error('Failed to load week settings');
      setLoading(false);
    }
  };

  const toggleWeek = async (weekId) => {
    try {
      await axios.post(
        `${process.env.REACT_APP_API_URL || 'http://localhost:8000'}/toggle-week`,
        { week_id: weekId, active: !activeWeeks[weekId] }
      );
      
      setActiveWeeks(prev => ({
        ...prev,
        [weekId]: !prev[weekId]
      }));
      
      toast.success(`${getWeekLabel(weekId)} ${!activeWeeks[weekId] ? 'enabled' : 'disabled'}`);
    } catch (err) {
      console.error('Failed to toggle week:', err);
      toast.error('Failed to update week settings');
    }
  };

  const getWeekLabel = (weekId) => {
    return weekId === 15 ? 'Monthly Group' : `Week ${weekId} Group`;
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-700"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <h2 className="text-3xl font-bold mb-6">Week Selector</h2>
      <p className="text-gray-600 mb-8">
        Toggle email groups on/off to control their visibility in the Email Groups page.
      </p>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(10)].map((_, index) => (
          <WeekToggleCard
            key={index + 1}
            weekId={index + 1}
            isActive={activeWeeks[index + 1] ?? true}
            onToggle={toggleWeek}
          />
        ))}
        <WeekToggleCard
          weekId={15}
          isActive={activeWeeks[15] ?? true}
          onToggle={toggleWeek}
        />
      </div>
    </div>
  );
};

const WeekToggleCard = ({ weekId, isActive, onToggle }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-semibold">
            {weekId === 15 ? 'Monthly Group' : `Week ${weekId}`}
          </h3>
          <p className="text-gray-600">
            {isActive ? 'Active' : 'Inactive'}
          </p>
        </div>
        <button
          onClick={() => onToggle(weekId)}
          className={`
            relative inline-flex h-6 w-11 items-center rounded-full 
            transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2
            ${isActive ? 'bg-red-700' : 'bg-gray-200'}
          `}
        >
          <span
            className={`
              inline-block h-4 w-4 transform rounded-full bg-white transition-transform
              ${isActive ? 'translate-x-6' : 'translate-x-1'}
            `}
          />
        </button>
      </div>
    </div>
  );
};

export default WeekSelector; 