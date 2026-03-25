import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './presentation/pages/Login';
import Dashboard from './presentation/pages/Dashboard';
import LockerDetail from './presentation/pages/LockerDetail';
import { isAuthenticated } from './application/useCases/AuthUseCase';

const ProtectedRoute = ({ children }) => {
    return isAuthenticated() ? children : <Navigate to="/login" replace />;
};

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/dashboard" element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                } />
                <Route path="/dashboard/casillero/:id" element={
                    <ProtectedRoute>
                        <LockerDetail />
                    </ProtectedRoute>
                } />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;