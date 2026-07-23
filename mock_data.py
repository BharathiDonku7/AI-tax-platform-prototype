"""
Mock data layer for the GreenGrowth CPAs AI Engineer case study.

EVERYTHING IN THIS FILE IS FABRICATED.
No OCR, no document parsing, no model inference happens anywhere in this app.
Confidence scores, bounding boxes, and AI rationales are hand-authored to
exercise the interface against realistic edge cases.

The sample return is a cannabis dispensary (Sec. 280E exposure) because that
is GreenGrowth's core client profile, and 280E is precisely where
"trace this number back to its source" carries audit consequences.
"""

# ---------------------------------------------------------------------------
# SOURCE DOCUMENTS
# Each doc has pages; each page has a rendered placeholder and text regions.
# bbox values are percentages (x, y, w, h) so the overlay scales with any
# viewport without needing real image dimensions.
# ---------------------------------------------------------------------------

DOCUMENTS = {
    "doc_pl_2025": {
        "id": "doc_pl_2025",
        "name": "Profit & Loss Statement FY2025.pdf",
        "kind": "Financial Statement",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-14",
        "pages": 3,
        "page_titles": {
            1: "Revenue Summary",
            2: "Cost of Goods Sold",
            3: "Operating Expenses",
        },
    },
    "doc_pos_export": {
        "id": "doc_pos_export",
        "name": "POS System Export - Gross Sales.csv",
        "kind": "System Export",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-14",
        "pages": 1,
        "page_titles": {1: "Transaction Totals by Month"},
    },
    "doc_inventory": {
        "id": "doc_inventory",
        "name": "Inventory Valuation Report 12-31-2025.pdf",
        "kind": "Inventory Report",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-16",
        "pages": 2,
        "page_titles": {1: "Ending Inventory Detail", 2: "Valuation Method Notes"},
    },
    "doc_payroll": {
        "id": "doc_payroll",
        "name": "Payroll Register Q1-Q4 2025.pdf",
        "kind": "Payroll Record",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-18",
        "pages": 4,
        "page_titles": {
            1: "Q1 Summary",
            2: "Q2 Summary",
            3: "Q3 Summary",
            4: "Annual Totals by Department",
        },
    },
    "doc_lease": {
        "id": "doc_lease",
        "name": "Commercial Lease Agreement.pdf",
        "kind": "Legal Agreement",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-11",
        "pages": 12,
        "page_titles": {4: "Rent Schedule", 7: "Square Footage & Use Clauses"},
    },
    "doc_bank_stmt": {
        "id": "doc_bank_stmt",
        "name": "Operating Account Statements 2025.pdf",
        "kind": "Bank Statement",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-20",
        "pages": 24,
        "page_titles": {23: "December Activity", 24: "Year-End Summary"},
    },
}


# ---------------------------------------------------------------------------
# RETURN FIELDS
# The single model that powers all three challenges:
#   01 - source_doc/page/bbox/transformation give traceability
#   08 - state gives the affordance system
#   10 - confidence/rationale/evidence/conflicts give the trust layer
# ---------------------------------------------------------------------------

