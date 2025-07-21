import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import EmploymentPage from './components/EmploymentPage';
import SpendingPage from './components/SpendingPage';
import SafetyPage from './components/SafetyPage';
import APISetupPage from './components/APISetupPage';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <main className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/employment" element={<EmploymentPage />} />
            <Route path="/spending" element={<SpendingPage />} />
            <Route path="/safety" element={<SafetyPage />} />
            <Route path="/api-setup" element={<APISetupPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 