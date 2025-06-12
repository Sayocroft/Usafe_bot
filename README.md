# 🦺 Usafe – Your Anti-Hate Crime Helpdesk

**Usafe** is an anonymous, AI-powered helpdesk designed to support individuals affected by hate crimes. Built with a focus on accessibility, empathy, and practical guidance, it helps users describe incidents, detect the hate crime category, and access legal and emotional resources.

> _“Your safety matters. Get confidential support and essential guidance in seconds.”_

---

## 📌 What It Does

- Accepts natural language input from users describing their experience
- Uses **VADER** sentiment analysis to evaluate tone
- Retrieves relevant legal definitions and resources using:
  - **FAISS** vector search
  - **HuggingFace embeddings**
- Classifies the type of hate crime:
  - 🏳️‍🌈 Gender & LGBTQI+
  - 🌍 Racist / Xenophobic
  - 🛐 Anti-Religious
- Delivers targeted legal info and support orgs in Germany

---

## 💡 Why It Matters

Many victims don’t know where to begin. Usafe:
- Offers anonymous support
- Helps users self-identify what happened
- Connects them to real resources (e.g., HateAid, ReachOut Berlin)
- In the long run, can inform NGOs and policymakers about systemic trends

---

## 🧱 Project Structure

Usafe_bot/
│
├── Usafe_app.py                # Streamlit app
├── notebooks/                  # Prototyping & model building
│   ├── EDA_data_hate_crime.ipynb
│   ├── general_vector.ipynb
│   ├── combined_vector.ipynb
│   └── Prompt_user.ipynb
├── data/                       # Legal PDFs + prompts
│   ├── gender_lgbt_def.pdf
│   ├── racist_def.pdf
│   ├── anti_religious_def.pdf
│   └── usafe_prompt.txt
├── models/, mlruns/            # ML model storage
├── environment.yml             # (optional) for Conda setup
├── requirements_*.txt          # Specific dependency groups

---

## ▶️ Running the App

This project uses **multiple environments** to avoid dependency conflicts.

### 1. 🔧 Development (Notebooks, EDA)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

2. 🚀 Production (Streamlit App)

python -m venv usafe_env
source usafe_env/bin/activate
pip install -r requirements_prod.txt

streamlit run Usafe_app.py

3. 🔍 RAG Environment (Vector Search + Prompting)

python -m venv rag_env
source rag_env/bin/activate
pip install -r requirements_rag.txt

💡 Run deactivate before switching between environments.

🧠 Tech Stack
	•	Python
	•	Streamlit – for the user interface
	•	NLTK / VADER – sentiment analysis
	•	LangChain + FAISS + HuggingFace – RAG (retrieval augmented generation)
	•	dotenv – environment management

🗺️ Resources Provided (Sample)

Depending on hate crime type, users receive support links like:
	•	🏳️‍🌈 LesMigraS (LGBTQI+ Counseling)
	•	🌍 ReachOut Berlin (Racism Support)
	•	⚖️ HateAid (Legal Aid)

🔮 Roadmap
	•	🎤 Add voice input for accessibility
	•	🤝 Collaborate with NGOs for live reporting + referrals
	•	📊 Build ML-based risk detection models
	•	🧾 Share anonymized trends with policymakers

👤 Author

Sayonara Andersson Ramos
Business & Strategy Leader → Data Scientist
Berlin, 2025
Queer | French-Brazilian | Building the future with care

📜 License

MIT License 