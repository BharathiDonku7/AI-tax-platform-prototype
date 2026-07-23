# GreenGrowth CPAs — AI Engineer Case Study

**Challenges covered: 01 (Source Document Traceability), 08 (Clickable vs. Editable), 10 (Trustworthy AI).**

I picked these three because they share one data model. A return field that carries its
provenance, its confidence, and its state can drive all three challenges from a single source of
truth — which meant I could build one screen properly instead of ten screens thinly.

## Stack

Flask + Jinja2 + Tailwind + Alpine.js, matching the Python/Flask/PostgreSQL monolith described in
the role. No build step; `pip install flask && python app.py`.

## What is real vs. simulated

**Real (genuinely wired up):**
- The full click-through: selecting any field re-renders the document viewer, the highlight
  overlay, and the trust panel from a live API call.
- The state filter chips filter the field list.
- Correcting a value POSTs to the server, appends to the audit trail, flips the field to
  *Verified*, and updates the counts.
- Conflict resolution: choosing between two competing figures writes the decision and clears the
  conflict.
- Locked fields reject edits server-side with a 409 and an explanation.
- The queue ranking function orders fields by decision urgency.

**Simulated (fabricated, as the brief permits):**
- No OCR, no document parsing, no model inference. Every confidence score, bounding box, and AI
  rationale in `mock_data.py` is hand-authored.
- Source documents are rendered as placeholder pages with a positioned highlight rather than real
  PDFs. The bounding boxes are percentages so the overlay behaves correctly at any viewport.
- State lives in an in-memory dict and resets on restart. In production this is a Postgres table.
- No auth. The header shows a fixed preparer identity.

## Decisions worth explaining

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
viewer for a step-by-step derivation with each input linked to its own source. Pointing at a
single page would have been a lie about where the number came from.

**Locked fields always explain themselves.** A grayed-out field with no reason is a support ticket.
Each one says what to change instead.

**State is never encoded by color alone.** Every state carries a border, a chip, and a text label,
so the system survives grayscale printing — which happens whenever a return package goes to a
client meeting.

## Edge cases wired in

| Case | Field | What it demonstrates |
|---|---|---|
| Two documents disagree | Gross receipts (Ln 1a) | Conflict UI, forced resolution, no silent pick |
| Low-confidence extraction | Officer compensation (Ln 12) | Honest uncertainty with the *reason* for it |
| Multi-step derivation | Cost of goods sold (Ln 2) | Calculation chain, each step traced |
| Human already overrode AI | Rents (Ln 16) | Audit trail preserving the original suggestion |
| Uneditable derived value | 280E disallowed (Ln 26) | Locked state with an actionable explanation |

## Run locally

```bash
pip install flask
python app.py     # http://127.0.0.1:5000
```
