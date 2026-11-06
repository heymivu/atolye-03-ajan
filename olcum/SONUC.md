# Atölye 3 ölçümü — aynı iş: sohbet kutusu mu, terminal ajanı mı (2026-11-06)

**Model:** Claude Sonnet (`claude -p --model sonnet`, Claude Code 2.1.312), boş klasörden, `--setting-sources ""` (hook/ayar yok), oturum kaydı yok.
**Veri:** kurgusal Köşe Kahve kasası, Ağustos–Ekim 2026: 80 CSV dosyası, 79 gün, 5.032 satır, 125 KB (`uret.py`, sabit tohum; doğru cevap `dogru.json`).
**Tuzaklar:** (1) 15–20 Eylül haftası `;` ayraçlı ve virgüllü ondalık (`75,00`); (2) `2026-09-26 (1).csv` aynı günün kopyası; (3) 22 iade satırı (adet −1); (4) Pazartesi dosyası yok (kafe kapalı; Atölye 2 tohumu).
**Soru (iki kolda aynı):** her ayın cirosu, üç ayda adetçe en çok satan, Ekimde badem sütlü latte adedi, kısa özet.
**Betikler:** `olc.sh` (kollar), `say.py` (→ `sonuc.json`), ham kayıt `ham/`.

## Doğru cevap
| | |
|---|---|
| Ağustos | 154.555 TL |
| Eylül | 148.585 TL |
| Ekim | 162.845 TL |
| En çok satan (adet) | Çay, 1.570 |
| Ekim badem sütlü latte | 226 |
| Dosyayı düz okuyan (kopya dahil, `;` haftası okunamaz) Eylül | 118.495 TL (30.090 TL eksik; `;` haftası 36.690 TL, kopya +6.600 TL) |

## Sonuç
| Kol | Ne verildi | Sonuç (5 deneme) | Süre | Liste fiyatı / deneme |
|---|---|---|---|---|
| **Sohbet** | araç yok; 80 dosyanın içeriği mesaja yapıştırıldı (86,6 bin token); sistem notu "sohbet penceresi, kod çalıştıramazsın" | **5/5 aylık ciroyu vermedi**: "kod çalıştıramıyorum, elle toplarsam yanlış olur" deyip bir Python betiği yazdı. 1/5 badem sütlü latteyi elle saydı (226, doğru). Üç tuzağı 5/5 metinde fark etti | 36–48 sn (yalnız cevap) | ~0,37 $ |
| Sohbetin betiği, **elle çalıştırılınca** | betik kaydedildi, dosyaların yanında `python betik.py` | **5/5 bütün sayılar doğru** | insanın adımları ölçülmedi | – |
| **Ajan** | dosyalar klasörde; araçlar Read/Write/Edit/Glob/Grep/Bash; izin yalnız okuma-yazma + `python` ve `ls` komutları | **5/5 bütün sayılar doğru, 5/5 üç tuzağı buldu, 5/5 `rapor.md` yazdı** | 70–105 sn (baştan sona) | 0,90–1,00 $ |
| Ajan + `CLAUDE.md` (2 satır: "Pazartesi kapalıyız", TL biçimi) | aynı | 3/3 doğru; **3/3 "Pazartesi kapalı, dosya yok, beklenen"** | 89–113 sn | 0,94–1,01 $ |

- Ajan araç çağrısı: 8–12 (çoğu Bash ve Write). **İzin reddi: 5 denemede 2–4**: ajan izin verilmeyen komutları (`cmp`, `awk`, `grep … | head`) denedi, reddedildi, izinli yoldan (Python betiği) devam etti. Hiçbir deneme izin dışına çıkamadı.
- CLAUDE.md'siz 5 ajanın eksik günler üzerine: 2'si "kapalı mı eksik mi bilmiyorum" dedi, 1'i "kapalı varsaydım, doğrulanmadı", 1'i "Pazartesi dosya yok" diye not etti, 1'i değinmedi. CLAUDE.md ile 3/3 biliyor.
- Ajan sohbetten ~2,6 kat pahalı (liste fiyatı): her adımda konuşmanın tamamını yeniden okuyor (Atölye 2 bulgusu). Abonelikte ayrı ücret yok.
- Ajan 1–3'ün ilk koşu kayıtları betik hatasıyla CLAUDE.md'li koşuların altında kaldı; özetleri `ham/sonuc_ilk5.json`'da (hepsi 5/5 doğru), ham kayıt için 1–3 yeniden koşuldu (aynı sonuç). Çağrı toplamı: pilot 2 + sohbet 5 + ajan 8 + ajan/CLAUDE.md 3 = 18.

## Videoda söylenebilecek (ölçülen) cümleler
- Aynı model, aynı soru. Sohbet kutusu beşte beş "kodu çalıştıramam, yanlış toplarım" dedi ve betik verdi.
- O betik doğru, ama kaydetmek, dosyaların yanına koymak ve çalıştırmak size kalıyor.
- Terminaldeki ajan beşte beş, bir buçuk dakikada, üç tuzağı bulup doğru raporu dosyaya yazdı.
- İzin vermediğimiz komutu denedi, durduruldu, izin verdiğimiz yoldan gitti.
- Klasöre iki satırlık not koyunca Pazartesileri "bilmiyorum" demeyi bıraktı.
- Söylenmeyecek: "sohbet yanlış hesapladı" (hesaplamadı, dürüstçe reddetti); "ajan ucuz" (2,6 kat pahalı); insan süresi (ölçülmedi).

## Ek koşular (aynı gün)
- **Plan modu** (`--permission-mode plan`, 2 deneme, 101–126 sn, 0,93–0,94 $): 2/2 dosyaları okudu, üç tuzağı buldu (biri Pazartesileri de "kapalı sayıyorum" dedi), ne yapacağını madde madde yazdı ve **klasöre hiçbir dosya yazmadı** (klasörde yalnız `kasa/`); "devam et" demenizi bekledi. Planı Claude Code'un kendi plan dosyasına yazdı (`~/.claude/plans/`), çalışma klasörüne değil.
- **Ek ajan koşusu ×2** (`ham/ajanek_*`): betik yaması tutmadığı için plan bayrağı verilmeden koştu = normal ajan koşusu; 2/2 doğru (66, 91 sn; 0,89–1,02 $).
- Çağrı toplamı güncel: 18 + 2 plan + 2 ek = **22**.
- **Betiği sakla** (`sakla`, 3 deneme, 76–100 sn): soruya "hesabı yapan betiği `ozet.py` adıyla kaydet, gelecek ay ben çalıştıracağım" eklendi. 3/3 Ağustos–Ekim cevapları doğru, 3/3 `ozet.py` kaydetti. **Ajansız yeniden kullanım testi:** klasöre 1–14 Kasım dosyaları (12 gün, yeni mevsimlik ürün Sahlep 7 Kasım'dan; `uret_kasim.py`, doğru cevap `dogru_kasim.json`) eklenip `python ozet.py` elle çalıştırıldı → **3/3 Kasım cirosu 74.950 TL doğru, 3/3 Sahlep 77 adet listede** (ürün adları betiğe gömülü değil), rapor.md yenilendi (`ham/sakla_*_kasim_testi/`).
- Çağrı toplamı güncel: 22 + 3 = **25**.
