#!/bin/bash
# Resize and re-encode above-the-fold imagery.
# Heroes are full-bleed CSS backgrounds; 1920px is ample and the originals
# were up to 2500px. Format is preserved (webp stays webp) because WebP
# already out-compresses JPEG for this content.
set -u
cd "$(dirname "$0")"
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
MAXW=1920; Q=80
before=0; after=0; n=0
tmp=$(mktemp -d)

while IFS= read -r f; do
  ext="${f##*.}"; b=$(stat -f%z "$f")
  case "$ext" in webp) fmt=webp;; jpg|jpeg) fmt=jpeg;; png) fmt=png;; *) continue;; esac
  rm -rf "$tmp"/*; mkdir -p "$tmp"
  npx --yes sharp-cli -i "$PWD/$f" -o "$tmp" \
      resize $MAXW --withoutEnlargement -f $fmt -q $Q >/dev/null 2>&1 || { echo "  skip (encode failed): $f"; continue; }
  out="$tmp/$(basename "$f")"
  [ -f "$out" ] || { echo "  skip (no output): $f"; continue; }
  a=$(stat -f%z "$out")
  if [ "$a" -lt "$b" ]; then
    cp "$out" "$f"; before=$((before+b)); after=$((after+a)); n=$((n+1))
    printf "  %6.0fKB -> %6.0fKB  %s\n" $((b/1024)) $((a/1024)) "$(basename "$f")"
  else
    echo "  kept original (re-encode was larger): $(basename "$f")"
  fi
done < <(find assets/img -maxdepth 1 -type f \( -name "*.webp" -o -name "*.jpg" -o -name "*.png" \) -size +250k | sort)

rm -rf "$tmp"
echo
printf "optimized %d files: %.1fMB -> %.1fMB (%d%% smaller)\n" \
  "$n" "$(echo "$before/1048576"|bc -l)" "$(echo "$after/1048576"|bc -l)" \
  $(( before>0 ? (before-after)*100/before : 0 ))
