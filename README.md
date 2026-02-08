# 🎓 Tutor Matematic Vocal

Aplicație web care rezolvă probleme de matematică pas cu pas, cu explicație vocală.

## Funcționalități

- **📝 Text** — scrii problema direct
- **📷 Imagine** — încarci o poză cu problema (sau Ctrl+V screenshot)
- **📸 Cameră** — fotografiezi problema direct din browser
- **🎤 Voce** — dictezi problema în română
- **🔊 Explicație vocală** — fiecare pas e citit cu voce
- **🌐 Ngrok** — accesibil de pe telefon prin link public

## Instalare rapidă

```bash
# 1. Clonează/copiază folderul math-tutor

# 2. Setează API key-ul Anthropic
export ANTHROPIC_API_KEY=sk-ant-api03-...

# 3. (Opțional) Pentru acces de pe telefon:
export NGROK_AUTHTOKEN=2xxx...

# 4. Pornește
bash start.sh
```

## Sau pas cu pas (manual)

```bash
# Instalează dependențe
pip install flask anthropic pyngrok Pillow

# Setează key
export ANTHROPIC_API_KEY=sk-ant-api03-...

# Pornește
python app.py
```

Apoi deschide http://localhost:5000

## Structură

```
math-tutor/
├── app.py              # Backend Flask + Claude API
├── templates/
│   └── index.html      # Frontend complet
├── requirements.txt
├── start.sh            # Script de pornire cu ngrok
└── README.md
```

## Note

- Folosește Claude Sonnet pentru viteză (2-4 secunde răspuns)
- Vocea folosește Web Speech API din browser
- Pentru voce românească naturală: deschide în Edge sau Chrome
- Camera funcționează doar pe HTTPS (ngrok) sau localhost
