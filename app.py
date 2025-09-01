import streamlit as st
import json
from datetime import datetime
import difflib

# Chargement des fichiers JSON
def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

faq = load_json("faq.json")
events = load_json("events.json")
leaders = load_json("leaders.json")
values = load_json("values.json")
bank_info = load_json("bank_info.json")  # Coordonnées bancaires

# Configuration page
st.set_page_config(page_title="Chatbot Eglise Méthodiste Canaan Paris", page_icon=":church:")

st.title("Chatbot - Eglise Méthodiste Canaan Paris")

# Sidebar avec contact, réseaux, lien officiel et logo
with st.sidebar:
    st.header("Contact & Réseaux")
    st.write("📍 Adresse Lieu de culte : 24 avenue Henri Barbusse, 93000 Bobigny")
    st.write("✉️ Secretariat : emccanaanparis@gmail.com")
    st.write("🔒 Association enregistrée :")
    st.markdown("[Voir le dossier officiel sur Pappers](https://www.pappers.fr/entreprise/eglise-methodiste-canaan-emc-W751280128aussi)")
    st.write("🔗 Réseaux sociaux :")
    st.markdown("[Instagram](https://www.instagram.com/eglise_methodiste_canaan_paris?igsh=dGkwbWx4eDdjYnJ5&utm_source=qr) | [Facebook](https://www.facebook.com/profile.php?id=61578324579713) | [TikTok](https://www.tiktok.com/@eglise.methodiste3)")
    st.image("Logo Canaan Paris V2 - removeBG.png", width=150)

if "messages" not in st.session_state:
    st.session_state.messages = []

def show_faq():
    st.subheader("FAQ - Questions fréquentes")
    for item in faq:
        st.markdown(f"**Q : {item['question']}**")
        st.markdown(f"A : {item['answer']}")

def show_events():
    st.subheader("Événements à venir")
    now = datetime.now().date()
    for event in events:
        event_date = datetime.strptime(event["date"], "%Y-%m-%d").date()
        if event_date >= now:
            st.markdown(f"**{event['title']} - {event['date']}**")
            st.write(event["description"])

def show_leaders():
    st.subheader("Responsables de l'église")
    for leader in leaders:
        st.markdown(f"**{leader['role']} :** {leader['name']}")

def show_values():
    st.subheader("Nos valeurs")
    for val in values:
        st.write(f"- {val}")

def find_best_faq_match(question, faq_list, threshold=0.5):
    questions = [item["question"].lower() for item in faq_list]
    matches = difflib.get_close_matches(question, questions, n=1, cutoff=threshold)
    if matches:
        for item in faq_list:
            if item["question"].lower() == matches[0]:
                return item["answer"]
    return None

def chatbot_response(question):
    question_lower = question.lower().strip()

    # Réponse accueil pour salutations
    greetings = ["bonjour", "salut", "hello", "bonsoir", "coucou"]
    if any(greet in question_lower for greet in greetings):
        return ("Bonjour, je suis le chatbot de l'Église Méthodiste Canaan Paris, "
                "comment puis-je vous aider aujourd'hui ?")

    if len(question_lower) < 4:
        return ("Votre question est un peu courte, pouvez-vous préciser un peu plus ? "
                "Par exemple, demandez l'horaire des cultes, les événements, ou les contacts.")

    # Afficher FAQ à la demande
    if any(word in question_lower for word in ["faq", "questions fréquentes", "question fréquente"]):
        return "AFFICHER_FAQ"

    # Correspondance proche dans la FAQ
    faq_answer = find_best_faq_match(question_lower, faq)
    if faq_answer:
        return faq_answer

    # Mots-clés élargis
    if any(word in question_lower for word in ["événements", "event", "agenda", "calendrier", "programme"]):
        return "Voici la liste des événements à venir."

    if any(word in question_lower for word in ["responsable", "dirigeant", "pasteur", "équipe"]):
        return "Voici les responsables de l'église."

    if "valeurs" in question_lower:
        return "Voici les valeurs de notre église."

    if any(word in question_lower for word in ["contact", "email", "mail", "joindre"]):
        return "Vous pouvez contacter le secrétariat à emccanaanparis@gmail.com"

    if any(word in question_lower for word in ["lieu", "adresse", "local", "où", "ou", "emplacement", "endroit"]):
        return "Notre lieu de culte est au 24 avenue Henri Barbusse, 93000 Bobigny."

    if any(word in question_lower for word in ["don", "offrande", "collecte", "virement", "banque", "iban", "rib", "coordonnées bancaires"]):
        return (
            "Voici les coordonnées bancaires pour vos dons ou virements :\n"
            f"- Titulaire : {bank_info['Titulaire']}\n"
            f"- IBAN : {bank_info['IBAN']}\n"
            f"- BIC : {bank_info['BIC']}"
        )

    if any(word in question_lower for word in ["aide", "quoi", "que", "comment", "?", "info"]):
        return ("Je ne suis pas sûr de comprendre votre question. "
                "Voici quelques exemples de questions que vous pouvez poser :\n"
                "- Quels sont les horaires des cultes ?\n"
                "- Quels sont les prochains événements ?\n"
                "- Qui sont les responsables ?\n"
                "- Quelles sont les valeurs de l'église ?\n"
                "- Comment puis-je contacter le secrétariat ?\n"
                "- Où se situe le lieu de culte ?\n"
                "- Affichez-moi la FAQ\n"
                "- Comment faire un don ou un virement ?")

    return ("Désolé, je n'ai pas compris votre question. "
            "Vous pouvez consulter la FAQ ci-dessous ou contacter le secrétariat pour plus d'informations.")

user_input = st.text_input("Posez votre question ici:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = chatbot_response(user_input)

    if response == "AFFICHER_FAQ":
        show_faq()
    elif response == "Voici la liste des événements à venir.":
        show_events()
    elif response == "Voici les responsables de l'église.":
        show_leaders()
    elif response == "Voici les valeurs de notre église.":
        show_values()
    else:
        st.write(response)

    st.session_state.messages.append({"role": "bot", "content": response})

st.markdown("---")
st.header("Historique de la conversation")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"**Vous :** {message['content']}")
    else:
        st.markdown(f"**Bot :** {message['content']}")
