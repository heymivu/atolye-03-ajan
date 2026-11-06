# -*- coding: utf-8 -*-
"""Kasım 1–14 kasa dosyaları (ajanın sakladığı betiğin yeniden kullanım testi) + doğru cevap.
Yeni durum: 7 Kasım'dan itibaren menüde mevsimlik "Sahlep" (70 TL). Biçim normal (',' ayraç), Pazartesi kapalı."""
import csv, json, os, random, sys, datetime as dt
sys.stdout.reconfigure(encoding="utf-8")
KOK = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(KOK, "girdi", "kasa_kasim")
MENU = [("Türk kahvesi", 60), ("Filtre kahve", 75), ("Latte", 95), ("Americano", 80), ("Çay", 25), ("Cheesecake", 120),
        ("Kurabiye", 45), ("Tost", 90), ("Badem sütlü latte", 110)]
SAHLEP = ("Sahlep", 70)
AG = {"Türk kahvesi": 14, "Filtre kahve": 12, "Latte": 15, "Americano": 9, "Çay": 22, "Cheesecake": 6, "Kurabiye": 10, "Tost": 8, "Badem sütlü latte": 9, "Sahlep": 12}
rnd = random.Random(20261107); os.makedirs(OUT, exist_ok=True); ciro = 0.0; adet = {}
g = dt.date(2026, 11, 1)
while g <= dt.date(2026, 11, 14):
    if g.weekday() != 0:
        menu = MENU + ([SAHLEP] if g >= dt.date(2026, 11, 7) else [])
        n = rnd.randint(44, 72) + (12 if g.weekday() >= 5 else 0)
        dk = sorted(rnd.sample(range(8 * 60, 21 * 60), n))
        with open(os.path.join(OUT, g.isoformat() + ".csv"), "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh); w.writerow(["saat", "urun", "adet", "birim_fiyat"])
            for t in dk:
                u, f = rnd.choices(menu, [AG[m[0]] for m in menu])[0]; a = rnd.choices([1, 2, 3], [70, 22, 8])[0]
                w.writerow(["%02d:%02d" % divmod(t, 60), u, a, "%.2f" % f]); ciro += a * f; adet[u] = adet.get(u, 0) + a
    g += dt.timedelta(days=1)
d = {"kasim_1_14_ciro_TL": round(ciro, 2), "adet": dict(sorted(adet.items(), key=lambda x: -x[1])), "sahlep": adet.get("Sahlep", 0)}
json.dump(d, open(os.path.join(KOK, "dogru_kasim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1); print(d)
