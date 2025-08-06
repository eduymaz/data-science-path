# Tavsiye Sistemleri Eğitimi (Recommendation System Tutorial)

Bu doküman, dört ana tavsiye sistemi yaklaşımını (Birliktelik Kuralı Öğrenimi, İçerik Tabanlı Tavsiye, Item-Based Collaborative Filtering, Model Tabanlı Matris Faktörizasyonu) detaylarıyla açıklar. Her bölümde yöntemin mantığı, kullanım alanı ve örnek Python kodları yer almaktadır. Son bölümde ise bu dört yöntemi bir projede adım adım nasıl uygulayacağınız anlatılmıştır.

---

## 1. Birliktelik Kuralı Öğrenimi (Association Rule Learning - ARL) 🛒

**Açıklama:**  
Birliktelik kuralı öğrenimi, büyük veri tabanlarında değişkenler arasındaki ilginç ilişkileri keşfetmek için kullanılan kural tabanlı bir makine öğrenimi yöntemidir. Market sepeti analizinde sıkça kullanılır.

**Temel Kavramlar:**
- **Destek (Support):** Bir ürün grubunun veri setinde görülme sıklığı.
- **Güven (Confidence):** A ürünü alındığında B ürününün de alınma olasılığı.
- **Lift:** A ve B ürünlerinin birlikte alınmasının beklenen sıklığa oranı.

**Adımlar ve Kod:**

### Adım 1: Veri Ön İşleme

Veri setini temizleyin, eksik değerleri ve iptal edilen işlemleri çıkarın, aykırı değerleri düzeltin.

```python
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

df = pd.read_excel("../datasets/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df.dropna(inplace=True)
df = df[~df["Invoice"].str.contains("C", na=False)]
df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]
```

### Adım 2: Fatura-Ürün Matrisi Oluşturma

Her satır bir fatura, her sütun bir ürün olacak şekilde ikili matris oluşturun.

```python
invoice_product_df = df.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0)
invoice_product_df = invoice_product_df.applymap(lambda x: 1 if x > 0 else 0)
```

### Adım 3: Sık Ürün Setlerini Bulma

Apriori algoritması ile sık ürün setlerini bulun.

```python
frequent_itemsets = apriori(invoice_product_df, min_support=0.01, use_colnames=True)
```

### Adım 4: Birliktelik Kurallarının Çıkarılması

Destek, güven ve lift değerlerine göre kuralları oluşturun.

```python
rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
rules = rules[(rules["support"] > 0.05) & (rules["confidence"] > 0.1) & (rules["lift"] > 5)]
```

### Adım 5: Ürün Önerisi

Bir ürün için önerilecek diğer ürünleri bulun.

```python
def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])
    return recommendation_list[0:rec_count]
```

---

## 2. İçerik Tabanlı Tavsiye (Content-Based Recommendation) 📚

**Açıklama:**  
İçerik tabanlı tavsiye sistemleri, kullanıcının daha önce beğendiği ürünlerin içerik özelliklerine (ör. film türü, özet, oyuncu) göre benzer ürünler önerir.

**Temel Kavramlar:**
- **TF-IDF:** Metin verisini sayısal vektörlere dönüştürür.
- **Cosine Similarity:** İki vektör arasındaki benzerliği ölçer.

**Adımlar ve Kod:**

### Adım 1: TF-IDF Matrisi Oluşturma

Film özetlerinden TF-IDF matrisi oluşturun.

```python
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("datasets/the_movies_dataset/movies_metadata.csv", low_memory=False)
df['overview'] = df['overview'].fillna('')
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df['overview'])
```

### Adım 2: Cosine Similarity Matrisi Oluşturma

Filmler arası benzerlik matrisini hesaplayın.

```python
from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
```

### Adım 3: Benzer Filmleri Önerme

Bir film için en benzer filmleri önerin.

```python
def content_based_recommender(title, cosine_sim, dataframe):
    indices = pd.Series(dataframe.index, index=dataframe['title'])
    indices = indices[~indices.index.duplicated(keep='last')]
    movie_index = indices[title]
    similarity_scores = pd.DataFrame(cosine_sim[movie_index], columns=["score"])
    movie_indices = similarity_scores.sort_values("score", ascending=False)[1:11].index
    return dataframe['title'].iloc[movie_indices]
```

---

## 3. Item-Based Collaborative Filtering 🧩

**Açıklama:**  
Item-based collaborative filtering, ürünler arasındaki benzerliği kullanıcı puanlarına göre hesaplar ve bir ürüne benzer diğer ürünleri önerir.

**Temel Kavramlar:**
- **Kullanıcı-Ürün Matrisi:** Satırlar kullanıcılar, sütunlar ürünler, değerler puanlardır.
- **Ürün Benzerliği:** İki ürün arasındaki korelasyon veya kosinüs benzerliği.

**Adımlar ve Kod:**

### Adım 1: Kullanıcı-Ürün Matrisi Oluşturma

```python
import pandas as pd
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
df = movie.merge(rating, how="left", on="movieId")
comment_counts = pd.DataFrame(df["title"].value_counts())
rare_movies = comment_counts[comment_counts["title"] <= 1000].index
common_movies = df[~df["title"].isin(rare_movies)]
user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")
```

### Adım 2: Ürünler Arası Benzerlik Hesaplama ve Öneri

Bir film için en benzer filmleri önerin.

```python
def item_based_recommender(movie_name, user_movie_df):
    movie_name = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)
```

---

