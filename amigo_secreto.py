import random
import streamlit as st

st.title("🎁 Sorteo del Amigo Secreto 🎁")

# Usamos una lista temporal para almacenar los nombres
if "participantes" not in st.session_state:
    st.session_state.participantes = []

# Entrada de nombre individual
nombre = st.text_input("Escribe tu nombre para participar:")

if st.button("Confirmar participación"):
    if nombre.strip() == "":
        st.error("Por favor escribe un nombre válido.")
    elif nombre in st.session_state.participantes:
        st.warning(f"{nombre} ya está en la lista.")
    else:
        st.session_state.participantes.append(nombre)
        st.success(f"{nombre} ha sido añadido al sorteo.")

# Mostrar lista de participantes actuales
if st.session_state.participantes:
    st.subheader("Participantes confirmados:")
    for p in st.session_state.participantes:
        st.write(f"- {p}")

# Botón para sortear
if st.button("Sortear"):
    participantes = st.session_state.participantes
    if len(participantes) < 2:
        st.error("Debe haber al menos 2 participantes.")
    else:
        asignados = participantes.copy()
        random.shuffle(asignados)

        # Evitar que alguien se asigne a sí mismo
        for i in range(len(participantes)):
            if participantes[i] == asignados[i]:
                j = (i + 1) % len(participantes)
                asignados[i], asignados[j] = asignados[j], asignados[i]

        st.subheader("Resultados del sorteo:")
        for i in range(len(participantes)):
            st.write(f"{participantes[i]} → {asignados[i]}")