# -*- coding: utf-8 -*-
"""ham/ → sonuc.json: her denemede cevap doğru mu, kaç araç çağrısı, kaç ret, süre, token, liste fiyatı."""
import json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
K = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(K, "ham")
D = json.load(open(os.path.join(K, "dogru.json"), encoding="utf-8"))
sure = {}
for l in open(os.path.join(H, "sure.txt"), encoding="utf-8"):
    a = l.split(); sure[(a[0], int(a[1]))] = float(a[2])

def sayilar(t):
    t = t.replace(" ", " ")
    return {"agustos": "154.555" in t or "154555" in t, "eylul": "148.585" in t or "148585" in t,
            "ekim": "162.845" in t or "162845" in t,
            "cay": bool(re.search(r"Çay[^\n]{0,40}1[.]?570", t)), "badem": bool(re.search(r"226", t)),
            "kopya": "(1).csv" in t, "noktali": "75,00" in t or ";" in t, "iade": "-1" in t or "iade" in t.lower(),
            "yanlis_eylul_kopyali": "155.185" in t or "155185" in t}

out = {"dogru": D, "sohbet": [], "ajan": []}
for i in range(1, 6):
    d = json.load(open(os.path.join(H, "sohbet_%d.json" % i), encoding="utf-8"))
    t = d.get("result", ""); u = d.get("usage", {})
    out["sohbet"].append({"n": i, "sure_sn": sure.get(("sohbet", i)), "sayi_verdi_mi": sayilar(t),
                          "betik_verdi": "```python" in t or "import csv" in t,
                          "maliyet_usd": d.get("total_cost_usd"), "girdi_token": u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0),
                          "cevap_ilk": t[:300]})
for i in range(1, 6):
    arac = []; ret = []; son = None; dosya = []
    for l in open(os.path.join(H, "ajan_%d.jsonl" % i), encoding="utf-8"):
        try: o = json.loads(l)
        except Exception: continue
        if o.get("type") == "assistant":
            for c in o["message"].get("content", []):
                if c.get("type") == "tool_use":
                    inp = c["input"]; ozet = inp.get("command") or inp.get("file_path") or inp.get("pattern") or ""
                    arac.append([c["name"], str(ozet)[:200]])
        if o.get("type") == "result": son = o
    ret = [[r["tool_name"], str(r["tool_input"].get("command", r["tool_input"]))[:200]] for r in son.get("permission_denials", [])]
    kl = os.path.join(H, "ajan_%d_klasor" % i)
    rap = open(os.path.join(kl, "rapor.md"), encoding="utf-8").read() if os.path.exists(os.path.join(kl, "rapor.md")) else ""
    out["ajan"].append({"n": i, "sure_sn": sure.get(("ajan", i)), "rapor_var": bool(rap), "rapor_dogru": sayilar(rap),
                        "son_cevap_dogru": sayilar(son.get("result", "")), "arac_cagrisi": len(arac),
                        "arac_turu": {a: sum(1 for x in arac if x[0] == a) for a in sorted(set(x[0] for x in arac))},
                        "ret": ret, "turn": son.get("num_turns"), "maliyet_usd": son.get("total_cost_usd"),
                        "araclar": arac})
json.dump(out, open(os.path.join(K, "sonuc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in out["sohbet"]:
    s = r["sayi_verdi_mi"]; print("SOHBET", r["n"], r["sure_sn"], "sn | ay doğru:", s["agustos"], s["eylul"], s["ekim"], "| çay", s["cay"], "| badem", s["badem"], "| betik", r["betik_verdi"], "| $", r["maliyet_usd"], "| tok", r["girdi_token"])
for r in out["ajan"]:
    s = r["rapor_dogru"]; print("AJAN", r["n"], r["sure_sn"], "sn | rapor:", r["rapor_var"], "| ay doğru:", s["agustos"], s["eylul"], s["ekim"], "| çay", s["cay"], "| badem", s["badem"], "| kopya/noktalı/iade", s["kopya"], s["noktali"], s["iade"], "| araç", r["arac_cagrisi"], r["arac_turu"], "| ret", len(r["ret"]), "| $", r["maliyet_usd"])
    for x in r["ret"]: print("   RET", x)
