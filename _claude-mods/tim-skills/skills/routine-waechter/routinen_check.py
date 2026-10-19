#!/usr/bin/env python3
"""routinen_check.py - Routinen (Claude-Code-Remote-Trigger) auf Ausfälle, Kostenfallen und Klartext-Geheimnisse prüfen.

    python3 routinen_check.py liste.json            # gespeicherte Ausgabe von list_triggers (eine oder mehrere Seiten)
    python3 routinen_check.py liste.json --json     # maschinenlesbar
    python3 routinen_check.py --prompt prompt.txt   # einen Routine-Prompt vor dem Anlegen prüfen

Liest nur lokale Dateien, kein Netz. Gibt gefundene Geheimnisse NIE aus, nur Art und Position.
Exit 0 = alles ok, 1 = Hinweise, 2 = Probleme (Ausfall, Geheimnis im Prompt).
"""
import json
import re
import sys
from datetime import datetime, timezone

# Muster für Zugangsdaten. Es wird nur gemeldet, dass etwas passt – nie der Wert.
GEHEIMNIS_MUSTER = [
    ("Instagram/Facebook-Token", r"\b(?:IGAA|IGQV|EAA[A-Za-z0-9])[A-Za-z0-9_\-]{30,}"),
    ("GitHub-Token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{40,}"),
    ("Anthropic/OpenAI-Key", r"\bsk-(?:ant-)?[A-Za-z0-9_\-]{30,}"),
    ("Google-API-Key", r"\bAIza[0-9A-Za-z_\-]{30,}"),
    ("Slack-Token", r"\bxox[abprs]-[A-Za-z0-9\-]{20,}"),
    ("AWS-Key", r"\bAKIA[0-9A-Z]{16}\b"),
    ("Privater Schlüssel", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ("Zuweisung mit Geheimnis", r"(?i)\b(?:access_token|api_key|apikey|secret|password|passwort|token)\s*[=:]\s*['\"]?[A-Za-z0-9_\-\.]{24,}"),
]


def geheimnisse(text):
    funde = []
    for art, muster in GEHEIMNIS_MUSTER:
        for m in re.finditer(muster, text or ""):
            zeile = text.count("\n", 0, m.start()) + 1
            funde.append({"art": art, "zeile": zeile, "laenge": len(m.group(0))})
    # gleiche Stelle nur einmal melden
    gesehen, eindeutig = set(), []
    for f in funde:
        if f["zeile"] not in gesehen:
            gesehen.add(f["zeile"])
            eindeutig.append(f)
    return eindeutig


def zeit(s):
    if not s:
        return None
    s = re.sub(r"(\.\d{6})\d+", r"\1", s).replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return None


def stuendlich(cron):
    felder = re.sub(r"^CRON_TZ=\S+\s+", "", cron or "").split()
    if len(felder) != 5:
        return False
    stunde = felder[1]
    return stunde == "*" or stunde.startswith("*/")


def lade(pfade):
    routinen = []
    for p in pfade:
        roh = open(p, encoding="utf-8").read()
        start = roh.find("{")
        daten = json.loads(roh[start: roh.rfind("}") + 1])
        if "ccr" in daten:
            daten = daten["ccr"]
        routinen += daten.get("data", daten if isinstance(daten, list) else [])
    return routinen


def pruefe(r, jetzt):
    hinweise, probleme = [], []
    name = r.get("name", "?")
    prompt = (r.get("derived_state") or {}).get("prompt") or r.get("prompt") or ""
    last = r.get("last_run") or {}
    status = (last.get("status") or "").replace("ROUTINE_RUN_STATUS_", "") or "NIE_GELAUFEN"
    aktiv = r.get("enabled", False)
    cron = r.get("cron_expression") or ""
    persist = r.get("persist_session")

    if status not in ("SUCCEEDED", "NIE_GELAUFEN"):
        grund = (last.get("failure_reason") or "").replace("ROUTINE_RUN_FAILURE_REASON_", "")
        probleme.append(f"letzter Lauf {status}" + (f" ({grund})" if grund and grund != "UNSPECIFIED" else ""))
    if r.get("ended_reason"):
        probleme.append(f"endgültig beendet: {r['ended_reason']}")
    if r.get("suspension_reason"):
        hinweise.append(f"pausiert: {r['suspension_reason']}")
    naechster = zeit(r.get("next_run_at"))
    if aktiv and naechster and naechster < jetzt and (jetzt - naechster).total_seconds() > 3 * 3600:
        probleme.append(f"überfällig seit {naechster:%d.%m. %H:%M} UTC")
    if aktiv and persist and cron and stuendlich(cron):
        hinweise.append("stündlich in derselben Session – jede Ausführung liest den ganzen Verlauf (teuer); frische Session pro Lauf erwägen")
    if aktiv and persist and status == "SUCCEEDED":
        hinweise.append("Session-Routine: SUCCEEDED heißt nur „zugestellt“ – Ergebnis im Verlauf der Session prüfen")
    for g in geheimnisse(prompt):
        probleme.append(f"Klartext-Geheimnis im Prompt: {g['art']} (Zeile {g['zeile']}, {g['laenge']} Zeichen) – Wert in Secret/Umgebung verschieben und Zugang erneuern")
    return {
        "name": name, "id": r.get("id"), "aktiv": aktiv, "zeitplan": cron or r.get("run_once_at") or "nur manuell",
        "letzter_lauf": status, "letzter_start": (last.get("fired_at") or r.get("last_fired_at") or "")[:16],
        "session": last.get("session_id"), "probleme": probleme, "hinweise": hinweise,
    }


def prompt_check(pfad):
    text = open(pfad, encoding="utf-8").read()
    probleme, hinweise = [], []
    for g in geheimnisse(text):
        probleme.append(f"Klartext-Geheimnis: {g['art']} (Zeile {g['zeile']}) – als Secret der Umgebung hinterlegen, im Prompt nur den Namen nennen")
    if not re.search(r"(?i)\b(main|branch)\b", text):
        hinweise.append("kein Branch genannt – festlegen, wohin gepusht wird (z. B. main oder PR gegen main)")
    if re.search(r"(?i)git push|commit", text) and not re.search(r"(?i)repo|timelapsemedia/", text):
        hinweise.append("es wird gepusht, aber kein Repo genannt")
    if not re.search(r"(?i)bericht|report|push-?benachrichtigung|pushnotification", text):
        hinweise.append("kein Abschlussbericht verlangt – ohne Bericht fallen Ausfälle nicht auf")
    if re.search(r"(?i)\bpost(e|en)?\b|veröffentlich|publish|upload", text) and not re.search(r"(?i)freigabe|freigegeben|approved|erlaubt", text):
        hinweise.append("Außenwirkung (posten/veröffentlichen) ohne genannte Freigabe – Tims Freigabe wörtlich mit Datum in den Prompt")
    if not re.search(r"(?i)token|ablauf|abgelaufen|401|auth", text) and re.search(r"(?i)instagram|facebook|graph\.|api", text):
        hinweise.append("API-Zugriff ohne Regel für abgelaufene Zugänge – „bei 401/abgelaufenem Token: stoppen und melden“ ergänzen")
    return probleme, hinweise


def main():
    a = sys.argv[1:]
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    if a[0] == "--prompt":
        probleme, hinweise = prompt_check(a[1])
        for p in probleme:
            print("  PROBLEM  " + p)
        for h in hinweise:
            print("  HINWEIS  " + h)
        if not probleme and not hinweise:
            print("  ok – keine Auffälligkeiten")
        sys.exit(2 if probleme else 1 if hinweise else 0)
    als_json = "--json" in a
    dateien = [x for x in a if not x.startswith("--")]
    jetzt = datetime.now(timezone.utc)
    ergebnisse = [pruefe(r, jetzt) for r in lade(dateien)]
    ergebnisse.sort(key=lambda e: (not e["probleme"], not e["hinweise"], e["name"]))
    if als_json:
        print(json.dumps(ergebnisse, ensure_ascii=False, indent=2))
    else:
        print(f"Routinen-Check {jetzt:%d.%m.%Y %H:%M} UTC – {len(ergebnisse)} Routinen")
        for e in ergebnisse:
            zeichen = "ROT " if e["probleme"] else "GELB" if e["hinweise"] else "OK  "
            aktiv = "aktiv" if e["aktiv"] else "aus"
            print(f"\n[{zeichen}] {e['name']}  ({aktiv}; {e['zeitplan']}; letzter Lauf {e['letzter_lauf']} {e['letzter_start']})")
            for p in e["probleme"]:
                print("       PROBLEM  " + p)
            for h in e["hinweise"]:
                print("       HINWEIS  " + h)
    rot = any(e["probleme"] for e in ergebnisse)
    gelb = any(e["hinweise"] for e in ergebnisse)
    sys.exit(2 if rot else 1 if gelb else 0)


if __name__ == "__main__":
    main()
