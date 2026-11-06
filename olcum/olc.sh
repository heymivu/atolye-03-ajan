#!/usr/bin/env bash
# Atölye 3 ölçümü: aynı iş, iki yol. Model Claude Sonnet, boş klasörden, ayar/hook yok.
# SOHBET: araç yok, 80 dosyanın içeriği mesaja yapıştırılmış. AJAN: dosyalar klasörde, araçlar açık.
# Kullanım: ./olc.sh sohbet|ajan N   (N = deneme no). Çıktı ham/<kol>_<N>.json (+ ajan için .jsonl + klasör)
set -u
D="$(cd "$(dirname "$0")" && pwd)"; KOL=$1; N=$2
SC="${A3_SCRATCH:?A3_SCRATCH yok}"; W="$SC/${KOL}_$N"; rm -rf "$W"; mkdir -p "$W"
SORU='Köşe Kahve'"'"'nin Ağustos–Ekim 2026 kasa dosyaları bunlar. Üç şey istiyorum. 1) Her ayın toplam cirosu kaç TL? 2) Üç ayda adet olarak en çok satan ürün hangisi, kaç adet? 3) Ekimde menüye giren badem sütlü latte Ekimde kaç adet sattı? Sonunda kısa bir özet yaz.'
CC=(claude -p --model sonnet --setting-sources "" --no-session-persistence --exclude-dynamic-system-prompt-sections)
T0=$(date +%s.%N)
if [ "$KOL" = sohbet ]; then
  { echo "$SORU Dosyaları aşağıya yapıştırıyorum."; echo; for f in "$D"/girdi/kasa/*.csv; do echo "=== $(basename "$f") ==="; cat "$f"; echo; done; } > "$W/mesaj.txt"
  (cd "$W" && "${CC[@]}" --tools "" --append-system-prompt "Bu bir sohbet penceresi. Dosya sistemine, koda ya da komut aracına erişimin yok. Yalnız mesajdaki metinle cevap ver." --output-format json < mesaj.txt > "$D/ham/sohbet_$N.json" 2> "$D/ham/sohbet_$N.err")
else
  cp -r "$D/girdi/kasa" "$W/kasa"
  [ "$KOL" = ajanmd ] && printf '%s
' "# Köşe Kahve" "- Köşe Kahve Pazartesi günleri kapalıdır, Pazartesi kasa dosyası olmaz." "- Para tutarlarını Türkçe biçimde yaz: 154.555,00 TL." > "$W/CLAUDE.md"
  PM=(); [ "$KOL" = plan ] && PM=(--permission-mode plan)
  EK=""; [ "$KOL" = sakla ] && EK=" Hesabı yapan betiği bu klasöre ozet.py adıyla kaydet. Gelecek ay yeni kasa dosyaları gelince ben tek komutla kendim çalıştıracağım."
  (cd "$W" && "${CC[@]}" "${PM[@]}" --tools "Read,Write,Edit,Glob,Grep,Bash" \
     --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Bash(python:*)" "Bash(python3:*)" "Bash(ls:*)" \
     --output-format stream-json --verbose \
     "$SORU Dosyalar bu klasörde, kasa/ altında. Sonucu rapor.md dosyasına da yaz.$EK" > "$D/ham/${KOL}_$N.jsonl" 2> "$D/ham/${KOL}_$N.err")
  mkdir -p "$D/ham/${KOL}_${N}_klasor"; cp "$W"/*.md "$W"/*.py "$D/ham/${KOL}_${N}_klasor/" 2>/dev/null || true
fi
T1=$(date +%s.%N); echo "$KOL $N $(python -c "print(round($T1-$T0,1))")" >> "$D/ham/sure.txt"
