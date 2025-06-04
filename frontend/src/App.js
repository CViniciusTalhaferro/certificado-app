import React from 'react';
import CertUpload from './CertUpload';
import CertList from './CertList';

function App() {
  return (
    <div style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>Gestão de Certificados Digitais</h1>
      <CertUpload />
      <hr style={{ margin: '2rem 0' }} />
      <CertList />
    </div>
  );
}

export default App;
