# Atölye 3 · İlk ajanın: terminalden iş yaptırma

Mivu kanalının üçüncü Atölye bölümünün deposu. Videoda aynı yapay zekâya (Claude Sonnet) aynı soruyu iki yoldan sorduk:

| Yol | Ne oldu (5 deneme, 6 Kasım 2026) |
|---|---|
| Sohbet penceresi (araç yok, 80 dosya mesaja yapıştırıldı) | 5/5 "kod çalıştıramıyorum, kafadan toplarsam yanlış olur" dedi ve bir Python betiği verdi. Betikleri biz çalıştırdık, 5/5 doğruydu. |
| Terminal ajanı (Claude Code, dosyalar klasörde) | 5/5 dosyaları kendisi açtı, üç tuzağı buldu, doğru raporu `rapor.md`'ye yazdı. Her biri 70–105 saniye. |

Bu depoda aynı işi kendi bilgisayarınızda yaptırmak için gereken her şey var. Ölçümün tamamı `olcum/SONUC.md`.

## İçinde ne var
```
kose-kahve/kasa/   Köşe Kahve'nin Ağustos–Ekim 2026 kasa dosyaları (80 CSV, kurgusal veri)
kasim/             1–14 Kasım dosyaları (ikinci ay testi; menüde yeni bir ürün var)
zarf.json          doğru cevaplar (önce bakmayın)
zarf_kasim.json    Kasım için doğru cevap
olcum/             videodaki ölçümün betikleri ve sonucu (uret.py veriyi yeniden üretir)
```
Dosyaların içinde üç tuzak var. Ne olduklarını videoda söylüyoruz, ama önce ajanın bulup bulmadığına bakın.

## 1. Kurulum (Claude Code)
Bilgiler resmî belgeden, 6 Kasım 2026 itibarıyla: https://code.claude.com/docs/en/setup

- **Windows (PowerShell):**
  ```powershell
  irm https://claude.ai/install.ps1 | iex
  ```
- **macOS / Linux / WSL:**
  ```bash
  curl -fsSL https://claude.ai/install.sh | bash
  ```
- Kontrol: `claude --version` bir sürüm numarası yazmalı. Sorun çıkarsa `claude doctor`.
- Windows'ta Git for Windows zorunlu değil (önerilir). Git yoksa ajan komutları PowerShell ile çalıştırır.
- **Hesap:** ilk `claude` açılışında tarayıcıdan giriş istenir. Ücretli bir Claude planı (Pro, Max, Team, Enterprise…) ya da Console (API) hesabı gerekir. Ücretsiz claude.ai planı Claude Code'u kapsamıyor.

## 2. İlk görev (10 dakika)
1. Depoyu indirin, `kose-kahve` klasörüne gidin ve ajanı açın:
   ```bash
   cd kose-kahve
   claude
   ```
2. Yeni sürümler **otomatik modda** açılır. İlk günlerde `Shift+Tab` ile **elle onay** moduna geçin (alt çubukta "manual mode on"). Bu modda okuma serbest, her dosya yazımı ve her komut için size sorar.
3. Şunu yazın:
   > Köşe Kahve'nin Ağustos–Ekim 2026 kasa dosyaları kasa/ altında. Üç şey istiyorum. 1) Her ayın toplam cirosu kaç TL? 2) Üç ayda adet olarak en çok satan ürün hangisi, kaç adet? 3) Ekimde menüye giren badem sütlü latte Ekimde kaç adet sattı? Sonucu rapor.md dosyasına da yaz.
4. Her onay kutusunu okuyun: **Evet**, **Evet ve bir daha sorma** (o komut bu klasörde serbest kalır), **Hayır**.
5. Bitince `rapor.md`'yi `zarf.json` ile karşılaştırın.

