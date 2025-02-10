import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';

const Header = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <img 
            src="/logo.png" 
            alt="US Observer Logo" 
            style={{ height: 40, marginRight: 16 }}
          />
          <Typography variant="h6">
            US Observer Email System
          </Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 