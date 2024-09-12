import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('Amazon/amazon.csv', delimiter=',', encoding='utf-8')

# Cambio el tipo de dato de las columnas
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
df['rating_count'] = pd.to_numeric(df['rating_count'].replace({',': ''}, regex=True), errors='coerce')
df['discount_percentage'] = pd.to_numeric(df['discount_percentage'].replace({'%': ''}, regex=True), errors='coerce')

# Elimino el símbolo de la moneda (Rupia india) y convierto a numérico
df['discounted_price'] = pd.to_numeric(df['discounted_price'].replace({'₹': '', ',': ''}, regex=True), errors='coerce')
df['actual_price'] = pd.to_numeric(df['actual_price'].replace({'₹': '', ',': ''}, regex=True), errors='coerce')

# Convierto las rupias indias a euros (una rupia india corresponde a aproximadamente 0,011 euros)
df['discounted_price'] = (df['discounted_price'] * 0.011).round(2)
df['actual_price'] = (df['actual_price'] * 0.011).round(2)

# Elimino las columnas de reviews de usuarios independientes
df.drop(columns=['user_id', 'user_name', 'review_id', 'review_title', 'review_content'], inplace=True)

# Elimino nulos
df.dropna(inplace=True)

# Elimino filas duplicadas, conservando solo la última ocurrencia de cada `product_id`
df = df.drop_duplicates(subset='product_id', keep='last')

# Cambio el primer separador de la columna `category` de '|' a '#' para después dividirlo en dos columnas
df['category'] = df['category'].str.replace('|', '#', 1)

# Separo la columna `category` en dos columnas `category` y `subcategory`
df[['category', 'subcategory']] = df['category'].str.split('#', expand=True)

# ¿Qué categorías tienen los productos con los precios más altos?
most_expensive_categories = df[['category', 'product_name', 'actual_price']].sort_values(by='actual_price', ascending=False).head(10)
# print(most_expensive_categories)

# ¿Existe correlación entre el rating y el precio de los productos?
rating_price_corr = df[['rating', 'actual_price']].corr()
# print(rating_price_corr)

# ¿Cuáles son los productos con mayor descuento?
most_discount_percentage = df[['discount_percentage', 'product_name']].sort_values(by="discount_percentage", ascending=False).head(10)
# print(most_discount_percentage)

# ¿Cuáles son los productos con mayor cantidad de reviews?
most_reviews = df[['rating_count', 'product_name']].sort_values(by="rating_count", ascending=False).head(10)
# print(most_reviews)

# ¿Cuáles son los productos con mayor rating?
best_rated = df[['rating', 'product_name']].sort_values(by="rating", ascending=False).head(10)
# print(best_rated)

# Gráficos
# Creo una figura con subplots
fig, axs = plt.subplots(2, 2, figsize=(16, 18))

# Histograma de distribución de precios
axs[0, 0].hist(df['actual_price'], bins=20, color='teal', edgecolor='black')
axs[0, 0].set_xlabel('Precio Actual (€)')
axs[0, 0].set_ylabel('Frecuencia')
axs[0, 0].set_title('Distribución de Precios de los Productos')

# Boxplot de precios por categoría
df.boxplot(column='actual_price', by='category', ax=axs[0, 1], grid=False, vert=False)
axs[0, 1].set_xlabel('Precio Actual (€)')
axs[0, 1].set_ylabel('Categoría')
axs[0, 1].set_title('Distribución de Precios por Categoría')
axs[0, 1].set_xticks(axs[0, 1].get_xticks()[::2])  # Simplifico los ticks

# Relación entre descuento y rating
axs[1, 0].scatter(df['discount_percentage'], df['rating'], alpha=0.5, color='purple')
axs[1, 0].set_xlabel('Porcentaje de Descuento (%)')
axs[1, 0].set_ylabel('Rating')
axs[1, 0].set_title('Relación entre Descuento y Rating')
axs[1, 0].grid(True)

# Cantidad de reviews vs rating
axs[1, 1].scatter(df['rating_count'], df['rating'], alpha=0.5, color='blue')
axs[1, 1].set_xlabel('Cantidad de Reviews')
axs[1, 1].set_ylabel('Rating')
axs[1, 1].set_title('Cantidad de Reviews vs Rating')
axs[1, 1].grid(True)

# Añado titulo a la figura
fig.suptitle('Análisis de Datos de Productos de Amazon', fontsize=16)

# Ajusto el espacio entre subplots
plt.subplots_adjust(top=0.9, hspace=0.26, wspace=0.45)
plt.show()
