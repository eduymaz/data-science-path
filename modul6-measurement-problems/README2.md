# Ölçüm Problemleri (Measurement Problems)

Bu doküman, veri biliminde karşılaşılan temel ölçüm problemlerini (ürün derecelendirme, ürün sıralama, yorum sıralama ve $A/B$ testi) akademik bir şekilde açıklamaktadır. Her bölümde kavramların tanımları, yöntemler ve detaylı örnekler yer almaktadır.

---

## 1. Ürün Derecelendirme

### Tanım:
Ürün derecelendirme, kullanıcı geri bildirimlerini toplayarak bir ürünün kalitesini veya popülerliğini değerlendirmeyi amaçlar.

### Yöntemler:
1. **Basit Ortalama:**  
   Tüm derecelendirmelerin aritmetik ortalaması.  
   Formül:  
   $\text{Ortalama} = \frac{\sum_{i=1}^{n} R_i}{n}$  
   Burada $R_i$, derecelendirme ve $n$, toplam derecelendirme sayısıdır.

2. **Zamana Dayalı Ağırlıklı Ortalama:**  
   Zamanla değişen trendleri hesaba katmak için son derecelendirmelere daha fazla ağırlık verir.

3. **Kullanıcı Bazlı Ağırlıklı Ortalama:**  
   Kullanıcı güvenilirliğine veya uzmanlığına göre derecelendirmelere ağırlık verir.

4. **Ağırlıklı Derecelendirme (IMDB Formülü):**  
   Ortalama derecelendirmeyi minimum oy sayısı ile birleştirerek güvenilirliği artırır.  
   Formül:  
   $WR = \frac{v}{v+m} \cdot R + \frac{m}{v+m} \cdot C$ 
   Burada:
   - $(v)$: Ürün için oy sayısı.
   - $(m)$: Minimum oy sayısı.
   - $(R)$: Ortalama derecelendirme.
   - $(C)$: Tüm ürünlerin ortalama derecelendirmesi.

---

## 2. Ürün Sıralama

### Tanım:
Ürün sıralama, kullanıcı deneyimini ve karar verme sürecini iyileştirmek için ürünleri belirli kriterlere göre sıralamayı içerir.

### Yöntemler:
1. **Derecelendirmeye Göre Sıralama:**  
   Ürünler, ortalama derecelendirmelerine göre sıralanır.

2. **Yorum Sayısına veya Satın Alma Sayısına Göre Sıralama:**  
   Daha fazla yoruma veya satın alma sayısına sahip ürünler üst sıralarda yer alır.

3. **Bayes Ortalama Derecelendirme Skoru:**  
   Derecelendirme sayısındaki değişkenliği ele almak için ön bilgi kullanarak ortalama derecelendirmeyi ayarlar.  
   Formül:  
   $BAR = \frac{\sum_{i=1}^{n} (R_i \cdot W_i)}{\sum_{i=1}^{n} W_i}$  
   Burada $W_i$, her derecelendirme için ağırlıktır.

4. **IMDB Bayes Formülü:**  
   IMDB tarafından kullanılan Bayes derecelendirme yöntemi.  
   Formül:  
   $WR = \frac{v}{v+m} \cdot R + \frac{m}{v+m} \cdot C$

---

## 3. Yorum Sıralama

### Tanım:
Yorum sıralama, kullanıcı yorumlarını en faydalı veya en alakalı olanları öne çıkarmak için sıralamayı içerir.

### Yöntemler:
1. **Up-Down Fark Skoru:**  
   Beğeni ve beğenmeme arasındaki farkı hesaplar.

2. **Ortalama Derecelendirme:**  
   Bir yorum için tüm derecelendirmelerin ortalamasını kullanır.

3. **Wilson Alt Güven Sınırı (WLB):**  
   Bernoulli parametresi $p$ için bir güven aralığının alt sınırını hesaplayan istatistiksel bir yöntemdir.  
   Formül:  
   $WLB = \hat{p} - z \cdot \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$ 
   Burada:
   - $(\hat{p})$: Pozitif derecelendirme oranı.
   - $(z)$: İstenen güven seviyesi için Z-skoru.
   - $(n)$: Toplam derecelendirme sayısı.

---

## 4. A/B Testi

### Tanım:
A/B testi, iki grubu (ör. kontrol ve tedavi) karşılaştırmak için kullanılan istatistiksel bir yöntemdir.

### Adımlar:
1. **Hipotez Kurulumu:**  
   - Null Hipotez $(H_0)$: Gruplar arasında fark yoktur.
   - Alternatif Hipotez $(H_1)$: Anlamlı bir fark vardır.

2. **Örnekleme:**  
   Her iki grup için temsil edici örnekler toplanır.

3. **Betimsel İstatistik:**  
   Veri, ortalama, medyan ve standart sapma gibi ölçülerle özetlenir.

4. **Varsayım Kontrolleri:**  
   - **Normallik:**  
     Verinin normal dağılıma uyup uymadığını kontrol etmek için *Shapiro-Wilk* testi kullanılır.
   - **Varyans Homojenliği:**  
     Varyansların eşit olup olmadığını kontrol etmek için *Levene* testi kullanılır.

5. **Hipotez Testi:**  
   - **Parametrik Test:**  
     Varsayımlar sağlanıyorsa bağımsız iki örneklem t-testi uygulanır.
   - **Non-Parametrik Test:**  
     Varsayımlar sağlanmıyorsa *Mann-Whitney U* testi uygulanır.

6. **P-Değeri Yorumu:**  
   - $p < 0.05$: $H_0$ reddedilir.
   - $p \geq 0.05$: $H_0$ reddedilemez.

---

## Sonuç

Bu doküman, veri biliminde ölçüm problemleriyle ilgili kapsamlı bir genel bakış sunar. Bu teknikler, veri odaklı kararlar almak ve kullanıcı deneyimini iyileştirmek için gereklidir.
