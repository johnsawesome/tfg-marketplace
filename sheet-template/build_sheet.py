"""Build the Topic Marketplace Google Sheet template (as .xlsx for import)."""
import sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1]

NAVY, ORANGE, TEAL, GREEN = "00355F", "E37F1C", "5B9B98", "82A52C"
PLACEHOLDER = "FFF4C2"
OVER = "F4C7C3"

# Soft limits (warning, not reject). Themes are what the projector shows: with per-card fit,
# last year's themes (up to ~135 chars) land at ~22px at 1080p. Context only shows when a card
# is tapped, so its limit is just a sanity check.
LIMITS = {"B": 110, "C": 300, "D": 110, "E": 300, "F": 60}

# HGI Riverwatch spaces as in the live Sheet 2026-10-12. "- 1"/"- 2" = two conversations in one room;
# the display merges them into one split card. Group puts rooms under a shared label.
B, M = "Ballroom", "Meeting rooms"
ROOMS = [("Canal - 1", B), ("Canal - 2", B), ("Millpond - 1", B), ("Millpond - 2", B),
         ("Great Falls - 1", B), ("Great Falls - 2", B), ("Rotunda", B), ("Board Room", M),
         ("Room 415", M), ("Room 515", M), ("Room 520", M), ("Room 615", M), ("Room 620", M)]
SPARE_ROWS = 7  # formatted and length-checked, left blank (blank Room = skipped by the display)

wb = Workbook()
ws = wb.active
ws.title = "Display"  # the display page reads this tab by name

headers = ["Room", "AM theme", "AM context", "PM theme", "PM context", "Note", "Group"]
fills = [NAVY, TEAL, TEAL, ORANGE, ORANGE, GREEN, TEAL]
widths = [20, 42, 55, 42, 55, 32, 18]
thin = Side(style="thin", color="C9D3DC")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap_top = Alignment(wrap_text=True, vertical="top")

for i, (h, f, w) in enumerate(zip(headers, fills, widths), start=1):
    c = ws.cell(row=1, column=i, value=h)
    c.font = Font(bold=True, color="FFFFFF", size=11)
    c.fill = PatternFill("solid", fgColor=f)
    c.alignment = Alignment(vertical="center", wrap_text=True)
    c.border = border
    ws.column_dimensions[c.column_letter].width = w
ws.row_dimensions[1].height = 24

last = len(ROOMS) + SPARE_ROWS + 1
for r, (room, group) in enumerate(ROOMS + [(None, None)] * SPARE_ROWS, start=2):
    a = ws.cell(row=r, column=1, value=room)
    a.font = Font(bold=True, color=NAVY)
    a.alignment = wrap_top
    a.border = border
    if room and "TBD" in room:
        a.fill = PatternFill("solid", fgColor=PLACEHOLDER)
    for col in range(2, 8):
        c = ws.cell(row=r, column=col)
        c.alignment = wrap_top
        c.border = border
    ws.cell(row=r, column=7, value=group)
    ws.row_dimensions[r].height = 48

ws.freeze_panes = "B2"

# Length checks: warning-style validation + red fill when over.
for col, n in LIMITS.items():
    rng = f"{col}2:{col}{last}"
    dv = DataValidation(
        type="custom",
        formula1=f"LEN({col}2)<={n}",
        allow_blank=True,
        showErrorMessage=True,
        errorStyle="warning",
        errorTitle="Long for the projector",
        error=f"Over {n} characters. It will still show, but text shrinks for every room. Shorten if you can.",
        showInputMessage=True,
        promptTitle=f"Up to ~{n} characters",
        prompt="Context: shows when someone taps the card, not on the projector. One line per bullet (Ctrl+Enter or Alt+Enter)." if col in "CE"
        else ("Fills the whole card if both themes are blank (e.g. Reset Room: open all day)." if col == "F"
              else "Keep it short; it's read from the back of the room."),
    )
    dv.add(rng)
    ws.add_data_validation(dv)
    ws.conditional_formatting.add(
        rng, FormulaRule(formula=[f"LEN({col}2)>{n}"], fill=PatternFill("solid", fgColor=OVER))
    )

# ---------------- Instructions tab ----------------
ins = wb.create_sheet("How to use")
ins.column_dimensions["A"].width = 110
lines = [
    ("Topic Marketplace: room sheet", "title"),
    ("The display page reads the 'Display' tab every ~3 seconds and shows one card per room, in row order. Attendees can open the same page on their phones via the QR code.", None),
    ("", None),
    ("Setup (once)", "h"),
    ("1. Upload this file to Google Drive, open it, then File > Save as Google Sheets. Work in the Google copy.", None),
    ("2. Share > General access > Anyone with the link > Viewer. (Topic text only; never put attendee names here.)", None),
    ("3. Copy the Sheet ID: the long string between /d/ and /edit in the URL. It goes into CONFIG.SHEET_ID on the display page.", None),
    ("4. Give edit access to the staff who will type on the day.", None),
    ("", None),
    ("Rules the display depends on", "h"),
    ("- Keep the tab named 'Display' and keep the header row and column order (Room, AM theme, AM context, PM theme, PM context, Note, Group).", None),
    ("- Row order is display order. Reorder rooms by moving rows; the layout picks whatever row arrangement gives the largest text.", None),
    ("- Two conversations in one room: name the rows '<Room> - 1' and '<Room> - 2' (e.g. Canal - 1, Canal - 2). They share one card, split in half.", None),
    ("- Group: rooms with the same Group (e.g. Ballroom, Meeting rooms) sit together under that label. Leave Group blank everywhere for no grouping.", None),
    ("- Keep room names short (e.g. Canal - 1) so each name fits on one line of its card header.", None),
    ("- A row with a blank Room is skipped, so you can leave spare rows at the bottom.", None),
    ("", None),
    ("Typing on the day", "h"),
    ("- Theme: the topic title; this is what the projector shows. Context: optional supporting lines, shown only when someone taps the card on a phone or laptop (one line per bullet: Ctrl+Enter or Alt+Enter). Cards with context get a small More tag.", None),
    ("- Blank theme shows 'Topic coming soon', so unfilled rooms look intentional.", None),
    ("- Note: if both themes are blank, the Note fills the card (e.g. 'Reset Room: open all day', 'Not in use'). Otherwise it shows as a small line under the topics.", None),
    ("- Red cell = over the soft length limit. It still displays, but that card's text shrinks to fit, so shorten if you can.", None),
    (f"  Limits: themes {LIMITS['B']}, note {LIMITS['F']} characters (projector); context {LIMITS['C']} (tap-to-view only). Each card sizes its own text; only the wordiest cards shrink.", None),
    ("- The projector laptop never opens this Sheet; type from a second device.", None),
]
for i, (text, kind) in enumerate(lines, start=1):
    c = ins.cell(row=i, column=1, value=text)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if kind == "title":
        c.font = Font(bold=True, size=14, color=NAVY)
    elif kind == "h":
        c.font = Font(bold=True, size=11, color=ORANGE)

wb.active = 0
wb.save(OUT)
print("wrote", OUT)
