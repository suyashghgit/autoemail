import axios from 'axios';

const API_URL = 'http://localhost:8000';

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