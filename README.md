# GreenGrowth CPAs — AI Engineer Case Study

**Challenges covered: 01 (Source Document Traceability), 08 (Clickable vs. Editable), 10 (Trustworthy AI).**

I picked these three because they share one data model. A return field that carries its
provenance, its confidence, and its state can drive all three challenges from a single source of
truth — which meant building one screen properly instead of ten screens thinly.

## Stack

Flask + Jinja2 + Tailwind + Alpine.js, matching the Python/Flask/PostgreSQL monolith described in
the role. No build step: `pip install -r requirements.txt && python app.py`.

## Scale

32 return fields across three sections, 11 source documents, 21 authored document pages.
Enough volume that search, filtering, and the review queue are doing real work rather than
decorating six demo rows.

## What is real vs. simulated

**Real (genuinely wired up):**
- Selecting any field loads it over the API, renders its source document page, and scrolls the
  highlighted row into view.
- Page navigation: prev/next across every page of a document, plus "back to source" when you've
  navigated away from the page the value came from.
- Derivation chains are clickable — each input step opens its own source document and page.
- Evidence items are clickable and navigate to the cited page.
- Conflict resolution writes the decision, clears the conflict, and updates the open-item count.
- Accept-as-verified and manual correction both POST, mutate state, and re-render without a reload.
- Locked fields reject edits server-side with a 409 and an explanation.
- Search filters the field list; state chips filter by state.

**Simulated (fabricated, as the brief permits):**
- No OCR, no document parsing, no model inference. Every confidence score, document row, and AI
  rationale in `mock_data.py` is hand-authored.
- Documents are rendered from structured row data rather than real PDFs. Pages that weren't
  authored say so explicitly instead of showing invented content.
- State lives in an in-memory dict and resets on restart. In production this is a Postgres table.
- No auth. The header shows a fixed preparer identity.

## Decisions worth explaining

**Traceability is row-level, not coordinate-level.** A field points at a document, a page, and a
specific row ID; the viewer renders that page's real content and highlights the row. Bounding
boxes over a scanned image break the moment the document is re-rendered at a different size. A
row reference survives it, and it's what a real extraction pipeline would emit anyway.

**The sample return is a cannabis dispensary with Sec. 280E exposure.** 280E disallows every
deduction except cost of goods sold, which makes COGS allocation the single highest-stakes number
on the return and the one most likely to be challenged. That makes it the honest test case for a
traceability interface, and it reflects GreenGrowth's actual client base.

**Confidence is shown as a band, not a decimal.** The panel leads with "Low confidence" and shows
the percentage in muted secondary text. A raw score like 0.6134 implies a precision the model
doesn't have, and reviewers anchor hard on numbers.

**Correcting the AI never erases it.** The original suggestion, the correction, the reason, and the
reviewer all stay in the record. The Rents field ships with an override already applied, so the
audit trail is visible without having to trigger one. Under audit, that history *is* the
substantiation.

**Derived fields show a chain, not a document.** Clicking a calculated field swaps the document
viewer for a step-by-step derivation, and each step is itself clickable back to its own source
page. Pointing a derived value at a single page would have been a lie about where it came from.

**Unindexed pages say so.** The lease has 12 pages; two were authored. Page 9 renders "not indexed
in this prototype" with links to the pages that do exist. Showing the seam is better than faking it.

**Accepting is one click; correcting asks for a reason.** A preparer confirming a high-confidence
extraction two hundred times a day shouldn't have to open a dialog. The rarer, higher-stakes
action is the one that demands justification.

**State is never encoded by color alone.** Every state carries a border, a chip, and a text label,
so the system survives grayscale printing — which happens whenever a return package goes to a
client meeting.

## Edge cases wired in

| Case | Field | What it demonstrates |
|---|---|---|
| Two documents disagree | Gross receipts (Ln 1a) | Conflict UI, forced resolution, no silent pick |
| Judgment call flagged for approval | Taxes and licenses (Ln 17) | AI excluded $1.68M of excise tax and says why |
| Low-confidence extraction | Officer compensation (Ln 12) | Honest uncertainty *with the reason for it* |
| Unexplained aggregate | Miscellaneous (Ln 26i) | AI flags an audit risk rather than just extracting |
| Multi-step derivation | Cost of goods sold (Ln 2) | Five inputs, each clickable to its own source |
| Human already overrode AI | Rents (Ln 16) | Audit trail preserving the original suggestion |
| Uneditable derived value | Sec. 280E disallowed, Total tax | Locked state with an actionable explanation |
| Document page not authored | Lease pages 1–3, 5–6, 8–12 | Prototype seams shown honestly |

## Run locally

```bash
pip install -r requirements.txt
python app.py     # http://127.0.0.1:5000
```
