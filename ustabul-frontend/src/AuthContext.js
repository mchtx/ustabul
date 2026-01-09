import React, { createContext, useState, useEffect } from 'react';
import { usersAPI } from './api';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Page yüklendiğinde user bilgisini localStorage'dan geri yükle
    const userId = localStorage.getItem('user_id');
    const username = localStorage.getItem('username');
    const role = localStorage.getItem('role');
    const email = localStorage.getItem('email');
    const subscriptionLevel = localStorage.getItem('subscription_level');
    if (userId && username) {
      setUser({ 
        id: parseInt(userId), 
        username: username,
        role: role || 'customer',
        email: email,
        subscription_level: subscriptionLevel || 'free'
      });
    }
    
    setIsLoading(false);
  }, []);

  const login = async (username, password) => {
    try {
      console.log('Logging in user:', username);
      
      // Login yap - session cookie otomatik olarak gönderilecek (withCredentials: true)
      const response = await usersAPI.login(username, password);
      
      console.log('Login successful:', response.data);
      
      setUser(response.data);
      localStorage.setItem('user_id', response.data.id);
      localStorage.setItem('username', response.data.username);
      localStorage.setItem('role', response.data.role);
      localStorage.setItem('email', response.data.email);
      localStorage.setItem('subscription_level', response.data.subscription_level);
      
      return true;
    } catch (error) {
      console.error('Login error:', error.response?.data || error.message);
      return false;
    }
  };

  const register = async (data) => {
    try {
      const response = await usersAPI.register(data);
      // Kaydolduktan hemen sonra login yap
      setUser(response.data);
      localStorage.setItem('user_id', response.data.id);
      localStorage.setItem('username', response.data.username);
      localStorage.setItem('role', response.data.role);
      localStorage.setItem('email', response.data.email);
      localStorage.setItem('subscription_level', response.data.subscription_level || 'free');
      return true;
    } catch (error) {
      console.error('Kayıt hatası:', error.response?.data || error.message);
      return false;
    }
  };

  const logout = () => {
    // Session-based auth olduğu için localStorage'ı temizle
    localStorage.removeItem('user_id');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    localStorage.removeItem('email');
    localStorage.removeItem('subscription_level');
    localStorage.removeItem('access_token');
    setUser(null);
  };

  const updateUser = (userData) => {
    setUser(prev => ({ ...prev, ...userData }));
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}
