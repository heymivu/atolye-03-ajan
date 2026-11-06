# -*- coding: utf-8 -*-
"""Köşe Kahve kasa dosyaları (Ağustos–Ekim 2026) + doğru cevap. Sabit tohum, kurgusal veri.
Tuzaklar: (1) 15–20 Eylül haftası kasa güncellemesi → ';' ayraç + virgüllü ondalık;
(2) '2026-09-26 (1).csv' aynı günün kopyası; (3) iade satırları negatif adet;
(4) Pazartesi kapalı → Pazartesi dosyası yok."""
import csv, json, os, random, shutil, sys, datetime as dt

KOK = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(KOK, "girdi", "kasa")
MENU = [("Türk kahvesi", 60), ("Filtre kahve", 75), ("Latte", 95), ("Americano", 80),
        ("Çay", 25), ("Cheesecake", 120), ("Kurabiye", 45), ("Tost", 90)]
BADEM = ("Badem sütlü latte", 110)  # Atölye 2 kararı: 1 Ekim'de menüye girdi
AGIRLIK = {"Türk kahvesi": 14, "Filtre kahve": 12, "Latte": 15, "Americano": 9, "Çay": 22,
           "Cheesecake": 6, "Kurabiye": 10, "Tost": 8, "Badem sütlü latte": 9}

def main():
    rnd = random.Random(20261106)
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    gun = dt.date(2026, 8, 1); son = dt.date(2026, 10, 31)
    satirlar = {}  # tarih -> [(saat, urun, adet, fiyat)]
    while gun <= son:
        if gun.weekday() != 0:  # Pazartesi kapalı
            menu = MENU + ([BADEM] if gun >= dt.date(2026, 10, 1) else [])
            w = [AGIRLIK[m[0]] for m in menu]
            n = rnd.randint(44, 72) + (12 if gun.weekday() >= 5 else 0)
            dk = sorted(rnd.sample(range(8 * 60, 21 * 60), n))
            s = []
            for t in dk:
                u, f = rnd.choices(menu, w)[0]
                a = rnd.choices([1, 2, 3], [70, 22, 8])[0]
                s.append(("%02d:%02d" % divmod(t, 60), u, a, float(f)))
            for _ in range(rnd.choice([0, 0, 0, 1])):  # iade
                u, f = rnd.choice(menu)
                s.append(("%02d:%02d" % divmod(rnd.randint(9 * 60, 20 * 60), 60), u, -1, float(f)))
            s.sort()
            satirlar[gun] = s
        gun += dt.timedelta(days=1)
    yeni = (dt.date(2026, 9, 15), dt.date(2026, 9, 20))
    for g, s in satirlar.items():
        ad = os.path.join(OUT, g.isoformat() + ".csv")
        if yeni[0] <= g <= yeni[1]:
            with open(ad, "w", encoding="utf-8", newline="") as fh:
                fh.write("saat;urun;adet;birim_fiyat\n")
                for r in s: fh.write("%s;%s;%d;%s\n" % (r[0], r[1], r[2], ("%.2f" % r[3]).replace(".", ",")))
        else:
            with open(ad, "w", encoding="utf-8", newline="") as fh:
                wr = csv.writer(fh); wr.writerow(["saat", "urun", "adet", "birim_fiyat"])
                for r in s: wr.writerow([r[0], r[1], r[2], "%.2f" % r[3]])
    shutil.copyfile(os.path.join(OUT, "2026-09-26.csv"), os.path.join(OUT, "2026-09-26 (1).csv"))
    # doğru cevap
    ay = {8: 0.0, 9: 0.0, 10: 0.0}; adet = {}; ekim_badem = 0; iade = 0; satir = 0
    for g, s in satirlar.items():
        for (_, u, a, f) in s:
            ay[g.month] += a * f; adet[u] = adet.get(u, 0) + a; satir += 1
            if a < 0: iade += 1
            if g.month == 10 and u == BADEM[0]: ekim_badem += a
    # tuzağa düşen hesaplar (yanlış yolların vereceği sayılar)
    kopya = sum(a * f for (_, u, a, f) in satirlar[dt.date(2026, 9, 26)])
    dogru = {"dosya_sayisi": len(satirlar) + 1, "gun_sayisi": len(satirlar), "satir": satir, "iade_satiri": iade,
             "ciro_TL": {"agustos": round(ay[8], 2), "eylul": round(ay[9], 2), "ekim": round(ay[10], 2)},
             "adet_3ay": dict(sorted(adet.items(), key=lambda x: -x[1])),
             "en_cok_satan": max(adet, key=adet.get), "ekim_badem_adet": ekim_badem,
             "tuzak": {"kopya_gun": "2026-09-26", "kopya_ciro_TL": round(kopya, 2),
                       "noktali_virgul_gunler": "2026-09-15..2026-09-20"}}
    with open(os.path.join(KOK, "dogru.json"), "w", encoding="utf-8") as fh:
        json.dump(dogru, fh, ensure_ascii=False, indent=1)
    print(json.dumps(dogru, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
