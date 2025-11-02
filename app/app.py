from flask import Flask, render_template
import yaml, os

app = Flask(__name__)

def load_config():
    cfg_path = os.path.join(os.path.dirname(__file__), "links.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

@app.get("/healthz")
def healthz():
    return {"status": "ok"}, 200

@app.get("/")
def index():
    cfg = load_config()
    return render_template(
        "index.html",
        title=cfg.get("title"),
        artist=cfg.get("artist"),
        subtitle=cfg.get("subtitle"),
        brand_color=cfg.get("brand_color"),
        cover_image=cfg.get("cover_image"),
        links=cfg.get("links", []),
        embeds=cfg.get("embeds", {}),
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)