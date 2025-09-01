import streamlit as st
import json
from datetime import datetime

# Chargement des fichiers JSON
def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

faq = load_json("faq.json")
events = load_json("events.json")
leaders = load_json("leaders.json")
values = load_json("values.json")

# Affichage du chatbot
st.set_page_config(page_title="Chatbot Eglise Méthodiste Canaan Paris", page_icon=":church:")

st.title("Chatbot - Eglise Méthodiste Canaan Paris")

# Barre latérale pour infos contact / réseaux sociaux
with st.sidebar:
    st.header("Contact & Réseaux")
    st.write("📍 Adresse Lieu de culte : 24 avenue Henri Barbusse, 93000 Bobigny")
    st.write("✉️ emccanaanparis@gmail.com")
    st.write("🔗 Réseaux sociaux :")
    st.markdown("[Instagram](https://www.instagram.com/eglise_methodiste_canaan_paris?igsh=dGkwbWx4eDdjYnJ5&utm_source=qr) | [Facebook](https://www.facebook.com/profile.php?id=61578324579713) | [TikTok](https://www.tiktok.com/@eglise.methodiste3)")
    st.image("Logo Canaan Paris V2 - removeBG.png", width=150)  # Affiche votre logo

# Initialisation de la conversation utilisateur
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fonction pour afficher FAQ
def show_faq():
    st.subheader("FAQ - Questions fréquentes")
    for item in faq:
        st.markdown(f"**Q : {item['question']}**")
        st.markdown(f"A : {item['answer']}")

# Fonction pour afficher événements à venir
def show_events():
    st.subheader("Événements à venir")
    now = datetime.now().date()
    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        if event_date >= now:
            st.markdown(f"**{event['title']} - {event['date']}**")
            st.write(event["description"])

# Fonction pour afficher responsables
def show_leaders():
    st.subheader("Responsables de l'église")
    for leader in leaders:
        st.markdown(f"**{leader['role']} :** {leader['name']}")

# Fonction pour afficher valeurs
def show_values():
    st.subheader("Nos valeurs")
    for val in values:
        st.write(f"- {val}")

# Entrée utilisateur
user_input = st.text_input("Posez votre question ici:")

# Logique basique de réponse
def chatbot_response(question):
    question_lower = question.lower()
    # Recherche simple dans FAQ
    for item in faq:
        if item["question"].lower() in question_lower:
            return item["answer"]
    # Mots clés hors FAQ
    if "événements" in question_lower or "event" in question_lower:
        return "Voici la liste des événements à venir."
    if "responsables" in question_lower or "dirigeants" in question_lower:
        return "Voici les responsables de l'église."
    if "valeurs" in question_lower:
        return "Voici les valeurs de notre église."
    if "contact" in question_lower or "email" in question_lower:
        return "Vous pouvez contacter le secrétariat à secretariat@eglise-mc-paris.org"
    return "Désolé, je n'ai pas compris votre question. Vous pouvez consulter la FAQ ou contacter le secrétariat."

# Interaction
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = chatbot_response(user_input)

    # Affichage des réponses spécifiques
    if response == "Voici la liste des événements à venir.":
        show_events()
    elif response == "Voici les responsables de l'église.":
        show_leaders()
    elif response == "Voici les valeurs de notre église.":
        show_values()
    else:
        st.write(response)
    st.session_state.messages.append({"role": "bot", "content": response})

# Affiche historique de la conversation
st.markdown("---")
st.header("Historique de la conversation")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**Vous :** {message['content']}")
    else:
        st.markdown(f"**Bot :** {message['content']}")
