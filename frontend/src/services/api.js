import axios from 'axios';

const ENV = process.env.REACT_APP_ENV || 'local';
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

console.log(`Running in ${ENV} environment`);
console.log(`API URL: ${API_URL}`);

export const sendEmail = async (emailData) => {
  try {
    const response = await axios.post(`${API_URL}/email/send`, {
      ...emailData,
      recipient_email: emailData.recipient_email
    });
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const checkAuthStatus = async () => {
  try {
    const response = await axios.get(`${API_URL}/auth/gmail`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getContacts = async () => {
  try {
    const response = await axios.get(`${API_URL}/contacts`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
};

export const getSequences = async () => {
  try {
    const response = await axios.get(`${API_URL}/sequences`);
    return response.data;
  } catch (error) {
    throw error.response?.data || error.message;
  }
}; 