## 3. Not dosyası (CLAUDE.md)
Ajan, eksik günler için "kapalı mı, eksik mi bilmiyorum" diyebilir. `kose-kahve/` içine `CLAUDE.md` adlı bir dosya açıp şunu yazın:
```markdown
# Köşe Kahve
- Köşe Kahve Pazartesi günleri kapalıdır, Pazartesi kasa dosyası olmaz.
- Para tutarlarını Türkçe biçimde yaz: 154.555,00 TL.
```
Ajan bu dosyayı her oturumun başında okur. Bizim ölçümde CLAUDE.md'li 3 denemenin 3'ü de "Pazartesi kapalı, beklenen durum" yazdı. İlk açılışta `/init` yazarsanız ajan klasörü inceleyip bu dosyanın taslağını kendisi çıkarır. Buraya ajanın kendi başına bilemeyeceği şeyleri yazın: kapalı günler, para biçimi, dokunulmayacak klasörler.

## 4. İkinci ay: ajansız
Aynı soruya şunu ekleyin: *"Hesabı yapan betiği bu klasöre ozet.py adıyla kaydet. Gelecek ay ben tek komutla kendim çalıştıracağım."*
Sonra `kasim/` içindeki dosyaları `kose-kahve/kasa/` içine kopyalayın ve ajanı çağırmadan çalıştırın:
```bash
python ozet.py
```
Bizim ölçümde 3 betiğin 3'ü de Kasım cirosunu (74.950 TL) doğru buldu ve menüye yeni giren ürünü kendiliğinden saydı.

## 5. İzinler: neye dikkat
Kaynak: https://code.claude.com/docs/en/permission-modes (6 Kasım 2026)

| Mod | Sormadan ne yapar |
|---|---|
| Elle onay (`default`, ekranda "manual") | Yalnız okuma |
| Düzenlemeyi kabul et (`acceptEdits`) | Okuma + dosya düzenleme + yaygın dosya komutları |
| Plan (`plan`) | Hiçbir şeye dokunmaz, önce ne yapacağını yazar |
| Otomatik (`auto`) | Çoğu işi yapar, arka planda güvenlik kontrolü denetler |
| İzinleri atla (`bypassPermissions`) | Her şeyi. **Yalnız kapalı bir deneme makinesinde** |

- Kural sırası: yasak (deny) → sor (ask) → izin (allow). İlk eşleşen kazanır.
- **Python'a izin vermek kapıyı sandığınızdan fazla açar:** Python ile dosya silmek de internete çıkmak da mümkün. İzni araç adına değil işe göre verin.
- Geri alma: girdi boşken `Esc` `Esc` (ya da `/rewind`) geri alma menüsünü açar. **Komutla (Bash) değişen dosyaları geri getirmez**, o yüzden ilk işlerde klasörün bir kopyasıyla ya da Git ile çalışın.
- Bizim ölçümde ajan her denemede 2–4 kez izin dışı komut denedi; hepsi durduruldu, ajan izinli yoldan devam etti.

## Codex CLI kullanıyorsanız
Kaynak: https://github.com/openai/codex (6 Kasım 2026)
- Kurulum: `npm install -g @openai/codex` (Node.js gerekir) ya da macOS'ta `brew install --cask codex`. Windows için README'deki güncel komutu kullanın.
- Giriş: ChatGPT hesabıyla (Plus, Pro, Business, Edu, Enterprise) ya da API anahtarıyla.
- Kum havuzu ayarları: `read-only` (yalnız okuma), `workspace-write` (klasöre yazma), `danger-full-access` (tam erişim, önerilmez). Git ile takip edilen klasörde `workspace-write` + gerektiğinde onayla açılır.
- Not dosyasının adı `AGENTS.md`. CLAUDE.md'deki iki satırı oraya yazın.

## Sınırlar
- Veri kurgusal (`olcum/uret.py`, sabit tohum). Ölçüm tek model (Claude Sonnet), tek gün, 25 çağrı. "Sohbet penceresi" araçsız modeldi: bazı sohbet uygulamaları yüklenen dosyayı kendi bulutunda kodla açabiliyor, onu ölçmedik.
- Maliyet (API liste fiyatıyla, deneme başına): sohbet ~0,37 $, ajan 0,90–1,01 $. Ajan her adımda o ana kadarki her şeyi yeniden okuduğu için daha pahalı. Abonelikte ayrıca ödenmez ama kullanım hakkından daha çok yer.
- Sürüm numaraları ve komutlar hızla değişir: çalıştırmadan önce resmî belgeye bakın.

Lisans: kod MIT, metinler CC BY 4.0. Video: YouTube · heymivu.
