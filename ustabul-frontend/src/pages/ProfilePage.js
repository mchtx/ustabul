import React, { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks';
import { reviewsAPI, usersAPI } from '../api';

function ProfilePage() {
  const { user, isLoading, logout, updateUser } = useAuth();
  const [userReviews, setUserReviews] = useState([]);
  const [reviewsLoading, setReviewsLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!isLoading && !user) {
      navigate('/login');
    }
  }, [user, isLoading, navigate]);

  useEffect(() => {
    if (user) {
      fetchUserReviews();
      fetchUserProfile();
    }
  }, [user?.id]); // Only re-run if user ID changes

  const fetchUserProfile = async () => {
    try {
      const response = await usersAPI.getProfile();
      updateUser(response.data);
    } catch (error) {
      console.error('Profil bilgileri yüklenemedi:', error);
    }
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('profile_picture', file);

    try {
      setUploading(true);
      const response = await usersAPI.updateProfile(formData);
      updateUser(response.data);
      alert('Profil resmi güncellendi!');
    } catch (error) {
      console.error('Profil resmi yükleme hatası:', error);
      alert('Profil resmi yüklenirken bir hata oluştu.');
    } finally {
      setUploading(false);
    }
  };

  const fetchUserReviews = async () => {
    try {
      setReviewsLoading(true);
      // Tüm reviews'i al (with approved ve pending)
      const response = await reviewsAPI.getReviews();
      let allReviews = response.data.results || response.data || [];
      
      // Eğer results boşsa, doğrudan array olabilir
      if (!Array.isArray(allReviews)) {
        allReviews = [];
      }
      
      // User'ın kendi review'larını filtrele
      const filtered = allReviews.filter(r => {
        return r.user_id === user?.id;
      });
      
      setUserReviews(filtered);
    } catch (error) {
      console.error('Yorum yükleme hatası:', error);
      setUserReviews([]);
    } finally {
      setReviewsLoading(false);
    }
  };

  if (isLoading) {
    return <div className="text-center py-8">Yükleniyor...</div>;
  }

  if (!user) {
    return null;
  }

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const StarRating = ({ rating }) => {
    return (
      <div className="flex gap-1">
        {[...Array(5)].map((_, i) => (
          <span key={i} className={i < rating ? 'text-yellow-400 text-lg' : 'text-gray-300 text-lg'}>
            ★
          </span>
        ))}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-orange-500 via-orange-600 to-red-600 text-white py-12 mb-8">
        <div className="max-w-6xl mx-auto px-4">
          <h1 className="text-5xl font-bold mb-2">Profilim</h1>
          <p className="text-orange-100 text-lg">Kişisel bilgileriniz ve yorumlarınız</p>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Sol: Profil Bilgileri */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 sticky top-4">
              <div className="text-center mb-6 relative group">
                <div className="w-32 h-32 mx-auto rounded-full overflow-hidden border-4 border-orange-100 shadow-md relative">
                  {user.profile_picture ? (
                    <img 
                      src={user.profile_picture} 
                      alt="Profil" 
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center text-white text-5xl font-bold">
                      {user.first_name?.[0]?.toUpperCase() || user.username?.[0]?.toUpperCase() || '👤'}
                    </div>
                  )}
                  
                  {/* Upload Overlay */}
                  <div 
                    onClick={() => fileInputRef.current.click()}
                    className="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer"
                  >
                    <span className="text-white font-bold text-sm">📷 Değiştir</span>
                  </div>
                </div>
                
                <input 
                  type="file" 
                  ref={fileInputRef} 
                  onChange={handleFileChange} 
                  className="hidden" 
                  accept="image/*"
                />
                
                {uploading && <p className="text-xs text-orange-500 mt-2">Yükleniyor...</p>}

                <h2 className="text-2xl font-bold text-gray-900 mt-4">{user.first_name || user.username}</h2>
                <p className="text-gray-600 text-sm">@{user.username}</p>
              </div>

              <div className="space-y-4 border-t border-gray-100 pt-6">
                <div>
                  <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Ad Soyadı</label>
                  <p className="text-lg font-semibold text-gray-800 mt-1">{user.first_name || '-'} {user.last_name || '-'}</p>
                </div>

                <div>
                  <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide">E-posta</label>
                  <p className="text-sm font-medium text-gray-700 mt-1 break-all">{user.email || '-'}</p>
                </div>

                <div>
                  <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Telefon</label>
                  <p className="text-sm font-medium text-gray-700 mt-1">{user.phone || '-'}</p>
                </div>

                <div>
                  <label className="text-xs font-semibold text-gray-600 uppercase tracking-wide">Rol</label>
                  <div className="mt-1">
                    <span className="inline-block px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                      {user.role === 'customer' ? '👤 Müşteri' : user.role === 'workshop' ? '🏪 Dükkân Sahibi' : user.role === 'parts_dealer' ? '🔧 Parçacı' : '⚙️ Admin'}
                    </span>
                  </div>
                </div>

                {user.is_premium && (
                  <div className="mt-4 p-3 bg-gradient-to-r from-orange-50 to-red-50 rounded-lg border border-orange-200">
                    <p className="text-orange-800 font-semibold flex items-center gap-2">
                      <span className="text-lg">⭐</span> Premium Üyesi
                    </p>
                  </div>
                )}

                <div className="pt-4 space-y-2">
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <span>📊</span>
                    <span>Toplam Yorum: <strong className="text-gray-900">{userReviews.length}</strong></span>
                  </div>
                  <div className="flex items-center gap-2 text-sm text-gray-600">
                    <span>⭐</span>
                    <span>Ortalama Puan: <strong className="text-gray-900">{userReviews.length > 0 ? (userReviews.reduce((sum, r) => sum + r.rating, 0) / userReviews.length).toFixed(1) : '-'}</strong></span>
                  </div>
                </div>
              </div>

              <button
                onClick={handleLogout}
                className="mt-8 w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white py-3 rounded-lg font-bold transition shadow-lg"
              >
                🚪 Çıkış Yap
              </button>
            </div>
          </div>

          {/* Sağ: Yorumlar */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100 mb-8">
              <h3 className="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-2">
                <span className="text-3xl">💬</span> Attığım Yorumlar
              </h3>

              {reviewsLoading ? (
                <div className="flex items-center justify-center py-12">
                  <div className="text-center">
                    <div className="w-10 h-10 border-4 border-orange-200 border-t-orange-500 rounded-full animate-spin mx-auto mb-3"></div>
                    <p className="text-gray-600">Yorum yükleniyor...</p>
                  </div>
                </div>
              ) : userReviews.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-4xl mb-3">📝</p>
                  <p className="text-gray-600 text-lg">Henüz yorum yapmadınız</p>
                  <p className="text-gray-500 text-sm mt-2">Beğendiğiniz dükkanları ziyaret etip yorum yapabilirsiniz</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {userReviews.map((review) => (
                    <div
                      key={review.id}
                      className="p-5 bg-gradient-to-r from-orange-50 to-red-50 rounded-xl border-2 border-orange-200 hover:shadow-md transition"
                    >
                      <div className="flex items-start justify-between gap-4 mb-3">
                        <div className="flex-1">
                          <h4 className="font-bold text-gray-900 text-lg">
                            {review.workshop_name || 'Dükkân'}
                          </h4>
                          <p className="text-xs text-gray-600 mt-1">
                            {review.workshop_category_name && (
                              <span className="inline-block bg-blue-100 text-blue-700 px-2 py-1 rounded">
                                {review.workshop_category_name}
                              </span>
                            )}
                          </p>
                        </div>
                        <div className="text-right">
                          <StarRating rating={review.rating} />
                          <p className="text-xs text-gray-600 mt-1">
                            {new Date(review.created_at).toLocaleDateString('tr-TR', {
                              year: 'numeric',
                              month: 'long',
                              day: 'numeric'
                            })}
                          </p>
                        </div>
                      </div>

                      {review.comment && (
                        <p className="text-gray-700 bg-white rounded-lg p-3 text-sm leading-relaxed">
                          "{review.comment}"
                        </p>
                      )}

                      {review.is_approved ? (
                        <div className="mt-3 flex items-center gap-1 text-xs text-green-700 font-semibold">
                          <span>✓</span> Onaylandı
                        </div>
                      ) : (
                        <div className="mt-3 flex items-center gap-1 text-xs text-yellow-700 font-semibold">
                          <span>⏳</span> Onay Beklemede
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* İstatistikler Kartı */}
            <div className="bg-gradient-to-br from-orange-500 to-red-600 rounded-2xl shadow-lg p-8 text-white border border-orange-400">
              <h3 className="text-2xl font-bold mb-6">📈 İstatistiklerim</h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur-sm">
                  <p className="text-orange-100 text-sm font-medium">Toplam Yorum</p>
                  <p className="text-3xl font-bold mt-1">{userReviews.length}</p>
                </div>
                <div className="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur-sm">
                  <p className="text-orange-100 text-sm font-medium">Onaylı Yorum</p>
                  <p className="text-3xl font-bold mt-1">{userReviews.filter(r => r.is_approved).length}</p>
                </div>
                <div className="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur-sm">
                  <p className="text-orange-100 text-sm font-medium">Ortalama Puan</p>
                  <p className="text-3xl font-bold mt-1">
                    {userReviews.length > 0 ? (userReviews.reduce((sum, r) => sum + r.rating, 0) / userReviews.length).toFixed(1) : '-'}
                  </p>
                </div>
                <div className="bg-white bg-opacity-20 rounded-lg p-4 backdrop-blur-sm">
                  <p className="text-orange-100 text-sm font-medium">En Yüksek Puan</p>
                  <p className="text-3xl font-bold mt-1">
                    {userReviews.length > 0 ? Math.max(...userReviews.map(r => r.rating)) : '-'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
