import os
import json
import base64
import re
import urllib.request
import urllib.error
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

SYSTEM_PROMPT = """Ești un tutor de matematică expert care explică pas cu pas în limba română.

Când primești o problemă de matematică (text sau imagine):
1. Identifică problema
2. Rezolv-o pas cu pas
3. Răspunde STRICT în format JSON valid, fără alte texte înainte sau după.

Format JSON obligatoriu:
{
  "titlu": "Descriere scurtă a problemei",
  "pasi": [
    {
      "label": "Pasul 1 — Titlu scurt",
      "math": "Formula/expresia matematică",
      "text": "Explicație scrisă (pentru afișare)",
      "speech": "Explicație pentru citit cu voce (scrie numerele în cuvinte, ex: 'doi la puterea a treia')"
    }
  ]
}

REGULI:
- Între 4 și 8 pași
- În câmpul "speech" scrie TOATE numerele în cuvinte românești
- În câmpul "math" folosește notație simplă: ^, /, *, √, etc.
- Fii clar, concis, prietenos
- Ultimul pas să conțină rezultatul final
- Răspunde DOAR cu JSON valid, nimic altceva"""


def call_claude(content):
    """Apel direct la API-ul Anthropic fara pachetul anthropic (doar urllib built-in)."""
    body = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 4096,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": content}]
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    try:
        content = []

        # Check for image
        if "image" in request.files and request.files["image"].filename:
            img = request.files["image"]
            img_data = base64.standard_b64encode(img.read()).decode("utf-8")
            fname = img.filename.lower()
            if fname.endswith(".png"):
                media = "image/png"
            elif fname.endswith(".gif"):
                media = "image/gif"
            elif fname.endswith(".webp"):
                media = "image/webp"
            else:
                media = "image/jpeg"
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": media, "data": img_data}
            })

        # Check for base64 image (from camera/paste)
        img_b64 = request.form.get("image_base64", "")
        if img_b64:
            if "," in img_b64:
                header, img_b64 = img_b64.split(",", 1)
                if "png" in header:
                    media = "image/png"
                else:
                    media = "image/jpeg"
            else:
                media = "image/jpeg"
            content.append({
                "type": "image",
                "source": {"type": "base64", "media_type": media, "data": img_b64}
            })

        # Check for text
        text = request.form.get("text", "").strip()
        if text:
            content.append({"type": "text", "text": f"Rezolvă și explică pas cu pas: {text}"})
        elif content:
            content.append({"type": "text", "text": "Identifică problema de matematică din imagine și rezolv-o pas cu pas."})
        else:
            return jsonify({"error": "Trimite o imagine sau scrie o problemă."}), 400

        result = call_claude(content)
        resp_text = result["content"][0]["text"].strip()

        # Try to extract JSON from response
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', resp_text)
        if json_match:
            resp_text = json_match.group(1).strip()

        data = json.loads(resp_text)
        return jsonify(data)

    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        return jsonify({"error": f"Eroare API ({e.code}): {err_body[:300]}"}), 500
    except json.JSONDecodeError as e:
        return jsonify({"error": f"Răspuns invalid de la AI: {str(e)}", "raw": resp_text[:500]}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    if not ANTHROPIC_API_KEY:
        print("\n⚠️  Setează ANTHROPIC_API_KEY!")
        print("   export ANTHROPIC_API_KEY=sk-ant-...\n")
        exit(1)
    print("\n🎓 Math Tutor Vocal pornit!")
    print("   http://localhost:5000\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
