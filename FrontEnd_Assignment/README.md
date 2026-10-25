# Front-End Development — Graded Assignment (Weeks 1–6)

**Student Name:** AMMAN JAKHAR
**Student UID:** 2025EB01187
**Date of Birth:** 29.08.1986

This folder contains the full, original, line-by-line commented solution for both
questions plus the compiled final output document with the output screenshots
embedded.

## Final output document

- **`finaloutput.docx`** — the submission document. It contains the cover details,
  Question 1 (output screenshot + commented `IDCard.html` and `IDCard_styles.css`)
  and Question 2 (form screenshot, console screenshot, and commented
  `StudentApp.html` and `StudentApp.js`).

> The assignment names the file `finaloutput.doc`. It is provided here as
> `finaloutput.docx` because it is a modern Word (OOXML) document; it opens
> directly in Microsoft Word / Google Docs / LibreOffice. Rename to `.doc`
> only if your portal strictly requires that extension.

## Question 1 — Student ID Card

| File | Purpose |
|------|---------|
| `IDCard.html` | HTML structure of the student ID card. Tab title = `2025EB01187`. |
| `IDCard_styles.css` | External stylesheet that paints the card. |

## Question 2 — Student ID Card Application

| File | Purpose |
|------|---------|
| `StudentApp.html` | The application form page. Tab title = `2025EB01187`. |
| `StudentApp.js` | Five field validations, a `Student` class logged with `console.log`, and cookie save/read helpers. |

## Screenshots

| File | Shows |
|------|-------|
| `screenshots/q1_idcard.png` | `IDCard.html` rendered (tab shows `2025EB01187`). |
| `screenshots/q2_form.png` | The form after a valid submission. |
| `screenshots/q2_console.png` | Console with the `Student` object and the stored cookie. |

## Rebuilding the document

`build_finaloutput.py` regenerates `finaloutput.docx` from the four source files
and the three screenshots using only the Python standard library:

```bash
python3 build_finaloutput.py
```

All work in this folder is original and was written for this submission.
