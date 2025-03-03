# Modern Coffee Machine (Kahve Makinesi)

Modern Coffee Machine, şık ve kullanıcı dostu bir arayüze sahip, Python ve CustomTkinter kullanılarak geliştirilmiş bir kahve makinesi simülasyonudur. Bu uygulama, gerçek bir kahve makinesinin tüm temel özelliklerini taklit eder ve kullanıcılara sanal bir kahve deneyimi sunar.

![Modern Coffee Machine](https://github.com/yourusername/modern-coffee-machine/raw/main/screenshots/main_screen.png)

## 🌟 Özellikler

### 🍵 Geniş İçecek Menüsü
- Espresso, Americano, Cappuccino, Latte ve Mocha dahil popüler kahve çeşitleri
- Her kahve için detaylı açıklamalar ve içerik bilgileri

### 🥤 Kahve Kişiselleştirme
- Farklı boyut seçenekleri (Küçük, Orta, Büyük)
- Çeşitli ekstralar (Extra Shot, Karamel Şurubu, Vanilya Şurubu, Çikolata Sosu, Krema)
- Sıcaklık ayarı

### 💼 Sipariş Yönetimi
- Müşteri adı ve masa numarası ile sipariş oluşturma
- Özel notlar ekleme
- Son siparişleri görüntüleme

### 📊 Kaynak Takibi
- Su, kahve çekirdeği, süt ve diğer malzemelerin seviyelerini görsel olarak takip etme
- Kaynakları tek tıkla yenileme

### 🌈 Ek Özellikler
- Günlük özel indirimler
- Dijital saat
- Kahve ipuçları ve bilgiler
- Gerçekçi kahve hazırlama animasyonları
- Şık ve modern kullanıcı arayüzü

## 📋 Gereksinimler

- Python 3.7+
- CustomTkinter
- Pillow (PIL)

## 🚀 Kurulum

1. Repoyu klonlayın:
   ```bash
   git clone https://github.com/yourusername/modern-coffee-machine.git
   cd modern-coffee-machine
   ```

2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Uygulamayı çalıştırın:
   ```bash
   python kahve.py
   ```

## 🎮 Kullanım

1. **Para Ekleme**: Bakiyenize para eklemek için "PARA EKLE" bölümündeki butonları kullanın.
2. **Kahve Seçimi**: İstediğiniz kahve türünü seçin.
3. **Boyut Seçimi**: Küçük, Orta veya Büyük boyutu seçin.
4. **Ekstralar**: İsteğe bağlı olarak ekstra malzemeler ekleyin.
5. **Sıcaklık Ayarı**: Slider ile kahvenizin sıcaklığını ayarlayın.
6. **Sipariş Bilgileri**: Müşteri adı, masa numarası ve özel notları girin.
7. **Kahve Hazırlama**: "BREW COFFEE" veya "KAHVE HAZIRLA" butonuna tıklayın.

## 🛠️ Teknik Detaylar

### Ana Modüller
- `ModernCoffeeMachine`: Ana uygulama sınıfı
- GUI Bileşenleri: CustomTkinter kullanılarak oluşturulmuş modern arayüz
- Çoklu iş parçacığı (threading): Kahve hazırlama işlemi ana uygulamayı bloke etmeden çalışır

### Özelleştirme
- `coffee_menu`: Yeni kahve türleri ekleyerek menüyü genişletebilirsiniz
- `daily_specials`: Günlük indirimleri değiştirebilirsiniz
- `coffee_tips`: Kahve ipuçlarını değiştirebilir veya yenilerini ekleyebilirsiniz

## 📝 Kod Yapısı

- `kahve.py`: Ana uygulama dosyası, `ModernCoffeeMachine` sınıfını içerir
- `main.py`: Alternatif ve daha basit bir versiyon
- `requirements.txt`: Gerekli kütüphanelerin listesi

## 🌍 Dil Desteği

Uygulama hem Türkçe hem de İngilizce arayüz desteği sunar:
- `kahve.py`: Genişletilmiş İngilizce versiyon
- `main.py`: Temel Türkçe versiyon

## 🤝 Katkıda Bulunma

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📬 İletişim

Sorularınız veya önerileriniz için lütfen bir issue açın veya pull request gönderin.

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

Geliştirici tarafından ❤️ ile yapılmıştır.
