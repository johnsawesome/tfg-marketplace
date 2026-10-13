# TFG Topic Marketplace display

Live breakout-room board for Together for Good 2026 (Thu 2026-11-19). Staff type topics into a Google
Sheet; `index.html` polls it every ~3s and shows one TFG-branded card per room.

- **Live page:** https://johnsawesome.github.io/tfg-marketplace/
- **Data:** Google Sheet `1Iykh5KMN1ZIvUTDodyzPvrXzGKMAu1NVQcG4JtWa_F0`, tab `Display` (shared anyone-with-link Viewer; topic text only, no attendee data)
- **Sheet template:** `sheet-template/` (`build_sheet.py` regenerates the .xlsx)
- **Assets:** `make_assets.py` rebuilds `logo.png` (from `Together_For_Good_2026_Logo.png`) and `qr.svg`. The QR points at the MANP redirect https://www.nonprofitmaine.org/tfg-topics, so if the page moves, update the redirect, not the QR.

Two layouts from one page:
- **Projector** (wide screens): everything fits one screen; themes only. Groups sit side by side (Ballroom | Meeting rooms) so every card is the same size; `CONFIG.LAYOUT` switches to `"stacked"` or `"auto"`. **F** toggles fullscreen.
- **Phone** (narrow or portrait): scrolling list grouped by area. Reached via the header QR code.

On both, clicking or tapping a card opens its details (context lines). If the network drops, the page keeps
the last good data and the status line turns red.
