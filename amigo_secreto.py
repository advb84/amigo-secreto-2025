import random
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.title("🎁 Sorteo del Amigo Secreto 🎁")

# 🔑 Conexión con Google Sheets
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credenciales.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("Amigo Secreto").sheet1  # Nombre de tu hoja

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

        st.session_state.resultados = {
            participantes[i]: asignados[i] for i in range(len(participantes))
        }

        # 📝 Guardar resultados en Google Sheets
        sheet.clear()
        sheet.append_row(["Participante", "Amigo Secreto"])
        for persona, amigo in st.session_state.resultados.items():
            sheet.append_row([persona, amigo])

        st.success("🎉 El sorteo se ha realizado y los resultados se guardaron en Google Sheets.")

# Consulta individual con globos 🎈
consulta = st.text_input("Escribe tu nombre para ver tu Amigo Secreto:")

if consulta.strip() != "":
    try:
        # Leer resultados desde Google Sheets
        data = sheet.get_all_records()
        resultado = next((row["Amigo Secreto"] for row in data if row["Participante"] == consulta), None)
        if resultado:
            st.info(f"👉 {consulta}, tu Amigo Secreto es: {resultado} 🎁")
            st.balloons()
        else:
            st.error("Ese nombre no está en la lista de participantes.")
    except Exception as e:
        st.error(f"Error al consultar los resultados en Google Sheets: {e}")

# Botón para reiniciar todo con mensajes aleatorios
if st.button("Reiniciar juego"):
    st.session_state.participantes = []
    st.session_state.resultados = {}
    sheet.clear()  # 🔥 Limpia la hoja de cálculo
    sheet.append_row(["Participante", "Amigo Secreto"])  # 📝 Vuelve a poner la cabecera

    # 🎯 Mensajes aleatorios divertidos
    mensajes = [
        "🎉 ¡Nueva ronda del Amigo Secreto!",
        "🎁 ¡Corre a comprar el regalo!",
        "🤫 ¡Tu misión secreta ha comenzado!",
        "🥳 ¡No se lo digas a nadie!",
        "🎊 ¡Que empiece la diversión!"
    ]
    mensaje = random.choice(mensajes)

    st.success(mensaje)
    st.balloons()