FIELDS = [
    # ---- Gross Receipts: the conflict case -------------------------------
    {
        "id": "f_gross_receipts",
        "form": "Form 1120",
        "line": "1a",
        "label": "Gross receipts or sales",
        "value": 4_827_400.00,
        "source_type": "extracted",
        "state": "needs_approval",
        "confidence": 0.71,
        "source_doc": "doc_pos_export",
        "page": 1,
        "bbox": {"x": 8, "y": 62, "w": 84, "h": 7},
        "source_excerpt": "TOTAL GROSS SALES (Jan-Dec 2025) ......... 4,827,400.00",
        "transformation": None,
        "ai_rationale": (
            "Pulled the annual gross sales total directly from the POS export. "
            "Flagged for approval because the P&L statement reports a different "
            "figure for the same period."
        ),
        "evidence": [
            {"doc": "doc_pos_export", "page": 1, "note": "POS annual total: $4,827,400"},
            {"doc": "doc_pl_2025", "page": 1, "note": "P&L revenue line: $4,791,220"},
        ],
        "conflicts": [
            {
                "competing_value": 4_791_220.00,
                "competing_doc": "doc_pl_2025",
                "competing_page": 1,
                "delta": 36_180.00,
                "explanation": (
                    "The POS export exceeds the P&L by $36,180. Common causes are "
                    "returns and voids recorded in the POS but netted out on the P&L, "
                    "or December transactions posted after the P&L close date. "
                    "Resolution requires client confirmation."
                ),
            }
        ],
        "override_history": [],
        "lock_reason": None,
    },
    # ---- COGS: the 280E-critical calculated field ------------------------
    {
        "id": "f_cogs",
        "form": "Form 1120",
        "line": "2",
        "label": "Cost of goods sold",
        "value": 2_913_650.00,
        "source_type": "calculated",
        "state": "ai_suggested",
        "confidence": 0.88,
        "source_doc": None,
        "page": None,
        "bbox": None,
        "source_excerpt": None,
        "transformation": {
            "formula": "Beginning Inventory + Purchases + Direct Labor + Allocated Indirect - Ending Inventory",
            "steps": [
                {"label": "Beginning inventory (01/01/2025)", "value": 412_800.00,
                 "doc": "doc_inventory", "page": 1},
                {"label": "Product purchases", "value": 2_640_100.00,
                 "doc": "doc_pl_2025", "page": 2},
                {"label": "Direct production labor", "value": 318_400.00,
                 "doc": "doc_payroll", "page": 4},
                {"label": "Allocated indirect costs (Sec. 471)", "value": 29_150.00,
                 "doc": "doc_pl_2025", "page": 2},
                {"label": "Ending inventory (12/31/2025)", "value": -486_800.00,
                 "doc": "doc_inventory", "page": 1},
            ],
        },
        "ai_rationale": (
            "Computed under Sec. 471 inventory rules. Only costs allocable to "
            "inventory are included; selling and administrative costs are excluded "
            "because Sec. 280E disallows them as deductions for this taxpayer."
        ),
        "evidence": [
            {"doc": "doc_inventory", "page": 2, "note": "Client uses FIFO; method documented"},
            {"doc": "doc_payroll", "page": 4, "note": "Production dept. wages isolated from retail"},
        ],
        "conflicts": [],
        "override_history": [],
        "lock_reason": None,
    },
    # ---- The low-confidence extraction -----------------------------------
    {
        "id": "f_officer_comp",
        "form": "Form 1120",
        "line": "12",
        "label": "Compensation of officers",
        "value": 185_000.00,
        "source_type": "extracted",
        "state": "ai_suggested",
        "confidence": 0.61,
        "source_doc": "doc_payroll",
        "page": 4,
        "bbox": {"x": 10, "y": 44, "w": 78, "h": 6},
        "source_excerpt": "OFFICER / EXEC COMP .......... 185,000.00  (see dept. note)",
        "transformation": None,
        "ai_rationale": (
            "Extracted from the annual payroll totals. Confidence is low: the "
            "payroll register groups officer compensation with an 'EXEC' department "
            "code that also contains two non-officer salaries. The figure may be "
            "overstated."
        ),
        "evidence": [
            {"doc": "doc_payroll", "page": 4, "note": "Dept. code EXEC contains 3 employees"},
        ],
        "conflicts": [],
        "override_history": [],
        "lock_reason": None,
    },
    # ---- A field a human already corrected -------------------------------
    {
        "id": "f_rent",
        "form": "Form 1120",
        "line": "16",
        "label": "Rents",
        "value": 288_000.00,
        "source_type": "manual",
        "state": "verified",
        "confidence": None,
        "source_doc": "doc_lease",
        "page": 4,
        "bbox": {"x": 12, "y": 30, "w": 76, "h": 10},
        "source_excerpt": "Base rent: $24,000/month commencing 01/01/2025, escalating 3% annually",
        "transformation": {
            "formula": "Monthly base rent x 12 months",
            "steps": [
                {"label": "Monthly base rent", "value": 24_000.00,
                 "doc": "doc_lease", "page": 4},
                {"label": "Months in tax year", "value": 12, "doc": None, "page": None},
            ],
        },
        "ai_rationale": (
            "Originally suggested $296,640 by applying the 3% escalation clause. "
            "Reviewer determined the escalation begins in year two, so FY2025 uses "
            "flat base rent."
        ),
        "evidence": [
            {"doc": "doc_lease", "page": 4, "note": "Escalation clause reads 'commencing on the first anniversary'"},
            {"doc": "doc_bank_stmt", "page": 24, "note": "12 rent payments of $24,000 confirmed"},
        ],
        "conflicts": [],
        "override_history": [
            {
                "from": 296_640.00,
                "to": 288_000.00,
                "by": "M. Reyes, CPA",
                "at": "2026-02-03 14:22",
                "reason": "Escalation clause applies from year two, not year one. "
                          "Bank statements confirm 12 payments at $24,000.",
            }
        ],
        "lock_reason": None,
    },
    # ---- The locked field ------------------------------------------------
    {
        "id": "f_280e_disallowed",
        "form": "Form 1120",
        "line": "26 (adj)",
        "label": "Sec. 280E disallowed deductions",
        "value": 641_900.00,
        "source_type": "calculated",
        "state": "locked",
        "confidence": None,
        "source_doc": None,
        "page": None,
        "bbox": None,
        "source_excerpt": None,
        "transformation": {
            "formula": "Total operating expenses - Sec. 471 allocable costs",
            "steps": [
                {"label": "Total operating expenses", "value": 671_050.00,
                 "doc": "doc_pl_2025", "page": 3},
                {"label": "Reclassified to COGS (Sec. 471)", "value": -29_150.00,
                 "doc": "doc_pl_2025", "page": 2},
            ],
        },
        "ai_rationale": (
            "Sec. 280E disallows all deductions other than cost of goods sold for "
            "businesses trafficking in controlled substances. This figure is derived "
            "from other fields on the return and cannot be edited directly."
        ),
        "evidence": [
            {"doc": "doc_pl_2025", "page": 3, "note": "Operating expense detail"},
        ],
        "conflicts": [],
        "override_history": [],
        "lock_reason": (
            "Derived field. Change the underlying operating expense or COGS "
            "allocation to affect this value."
        ),
    },
    # ---- Straightforward verified extractions ----------------------------
    {
        "id": "f_salaries",
        "form": "Form 1120",
        "line": "13",
        "label": "Salaries and wages (less employment credits)",
        "value": 704_200.00,
        "source_type": "extracted",
        "state": "verified",
        "confidence": 0.96,
        "source_doc": "doc_payroll",
        "page": 4,
        "bbox": {"x": 10, "y": 52, "w": 78, "h": 6},
        "source_excerpt": "TOTAL WAGES - NON-PRODUCTION .......... 704,200.00",
        "transformation": None,
        "ai_rationale": (
            "Extracted from annual payroll totals, excluding the $318,400 in "
            "production labor already captured in cost of goods sold."
        ),
        "evidence": [
            {"doc": "doc_payroll", "page": 4, "note": "Non-production wage total"},
        ],
        "conflicts": [],
        "override_history": [],
        "lock_reason": None,
    },
    {
        "id": "f_interest",
        "form": "Form 1120",
        "line": "18",
        "label": "Interest expense",
        "value": 47_300.00,
        "source_type": "extracted",
        "state": "editable",
        "confidence": 0.93,
        "source_doc": "doc_bank_stmt",
        "page": 24,
        "bbox": {"x": 14, "y": 71, "w": 72, "h": 5},
        "source_excerpt": "Total interest charged YTD .......... 47,300.00",
        "transformation": None,
        "ai_rationale": "Extracted from the year-end bank summary.",
        "evidence": [
            {"doc": "doc_bank_stmt", "page": 24, "note": "Year-end interest total"},
        ],
        "conflicts": [],
        "override_history": [],
        "lock_reason": None,
    },
    {
        "id": "f_depreciation",
        "form": "Form 1120",
        "line": "20",
        "label": "Depreciation",
        "value": 96_450.00,
        "source_type": "extracted",
        "state": "ai_suggested",
        "confidence": 0.84,
        "source_doc": "doc_pl_2025",
        "page": 3,
        "bbox": {"x": 12, "y": 38, "w": 74, "h": 6},
        "source_excerpt": "Depreciation & amortization .......... 96,450.00",
        "transformation": None,
        "ai_rationale": (
            "Extracted from the operating expense section. Note that the P&L "
            "combines depreciation and amortization on a single line; if the client "
            "has amortizable intangibles, this figure needs to be split."
        ),
        "evidence": [
            {"doc": "doc_pl_2025", "page": 3, "note": "Combined D&A line item"},
        ],
        "conflicts": [],
        "override_history": [],
        "lock_reason": None,
    },
]


