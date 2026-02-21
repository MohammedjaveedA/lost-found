import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import PrivateRoute from './components/PrivateRoute';
import Landing from './pages/Landing';
import Login from './pages/Login';
import RegisterOrg from './pages/RegisterOrg';
import RegisterUser from './pages/RegisterUser';
import OrgDashboard from './pages/OrgDashboard';
import UserDashboard from './pages/UserDashboard';


function AppRoutes() {
  const { user } = useAuth();

  return (
    <>
      <Navbar />
      <main className="w-full">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register/org" element={<RegisterOrg />} />
          <Route path="/register/user" element={<RegisterUser />} />
          
          <Route path="/org-dashboard" element={
            <PrivateRoute>
              {user?.role === 'org_admin' ? <OrgDashboard /> : <Navigate to="/" />}
            </PrivateRoute>
          } />
          
          <Route path="/dashboard" element={
            <PrivateRoute>
              {user?.role === 'regular' ? <UserDashboard /> : <Navigate to="/" />}
            </PrivateRoute>
          } />
        </Routes>
      </main>
    </>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Toaster position="top-right" />
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;