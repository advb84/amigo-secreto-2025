import random
import streamlit as st

st.title("🎁 Sorteo del Amigo Secreto 🎁")

# Estado inicial
if "participantes" not in st.session_state:
    st.session_state.participantes = []
if "resultados" not in st.session_state:
    st.session_state.resultados = {}

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

# Botón para sortear (solo una vez)
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

        # Guardar resultados en session_state
        st.session_state.resultados = {
            participantes[i]: asignados[i] for i in range(len(participantes))
        }

        st.success("🎉 El sorteo se ha realizado. Cada participante puede consultar su resultado.")

# Consulta individual con globos
if st.session_state.resultados:
    consulta = st.text_input("Escribe tu nombre para ver tu Amigo Secreto:")
    if consulta.strip() != "":
        if consulta in st.session_state.resultados:
            st.info(f"👉 {consulta}, tu Amigo Secreto es: {st.session_state.resultados[consulta]} 🎁")
            st.balloons()  # 🎈 Animación especial solo para el participante
        else:
            st.error("Ese nombre no está en la lista de participantes.")

