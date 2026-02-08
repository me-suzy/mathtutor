#!/bin/bash
# ============================================
#  🎓 Math Tutor Vocal - Start Script
# ============================================

echo ""
echo "🎓 =================================="
echo "   TUTOR MATEMATIC VOCAL"
echo "   =================================="
echo ""

# Check API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  Lipsește ANTHROPIC_API_KEY!"
    echo ""
    echo "   Setează-l astfel:"
    echo "   export ANTHROPIC_API_KEY=sk-ant-api03-..."
    echo ""
    echo "   Sau creează un fișier .env:"
    echo "   echo 'ANTHROPIC_API_KEY=sk-ant-api03-...' > .env"
    echo ""
    
    # Try .env file
    if [ -f .env ]; then
        echo "   📂 Am găsit .env, încarc..."
        export $(cat .env | xargs)
    else
        exit 1
    fi
fi

# Check ngrok token
if [ -z "$NGROK_AUTHTOKEN" ]; then
    echo "⚠️  Pentru acces de pe telefon, setează NGROK_AUTHTOKEN:"
    echo "   export NGROK_AUTHTOKEN=2xxx..."
    echo "   (Obține gratuit de pe https://dashboard.ngrok.com)"
    echo ""
    echo "   ▶ Pornesc doar local (http://localhost:5000)"
    echo ""
fi

# Install dependencies
echo "📦 Instalez dependențele..."
pip install -r requirements.txt --break-system-packages -q 2>/dev/null || pip install -r requirements.txt -q

# Start Flask
echo ""
echo "🚀 Pornesc serverul..."
echo ""

if [ -n "$NGROK_AUTHTOKEN" ]; then
    # Start with ngrok
    python3 -c "
import os, threading, time
from pyngrok import ngrok, conf

# Configure ngrok
conf.get_default().auth_token = os.environ.get('NGROK_AUTHTOKEN')

# Start tunnel
tunnel = ngrok.connect(5000)
print(f'')
print(f'🌐 Link public (ngrok): {tunnel.public_url}')
print(f'🏠 Link local:          http://localhost:5000')
print(f'')
print(f'📱 Deschide link-ul ngrok pe telefon!')
print(f'   Ctrl+C pentru a opri')
print(f'')

# Start Flask
from app import app
app.run(host='0.0.0.0', port=5000, debug=False)
"
else
    python3 app.py
fi
