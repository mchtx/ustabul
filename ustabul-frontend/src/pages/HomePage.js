import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { workshopsAPI } from '../api';
import AssistantBot from '../components/AssistantBot';

function HomePage() {
  const [categories, setCategories] = useState([]);
  const [premiumWorkshops, setPremiumWorkshops] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [categoriesRes, workshopsRes] = await Promise.all([
        workshopsAPI.getCategories(),
        workshopsAPI.getWorkshops({ is_premium: true })
      ]);
      setCategories(categoriesRes.data.results || categoriesRes.data || []);
      setPremiumWorkshops(workshopsRes.data.results || workshopsRes.data || []);
    } catch (error) {
      console.error('Veri yükleme hatası:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Yükleniyor...</div>;
  }

  return (
    <div className="space-y-12">
      <AssistantBot />
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-orange-500 to-orange-600 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-4xl font-bold mb-4">Adıyaman'da Güvenilir Usta Bulun</h1>
          <p className="text-xl mb-8">Dükkan puan, yorum ve profesyonel referanslarıyla karşılaştırın</p>
          <Link to="/workshops" className="bg-white text-orange-600 px-8 py-3 rounded-lg font-bold hover:bg-gray-50">
            Dükkanları Gözat
          </Link>
        </div>
      </div>

      {/* Kategoriler */}
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8">Kategoriler</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {categories.map((cat) => (
            <Link key={cat.id} to={`/workshops?category=${cat.id}`}
              className="p-6 bg-white rounded-lg shadow hover:shadow-lg hover:bg-orange-50 transition">
              <h3 className="text-lg font-semibold text-gray-800">{cat.name}</h3>
              <p className="text-sm text-gray-600 mt-2">{cat.description}</p>
            </Link>
          ))}
        </div>
      </div>

      {/* Premium Dükkanlar */}
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8">Öne Çıkan Premium Dükkanlar</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {premiumWorkshops.map((ws) => (
            <Link key={ws.id} to={`/workshops/${ws.id}`}
              className="bg-white rounded-lg shadow hover:shadow-lg overflow-hidden transition">
              {ws.image && <img src={ws.image} alt={ws.name} className="w-full h-48 object-cover object-center" />}
              <div className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-bold text-lg text-gray-800">{ws.name}</h3>
                  <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded text-sm">★ {ws.average_rating}</span>
                </div>
                <p className="text-sm text-gray-600 mb-2">{ws.category_name}</p>
                <p className="text-sm text-gray-600">{ws.district}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HomePage;
