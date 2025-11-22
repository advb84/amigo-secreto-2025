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

        # Guardar resultados en session_state
        st.session_state.resultados = {
            participantes[i]: asignados[i] for i in range(len(participantes))
        }

# Mostrar resultados si existen
if st.session_state.resultados:
    st.subheader("Resultados del sorteo:")
    for persona, amigo in st.session_state.resultados.items():
        st.write(f"{persona} → {amigo}")

    # Botón para borrar solo resultados
    if st.button("Borrar resultados"):
        st.session_state.resultados = {}
        st.success("Los resultados han sido borrados. ¡Listo para un nuevo sorteo!")

# Botón para reiniciar todo
if st.button("Reiniciar juego"):
    st.session_state.participantes = []
    st.session_state.resultados = {}
    st.success("🇻🇪 Se ha reiniciado el juego. 🎉 ¡Nueva ronda del Amigo Secreto con sabor a arepa venezolana!")
    st.balloons()  # Animación de globos estilo celebración
