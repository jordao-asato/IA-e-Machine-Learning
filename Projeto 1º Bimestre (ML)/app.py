import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Carregar os dados
df = pd.read_csv("pizza2.csv")

# Criação do modelo
modelo = LinearRegression()

# Treinar o modelo com diâmetro e custo total dos ingredientes
X = df[["diametro", "custo_ingredientes"]]  # Variáveis independentes
y = df["preco"]  # Variável dependente: preço

# Treinando o modelo
modelo.fit(X, y)

# Configuração da página
st.set_page_config(page_title="Pizzaria Gourmet 🍕", page_icon="🍕", layout="centered")

st.title("🍕 Pizzaria do Calabreso 🍕")
st.divider()

st.subheader("Monte sua pizza ideal 🍽️")

# Dicionário de ingredientes e seus custos
custo_ingredientes = {
    "queijo": 5,
    "molho": 2,
    "calabresa": 8,
    "frango": 7,
    "catupiry": 6,
    "presunto": 6,
    "ovo": 2,
    "cebola": 1,
    "pepperoni": 9,
    "tomate": 3,
    "manjericão": 2,
    "chocolate": 5,
    "morango": 8
}

# Sabores e seus ingredientes
sabores_ingredientes = {
    "🧀Mussarela🧀": ["queijo", "molho"],
    "🐷Calabresa🐷": ["queijo", "molho", "calabresa"],
    "🍗Frango com catupiry🍗": ["queijo", "molho", "frango", "catupiry"],
    "😡Portuguesa😡": ["queijo", "molho", "presunto", "ovo", "cebola"],
    "🤌Pepperoni🤌": ["queijo", "molho", "pepperoni"],
    "🍅Marguerita🍅": ["queijo", "molho", "tomate", "manjericão"],
    "🍫Chocolate com Morango🍫": ["chocolate", "morango"]
}

# Escolha do sabor
sabor_escolhido = st.selectbox("Selecione o sabor da pizza", list(sabores_ingredientes.keys()))

# Calcular o custo total dos ingredientes
ingredientes_sabor = sabores_ingredientes[sabor_escolhido]

# Para cada ingrediente da lista, armazena o custo de cada ingrediente e soma os valores
custo_total_ingredientes = sum(custo_ingredientes[ing] for ing in ingredientes_sabor)

# Entrada do diâmetro
diametro = st.number_input("Digite o tamanho do diâmetro da pizza (em cm):", min_value=0.0, step=0.5)

# Previsão de preço
if diametro > 0:
    preco_previsto = modelo.predict([[diametro, custo_total_ingredientes]])[0]
    st.markdown(f"### 🛒 Preço estimado da pizza sabor *{sabor_escolhido}*:")
    st.markdown(f"*R$ {preco_previsto:.2f}* para uma pizza de {diametro:.2f} cm com ingredientes: {', '.join(ingredientes_sabor)}.")
    st.success("Aproveite sua pizza! 🍕")
    st.balloons()
else:
    st.info("Por favor, insira um diâmetro maior que 0.")

st.divider()
st.markdown("### 📞 Entre em contato:")
st.write("📍 Rua das Pizzas, 123 - Cidade Gourmet")
st.write("📞 **Telefone:** (11) 98765-4321")
st.write("🕒 **Horário:** Todos os dias, das 18h às 23h")
