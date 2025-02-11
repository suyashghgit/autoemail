import React, { useState } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  Paper, 
  Typography,
  Snackbar,
  Alert
} from '@mui/material';
import { sendEmail } from '../services/api';

const EmailForm = () => {
  const [formData, setFormData] = useState({
    recipient_email: '',
    subject: '',
    body: '',
    article_link: ''
  });
  const [notification, setNotification] = useState({
    open: false,
    message: '',
    severity: 'success'
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await sendEmail(formData);
      setNotification({
        open: true,
        message: 'Email sent successfully!',
        severity: 'success'
      });
      setFormData({
        recipient_email: '',
        subject: '',
        body: '',
        article_link: ''
      });
    } catch (error) {
      setNotification({
        open: true,
        message: error.detail || 'Failed to send email',
        severity: 'error'
      });
    }
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      <Paper elevation={3} sx={{ p: 4 }}>
        <Typography variant="h5" gutterBottom>
          Send Email
        </Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Recipient Email"
            name="recipient_email"
            value={formData.recipient_email}
            onChange={handleChange}
            margin="normal"
            required
            type="email"
          />
          <TextField
            fullWidth
            label="Subject"
            name="subject"
            value={formData.subject}
            onChange={handleChange}
            margin="normal"
            required
          />
          <TextField
            fullWidth
            label="Article Link"
            name="article_link"
            value={formData.article_link}
            onChange={handleChange}
            margin="normal"
            required
            type="url"
          />
          <TextField
            fullWidth
            label="Email Body"
            name="body"
            value={formData.body}
            onChange={handleChange}
            margin="normal"
            required
            multiline
            rows={6}
          />
          <Button 
            variant="contained" 
            type="submit"
            sx={{ mt: 2 }}
          >
            Send Email
          </Button>
        </form>
      </Paper>
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={() => setNotification({ ...notification, open: false })}
      >
        <Alert severity={notification.severity}>
          {notification.message}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default EmailForm; 