# ---------------------------------------------------------------------------
# AFFORDANCE SYSTEM (Challenge 08)
# One definition, consumed by every screen so the visual language cannot drift.
# ---------------------------------------------------------------------------

STATES = {
    "ai_suggested": {
        "label": "AI suggested",
        "meaning": "Generated by AI. Not yet reviewed by a human.",
        "editable": True,
        "border": "border-l-4 border-amber-400",
        "chip_bg": "bg-amber-50 text-amber-800 ring-amber-200",
        "icon": "sparkle",
    },
    "needs_approval": {
        "label": "Needs approval",
        "meaning": "AI found a conflict it cannot resolve. Requires a decision.",
        "editable": True,
        "border": "border-l-4 border-rose-400",
        "chip_bg": "bg-rose-50 text-rose-800 ring-rose-200",
        "icon": "alert",
    },
    "verified": {
        "label": "Verified",
        "meaning": "Reviewed and confirmed by a human preparer.",
        "editable": True,
        "border": "border-l-4 border-emerald-400",
        "chip_bg": "bg-emerald-50 text-emerald-800 ring-emerald-200",
        "icon": "check",
    },
    "editable": {
        "label": "Editable",
        "meaning": "Standard field. Extracted with high confidence, open to edit.",
        "editable": True,
        "border": "border-l-4 border-slate-200",
        "chip_bg": "bg-slate-50 text-slate-600 ring-slate-200",
        "icon": "pencil",
    },
    "locked": {
        "label": "Locked",
        "meaning": "Derived from other fields. Cannot be edited directly.",
        "editable": False,
        "border": "border-l-4 border-slate-400",
        "chip_bg": "bg-slate-100 text-slate-700 ring-slate-300",
        "icon": "lock",
    },
}


