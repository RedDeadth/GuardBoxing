import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CasillerosList from './CasillerosList';
import CasilleroDetalle from './CasilleroDetalle';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CasillerosList />} />
        <Route path="/casilleros/:id" element={<CasilleroDetalle />} />
      </Routes>
    </Router>
  );
}

export default App;
