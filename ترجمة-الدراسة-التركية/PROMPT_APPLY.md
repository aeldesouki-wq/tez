You apply referee (hakem) findings to the Turkish translation. Working dir: /tmp/claude-0/-home-user-tez/74fd3fef-0066-53e0-a55d-60db26a4e415/scratchpad
Read DECISIONS_FINAL.md (binding, overrides referees and STYLE_GUIDE where they conflict), STYLE_GUIDE.md, GLOSSARY.md.
Your files: tr/chunk_{IDS}.md (edit in place with Edit), Arabic chunks/chunk_{IDS}.md (verify every change against the Arabic before applying). Referee reports: {REPORTS} (in hakem/).
For each finding decide and apply. Never add meaning, never drop meaning; footnote numbers unchanged; keep NOTLAR blocks (update entries that became inconsistent). Then append your decisions to hakem/UYGULAMA_{TAG}.md: one line per finding: "rapor#bulgu → uygulandı / kısmen / uygulanmadı — gerekçe".
Finally run: grep -c '\[\^' on each file and confirm footnote reference/definition pairs are intact (python check: each [^N] appears exactly twice). Final reply ≤6 lines.
