import streamlit as st
import pickle
import numpy as np

# Cargar modelo y encoders
with open("modelo.pkl", "rb") as f:
    model, label_encoders, feature_names = pickle.load(f)

st.title("Predicción de hongos 🍄")
st.write("Selecciona las características del hongo para predecir si es comestible o venenoso.")

# Diccionario de opciones amigables por campo
opciones_visuales = {
    "cap-shape": {
        "bell": "b", "conical": "c", "convex": "x", "flat": "f", "knobbed": "k", "sunken": "s"
    },
    "cap-surface": {
        "fibrous": "f", "grooves": "g", "scaly": "y", "smooth": "s"
    },
    "cap-color": {
        "brown": "n", "buff": "b", "cinnamon": "c", "gray": "g", "green": "r", "pink": "p",
        "purple": "u", "red": "e", "white": "w", "yellow": "y"
    },
    "bruises?": {
        "bruises": "t", "no": "f"
    },
    "odor": {
        "almond": "a", "anise": "l", "creosote": "c", "fishy": "y", "foul": "f",
        "musty": "m", "none": "n", "pungent": "p", "spicy": "s"
    },
    "gill-attachment": {
        "attached": "a", "descending": "d", "free": "f", "notched": "n"
    },
    "gill-spacing": {
        "close": "c", "crowded": "w", "distant": "d"
    },
    "gill-size": {
        "broad": "b", "narrow": "n"
    },
    "gill-color": {
        "black": "k", "brown": "n", "buff": "b", "chocolate": "h", "gray": "g", "green": "r",
        "orange": "o", "pink": "p", "purple": "u", "red": "e", "white": "w", "yellow": "y"
    },
    "stalk-shape": {
        "enlarging": "e", "tapering": "t"
    },
    "stalk-root": {
        "bulbous": "b", "club": "c", "cup": "u", "equal": "e", "rhizomorphs": "z",
        "rooted": "r", "missing": "?"
    },
    "stalk-surface-above-ring": {
        "fibrous": "f", "scaly": "y", "silky": "k", "smooth": "s"
    },
    "stalk-surface-below-ring": {
        "fibrous": "f", "scaly": "y", "silky": "k", "smooth": "s"
    },
    "stalk-color-above-ring": {
        "brown": "n", "buff": "b", "cinnamon": "c", "gray": "g", "orange": "o",
        "pink": "p", "red": "e", "white": "w", "yellow": "y"
    },
    "stalk-color-below-ring": {
        "brown": "n", "buff": "b", "cinnamon": "c", "gray": "g", "orange": "o",
        "pink": "p", "red": "e", "white": "w", "yellow": "y"
    },
    "veil-type": {
        "partial": "p", "universal": "u"
    },
    "veil-color": {
        "brown": "n", "orange": "o", "white": "w", "yellow": "y"
    },
    "ring-number": {
        "none": "n", "one": "o", "two": "t"
    },
    "ring-type": {
        "evanescent": "e", "flaring": "f", "large": "l", "none": "n",
        "pendant": "p", "sheathing": "s", "zone": "z"
    },
    "spore-print-color": {
        "black": "k", "brown": "n", "buff": "b", "chocolate": "h", "green": "r",
        "orange": "o", "purple": "u", "white": "w", "yellow": "y"
    },
    "population": {
        "abundant": "a", "clustered": "c", "numerous": "n", "scattered": "s",
        "several": "v", "solitary": "y"
    },
    "habitat": {
        "grasses": "g", "leaves": "l", "meadows": "m", "paths": "p",
        "urban": "u", "waste": "w", "woods": "d"
    },
    "bruises": {
    "bruises": "t", "no": "f"
    }
}

# Crear inputs dinámicamente con nombres amigables
user_input = []
for feature in feature_names:
    opciones = opciones_visuales.get(feature, None)
    if opciones:
        choice = st.selectbox(f"{feature}", list(opciones.keys()))
        valor = opciones[choice]
        try:
            encoded = label_encoders[feature].transform([valor])[0]
        except Exception as e:
            st.error(f"Error al codificar la característica '{feature}': {str(e)}")
            st.stop()
        user_input.append(encoded)

#st.write(f"Características esperadas por el modelo: {len(feature_names)}")
#st.write(feature_names)


# Hacer predicción
if st.button("Predecir"):
    input_array = np.array([user_input])
    prediction = model.predict(input_array)[0]
    try:
        clase = label_encoders['poisonous'].inverse_transform([prediction])[0]
    except Exception as e:
        st.error(f"Error al decodificar la predicción: {str(e)}")
        st.stop()

    mensaje = "🍄 El hongo es **VENENOSO** ⚠️" if clase == 'p' else "🍽️ El hongo es **COMESTIBLE**"
    st.success(f"Resultado: {mensaje}")