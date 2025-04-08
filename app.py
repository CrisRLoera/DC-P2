import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Cargar modelo y codificadores
modelo, label_encoders, feature_names = joblib.load("modelo.pkl")

st.title("Predicción de hongos 🍄")
st.write("Selecciona las características del hongo para predecir si es comestible o venenoso.")

# Diccionario de valores posibles por atributo
atributos = {
    "cap-shape": ['b', 'c', 'x', 'f', 'k', 's'],
    "cap-surface": ['f', 'g', 'y', 's'],
    "cap-color": ['n', 'b', 'c', 'g', 'r', 'p', 'u', 'e', 'w', 'y'],
    "bruises": ['t', 'f'],
    "odor": ['a', 'l', 'c', 'y', 'f', 'm', 'n', 'p', 's'],
    "gill-attachment": ['a', 'd', 'f', 'n'],
    "gill-spacing": ['c', 'w', 'd'],
    "gill-size": ['b', 'n'],
    "gill-color": ['k', 'n', 'b', 'h', 'g', 'r', 'o', 'p', 'u', 'e', 'w', 'y'],
    "stalk-shape": ['e', 't'],
    "stalk-root": ['b', 'c', 'u', 'e', 'z', 'r', '?'],
    "stalk-surface-above-ring": ['f', 'y', 'k', 's'],
    "stalk-surface-below-ring": ['f', 'y', 'k', 's'],
    "stalk-color-above-ring": ['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'],
    "stalk-color-below-ring": ['n', 'b', 'c', 'g', 'o', 'p', 'e', 'w', 'y'],
    "veil-type": ['p', 'u'],
    "veil-color": ['n', 'o', 'w', 'y'],
    "ring-number": ['n', 'o', 't'],
    "ring-type": ['c', 'e', 'f', 'l', 'n', 'p', 's', 'z'],
    "spore-print-color": ['k', 'n', 'b', 'h', 'r', 'o', 'u', 'w', 'y'],
    "population": ['a', 'c', 'n', 's', 'v', 'y'],
    "habitat": ['g', 'l', 'm', 'p', 'u', 'w', 'd']
}

# Crear inputs para cada atributo
user_input = []
for feature in feature_names:
    opciones = atributos[feature]
    seleccion = st.selectbox(f"{feature}", opciones)
    codificado = label_encoders[feature].transform([seleccion])[0]
    user_input.append(codificado)

# Predecir si el hongo es venenoso o comestible
if st.button("Predecir"):
    entrada = np.array([user_input])
    pred = modelo.predict(entrada)[0]
    clase = label_encoders['poisonous'].inverse_transform([pred])[0]
    resultado = "VENENOSO" if clase == 'p' else "COMESTIBLE"
    st.success(f"Resultado: El hongo es **{resultado}** 🍄")
