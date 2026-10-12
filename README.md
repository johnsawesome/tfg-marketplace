# TFG Topic Marketplace display

Live breakout-room board for Together for Good 2026 (Thu 2026-11-19). Staff type topics into a Google
Sheet; `index.html` polls it every ~3s and shows one TFG-branded card per room.

- **Live page:** https://johnsawesome.github.io/tfg-marketplace/
- **Data:** Google Sheet `1Iykh5KMN1ZIvUTDodyzPvrXzGKMAu1NVQcG4JtWa_F0`, tab `Display` (shared anyone-with-link Viewer; topic text only, no attendee data)
- **Sheet template:** `sheet-template/` (`build_sheet.py` regenerates the .xlsx)

Keys: **F** fullscreen. With `CONFIG.SHEET_ID` empty the page runs on sample data and **E** edits it.
If the network drops, the page keeps the last good data and the status line turns red.