## 4. Model Tabanlı Matris Faktörizasyonu (Matrix Factorization) 🧮

**Açıklama:**  
Matris faktörizasyonu, kullanıcı-ürün matrisini gizli faktörlere ayırarak kullanıcı ve ürünlerin gizli özelliklerini öğrenir. En popüler yöntemlerden biri SVD'dir.

**Temel Kavramlar:**
- **SVD:** Kullanıcı ve ürün matrislerini çarpanlara ayırır.
- **Gizli Faktörler:** Kullanıcı ve ürünlerin soyut özellikleri.

**Adımlar ve Kod:**

### Adım 1: Veri Hazırlama

```python
import pandas as pd
from surprise import Reader, SVD, Dataset

movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
df = movie.merge(rating, how="left", on="movieId")
sample_df = df[df.movieId.isin([130219, 356, 4422, 541])]
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(sample_df[['userId', 'movieId', 'rating']], reader)
```

### Adım 2: Model Eğitimi

```python
from surprise.model_selection import train_test_split
trainset, testset = train_test_split(data, test_size=.25)
svd_model = SVD()
svd_model.fit(trainset)
```

### Adım 3: Model Tuning

```python
from surprise.model_selection import GridSearchCV
param_grid = {'n_epochs': [5, 10, 20], 'lr_all': [0.002, 0.005, 0.007]}
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3, n_jobs=-1)
gs.fit(data)
```

### Adım 4: Tahmin ve Öneri

```python
svd_model = SVD(**gs.best_params['rmse'])
full_trainset = data.build_full_trainset()
svd_model.fit(full_trainset)
svd_model.predict(uid=1.0, iid=541, verbose=True)
```

---

## Proje Akışı: Dört Yöntemi Adım Adım Uygulama

Aşağıda, dört yöntemi bir projede uygulamak için adım adım rehber bulabilirsiniz.

### Adım 1: Veri Hazırlama

Veri setini toplayın, temizleyin ve analiz için uygun hale getirin.

```python
import pandas as pd
# Örnek: MovieLens veri seti için
movie = pd.read_csv('datasets/movie_lens_dataset/movie.csv')
rating = pd.read_csv('datasets/movie_lens_dataset/rating.csv')
df = movie.merge(rating, how="left", on="movieId")
df.dropna(inplace=True)
```

### Adım 2: Birliktelik Kuralı Öğrenimi

```python
from mlxtend.frequent_patterns import apriori, association_rules

invoice_product_df = df.groupby(['userId', 'title'])['rating'].count().unstack().fillna(0)
invoice_product_df = invoice_product_df.applymap(lambda x: 1 if x > 0 else 0)
frequent_itemsets = apriori(invoice_product_df, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)
rules = rules[(rules["support"] > 0.05) & (rules["confidence"] > 0.1) & (rules["lift"] > 5)]
```

### Adım 3: İçerik Tabanlı Tavsiye

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df_movies = pd.read_csv("datasets/the_movies_dataset/movies_metadata.csv", low_memory=False)
df_movies['overview'] = df_movies['overview'].fillna('')
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df_movies['overview'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def content_based_recommender(title, cosine_sim, dataframe):
    indices = pd.Series(dataframe.index, index=dataframe['title'])
    indices = indices[~indices.index.duplicated(keep='last')]
    movie_index = indices[title]
    similarity_scores = pd.DataFrame(cosine_sim[movie_index], columns=["score"])
    movie_indices = similarity_scores.sort_values("score", ascending=False)[1:11].index
    return dataframe['title'].iloc[movie_indices]
```

### Adım 4: Item-Based Collaborative Filtering

```python
comment_counts = pd.DataFrame(df["title"].value_counts())
rare_movies = comment_counts[comment_counts["title"] <= 1000].index
common_movies = df[~df["title"].isin(rare_movies)]
user_movie_df = common_movies.pivot_table(index=["userId"], columns=["title"], values="rating")

def item_based_recommender(movie_name, user_movie_df):
    movie_name = user_movie_df[movie_name]
    return user_movie_df.corrwith(movie_name).sort_values(ascending=False).head(10)
```

### Adım 5: Model Tabanlı Matris Faktörizasyonu

```python
from surprise import Reader, SVD, Dataset
from surprise.model_selection import train_test_split, GridSearchCV

reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)
trainset, testset = train_test_split(data, test_size=.25)
svd_model = SVD()
svd_model.fit(trainset)
param_grid = {'n_epochs': [5, 10, 20], 'lr_all': [0.002, 0.005, 0.007]}
gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3, n_jobs=-1)
gs.fit(data)
svd_model = SVD(**gs.best_params['rmse'])
full_trainset = data.build_full_trainset()
svd_model.fit(full_trainset)
svd_model.predict(uid=1.0, iid=541, verbose=True)
```

### Adım 6: Değerlendirme ve Karşılaştırma

Her yöntemi uygun metriklerle değerlendirin ve karşılaştırın.

```python
from surprise import accuracy
predictions = svd_model.test(testset)
print("RMSE:", accuracy.rmse(predictions))
# Diğer yöntemler için precision, recall gibi metrikler de kullanılabilir.
```

---

## Sonuç

Bu doküman ile tavsiye sistemlerinin temel yöntemlerini ve her birinin Python ile nasıl uygulanacağını öğrendiniz. Her yöntemin avantajları ve kullanım alanları farklıdır. Gerçek projelerde genellikle birden fazla yöntemi birleştirmek en iyi sonuçları verir.

