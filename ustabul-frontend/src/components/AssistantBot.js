import React, { useState, useRef, useEffect } from 'react';

function AssistantBot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { type: 'bot', text: 'Merhaba! 👋 UstaBul\'a hoşgeldiniz. Size nasıl yardımcı olabilirim?' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  const HUGGINGFACE_TOKEN = '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';

  // Yapay zeka cevap sistemi - Türkçe bilgiler
  const getAssistantResponse = (userMessage) => {
    const lowerMessage = userMessage.toLowerCase();
    
    const responses = {
      // Hoşlanma ve selamlaşma
      'merhaba|selam|hi|hey': 'Merhaba! 👋 Size nasıl yardımcı olabilirim?',
      'nasılsın|nasilsin': 'Teşekkür ederim, ben iyiyim! Siz nasılsınız? UstaBul\'u nasıl buluyorsunuz?',
      
      // Usta/Dükkan arama
      'usta.*bul|dükkan.*ara|workshop': 'UstaBul\'da ustalar bulmak çok kolay! 🔍\n\n1. "Dükkanlar" sayfasına gidin\n2. Kategori seçin (Elektrikçi, Tesisatçı, vb.)\n3. Bölge veya ada göre filtreleyin\n4. Puan ve yorumları inceleyin\n5. İletişim bilgisine tıklayın\n\nNe tür bir usta arıyorsunuz?',
      
      // Kategori sorgusu
      'kategor': 'UstaBul\'da şu kategoriler var:\n⚡ Elektrik\n🔧 Tesisatçılık\n🪟 Cam ve Çatı\n🏗️ Yapı Ustası\n🚗 Oto Elektrikçi\n🪟 Camcı\n📱 Elektronik Tamircisi\n\nHangi kategoriye ilgi duyuyorsunuz?',
      
      // Yorum ve puan
      'yorum|puan|rating': 'Yorumlar çok önemlidir! 🌟\n\nHer usta için diğer müşterilerin yorumlarını görebilirsiniz:\n- Hizmet kalitesi\n- Fiyat\n- Zamanında tamamlama\n- Profesyonellik\n\nYorum okuyarak en iyi ustayı seçebilirsiniz!',
      
      // Profil\n      'profil|hesap|kayıt': 'Profilinizi yönetmek için:\n1. Sağ üstteki adınıza tıklayın\n2. "Profil" sayfasına gidin\n3. Bilgilerinizi güncelleyin\n4. Fotoğraf ve açıklamalar ekleyin',
      
      // Giriş ve çıkış
      'giriş|login|çıkış|logout': 'Giriş/Çıkış:\n📱 Sağ üstteki menüden "Giriş Yap" veya "Kaydol" seçeneğine tıklayın\n🚪 Çıkmak için "Çıkış" butonuna tıklayın',
      
      // Güvenlik
      'şifre|güvenlik|hesap.*sifre': 'Hesap güvenliğiniz bizim önceliğimiz! 🔒\n\nŞifreniz:\n- Güvenli sunucularda şifrelenir\n- En az 8 karakter olmalıdır\n- Özel karakterler içermesi önerilir\n- Kimseyle paylaşmayın!',
      
      // İletişim
      'iletişim|destek|yardım|problem': 'Bize ulaşmak için:\n📧 Email: info@ustabul.com\n📱 Telefon: +90 xxx xxx xx xx\n💬 Canlı destek 24/7 açıktır\n\nSorunuz nedir?',
      
      // Ücretler
      'ücret|fiyat|para|ödeme': 'Fiyatlandırma hakkında:\n💰 Her usta kendi tarifesini belirler\n📊 Karşılaştırma yapabilirsiniz\n🎯 Teklifleri isteyin\n✅ Tarifeler profilde açıkça görünür',
      
      // Randevu\n      'randevu|appointment|zaman': 'Randevu almak için:\n1. Usta profiline gidin\n2. "Randevu Al" butonuna tıklayın\n3. Uygun saati seçin\n4. Bilgilerinizi onaylayın\n\nUsta konfirmasyon için sizinle iletişim kuracak!',
      
      // Genel bilgiler
      'ustabul|hakkında|about': 'UstaBul hakkında:\n🏢 Adıyaman\'da en güvenilir usta platformu\n👥 Binlerce profesyonel usta\n⭐ Müşteri puanları ve yorumları\n✅ Doğrulanmış kullanıcılar\n🔐 Güvenli ödeme sistemi',
      
      // Teşekkür
      'teşekkür|thank|sağol': 'Sizinle yardımcı olabilmekten mutluyum! 😊 Başka bir sorunuz var mı?',
      
      // Varsayılan cevap
      'default': 'Anladığım kadarıyla, bu konuda yardımcı olacak bilgim maalesef yok. 🤔\n\nÖneririm:\n1. Dükkanları inceleyin\n2. Puan ve yorumları okuyun\n3. Destek ekibine ulaşın\n\nBaşka ne sorabilirim?'
    };

    // Cevap bulma
    for (const [key, value] of Object.entries(responses)) {
      if (key !== 'default') {
        const patterns = key.split('|');
        if (patterns.some(pattern => lowerMessage.includes(pattern.trim()))) {
          return value;
        }
      }
    }
    
    return responses.default;
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = inputValue;
    setInputValue('');
    setMessages(prev => [...prev, { type: 'user', text: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch(
        'http://localhost:8000/api/reviews/ai/chat/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: userMessage })
        }
      );

      const data = await response.json();
      console.log('API Response:', data);
      
      if (data.error) {
        console.error('API Error:', data.error);
        setMessages(prev => [...prev, { 
          type: 'bot', 
          text: `Hata: ${data.error}` 
        }]);
      } else if (data.reply) {
        setMessages(prev => [...prev, { type: 'bot', text: data.reply }]);
      } else {
        console.error('Beklenmedik API yanıt formatı:', data);
        setMessages(prev => [...prev, { 
          type: 'bot', 
          text: 'Özür dilerim, yanıt işlenemiyor. Lütfen daha sonra tekrar deneyin.' 
        }]);
      }
    } catch (error) {
      console.error('Asistan hatası:', error);
      setMessages(prev => [...prev, { 
        type: 'bot', 
        text: `Bağlantı hatası: ${error.message}. Lütfen backend'in çalışıyor olduğundan emin olun.` 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      {/* Chat Window */}
      {isOpen && (
        <div className="mb-4 w-96 h-96 bg-white rounded-lg shadow-2xl flex flex-col border border-orange-200">
          {/* Header */}
          <div className="bg-gradient-to-r from-orange-500 to-orange-600 text-white p-4 rounded-t-lg flex justify-between items-center">
            <div>
              <h3 className="font-bold text-lg">UstaBul Asistanı</h3>
              <p className="text-xs text-orange-100">Size yardımcı olmaktan mutluyum</p>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:bg-orange-700 rounded-full p-1 transition"
            >
              ✕
            </button>
          </div>

          {/* Messages */}
          <div 
            ref={chatContainerRef}
            className="flex-1 overflow-y-auto p-4 space-y-3 bg-gray-50"
          >
            {messages.map((msg, idx) => (
              <div 
                key={idx}
                className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs px-4 py-2 rounded-lg text-sm ${
                    msg.type === 'user'
                      ? 'bg-orange-500 text-white rounded-br-none'
                      : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'
                  }`}
                >
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white text-gray-800 border border-gray-200 px-4 py-2 rounded-lg rounded-bl-none">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-200 bg-white rounded-b-lg">
            <div className="flex gap-2">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Mesajınız..."
                className="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 resize-none"
                rows="1"
              />
              <button
                onClick={sendMessage}
                disabled={isLoading || !inputValue.trim()}
                className="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-300 text-white px-4 py-2 rounded-lg transition font-medium"
              >
                Gönder
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-14 h-14 bg-gradient-to-r from-orange-500 to-orange-600 text-white rounded-full shadow-lg hover:shadow-xl transition transform hover:scale-110 flex items-center justify-center text-2xl border-2 border-white"
        title="Asistan"
      >
        {isOpen ? '✕' : '💬'}
      </button>
    </div>
  );
}

export default AssistantBot;
