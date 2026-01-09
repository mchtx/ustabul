import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks';

function PartsListPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [parts, setParts] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [editingPart, setEditingPart] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  
  const [formData, setFormData] = useState({
    name: '',
    code: '',
    brand: '',
    quantity: 0,
    min_stock_level: 0,
    unit_price: 0,
    current_sale_price: 0,
    notes: '',
    category: ''
  });

  // Parçacı (parts_dealer) rolü kontrolü
  useEffect(() => {
    if (user && user.role !== 'parts_dealer') {
      navigate('/');
    }
  }, [user, navigate]);

  // Parçaları yükle
  useEffect(() => {
    fetchParts();
  }, []);

  const fetchParts = async () => {
    try {
      setIsLoading(true);
      const response = await fetch('http://127.0.0.1:8000/api/inventory/parts/', {
        credentials: 'include'
      });
      if (response.ok) {
        const data = await response.json();
        setParts(data.results || data || []);
      } else {
        console.error('Parçalar yüklenemedi:', response.status);
      }
    } catch (error) {
      console.error('Parçalar yükleme hatası:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name.includes('quantity') || name.includes('price') || name.includes('stock_level') 
        ? parseFloat(value) || 0 
        : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.name.trim()) {
      alert('Parça adı gereklidir');
      return;
    }

    try {
      const method = editingPart ? 'PATCH' : 'POST';
      const url = editingPart 
        ? `http://127.0.0.1:8000/api/inventory/parts/${editingPart.id}/`
        : 'http://127.0.0.1:8000/api/inventory/parts/';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        alert(editingPart ? 'Parça güncellendi!' : 'Parça eklendi!');
        setShowAddModal(false);
        setEditingPart(null);
        setFormData({
          name: '',
          code: '',
          brand: '',
          quantity: 0,
          min_stock_level: 0,
          unit_price: 0,
          current_sale_price: 0,
          notes: '',
          category: ''
        });
        fetchParts();
      } else {
        const error = await response.json();
        alert(`Hata: ${error.detail || 'İşlem başarısız'}`);
      }
    } catch (error) {
      console.error('İşlem hatası:', error);
      alert('İşlem sırasında hata oluştu');
    }
  };

  const handleEdit = (part) => {
    setEditingPart(part);
    setFormData({
      name: part.name || '',
      code: part.code || '',
      brand: part.brand || '',
      quantity: part.quantity || 0,
      min_stock_level: part.min_stock_level || 0,
      unit_price: part.unit_price || 0,
      current_sale_price: part.current_sale_price || 0,
      notes: part.notes || '',
      category: part.category || ''
    });
    setShowAddModal(true);
  };

  const handleDelete = async (partId) => {
    if (!window.confirm('Bu parçayı silmek istediğinize emin misiniz?')) return;

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/inventory/parts/${partId}/`, {
        method: 'DELETE',
        credentials: 'include'
      });

      if (response.ok) {
        alert('Parça silindi!');
        fetchParts();
      } else {
        alert('Silme işlemi başarısız oldu');
      }
    } catch (error) {
      console.error('Silme hatası:', error);
      alert('Silme sırasında hata oluştu');
    }
  };

  const addStockModal = (part) => {
    const quantity = prompt(`${part.name} için kaç adet stok eklemek istiyorsunuz?`, '1');
    if (quantity === null) return;

    const addAmount = parseFloat(quantity);
    if (isNaN(addAmount) || addAmount <= 0) {
      alert('Geçerli bir miktar giriniz');
      return;
    }

    handleEdit({
      ...part,
      quantity: part.quantity + addAmount
    });
  };

  const filteredParts = parts.filter(part =>
    part.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    part.code?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    part.brand?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-orange-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">🔧 Parça Yönetimi</h1>
          <p className="text-gray-600">Stoklarınızı yönetin ve takip edin</p>
        </div>

        {/* Arama ve Butonlar */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <div className="flex flex-col sm:flex-row gap-4 items-center">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Parça adı, kod veya markaya göre ara..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
            />
            <button
              onClick={() => {
                setEditingPart(null);
                setFormData({
                  name: '',
                  code: '',
                  brand: '',
                  quantity: 0,
                  min_stock_level: 0,
                  unit_price: 0,
                  current_sale_price: 0,
                  notes: '',
                  category: ''
                });
                setShowAddModal(true);
              }}
              className="bg-green-600 hover:bg-green-700 text-white font-bold px-6 py-2 rounded-lg transition"
            >
              ➕ Yeni Parça Ekle
            </button>
          </div>
        </div>

        {/* Parça Listesi */}
        {filteredParts.length === 0 ? (
          <div className="bg-white rounded-lg shadow p-12 text-center">
            <p className="text-gray-500 text-lg mb-4">
              {searchQuery ? 'Arama sonucu bulunamadı.' : 'Henüz parça eklenmemiş.'}
            </p>
            {!searchQuery && (
              <button
                onClick={() => setShowAddModal(true)}
                className="bg-orange-600 hover:bg-orange-700 text-white font-bold px-6 py-3 rounded-lg transition"
              >
                İlk Parçayı Ekle
              </button>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredParts.map(part => (
              <div
                key={part.id}
                className="bg-white rounded-lg shadow-lg hover:shadow-xl transition p-6 border border-gray-100"
              >
                <div className="flex justify-between items-start mb-3">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-900">{part.name}</h3>
                    {part.code && (
                      <p className="text-sm text-gray-500">Kod: {part.code}</p>
                    )}
                  </div>
                  {part.quantity <= (part.min_stock_level || 10) && (
                    <span className="bg-red-100 text-red-700 px-2 py-1 rounded text-xs font-bold">
                      ⚠️ Düşük
                    </span>
                  )}
                </div>

                <div className="space-y-2 mb-4">
                  {part.brand && (
                    <div className="text-sm text-gray-600">
                      <strong>Marka:</strong> {part.brand}
                    </div>
                  )}
                  <div className="text-sm">
                    <strong className="text-gray-700">Stok:</strong>
                    <span className={`ml-2 font-bold ${part.quantity <= (part.min_stock_level || 10) ? 'text-red-600' : 'text-green-600'}`}>
                      {part.quantity} adet
                    </span>
                  </div>
                  {part.unit_price > 0 && (
                    <div className="text-sm text-gray-600">
                      <strong>Birim Fiyat:</strong> {parseFloat(part.unit_price).toFixed(2)} TL
                    </div>
                  )}
                  {part.current_sale_price > 0 && (
                    <div className="text-sm text-orange-600 font-bold">
                      Satış Fiyatı: {parseFloat(part.current_sale_price).toFixed(2)} TL
                    </div>
                  )}
                </div>

                {part.notes && (
                  <p className="text-xs text-gray-500 mb-4 italic">{part.notes}</p>
                )}

                <div className="flex gap-2">
                  <button
                    onClick={() => addStockModal(part)}
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-bold px-3 py-2 rounded transition text-sm"
                  >
                    📦 Stok Ekle
                  </button>
                  <button
                    onClick={() => handleEdit(part)}
                    className="flex-1 bg-orange-600 hover:bg-orange-700 text-white font-bold px-3 py-2 rounded transition text-sm"
                  >
                    ✏️ Düzenle
                  </button>
                  <button
                    onClick={() => handleDelete(part.id)}
                    className="flex-1 bg-red-600 hover:bg-red-700 text-white font-bold px-3 py-2 rounded transition text-sm"
                  >
                    🗑️ Sil
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add/Edit Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg shadow-2xl max-w-2xl w-full max-h-96 overflow-y-auto">
            <div className="sticky top-0 bg-orange-600 text-white p-6 flex justify-between items-center">
              <h2 className="text-2xl font-bold">
                {editingPart ? '✏️ Parçayı Düzenle' : '➕ Yeni Parça Ekle'}
              </h2>
              <button
                onClick={() => setShowAddModal(false)}
                className="text-2xl font-bold hover:bg-orange-700 rounded-full w-8 h-8 flex items-center justify-center"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Parça Adı *
                  </label>
                  <input
                    type="text"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Parça Kodu
                  </label>
                  <input
                    type="text"
                    name="code"
                    value={formData.code}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Marka
                  </label>
                  <input
                    type="text"
                    name="brand"
                    value={formData.brand}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Stok Miktarı
                  </label>
                  <input
                    type="number"
                    name="quantity"
                    value={formData.quantity}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
                    min="0"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Min. Stok Seviyesi
                  </label>
                  <input
                    type="number"
                    name="min_stock_level"
                    value={formData.min_stock_level}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
                    min="0"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Birim Fiyatı (TL)
                  </label>
                  <input
                    type="number"
                    name="unit_price"
                    value={formData.unit_price}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
                    min="0"
                    step="0.01"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Satış Fiyatı (TL)
                  </label>
                  <input
                    type="number"
                    name="current_sale_price"
                    value={formData.current_sale_price}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
                    min="0"
                    step="0.01"
                  />
                </div>

                <div>
                  <label className="block text-sm font-bold text-gray-700 mb-2">
                    Kategori
                  </label>
                  <input
                    type="text"
                    name="category"
                    value={formData.category}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-bold text-gray-700 mb-2">
                  Notlar
                </label>
                <textarea
                  name="notes"
                  value={formData.notes}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 outline-none"
                  rows="3"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="submit"
                  className="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-2 rounded-lg transition"
                >
                  {editingPart ? '💾 Güncelle' : '➕ Ekle'}
                </button>
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="flex-1 bg-gray-400 hover:bg-gray-500 text-white font-bold py-2 rounded-lg transition"
                >
                  ✕ İptal
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default PartsListPage;

