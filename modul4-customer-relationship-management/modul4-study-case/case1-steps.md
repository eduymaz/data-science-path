# Görevler: RFM Analizi

## GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
1. `flo_data_20K.csv` verisini okuyun ve bir kopyasını oluşturun.
2. Veri setinde aşağıdaki incelemeleri yapın:
   - İlk 10 gözlem,
   - Değişken isimleri,
   - Boyut,
   - Betimsel istatistik,
   - Boş değer analizi,
   - Değişken tipleri.
3. Omnichannel müşterilerin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturun:
   - `order_num_total`
   - `customer_value_total`
4. Tarih ifade eden değişkenlerin tipini `datetime` formatına çevirin.
5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısının ve toplam harcamaların dağılımını inceleyin.
6. En fazla kazancı getiren ilk 10 müşteriyi sıralayın.
7. En fazla siparişi veren ilk 10 müşteriyi sıralayın.
8. Veri ön hazırlık sürecini bir fonksiyon haline getirin.

## GÖREV 2: RFM Metriklerinin Hesaplanması
1. Analiz tarihini belirleyin (son alışveriş tarihinden 2 gün sonrası).
2. Aşağıdaki metrikleri içeren bir `rfm` DataFrame oluşturun:
   - `customer_id`
   - `recency` (Son alışverişten bu yana geçen gün sayısı)
   - `frequency` (Toplam alışveriş sayısı)
   - `monetary` (Toplam harcama)

## GÖREV 3: RF ve RFM Skorlarının Hesaplanması
1. `recency`, `frequency` ve `monetary` metriklerini `qcut` ile 1-5 arasında skorlara çevirin:
   - `recency_score`
   - `frequency_score`
   - `monetary_score`
2. `recency_score` ve `frequency_score` değerlerini birleştirerek `RF_SCORE` değişkenini oluşturun.
3. `recency_score`, `frequency_score` ve `monetary_score` değerlerini birleştirerek `RFM_SCORE` değişkenini oluşturun.

## GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
1. RF skorlarını daha açıklayıcı hale getirmek için segment tanımlamaları yapın.
2. `seg_map` yardımıyla `RF_SCORE` değerlerini segmentlere çevirin:
   - Örneğin: `champions`, `loyal_customers`, `hibernating`, vb.

## GÖREV 5: Aksiyon Zamanı!
1. Segmentlerin `recency`, `frequency` ve `monetary` ortalamalarını inceleyin.
2. RFM analizi yardımıyla iki farklı senaryo için müşteri profillerini belirleyin ve CSV dosyalarına kaydedin:
   - **Senaryo 1:** Yeni bir kadın ayakkabı markası için hedef müşteri profili:
     - Segmentler: `champions`, `loyal_customers`
     - Kadın kategorisinden alışveriş yapanlar.
     - Çıktı dosyası: `yeni_marka_hedef_müşteri_id.csv`
   - **Senaryo 2:** Erkek ve çocuk ürünlerinde indirim için hedef müşteri profili:
     - Segmentler: `cant_loose`, `hibernating`, `new_customers`
     - Erkek veya çocuk kategorisinden alışveriş yapanlar.
     - Çıktı dosyası: `indirim_hedef_müşteri_ids.csv`

## GÖREV 6: Tüm Süreci Fonksiyonlaştırma
1. Tüm veri hazırlama, RFM hesaplama ve segmentasyon işlemlerini bir fonksiyon haline getirin:
   - Fonksiyon adı: `create_rfm`
   - Çıktı: RFM DataFrame (`customer_id`, `recency`, `frequency`, `monetary`, `RF_SCORE`, `RFM_SCORE`, `segment`)