import React, { useEffect, useState } from 'react';
import { Box, Button, Alert } from '@mui/material';
import { checkAuthStatus } from '../services/api';

const AuthStatus = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      await checkAuthStatus();
      setIsAuthenticated(true);
    } catch (error) {
      setIsAuthenticated(false);
    }
  };

  const handleAuth = () => {
    window.location.href = 'http://localhost:8000/auth/gmail';
  };

  return (
    <Box sx={{ m: 2 }}>
      {!isAuthenticated ? (
        <Alert 
          severity="warning"
          action={
            <Button color="inherit" size="small" onClick={handleAuth}>
              Authenticate
            </Button>
          }
        >
          Please authenticate with Gmail to send emails
        </Alert>
      ) : (
        <Alert severity="success">
          Authenticated with Gmail
        </Alert>
      )}
    </Box>
  );
};

export default AuthStatus; 