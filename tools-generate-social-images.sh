#!/bin/bash
# Generate 1200x630 JPG social-share crops (og:image / twitter:image).
# JPG is used deliberately: LinkedIn and X do not reliably ingest WebP.
# Center-crop "cover" fit via sips (macOS built-in). Idempotent.
set -u
cd "$(dirname "$0")"
OUT="assets/img/social"; mkdir -p "$OUT" "$OUT/properties"
TW=1200; TH=630

crop() { # $1=src $2=dest
  local src="$1" dest="$2" w h
  [ -f "$src" ] || { echo "  !! source missing: $src"; return 1; }
  w=$(sips -g pixelWidth  "$src" 2>/dev/null | awk '/pixelWidth/{print $2}')
  h=$(sips -g pixelHeight "$src" 2>/dev/null | awk '/pixelHeight/{print $2}')
  [ -z "$w" ] && { echo "  !! unreadable: $src"; return 1; }
  local tmp="/tmp/ac-social-$$.jpg"
  sips -s format jpeg "$src" --out "$tmp" >/dev/null 2>&1 || return 1
  # scale so BOTH dimensions cover the target, then centre-crop
  if [ $(( w * TH )) -gt $(( h * TW )) ]; then
    sips --resampleHeight $TH "$tmp" >/dev/null 2>&1   # wider than target
  else
    sips --resampleWidth  $TW "$tmp" >/dev/null 2>&1   # taller than target
  fi
  sips -c $TH $TW "$tmp" >/dev/null 2>&1
  sips -s format jpeg -s formatOptions 80 "$tmp" --out "$dest" >/dev/null 2>&1
  rm -f "$tmp"
  echo "  $(basename "$dest")  <-  $(basename "$src")  [${w}x${h}]"
}

echo "== core pages =="
crop assets/img/hideaway.webp          "$OUT/home-1200x630.jpg"
crop assets/img/berryman-home.jpg      "$OUT/about-1200x630.jpg"
crop assets/img/gonzaga.webp           "$OUT/strategies-1200x630.jpg"
crop assets/img/villa-de-vistas.webp   "$OUT/luxury-redevelopment-1200x630.jpg"
crop assets/img/calvert-home.jpg       "$OUT/boutique-multifamily-1200x630.jpg"
crop assets/img/culver.webp            "$OUT/infill-subdivisions-1200x630.jpg"
crop assets/img/samo.webp              "$OUT/tic-housing-1200x630.jpg"
crop assets/img/85th.jpg               "$OUT/portfolio-1200x630.jpg"
crop assets/img/macapa-oasis-hd.jpg    "$OUT/track-record-1200x630.jpg"
crop assets/img/david.webp             "$OUT/insights-1200x630.jpg"
crop assets/img/june.webp              "$OUT/contact-1200x630.jpg"

echo "== property pages (each uses its own primary photo) =="
for d in assets/img/properties/*/; do
  slug=$(basename "$d")
  crop "${d}01.jpg" "$OUT/properties/${slug}-1200x630.jpg"
done
echo "done"
