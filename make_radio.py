import json, urllib.request

LOGO_ONLY = False
SERVERS = ["de1", "nl1", "at1"]
PATH = ("/json/stations/search?countrycodeexact=GB&hidebroken=true"
        "&order=clickcount&reverse=true&limit=10000")

def fetch():
    for s in SERVERS:
        try:
            req = urllib.request.Request(
                f"https://{s}.api.radio-browser.info{PATH}",
                headers={"User-Agent": "uk-radio-playlist/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            print(f"{s} failed: {e}")
    raise SystemExit("all servers failed")

def clean(t):
    return t.replace('"', "'").replace(",", " ").replace("\n", " ").strip()

stations = fetch()
seen, lines = set(), ["#EXTM3U"]
for st in stations:
    name = clean(st.get("name", ""))
    url = st.get("url_resolved") or st.get("url")
    if not name or not url or name.lower() in seen:
        continue
    seen.add(name.lower())
    logo = st.get("favicon", "")
    if LOGO_ONLY and not logo.startswith("http"):
        continue
    logo_tag = f' tvg-logo="{logo}"' if logo.startswith("http") else ""
    lines.append(f'#EXTINF:-1 tvg-name="{name}"{logo_tag} group-title="Radio",{name}')
    lines.append(url)

with open("radio.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"wrote {len(seen)} stations")