def confidence_band(c):
    """Map a raw score to a band. Deliberately coarse: exposing '0.6134' to a
    CPA implies a precision the model does not have."""
    if c is None:
        return None
    if c >= 0.90:
        return {"key": "high", "label": "High confidence",
                "cls": "text-emerald-700 bg-emerald-50 ring-emerald-200"}
    if c >= 0.75:
        return {"key": "medium", "label": "Medium confidence",
                "cls": "text-amber-700 bg-amber-50 ring-amber-200"}
    return {"key": "low", "label": "Low confidence",
            "cls": "text-rose-700 bg-rose-50 ring-rose-200"}


def get_field(field_id):
    return next((f for f in FIELDS if f["id"] == field_id), None)


def review_queue():
    """Ranking stub (the 'small script that fakes the logic' the brief allows).
    Orders by decision urgency, not by form line number."""
    priority = {"needs_approval": 0, "ai_suggested": 1, "editable": 2,
                "verified": 3, "locked": 4}
    return sorted(
        FIELDS,
        key=lambda f: (priority[f["state"]],
                       f["confidence"] if f["confidence"] is not None else 1.0),
    )


def summary_counts():
    counts = {k: 0 for k in STATES}
    for f in FIELDS:
        counts[f["state"]] += 1
    return counts
