import React, { useState, useEffect, useCallback } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { workshopsAPI } from '../api';

function WorkshopListPage() {
  const [workshops, setWorkshops] = useState([]);
  const [categories, setCategories] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchParams] = useSearchParams();
  const [currentPage, setCurrentPage] = useState(1);
  const ITEMS_PER_PAGE = 6;
  
  const [filters, setFilters] = useState({
    category: searchParams.get('category') || '',
    district: '',
    min_rating: '',
    search: '',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setIsLoading(true);
        const [categoriesRes, workshopsRes] = await Promise.all([
          workshopsAPI.getCategories(),
          workshopsAPI.getWorkshops(filters)
        ]);
        setCategories(categoriesRes.data.results || categoriesRes.data || []);
        setWorkshops(workshopsRes.data.results || workshopsRes.data || []);
      } catch (error) {
        console.error('Veri yükleme hatası:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchData();
  }, [filters]);

  const handleFilterChange = useCallback((e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value }));
    setCurrentPage(1); // Filtre değişince sayfa 1'e dön
  }, []);

  const StarRating = ({ rating, reviews }) => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span key={i} className={i <= Math.floor(rating) ? 'text-yellow-400' : 'text-gray-300'}>
          ★
        </span>
      );
    }
    return (
      <div className="flex items-center gap-2">
        <div className="flex text-sm">{stars}</div>
        <span className="text-xs text-gray-600 font-medium">{rating.toFixed(1)}</span>
        <span className="text-xs text-gray-500">({reviews})</span>
      </div>
    );
  };

  // Kategori renklerini belirle
  const getCategoryColor = (categoryName) => {
    const colors = {
      'Elektrikçi': 'from-yellow-100 to-yellow-50 border-yellow-200',
      'Tesisatçı': 'from-blue-100 to-blue-50 border-blue-200',
      'Marangoz': 'from-amber-100 to-amber-50 border-amber-200',
      'Boyacı': 'from-red-100 to-red-50 border-red-200',
      'Cam Ustası': 'from-cyan-100 to-cyan-50 border-cyan-200',
      'Asansörcü': 'from-indigo-100 to-indigo-50 border-indigo-200',
      'Kaloriferci': 'from-orange-100 to-orange-50 border-orange-200',
      'Cam Ustası': 'from-slate-100 to-slate-50 border-slate-200',
    };
    return colors[categoryName] || 'from-gray-100 to-gray-50 border-gray-200';
  };

  // Kategori ikonu belirle
  const getCategoryIcon = (categoryName) => {
    const icons = {
      'Elektrikçi': '⚡',
      'Tesisatçı': '🔧',
      'Marangoz': '🪵',
      'Boyacı': '🎨',
      'Cam Ustası': '🪟',
      'Asansörcü': '🏢',
      'Kaloriferci': '🔥',
    };
    return icons[categoryName] || '🏪';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Hero Alanı */}
      <div className="bg-gradient-to-r from-orange-500 via-orange-600 to-red-600 text-white py-12">
        <div className="w-full px-4">
          <div className="max-w-full">
            <h1 className="text-5xl font-bold mb-3">Dükkanları Keşfet</h1>
            <p className="text-xl text-orange-100 mb-8">En iyi dükkanları keşfet, işçileri puanla ve gözden kaçırmayacak hizmetler al</p>
            
            {/* Hero Arama Alanı */}
            <div className="flex gap-3">
              <input
                type="text"
                name="search"
                value={filters.search}
                onChange={handleFilterChange}
                placeholder="Dükkân, kategori veya işçi adı ara..."
                className="flex-1 px-6 py-3 rounded-lg text-gray-900 focus:outline-none focus:ring-4 focus:ring-orange-300 transition text-lg"
              />
              <button className="bg-white hover:bg-gray-50 text-orange-600 font-bold px-8 py-3 rounded-lg transition shadow-lg hover:shadow-xl">
                🔍 Ara
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Ana İçerik */}
      <div className="w-full px-4 py-8 relative">
        {/* Arka plan şeridi */}
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-gradient-to-b from-gray-200 to-gray-100 opacity-40 rounded-3xl"></div>
        
        <div className="max-w-full relative z-10">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Sol: Filtre Paneli */}
            <div className="lg:col-span-2">
              <div className="sticky top-4 bg-white rounded-2xl shadow-lg p-6 border border-gray-100 h-fit">
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                  <span className="text-2xl">🔍</span> Filtrele
                </h2>
                
                <div className="space-y-6">
                  {/* Kategori */}
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">Kategori</label>
                    <select
                      name="category"
                      value={filters.category}
                      onChange={handleFilterChange}
                      className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition text-sm appearance-none bg-white cursor-pointer"
                    >
                      <option value="">Tüm Kategoriler</option>
                      {categories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                      ))}
                    </select>
                  </div>

                  {/* İlçe */}
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">İlçe</label>
                    <input
                      type="text"
                      name="district"
                      value={filters.district}
                      onChange={handleFilterChange}
                      placeholder="İlçe adı..."
                      className="w-full px-4 py-2.5 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent transition text-sm"
                    />
                  </div>

                  {/* Minimum Puan */}
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-3">Minimum Puan</label>
                    <div className="space-y-2">
                      {[
                        { value: '', label: 'Tümü' },
                        { value: '3', label: '⭐ 3 yıldız +' },
                        { value: '4', label: '⭐ 4 yıldız +' },
                        { value: '5', label: '⭐ 5 yıldız' }
                      ].map(option => (
                        <label key={option.value} className="flex items-center gap-3 cursor-pointer group">
                          <input
                            type="radio"
                            name="min_rating"
                            value={option.value}
                            checked={filters.min_rating === option.value}
                            onChange={handleFilterChange}
                            className="w-4 h-4 text-orange-500 cursor-pointer"
                          />
                          <span className="text-sm text-gray-700 group-hover:text-orange-600 transition">{option.label}</span>
                        </label>
                      ))}
                    </div>
                  </div>

                  {/* Reset Filtresi */}
                  <button
                    onClick={() => setFilters({ category: '', district: '', min_rating: '', search: '' })}
                    className="w-full py-2.5 bg-gradient-to-r from-gray-200 to-gray-300 hover:from-gray-300 hover:to-gray-400 text-gray-700 rounded-lg font-medium transition text-sm"
                  >
                    Sıfırla
                  </button>
                </div>
              </div>
            </div>

            {/* Ortada: Dükkan Grid (1 sütun - büyük kartlar) */}
            <div className="lg:col-span-10">
              {isLoading ? (
                <div className="flex items-center justify-center py-20">
                  <div className="text-center">
                    <div className="w-12 h-12 border-4 border-orange-200 border-t-orange-500 rounded-full animate-spin mx-auto mb-4"></div>
                    <p className="text-gray-600">Yükleniyor...</p>
                  </div>
                </div>
              ) : workshops.length === 0 ? (
                <div className="bg-white rounded-2xl shadow-lg p-12 text-center border border-gray-100">
                  <p className="text-2xl mb-2">🔍</p>
                  <p className="text-gray-600 text-lg">Arama kriterlerine uygun dükkân bulunamadı.</p>
                  <p className="text-gray-500 text-sm mt-2">Filtrelerinizi değiştirmeyi deneyin.</p>
                </div>
              ) : (
                <div>
                  <div className="grid grid-cols-2 gap-6">
                    {workshops.slice((currentPage - 1) * ITEMS_PER_PAGE, currentPage * ITEMS_PER_PAGE).map((ws) => (
                      <Link
                        key={ws.id}
                        to={`/workshops/${ws.id}`}
                        className={`bg-gradient-to-br ${getCategoryColor(ws.category_name)} rounded-2xl shadow-md hover:shadow-2xl transition-all duration-300 overflow-hidden border group flex flex-col h-80 relative`}
                      >
                        {/* Resim - Arka Plan (Tamamı) */}
                        <div className="absolute inset-0 w-full h-full">
                          {ws.image ? (
                            <img
                              src={ws.image}
                              alt={ws.name}
                              className="w-full h-full object-cover object-center group-hover:scale-110 transition-transform duration-300"
                            />
                          ) : (
                            <div className={`w-full h-full bg-gradient-to-br ${getCategoryColor(ws.category_name)} flex items-center justify-center text-7xl`}>
                              {getCategoryIcon(ws.category_name)}
                            </div>
                          )}
                          {/* Üzerine siyah overlay */}
                          <div className="absolute inset-0 bg-gradient-to-t from-black via-black/30 to-transparent"></div>
                        </div>

                        {/* İçerik - Alt Köşe */}
                        <div className="absolute bottom-0 left-0 right-0 p-4 z-10">
                          <div className="flex items-start justify-between gap-2 mb-2">
                            <div className="flex-1 min-w-0">
                              <h3 className="font-bold text-base text-white group-hover:text-orange-300 transition line-clamp-1">
                                {ws.name}
                              </h3>
                              <p className="text-xs text-orange-100 font-medium truncate">{ws.category_name}</p>
                            </div>
                            {ws.is_premium && (
                              <div className="bg-gradient-to-r from-orange-400 to-red-500 text-white px-2 py-0.5 rounded-full text-xs font-bold whitespace-nowrap">
                                ⭐
                              </div>
                            )}
                          </div>

                          <p className="text-xs text-orange-100 mb-1">📍 {ws.district}</p>
                          
                          {ws.phone && (
                            <p className="text-xs text-orange-100 line-clamp-1">
                              📞 {ws.phone}
                            </p>
                          )}

                          {/* Puan - Çok Küçük */}
                          <div className="flex items-center gap-1 mt-2 text-xs">
                            <div className="flex text-xs gap-0.5">
                              {[...Array(5)].map((_, i) => (
                                <span key={i} className={i < Math.floor(ws.average_rating || 0) ? 'text-yellow-300' : 'text-gray-300'}>
                                  ★
                                </span>
                              ))}
                            </div>
                            <span className="text-orange-100 font-semibold">{(ws.average_rating || 0).toFixed(1)}</span>
                            <span className="text-orange-200">({ws.total_reviews || 0})</span>
                          </div>
                        </div>
                      </Link>
                    ))}
                  </div>

                  {/* Pagination */}
                  {workshops.length > ITEMS_PER_PAGE && (
                    <div className="mt-8 flex items-center justify-center gap-2">
                      <button
                        onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                        disabled={currentPage === 1}
                        className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
                      >
                        ← Önceki
                      </button>

                      <div className="flex gap-1">
                        {Array.from({ length: Math.ceil(workshops.length / ITEMS_PER_PAGE) }).map((_, index) => (
                          <button
                            key={index + 1}
                            onClick={() => setCurrentPage(index + 1)}
                            className={`px-3 py-2 rounded-lg font-medium transition ${
                              currentPage === index + 1
                                ? 'bg-gradient-to-r from-orange-500 to-red-600 text-white shadow-lg'
                                : 'border border-gray-300 text-gray-700 hover:bg-gray-50'
                            }`}
                          >
                            {index + 1}
                          </button>
                        ))}
                      </div>

                      <button
                        onClick={() => setCurrentPage(prev => Math.min(Math.ceil(workshops.length / ITEMS_PER_PAGE), prev + 1))}
                        disabled={currentPage === Math.ceil(workshops.length / ITEMS_PER_PAGE)}
                        className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition font-medium"
                      >
                        Sonraki →
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Sağ Panel - Aşağıda */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-8">
            <div className="lg:col-span-2"></div>
            
            <div className="lg:col-span-10 space-y-6">
              {/* Premium Ustalar */}
              <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
                  <span className="text-2xl">⭐</span> Premium Ustalar
                </h3>
                <div className="space-y-3">
                  {workshops
                    .filter(w => w.is_premium)
                    .slice(0, 5)
                    .map(ws => (
                      <Link
                        key={ws.id}
                        to={`/workshops/${ws.id}`}
                        className="block p-3 bg-gradient-to-r from-orange-50 to-red-50 rounded-lg hover:shadow-md transition border border-orange-100"
                      >
                        <div className="flex items-start gap-2">
                          <span className="text-xl">{getCategoryIcon(ws.category_name)}</span>
                          <div className="flex-1 min-w-0">
                            <p className="font-semibold text-sm text-gray-900 truncate">{ws.name}</p>
                            <p className="text-xs text-gray-600">{ws.category_name}</p>
                            <div className="flex gap-1 mt-1">
                              {[...Array(5)].map((_, i) => (
                                <span key={i} className={i < Math.floor(ws.average_rating || 0) ? 'text-yellow-400' : 'text-gray-300'}>
                                  ★
                                </span>
                              ))}
                            </div>
                          </div>
                        </div>
                      </Link>
                    ))}
                </div>
              </div>

              {/* Popüler Aramalar */}
              <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
                  <span className="text-2xl">🔥</span> Popüler Aramalar
                </h3>
                <div className="space-y-2">
                  {['Elektrikçi', 'Tesisatçı', 'Marangoz', 'Boyacı', 'Cam Ustası'].map(cat => (
                    <button
                      key={cat}
                      onClick={() => setFilters(prev => ({ ...prev, category: categories.find(c => c.name === cat)?.id || '' }))}
                      className="w-full text-left px-4 py-2 bg-gradient-to-r from-orange-50 to-red-50 hover:from-orange-100 hover:to-red-100 text-gray-800 rounded-lg transition border border-orange-100 text-sm font-medium"
                    >
                      🔍 {cat}
                    </button>
                  ))}
                </div>
              </div>

              {/* Bize Katıl CTA */}
              <div className="bg-gradient-to-br from-orange-500 to-red-600 rounded-2xl shadow-lg p-6 text-white border border-orange-400">
                <h3 className="font-bold text-lg mb-3 flex items-center gap-2">
                  <span className="text-2xl">🚀</span> Işletmeni Ekle
                </h3>
                <p className="text-sm text-orange-100 mb-4">Platformda yer alarak müşterilere ulaş ve işini büyüt</p>
                <button className="w-full bg-white text-orange-600 font-bold py-2 rounded-lg hover:bg-orange-50 transition">
                  Hemen Başla →
                </button>
              </div>

              {/* İletişim & Destek */}
              <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                <h3 className="font-bold text-lg text-gray-900 mb-4 flex items-center gap-2">
                  <span className="text-2xl">💬</span> Bize Ulaş
                </h3>
                <div className="space-y-3 text-sm">
                  <div className="flex items-center gap-2 text-gray-700">
                    <span className="text-lg">📞</span>
                    <span>(380) 215-2520</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-700">
                    <span className="text-lg">📧</span>
                    <span>info@ustabul.com</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-700">
                    <span className="text-lg">📍</span>
                    <span>Adıyaman, Türkiye</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default WorkshopListPage;
