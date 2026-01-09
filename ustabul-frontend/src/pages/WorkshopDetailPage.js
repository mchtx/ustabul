import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { workshopsAPI, reviewsAPI, messagingAPI } from '../api';
import { useAuth } from '../hooks';

function WorkshopDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [workshop, setWorkshop] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [reviewError, setReviewError] = useState('');
  const [reviewSuccess, setReviewSuccess] = useState('');
  const [conversationError, setConversationError] = useState('');
  const [conversationSuccess, setConversationSuccess] = useState('');
  const [newReview, setNewReview] = useState({ rating: 5, comment: '' });

  const fetchData = async () => {
    try {
      setIsLoading(true);
      const [workshopRes, reviewsRes] = await Promise.all([
        workshopsAPI.getWorkshop(id),
        reviewsAPI.getReviews(id)
      ]);
      setWorkshop(workshopRes.data);
      setReviews(reviewsRes.data.results || reviewsRes.data || []);
    } catch (error) {
      console.error('Veri yükleme hatası:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  const handleSubmitReview = async () => {
    setReviewError('');
    setReviewSuccess('');

    if (!newReview.comment.trim()) {
      setReviewError('Lütfen bir yorum yazınız.');
      return;
    }

    try {
      setIsSubmitting(true);
      await reviewsAPI.createReview(id, newReview);
      setNewReview({ rating: 5, comment: '' });
      setReviewSuccess('Yorumunuz başarıyla gönderildi!');
      await fetchData();
      setTimeout(() => setReviewSuccess(''), 3000);
    } catch (error) {
      console.error('Yorum gönderme hatası:', error);
      setReviewError(error.response?.data?.detail || 'Yorum gönderirken hata oluştu.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleStartConversation = async () => {
    setConversationError('');
    setConversationSuccess('');

    if (!user) {
      setConversationError('Mesaj göndermek için giriş yapmalısınız.');
      return;
    }

    try {
      setIsSubmitting(true);
      const response = await messagingAPI.startConversation({ workshop_id: id });
      setConversationSuccess('Sohbet başlatıldı! Mesaj sayfasına yönlendiriliyorsunuz...');
      // Mesaj sayfasına yönlendir
      setTimeout(() => {
        navigate(`/messages/${response.data.id}`);
      }, 1000);
    } catch (error) {
      console.error('Sohbet başlatma hatası:', error);
      setConversationError(error.response?.data?.detail || 'Sohbet başlatırken hata oluştu.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-orange-500"></div>
      </div>
    );
  }

  if (!workshop) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Dükkân Bulunamadı</h2>
          <p className="text-gray-600">Aradığınız dükkân mevcut değil veya kaldırılmış olabilir.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 pb-12">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-orange-500 via-orange-600 to-red-600 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-start justify-between gap-6">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <span className="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium border border-white/30">
                  {workshop.category_name}
                </span>
                {workshop.is_premium && (
                  <span className="bg-yellow-400 text-yellow-900 px-3 py-1 rounded-full text-sm font-bold shadow-sm">
                    ⭐ PREMIUM
                  </span>
                )}
              </div>
              <h1 className="text-4xl md:text-5xl font-bold mb-2">{workshop.name}</h1>
              <div className="flex items-center gap-4 text-orange-100 text-lg">
                <span className="flex items-center gap-1">
                  📍 {workshop.district}
                </span>
                <span className="flex items-center gap-1">
                  ⭐ {workshop.average_rating.toFixed(1)} ({workshop.total_reviews} yorum)
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Image & Info & Reviews */}
          <div className="lg:col-span-2 space-y-8">
            {/* Image Card */}
            <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-100">
              {workshop.image ? (
                <img 
                  src={workshop.image} 
                  alt={workshop.name} 
                  className="w-full h-96 object-cover"
                />
              ) : (
                <div className="w-full h-96 bg-gray-100 flex items-center justify-center text-gray-400 text-6xl">
                  🏪
                </div>
              )}
            </div>

            {/* About Section */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span className="text-orange-500">📝</span> Hakkında
              </h2>
              <p className="text-gray-700 leading-relaxed text-lg">
                {workshop.description}
              </p>
            </div>

            {/* Reviews Section */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center justify-between mb-8">
                <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <span className="text-orange-500">💬</span> Yorumlar
                </h2>
                <span className="bg-orange-100 text-orange-700 px-4 py-1 rounded-full font-medium">
                  {reviews.length} Değerlendirme
                </span>
              </div>

              {/* Review Form */}
              {user ? (
                <div className="bg-gray-50 rounded-xl p-6 mb-8 border border-gray-200">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Deneyiminizi Paylaşın</h3>
                  
                  {reviewError && (
                    <div className="bg-red-50 text-red-600 p-3 rounded-lg mb-4 text-sm">
                      {reviewError}
                    </div>
                  )}
                  {reviewSuccess && (
                    <div className="bg-green-50 text-green-600 p-3 rounded-lg mb-4 text-sm">
                      {reviewSuccess}
                    </div>
                  )}

                  <div className="mb-4">
                    <div className="flex gap-2 mb-2">
                      {[1, 2, 3, 4, 5].map(star => (
                        <button
                          key={star}
                          onClick={() => setNewReview({ ...newReview, rating: star })}
                          className={`text-3xl transition-colors ${
                            star <= newReview.rating ? 'text-yellow-400' : 'text-gray-300'
                          } hover:text-yellow-500`}
                        >
                          ★
                        </button>
                      ))}
                    </div>
                    <span className="text-sm text-gray-500">Puanınız: {newReview.rating}/5</span>
                  </div>

                  <textarea
                    value={newReview.comment}
                    onChange={(e) => setNewReview({ ...newReview, comment: e.target.value })}
                    placeholder="Bu dükkan hakkında ne düşünüyorsunuz?"
                    className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-orange-500 focus:border-transparent outline-none transition mb-4 min-h-[100px]"
                  />

                  <button
                    onClick={handleSubmitReview}
                    disabled={isSubmitting}
                    className="bg-orange-600 hover:bg-orange-700 text-white font-bold py-2 px-6 rounded-lg transition shadow-md disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isSubmitting ? 'Gönderiliyor...' : 'Yorum Yap'}
                  </button>
                </div>
              ) : (
                <div className="bg-blue-50 text-blue-800 p-4 rounded-xl mb-8 text-center">
                  Yorum yapmak için <a href="/login" className="font-bold underline">giriş yapmalısınız</a>.
                </div>
              )}

              {/* Reviews List */}
              <div className="space-y-6">
                {reviews.length === 0 ? (
                  <p className="text-center text-gray-500 py-8">Henüz yorum yapılmamış.</p>
                ) : (
                  reviews.map(review => (
                    <div key={review.id} className="border-b border-gray-100 last:border-0 pb-6 last:pb-0">
                      <div className="flex justify-between items-start mb-2">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-orange-100 rounded-full flex items-center justify-center text-orange-600 font-bold">
                            {(review.user_name || 'A')[0].toUpperCase()}
                          </div>
                          <div>
                            <p className="font-bold text-gray-900">{review.user_name || 'Anonim'}</p>
                            <div className="flex text-yellow-400 text-sm">
                              {[...Array(5)].map((_, i) => (
                                <span key={i}>{i < review.rating ? '★' : '☆'}</span>
                              ))}
                            </div>
                          </div>
                        </div>
                        <span className="text-sm text-gray-400">
                          {new Date(review.created_at).toLocaleDateString('tr-TR')}
                        </span>
                      </div>
                      <p className="text-gray-600 mt-2 pl-13">{review.comment}</p>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Right Column: Sticky Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-8 space-y-6">
              {/* Contact Card */}
              <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                <h3 className="text-xl font-bold text-gray-900 mb-6">İletişim Bilgileri</h3>
                
                <div className="space-y-4">
                  <div className="flex items-center gap-4 p-3 bg-gray-50 rounded-xl">
                    <div className="w-10 h-10 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xl">
                      📞
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Telefon</p>
                      <p className="font-bold text-gray-900">{workshop.phone}</p>
                    </div>
                  </div>

                  {workshop.whatsapp && (
                    <div className="flex items-center gap-4 p-3 bg-green-50 rounded-xl">
                      <div className="w-10 h-10 bg-green-100 text-green-600 rounded-full flex items-center justify-center text-xl">
                        💬
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">WhatsApp</p>
                        <p className="font-bold text-gray-900">{workshop.whatsapp}</p>
                      </div>
                    </div>
                  )}

                  {workshop.email && (
                    <div className="flex items-center gap-4 p-3 bg-purple-50 rounded-xl">
                      <div className="w-10 h-10 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center text-xl">
                        📧
                      </div>
                      <div>
                        <p className="text-sm text-gray-500">Email</p>
                        <p className="font-bold text-gray-900">{workshop.email}</p>
                      </div>
                    </div>
                  )}
                </div>

                <button
                  onClick={handleStartConversation}
                  disabled={isSubmitting}
                  className="w-full mt-6 bg-gradient-to-r from-orange-500 to-red-600 text-white font-bold py-4 rounded-xl hover:shadow-lg hover:scale-[1.02] transition-all disabled:opacity-50 disabled:hover:scale-100"
                >
                  💬 Mesaj Gönder
                </button>

                {conversationError && (
                  <div className="mt-3 text-red-600 text-sm text-center font-medium bg-red-50 p-3 rounded-lg border border-red-100">
                    {conversationError}
                  </div>
                )}
                
                {conversationSuccess && (
                  <div className="mt-3 text-green-600 text-sm text-center font-medium bg-green-50 p-3 rounded-lg border border-green-100">
                    {conversationSuccess}
                  </div>
                )}
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

export default WorkshopDetailPage;
