import React from 'react';
import { CssBaseline, Container } from '@mui/material';
import Header from './components/Header';
import EmailForm from './components/EmailForm';
import AuthStatus from './components/AuthStatus';

function App() {
  return (
    <>
      <CssBaseline />
      <Header />
      <Container>
        <AuthStatus />
        <EmailForm />
      </Container>
    </>
  );
}

export default App; 