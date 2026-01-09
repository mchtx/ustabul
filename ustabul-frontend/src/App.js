import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import { useAuth } from './hooks';
import HomePage from './pages/HomePage';
import WorkshopListPage from './pages/WorkshopListPage';
import WorkshopDetailPage from './pages/WorkshopDetailPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import PartsListPage from './pages/PartsListPage';
import Footer from './components/Footer';
import './index.css';

function NavBar() {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="bg-white shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <Link to="/" className="flex items-center text-2xl font-bold text-orange-600">
            UstaBul
          </Link>
          <div className="flex items-center space-x-4">
            <Link to="/workshops" className="text-gray-700 hover:text-orange-600">Dükkanlar</Link>
            {user?.role === 'parts_dealer' && (
              <Link to="/parts" className="text-gray-700 hover:text-orange-600 flex items-center gap-1">
                🔧 Parçalar
              </Link>
            )}
            {user ? (
              <>
                <Link to="/profile" className="text-gray-700 hover:text-orange-600">
                  {user.username}
                </Link>
                <button
                  onClick={handleLogout}
                  className="bg-red-600 text-white px-3 py-1 rounded-lg hover:bg-red-700"
                >
                  Çıkış
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700 hover:text-orange-600">Giriş</Link>
                <Link to="/register" className="bg-orange-600 text-white px-3 py-1 rounded-lg hover:bg-orange-700">
                  Kaydol
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen flex flex-col bg-gray-50">
          <NavBar />

          <main className="flex-1">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/workshops" element={<WorkshopListPage />} />
              <Route path="/workshops/:id" element={<WorkshopDetailPage />} />
              <Route path="/parts" element={<PartsListPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/profile" element={<ProfilePage />} />
            </Routes>
          </main>

          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
