import React from 'react';
import { Link } from 'react-router-dom';

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-gray-300 mt-20">
      <div className="max-w-7xl mx-auto px-4 py-16">
        {/* Main Footer Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          {/* Brand Section */}
          <div className="space-y-4">
            <Link to="/" className="text-2xl font-bold text-orange-500 hover:text-orange-400 transition">
              UstaBul
            </Link>
            <p className="text-sm text-gray-400">
              Adıyaman'da güvenilir usta ve dükkanları bulmak artık çok kolay. Binlerce müşteri tarafından puanlanmış ve incelenen işletmeleri keşfet.
            </p>
            <div className="flex gap-4 pt-2">
              <a href="#" className="w-10 h-10 bg-gray-800 hover:bg-orange-500 rounded-full flex items-center justify-center transition">
                <span className="text-sm">f</span>
              </a>
              <a href="#" className="w-10 h-10 bg-gray-800 hover:bg-orange-500 rounded-full flex items-center justify-center transition">
                <span className="text-sm">𝕏</span>
              </a>
              <a href="#" className="w-10 h-10 bg-gray-800 hover:bg-orange-500 rounded-full flex items-center justify-center transition">
                <span className="text-sm">📷</span>
              </a>
              <a href="#" className="w-10 h-10 bg-gray-800 hover:bg-orange-500 rounded-full flex items-center justify-center transition">
                <span className="text-sm">in</span>
              </a>
            </div>
          </div>

          {/* Kullanıcılar */}
          <div>
            <h3 className="text-white font-semibold mb-6 text-lg">Kullanıcılar</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/workshops" className="hover:text-orange-500 transition text-sm">
                  Dükkanları Keşfet
                </Link>
              </li>
              <li>
                <Link to="/login" className="hover:text-orange-500 transition text-sm">
                  Giriş Yap
                </Link>
              </li>
              <li>
                <Link to="/register" className="hover:text-orange-500 transition text-sm">
                  Kaydol
                </Link>
              </li>
              <li>
                <Link to="/profile" className="hover:text-orange-500 transition text-sm">
                  Profilim
                </Link>
              </li>
              <li>
                <Link to="/parts" className="hover:text-orange-500 transition text-sm">
                  Parçalar
                </Link>
              </li>
            </ul>
          </div>

          {/* İşletmeler */}
          <div>
            <h3 className="text-white font-semibold mb-6 text-lg">İşletmeler</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/register" className="hover:text-orange-500 transition text-sm">
                  İşletme Kaydı
                </Link>
              </li>
              <li>
                <Link to="/profile" className="hover:text-orange-500 transition text-sm">
                  Profilim
                </Link>
              </li>
              <li>
                <a href="/" className="hover:text-orange-500 transition text-sm">
                  Premium Üyelik
                </a>
              </li>
              <li>
                <Link to="/workshops" className="hover:text-orange-500 transition text-sm">
                  Dükkanlarım
                </Link>
              </li>
              <li>
                <a href="/" className="hover:text-orange-500 transition text-sm">
                  Destek
                </a>
              </li>
            </ul>
          </div>

          {/* Hakkında */}
          <div>
            <h3 className="text-white font-semibold mb-6 text-lg">Hakkında</h3>
            <ul className="space-y-3">
              <li>
                <Link to="/" className="hover:text-orange-500 transition text-sm">
                  Hakkımızda
                </Link>
              </li>
              <li>
                <a href="mailto:info@ustabul.com" className="hover:text-orange-500 transition text-sm">
                  İletişim
                </a>
              </li>
              <li>
                <Link to="/" className="hover:text-orange-500 transition text-sm">
                  Gizlilik Politikası
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-orange-500 transition text-sm">
                  Kullanım Şartları
                </Link>
              </li>
              <li>
                <Link to="/" className="hover:text-orange-500 transition text-sm">
                  Blog
                </Link>
              </li>
            </ul>
          </div>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-800 pt-8 mt-8">
          {/* Bottom Footer */}
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className="text-sm text-gray-500">
              © {currentYear} UstaBul. Tüm hakları saklıdır.
            </p>
            <div className="flex gap-6">
              <Link to="/" className="text-sm text-gray-400 hover:text-orange-500 transition">
                Gizlilik
              </Link>
              <Link to="/" className="text-sm text-gray-400 hover:text-orange-500 transition">
                Şartlar
              </Link>
              <Link to="/" className="text-sm text-gray-400 hover:text-orange-500 transition">
                Çerezler
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
