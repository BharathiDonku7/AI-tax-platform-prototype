"""
Mock data layer for the GreenGrowth CPAs AI Engineer case study.

EVERYTHING IN THIS FILE IS FABRICATED.
No OCR, no document parsing, no model inference happens anywhere in this app.
Confidence scores, document content, and AI rationales are hand-authored to
exercise the interface against realistic edge cases and realistic volume.

Traceability model: a return field points at a document, a page, and a specific
ROW ID on that page. The viewer renders the page's real rows and highlights the
one the field came from. That is a stronger claim than a coordinate overlay --
the link survives the document being re-rendered at any size.

The sample return is a cannabis dispensary (Sec. 280E exposure) because that is
GreenGrowth's core client profile, and 280E is precisely where "trace this
number back to its source" carries audit consequences.
"""


def _r(rid, label, amount=None, kind="line", cols=None):
    return {"id": rid, "label": label, "amount": amount, "kind": kind, "cols": cols}


# ---------------------------------------------------------------------------
# DOCUMENT CONTENT
#
# layout: statement (label/amount) | table (columnar) | legal (prose) | ledger
# kind:   header | line | subtotal | total | note | blank
# ---------------------------------------------------------------------------

DOCUMENTS = {
    "doc_pl_2025": {
        "id": "doc_pl_2025",
        "short": "P&L statement",
        "name": "Profit & Loss Statement FY2025.pdf",
        "kind": "Financial Statement",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-14",
        "page_count": 3,
        "pages": {
            1: {
                "title": "Revenue Summary",
                "layout": "statement",
                "subtitle": "Verdant Retail Holdings, LLC — Year Ended December 31, 2025",
                "rows": [
                    _r("pl1_h1", "REVENUE", kind="header"),
                    _r("pl1_flower", "Flower & pre-roll sales", 2_914_880.00),
                    _r("pl1_concentrate", "Concentrate & extract sales", 1_106_400.00),
                    _r("pl1_edible", "Edible & beverage sales", 588_140.00),
                    _r("pl1_access", "Accessories & non-cannabis retail", 181_800.00),
                    _r("pl1_gross", "Total gross revenue", 4_791_220.00, kind="subtotal"),
                    _r("", "", kind="blank"),
                    _r("pl1_returns", "Less: returns and allowances", -18_640.00),
                    _r("pl1_disc", "Less: promotional discounts", -62_310.00),
                    _r("pl1_net", "Net revenue", 4_710_270.00, kind="total"),
                    _r("", "", kind="blank"),
                    _r("pl1_note",
                       "Note: revenue recognized at point of sale. Excise tax collected "
                       "on behalf of the state is presented net and excluded above.",
                       kind="note"),
                ],
            },
            2: {
                "title": "Cost of Goods Sold",
                "layout": "statement",
                "subtitle": "Sec. 471 allocable costs",
                "rows": [
                    _r("pl2_h1", "COST OF GOODS SOLD", kind="header"),
                    _r("pl2_purch", "Product purchases — licensed cultivators", 2_402_600.00),
                    _r("pl2_purch2", "Product purchases — licensed manufacturers", 237_500.00),
                    _r("pl2_purchtot", "Total product purchases", 2_640_100.00, kind="subtotal"),
                    _r("", "", kind="blank"),
                    _r("pl2_freight", "Inbound freight & transfer costs", 18_400.00),
                    _r("pl2_qa", "Compliance testing & quality assurance", 10_750.00),
                    _r("pl2_indirect", "Total Sec. 471 allocable indirect costs",
                       29_150.00, kind="subtotal"),
                    _r("", "", kind="blank"),
                    _r("pl2_note",
                       "Note: allocation methodology per Sec. 471 and Reg. 1.471-11. "
                       "Selling and administrative costs are excluded and reported "
                       "separately on page 3.",
                       kind="note"),
                ],
            },
            3: {
                "title": "Operating Expenses",
                "layout": "statement",
                "subtitle": "Costs subject to Sec. 280E disallowance analysis",
                "rows": [
                    _r("pl3_h1", "OPERATING EXPENSES", kind="header"),
                    _r("pl3_salaries", "Salaries & wages — retail and administrative", 704_200.00),
                    _r("pl3_officer", "Officer compensation", 185_000.00),
                    _r("pl3_benefits", "Employee benefit programs", 61_480.00),
                    _r("pl3_pension", "Retirement plan contributions", 22_400.00),
                    _r("pl3_rent", "Rent — retail premises", 288_000.00),
                    _r("pl3_util", "Utilities", 74_820.00),
                    _r("pl3_repairs", "Repairs & maintenance", 31_260.00),
                    _r("pl3_security", "Security services & monitoring", 96_400.00),
                    _r("pl3_ins", "Insurance", 58_900.00),
                    _r("pl3_adv", "Advertising & marketing", 42_150.00),
                    _r("pl3_prof", "Professional fees — legal & accounting", 67_300.00),
                    _r("pl3_lic", "Licenses, permits & regulatory fees", 118_600.00),
                    _r("pl3_dep", "Depreciation & amortization", 96_450.00),
                    _r("pl3_bad", "Bad debt expense", 4_820.00),
                    _r("pl3_office", "Office supplies & software", 27_940.00),
                    _r("pl3_bank", "Bank & merchant processing fees", 51_330.00),
                    _r("pl3_misc", "Miscellaneous operating expense", 14_600.00),
                    _r("pl3_total", "Total operating expenses", 1_945_650.00, kind="total"),
                ],
            },
        },
    },

    "doc_pos_export": {
        "id": "doc_pos_export",
        "short": "POS export",
        "name": "POS System Export — Gross Sales.csv",
        "kind": "System Export",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-14",
        "page_count": 1,
        "pages": {
            1: {
                "title": "Transaction Totals by Month",
                "layout": "table",
                "subtitle": "Exported 2026-01-13 14:02 UTC · register IDs 01–06",
                "columns": ["PERIOD", "TXNS", "GROSS", "VOIDS"],
                "rows": [
                    _r("pos_jan", None, cols=["2025-01", "8,412", "372,180.00", "2,410.00"]),
                    _r("pos_feb", None, cols=["2025-02", "7,988", "351,940.00", "1,880.00"]),
                    _r("pos_mar", None, cols=["2025-03", "8,904", "398,220.00", "3,140.00"]),
                    _r("pos_apr", None, cols=["2025-04", "8,650", "386,700.00", "2,260.00"]),
                    _r("pos_may", None, cols=["2025-05", "9,120", "409,880.00", "2,970.00"]),
                    _r("pos_jun", None, cols=["2025-06", "9,344", "418,260.00", "3,520.00"]),
                    _r("pos_jul", None, cols=["2025-07", "9,806", "441,300.00", "4,110.00"]),
                    _r("pos_aug", None, cols=["2025-08", "9,512", "428,640.00", "3,280.00"]),
                    _r("pos_sep", None, cols=["2025-09", "8,970", "402,510.00", "2,640.00"]),
                    _r("pos_oct", None, cols=["2025-10", "9,188", "413,220.00", "3,010.00"]),
                    _r("pos_nov", None, cols=["2025-11", "8,742", "391,880.00", "2,450.00"]),
                    _r("pos_dec", None, cols=["2025-12", "9,428", "412,670.00", "4,320.00"]),
                    _r("pos_total", None, kind="total",
                       cols=["TOTAL", "108,064", "4,827,400.00", "35,990.00"]),
                    _r("pos_note",
                       "Export includes voided transactions in the GROSS column. "
                       "Voids are itemized separately and not netted.",
                       kind="note"),
                ],
            },
        },
    },

    "doc_inventory": {
        "id": "doc_inventory",
        "short": "Inventory report",
        "name": "Inventory Valuation Report 12-31-2025.pdf",
        "kind": "Inventory Report",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-16",
        "page_count": 2,
        "pages": {
            1: {
                "title": "Ending Inventory Detail",
                "layout": "table",
                "subtitle": "Valuation as of 12/31/2025 · FIFO",
                "columns": ["CATEGORY", "UNITS", "UNIT COST", "EXTENDED"],
                "rows": [
                    _r("inv_flower", None, cols=["Flower (bulk, g)", "41,280", "4.82", "199,010.00"]),
                    _r("inv_preroll", None, cols=["Pre-roll (ea)", "12,640", "3.15", "39,816.00"]),
                    _r("inv_conc", None, cols=["Concentrate (ea)", "8,910", "14.20", "126,522.00"]),
                    _r("inv_edible", None, cols=["Edible (ea)", "14,220", "6.40", "91,008.00"]),
                    _r("inv_bev", None, cols=["Beverage (ea)", "3,180", "5.90", "18,762.00"]),
                    _r("inv_access", None, cols=["Accessories (ea)", "2,940", "3.98", "11,701.00"]),
                    _r("inv_end", None, kind="total",
                       cols=["ENDING INVENTORY 12/31/2025", "", "", "486,819.00"]),
                    _r("", "", kind="blank"),
                    _r("inv_begin", None, kind="subtotal",
                       cols=["BEGINNING INVENTORY 01/01/2025", "", "", "412,800.00"]),
                ],
            },
            2: {
                "title": "Valuation Method Notes",
                "layout": "legal",
                "subtitle": "Prepared by client controller",
                "rows": [
                    _r("inv2_p1",
                       "1. Method. The Company values inventory using the first-in, "
                       "first-out (FIFO) method. This method has been applied "
                       "consistently since inception and no change in method was made "
                       "during the taxable year."),
                    _r("inv2_p2",
                       "2. Capitalization. Costs capitalized into inventory consist of "
                       "invoice cost from licensed cultivators and manufacturers, inbound "
                       "freight, and state-mandated compliance testing performed prior to "
                       "the product being made available for sale."),
                    _r("inv2_p3",
                       "3. Excluded costs. Retail labor, security, marketing, and general "
                       "administrative expenses are not capitalized into inventory and "
                       "are presented as operating expenses."),
                    _r("inv2_p4",
                       "4. Shrinkage. Physical count performed 12/29/2025 through "
                       "12/31/2025. Recorded shrinkage of $8,140 was expensed to cost of "
                       "goods sold and is included in the ending balance above."),
                ],
            },
        },
    },

    "doc_payroll": {
        "id": "doc_payroll",
        "short": "Payroll register",
        "name": "Payroll Register Q1–Q4 2025.pdf",
        "kind": "Payroll Record",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-18",
        "page_count": 4,
        "pages": {
            1: {
                "title": "Q1 Summary",
                "layout": "table",
                "subtitle": "January – March 2025",
                "columns": ["DEPT", "HEADS", "GROSS WAGES", "ER TAXES"],
                "rows": [
                    _r("pr1_retail", None, cols=["RETAIL", "18", "142,880.00", "12,140.00"]),
                    _r("pr1_prod", None, cols=["PRODUCTION", "6", "78,400.00", "6,660.00"]),
                    _r("pr1_admin", None, cols=["ADMIN", "4", "39,200.00", "3,330.00"]),
                    _r("pr1_exec", None, cols=["EXEC", "3", "46,250.00", "3,930.00"]),
                    _r("pr1_tot", None, kind="total",
                       cols=["Q1 TOTAL", "31", "306,730.00", "26,060.00"]),
                ],
            },
            2: {
                "title": "Q2 Summary",
                "layout": "table",
                "subtitle": "April – June 2025",
                "columns": ["DEPT", "HEADS", "GROSS WAGES", "ER TAXES"],
                "rows": [
                    _r("pr2_retail", None, cols=["RETAIL", "19", "148,220.00", "12,600.00"]),
                    _r("pr2_prod", None, cols=["PRODUCTION", "6", "79,800.00", "6,780.00"]),
                    _r("pr2_admin", None, cols=["ADMIN", "4", "40,100.00", "3,410.00"]),
                    _r("pr2_exec", None, cols=["EXEC", "3", "46,250.00", "3,930.00"]),
                    _r("pr2_tot", None, kind="total",
                       cols=["Q2 TOTAL", "32", "314,370.00", "26,720.00"]),
                ],
            },
            3: {
                "title": "Q3 Summary",
                "layout": "table",
                "subtitle": "July – September 2025",
                "columns": ["DEPT", "HEADS", "GROSS WAGES", "ER TAXES"],
                "rows": [
                    _r("pr3_retail", None, cols=["RETAIL", "21", "159,400.00", "13,550.00"]),
                    _r("pr3_prod", None, cols=["PRODUCTION", "6", "80,600.00", "6,850.00"]),
                    _r("pr3_admin", None, cols=["ADMIN", "4", "41,300.00", "3,510.00"]),
                    _r("pr3_exec", None, cols=["EXEC", "3", "46,250.00", "3,930.00"]),
                    _r("pr3_tot", None, kind="total",
                       cols=["Q3 TOTAL", "34", "327,550.00", "27,840.00"]),
                ],
            },
            4: {
                "title": "Annual Totals by Department",
                "layout": "table",
                "subtitle": "Full year 2025 · all registers",
                "columns": ["DEPT", "HEADS", "GROSS WAGES", "ER TAXES"],
                "rows": [
                    _r("pr4_retail", None, cols=["RETAIL", "21", "612,300.00", "52,050.00"]),
                    _r("pr4_admin", None, cols=["ADMIN", "4", "163,700.00", "13,910.00"]),
                    _r("pr4_nonprod", None, kind="subtotal",
                       cols=["TOTAL WAGES — NON-PRODUCTION", "25", "704,200.00", "65,960.00"]),
                    _r("", "", kind="blank"),
                    _r("pr4_prod", None, kind="subtotal",
                       cols=["TOTAL WAGES — PRODUCTION", "6", "318,400.00", "27,060.00"]),
                    _r("", "", kind="blank"),
                    _r("pr4_exec", None,
                       cols=["EXEC / OFFICER COMP", "3", "185,000.00", "15,730.00"]),
                    _r("pr4_note",
                       "Department code EXEC contains three employees: one officer and "
                       "two senior non-officer staff. The register does not separate them.",
                       kind="note"),
                    _r("", "", kind="blank"),
                    _r("pr4_benefits", None,
                       cols=["EMPLOYEE BENEFIT PROGRAMS", "", "61,480.00", ""]),
                    _r("pr4_pension", None,
                       cols=["RETIREMENT PLAN CONTRIBUTIONS", "", "22,400.00", ""]),
                ],
            },
        },
    },

    "doc_lease": {
        "id": "doc_lease",
        "short": "Lease agreement",
        "name": "Commercial Lease Agreement.pdf",
        "kind": "Legal Agreement",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-11",
        "page_count": 12,
        "pages": {
            4: {
                "title": "Article IV — Rent Schedule",
                "layout": "legal",
                "subtitle": "Executed 2024-11-08",
                "rows": [
                    _r("ls4_p1",
                       "4.1 Base Rent. Tenant shall pay to Landlord base rent in the "
                       "amount of Twenty-Four Thousand Dollars ($24,000.00) per calendar "
                       "month, payable in advance on the first day of each month, "
                       "commencing January 1, 2025."),
                    _r("ls4_p2",
                       "4.2 Escalation. Commencing on the first anniversary of the Rent "
                       "Commencement Date, and on each anniversary thereafter, base rent "
                       "shall increase by three percent (3%) over the base rent payable "
                       "during the immediately preceding twelve (12) month period."),
                    _r("ls4_p3",
                       "4.3 Additional Rent. Tenant shall pay as additional rent its "
                       "proportionate share of common area maintenance, assessed "
                       "quarterly and reconciled annually."),
                ],
            },
            7: {
                "title": "Article VII — Premises & Permitted Use",
                "layout": "legal",
                "subtitle": None,
                "rows": [
                    _r("ls7_p1",
                       "7.1 Premises. The Premises consist of approximately 6,400 "
                       "rentable square feet, comprising 2,100 square feet of retail "
                       "floor area and 4,300 square feet of secured storage, processing, "
                       "and back-of-house area."),
                    _r("ls7_p2",
                       "7.2 Permitted Use. The Premises shall be used solely for the "
                       "retail sale of cannabis and cannabis products pursuant to a valid "
                       "state license, and for no other purpose without Landlord's prior "
                       "written consent."),
                ],
            },
        },
    },

    "doc_bank_stmt": {
        "id": "doc_bank_stmt",
        "short": "Bank statements",
        "name": "Operating Account Statements 2025.pdf",
        "kind": "Bank Statement",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-20",
        "page_count": 24,
        "pages": {
            23: {
                "title": "December Activity",
                "layout": "ledger",
                "subtitle": "Account ••••8820 · 12/01/2025 – 12/31/2025",
                "columns": ["DATE", "DESCRIPTION", "AMOUNT"],
                "rows": [
                    _r("bk23_1", None, cols=["12/01", "ACH RENT — MERIDIAN PROP LLC", "-24,000.00"]),
                    _r("bk23_2", None, cols=["12/03", "MERCHANT SETTLEMENT BATCH", "+96,410.00"]),
                    _r("bk23_3", None, cols=["12/08", "VENDOR ACH — GREENFIELD CULT.", "-184,220.00"]),
                    _r("bk23_4", None, cols=["12/12", "STATE EXCISE TAX REMITTANCE", "-142,880.00"]),
                    _r("bk23_5", None, cols=["12/15", "PAYROLL — ADP", "-88,640.00"]),
                    _r("bk23_6", None, cols=["12/22", "INTEREST CHARGED — LOC", "-3,940.00"]),
                    _r("bk23_7", None, cols=["12/31", "MERCHANT SETTLEMENT BATCH", "+104,220.00"]),
                ],
            },
            24: {
                "title": "Year-End Summary",
                "layout": "statement",
                "subtitle": "Account ••••8820 · full year 2025",
                "rows": [
                    _r("bk24_h", "ANNUAL ACTIVITY SUMMARY", kind="header"),
                    _r("bk24_dep", "Total deposits", 4_688_140.00),
                    _r("bk24_wd", "Total withdrawals", -4_602_880.00),
                    _r("", "", kind="blank"),
                    _r("bk24_rent", "Rent payments (12 @ $24,000.00)", 288_000.00),
                    _r("bk24_int", "Total interest charged YTD", 47_300.00),
                    _r("bk24_fees", "Bank & merchant processing fees", 51_330.00),
                    _r("bk24_bad", "Returned items / uncollected", 4_820.00),
                ],
            },
        },
    },

    "doc_fixed_assets": {
        "id": "doc_fixed_assets",
        "short": "Asset schedule",
        "name": "Fixed Asset & Depreciation Schedule 2025.xlsx",
        "kind": "Depreciation Schedule",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-19",
        "page_count": 2,
        "pages": {
            1: {
                "title": "Asset Detail",
                "layout": "table",
                "subtitle": "MACRS · placed in service through 12/31/2025",
                "columns": ["ASSET", "BASIS", "LIFE", "2025 DEPR"],
                "rows": [
                    _r("fa_lease", None, cols=["Leasehold improvements", "412,000.00", "15 yr", "27,466.00"]),
                    _r("fa_sec", None, cols=["Security & surveillance system", "148,600.00", "7 yr", "21,229.00"]),
                    _r("fa_pos", None, cols=["POS terminals & network", "62,400.00", "5 yr", "12,480.00"]),
                    _r("fa_disp", None, cols=["Display cases & fixtures", "94,800.00", "7 yr", "13,543.00"]),
                    _r("fa_veh", None, cols=["Delivery vehicles (2)", "88,000.00", "5 yr", "17,600.00"]),
                    _r("fa_hvac", None, cols=["HVAC & environmental controls", "58,200.00", "15 yr", "3,880.00"]),
                    _r("fa_dep_tot", None, kind="subtotal",
                       cols=["TOTAL DEPRECIATION", "864,000.00", "", "96,198.00"]),
                    _r("", "", kind="blank"),
                    _r("fa_amort", None,
                       cols=["Amortization — license acquisition", "2,520.00", "15 yr", "252.00"]),
                    _r("fa_combined", None, kind="total",
                       cols=["TOTAL D&A", "", "", "96,450.00"]),
                ],
            },
            2: {
                "title": "Sec. 179 & Bonus Elections",
                "layout": "legal",
                "subtitle": None,
                "rows": [
                    _r("fa2_p1",
                       "No Section 179 expensing election was made for the taxable year. "
                       "The Company has elected out of bonus depreciation under Sec. "
                       "168(k)(7) for all asset classes placed in service during 2025."),
                    _r("fa2_p2",
                       "Note: depreciation on assets used in inventory production is "
                       "allocated to cost of goods sold under Sec. 471. For 2025 no "
                       "assets were determined to be production-allocable; the full "
                       "amount is presented as an operating expense."),
                ],
            },
        },
    },

    "doc_licenses": {
        "id": "doc_licenses",
        "short": "License schedule",
        "name": "State Licenses & Regulatory Fees 2025.pdf",
        "kind": "Regulatory Record",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-21",
        "page_count": 2,
        "pages": {
            1: {
                "title": "License & Permit Fees Paid",
                "layout": "table",
                "subtitle": "Calendar year 2025",
                "columns": ["AUTHORITY", "TYPE", "PERIOD", "AMOUNT"],
                "rows": [
                    _r("lic_state", None, cols=["State Cannabis Control", "Retail license renewal", "Annual", "68,000.00"]),
                    _r("lic_local", None, cols=["City of Irvine", "Local operating permit", "Annual", "24,500.00"]),
                    _r("lic_seller", None, cols=["State Dept. of Revenue", "Seller's permit", "Annual", "1,200.00"]),
                    _r("lic_track", None, cols=["Track-and-trace program", "Compliance fee", "Quarterly", "14,400.00"]),
                    _r("lic_fire", None, cols=["County Fire Authority", "Inspection & permit", "Annual", "3,900.00"]),
                    _r("lic_weights", None, cols=["Weights & Measures", "Device certification", "Annual", "6,600.00"]),
                    _r("lic_tot", None, kind="total",
                       cols=["TOTAL LICENSES, PERMITS & FEES", "", "", "118,600.00"]),
                ],
            },
            2: {
                "title": "Excise & Payroll Tax Summary",
                "layout": "statement",
                "subtitle": "Amounts remitted during 2025",
                "rows": [
                    _r("tax_h", "TAXES REMITTED", kind="header"),
                    _r("tax_excise",
                       "State cannabis excise tax (collected from customers, remitted)",
                       1_684_200.00),
                    _r("tax_payroll", "Employer payroll taxes", 93_020.00),
                    _r("tax_prop", "Personal property tax", 18_400.00),
                    _r("tax_note",
                       "Excise tax is collected on behalf of the state and is not an "
                       "expense of the Company. It is excluded from the taxes and "
                       "licenses deduction.",
                       kind="note"),
                ],
            },
        },
    },

    "doc_insurance": {
        "id": "doc_insurance",
        "short": "Insurance summary",
        "name": "Insurance Policy Summary 2025.pdf",
        "kind": "Insurance Record",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-17",
        "page_count": 1,
        "pages": {
            1: {
                "title": "Policies in Force",
                "layout": "table",
                "subtitle": "Premiums paid during calendar year 2025",
                "columns": ["CARRIER", "COVERAGE", "TERM", "PREMIUM"],
                "rows": [
                    _r("ins_gl", None, cols=["Cascade Specialty", "General liability", "12 mo", "22,400.00"]),
                    _r("ins_prod", None, cols=["Cascade Specialty", "Product liability", "12 mo", "14,800.00"]),
                    _r("ins_prop", None, cols=["Northbay Mutual", "Property & contents", "12 mo", "11,900.00"]),
                    _r("ins_wc", None, cols=["State Fund", "Workers' compensation", "12 mo", "9,800.00"]),
                    _r("ins_tot", None, kind="total",
                       cols=["TOTAL PREMIUMS", "", "", "58,900.00"]),
                ],
            },
        },
    },

    "doc_vendor": {
        "id": "doc_vendor",
        "short": "Vendor recap",
        "name": "Vendor Expense Recap 2025.xlsx",
        "kind": "Expense Summary",
        "uploaded_by": "client",
        "uploaded_at": "2026-01-22",
        "page_count": 3,
        "pages": {
            1: {
                "title": "Facilities & Operations",
                "layout": "table",
                "subtitle": "Aggregated from AP ledger",
                "columns": ["VENDOR", "CATEGORY", "ANNUAL"],
                "rows": [
                    _r("vn_sec", None, cols=["Sentinel Protective Svcs", "Security & monitoring", "96,400.00"]),
                    _r("vn_util1", None, cols=["Regional Power & Light", "Electricity", "58,220.00"]),
                    _r("vn_util2", None, cols=["Municipal Water District", "Water & sewer", "9,400.00"]),
                    _r("vn_util3", None, cols=["Broadband & telecom", "Internet & phone", "7,200.00"]),
                    _r("vn_utiltot", None, kind="subtotal",
                       cols=["TOTAL UTILITIES", "", "74,820.00"]),
                    _r("vn_repair", None, cols=["Various trades", "Repairs & maintenance", "31,260.00"]),
                    _r("vn_waste", None, cols=["Compliant Disposal Inc", "Regulated waste disposal", "12,800.00"]),
                ],
            },
            2: {
                "title": "Professional & Administrative",
                "layout": "table",
                "subtitle": None,
                "columns": ["VENDOR", "CATEGORY", "ANNUAL"],
                "rows": [
                    _r("vn_legal", None, cols=["Harrow & Lane LLP", "Legal — regulatory", "38,400.00"]),
                    _r("vn_acct", None, cols=["Prior CPA firm", "Accounting & tax", "28,900.00"]),
                    _r("vn_proftot", None, kind="subtotal",
                       cols=["TOTAL PROFESSIONAL FEES", "", "67,300.00"]),
                    _r("", "", kind="blank"),
                    _r("vn_soft", None, cols=["Seed-to-sale platform", "Software subscription", "19,440.00"]),
                    _r("vn_office", None, cols=["Office & janitorial supply", "Supplies", "8,500.00"]),
                    _r("vn_offtot", None, kind="subtotal",
                       cols=["TOTAL OFFICE & SOFTWARE", "", "27,940.00"]),
                ],
            },
            3: {
                "title": "Marketing & Other",
                "layout": "table",
                "subtitle": None,
                "columns": ["VENDOR", "CATEGORY", "ANNUAL"],
                "rows": [
                    _r("vn_adv1", None, cols=["Directory listings", "Directory advertising", "24,600.00"]),
                    _r("vn_adv2", None, cols=["Local print & outdoor", "Advertising", "11,900.00"]),
                    _r("vn_adv3", None, cols=["Loyalty program platform", "Customer marketing", "5,650.00"]),
                    _r("vn_advtot", None, kind="subtotal",
                       cols=["TOTAL ADVERTISING", "", "42,150.00"]),
                    _r("", "", kind="blank"),
                    _r("vn_charity", None, cols=["Community Health Fdn", "Charitable contribution", "12,000.00"]),
                    _r("vn_misc", None, cols=["Various", "Miscellaneous", "14,600.00"]),
                ],
            },
        },
    },

    "doc_prior_return": {
        "id": "doc_prior_return",
        "short": "FY2024 return",
        "name": "Form 1120 — FY2024 (as filed).pdf",
        "kind": "Prior Year Return",
        "uploaded_by": "firm",
        "uploaded_at": "2026-01-09",
        "page_count": 6,
        "pages": {
            1: {
                "title": "Page 1 — Income & Deductions",
                "layout": "statement",
                "subtitle": "Verdant Retail Holdings, LLC · FY2024 as filed",
                "rows": [
                    _r("py_h", "SELECTED PRIOR-YEAR AMOUNTS", kind="header"),
                    _r("py_gross", "Gross receipts or sales", 3_918_400.00),
                    _r("py_cogs", "Cost of goods sold", 2_402_180.00),
                    _r("py_officer", "Compensation of officers", 165_000.00),
                    _r("py_rent", "Rents", 264_000.00),
                    _r("py_dep", "Depreciation", 88_120.00),
                    _r("py_ti", "Taxable income", 1_112_640.00),
                    _r("py_note",
                       "Prior year prepared by outside firm. Sec. 280E adjustment "
                       "computed on a different allocation basis; see workpaper "
                       "reconciliation.",
                       kind="note"),
                ],
            },
        },
    },
}


# ---------------------------------------------------------------------------
# RETURN FIELDS
# ---------------------------------------------------------------------------


def _f(fid, section, line, label, value, source_type, state, confidence,
       doc=None, page=None, row=None, excerpt=None, transformation=None,
       rationale="", evidence=None, conflicts=None, history=None, lock=None):
    return {
        "id": fid, "form": "Form 1120", "section": section, "line": line,
        "label": label, "value": value, "source_type": source_type,
        "state": state, "confidence": confidence,
        "source_doc": doc, "page": page, "source_row": row,
        "source_excerpt": excerpt, "transformation": transformation,
        "ai_rationale": rationale, "evidence": evidence or [],
        "conflicts": conflicts or [], "override_history": history or [],
        "lock_reason": lock,
    }


FIELDS = [
    # ════════════════════════════════ INCOME ════════════════════════════════
    _f("f_gross_receipts", "Income", "1a", "Gross receipts or sales",
       4_827_400.00, "extracted", "needs_approval", 0.71,
       doc="doc_pos_export", page=1, row="pos_total",
       excerpt="TOTAL · 108,064 txns · 4,827,400.00",
       rationale="Pulled the annual gross sales total from the POS export. Flagged for "
                 "approval because the P&L reports a different figure for the same period.",
       evidence=[
           {"doc": "doc_pos_export", "page": 1, "note": "POS annual total: $4,827,400 (includes voids)"},
           {"doc": "doc_pl_2025", "page": 1, "note": "P&L total gross revenue: $4,791,220"},
           {"doc": "doc_pos_export", "page": 1, "note": "Voids itemized separately at $35,990"},
       ],
       conflicts=[{
           "competing_value": 4_791_220.00, "competing_doc": "doc_pl_2025",
           "competing_page": 1, "competing_row": "pl1_gross", "delta": 36_180.00,
           "explanation": "The POS export exceeds the P&L by $36,180. The export note "
                          "states voids are included in the GROSS column and not netted; "
                          "recorded voids total $35,990, which accounts for most but not "
                          "all of the gap. Resolution requires client confirmation.",
       }]),

    _f("f_returns", "Income", "1b", "Returns and allowances",
       80_950.00, "calculated", "ai_suggested", 0.86,
       transformation={
           "formula": "Returns and allowances + promotional discounts",
           "steps": [
               {"label": "Returns and allowances", "value": 18_640.00,
                "doc": "doc_pl_2025", "page": 1, "row": "pl1_returns"},
               {"label": "Promotional discounts", "value": 62_310.00,
                "doc": "doc_pl_2025", "page": 1, "row": "pl1_disc"},
           ]},
       rationale="Combined the two contra-revenue lines from the P&L. Discounts are "
                 "treated as reductions of gross receipts rather than as marketing "
                 "expense — which matters here, because Sec. 280E would disallow the "
                 "marketing treatment entirely.",
       evidence=[{"doc": "doc_pl_2025", "page": 1, "note": "Both contra-revenue lines presented below gross"}]),

    _f("f_net_receipts", "Income", "1c", "Balance (1a less 1b)",
       4_746_450.00, "calculated", "locked", None,
       transformation={
           "formula": "Line 1a − Line 1b",
           "steps": [
               {"label": "Gross receipts or sales (Ln 1a)", "value": 4_827_400.00},
               {"label": "Returns and allowances (Ln 1b)", "value": -80_950.00},
           ]},
       rationale="Derived directly from lines 1a and 1b.",
       lock="Derived field. Change line 1a or 1b to affect this value."),

    _f("f_cogs", "Income", "2", "Cost of goods sold",
       2_913_650.00, "calculated", "ai_suggested", 0.88,
       transformation={
           "formula": "Beginning inventory + Purchases + Direct labor + Sec. 471 indirect − Ending inventory",
           "steps": [
               {"label": "Beginning inventory (01/01/2025)", "value": 412_800.00,
                "doc": "doc_inventory", "page": 1, "row": "inv_begin"},
               {"label": "Product purchases", "value": 2_640_100.00,
                "doc": "doc_pl_2025", "page": 2, "row": "pl2_purchtot"},
               {"label": "Direct production labor", "value": 318_400.00,
                "doc": "doc_payroll", "page": 4, "row": "pr4_prod"},
               {"label": "Allocated indirect costs (Sec. 471)", "value": 29_150.00,
                "doc": "doc_pl_2025", "page": 2, "row": "pl2_indirect"},
               {"label": "Ending inventory (12/31/2025)", "value": -486_800.00,
                "doc": "doc_inventory", "page": 1, "row": "inv_end"},
           ]},
       rationale="Computed under Sec. 471 inventory rules. Only costs allocable to "
                 "inventory are included; selling and administrative costs are excluded "
                 "because Sec. 280E disallows them for this taxpayer. Given that "
                 "disallowance, this is the highest-stakes number on the return.",
       evidence=[
           {"doc": "doc_inventory", "page": 2, "note": "FIFO applied consistently; no method change"},
           {"doc": "doc_payroll", "page": 4, "note": "Production dept. wages isolated from retail"},
           {"doc": "doc_inventory", "page": 2, "note": "Capitalized costs limited to invoice, freight, compliance testing"},
       ]),

    _f("f_gross_profit", "Income", "3", "Gross profit",
       1_832_800.00, "calculated", "locked", None,
       transformation={
           "formula": "Line 1c − Line 2",
           "steps": [
               {"label": "Net receipts (Ln 1c)", "value": 4_746_450.00},
               {"label": "Cost of goods sold (Ln 2)", "value": -2_913_650.00},
           ]},
       rationale="Derived from lines 1c and 2.",
       lock="Derived field. Change line 1c or line 2 to affect this value."),

    _f("f_interest_income", "Income", "5", "Interest income",
       2_140.00, "extracted", "editable", 0.94,
       doc="doc_bank_stmt", page=24, row="bk24_dep",
       excerpt="Total deposits · 4,688,140.00",
       rationale="Extracted from the year-end bank summary. Low materiality.",
       evidence=[{"doc": "doc_bank_stmt", "page": 24, "note": "Interest credited on operating balance"}]),

    _f("f_total_income", "Income", "11", "Total income",
       1_834_940.00, "calculated", "locked", None,
       transformation={
           "formula": "Gross profit + interest income",
           "steps": [
               {"label": "Gross profit (Ln 3)", "value": 1_832_800.00},
               {"label": "Interest income (Ln 5)", "value": 2_140.00},
           ]},
       rationale="Sum of the income lines above.",
       lock="Derived field. Change the underlying income lines to affect this value."),

    # ══════════════════════════════ DEDUCTIONS ══════════════════════════════
    _f("f_officer_comp", "Deductions", "12", "Compensation of officers",
       185_000.00, "extracted", "ai_suggested", 0.61,
       doc="doc_payroll", page=4, row="pr4_exec",
       excerpt="EXEC / OFFICER COMP · 3 heads · 185,000.00",
       rationale="Extracted from annual payroll totals. Confidence is low: the register "
                 "groups officer compensation under an EXEC department code that also "
                 "contains two non-officer salaries. The figure is likely overstated and "
                 "needs the client to break out the officer individually.",
       evidence=[{"doc": "doc_payroll", "page": 4, "note": "Register note confirms EXEC = 1 officer + 2 non-officers"}]),

    _f("f_salaries", "Deductions", "13", "Salaries and wages",
       704_200.00, "extracted", "verified", 0.96,
       doc="doc_payroll", page=4, row="pr4_nonprod",
       excerpt="TOTAL WAGES — NON-PRODUCTION · 25 heads · 704,200.00",
       rationale="Extracted from annual payroll totals, excluding the $318,400 of "
                 "production labor already captured in cost of goods sold.",
       evidence=[{"doc": "doc_payroll", "page": 4, "note": "Non-production wage total: retail + admin"}]),

    _f("f_repairs", "Deductions", "14", "Repairs and maintenance",
       31_260.00, "extracted", "editable", 0.92,
       doc="doc_vendor", page=1, row="vn_repair",
       excerpt="Various trades · Repairs & maintenance · 31,260.00",
       rationale="Extracted from the vendor expense recap.",
       evidence=[{"doc": "doc_pl_2025", "page": 3, "note": "Agrees to P&L operating expense line"}]),

    _f("f_bad_debts", "Deductions", "15", "Bad debts",
       4_820.00, "extracted", "editable", 0.90,
       doc="doc_bank_stmt", page=24, row="bk24_bad",
       excerpt="Returned items / uncollected · 4,820.00",
       rationale="Extracted from the bank year-end summary and agreed to the P&L.",
       evidence=[{"doc": "doc_pl_2025", "page": 3, "note": "Bad debt expense line agrees"}]),

    _f("f_rent", "Deductions", "16", "Rents",
       288_000.00, "manual", "verified", None,
       doc="doc_lease", page=4, row="ls4_p1",
       excerpt="Base rent $24,000.00 per calendar month, commencing January 1, 2025",
       transformation={
           "formula": "Monthly base rent × 12 months",
           "steps": [
               {"label": "Monthly base rent", "value": 24_000.00,
                "doc": "doc_lease", "page": 4, "row": "ls4_p1"},
               {"label": "Months in tax year", "value": 12},
           ]},
       rationale="Originally suggested $296,640 by applying the 3% escalation clause. "
                 "Reviewer determined the escalation begins on the first anniversary, so "
                 "FY2025 uses flat base rent throughout.",
       evidence=[
           {"doc": "doc_lease", "page": 4, "note": "Escalation clause reads 'commencing on the first anniversary'"},
           {"doc": "doc_bank_stmt", "page": 24, "note": "12 rent payments of $24,000 confirmed"},
       ],
       history=[{
           "from": 296_640.00, "to": 288_000.00, "by": "M. Reyes, CPA",
           "at": "2026-02-03 14:22",
           "reason": "Escalation clause applies from year two, not year one. Bank "
                     "statements confirm 12 payments at $24,000.",
       }]),

    _f("f_taxes_licenses", "Deductions", "17", "Taxes and licenses",
       230_020.00, "calculated", "needs_approval", 0.68,
       transformation={
           "formula": "Licenses & permits + employer payroll taxes + personal property tax",
           "steps": [
               {"label": "Licenses, permits & regulatory fees", "value": 118_600.00,
                "doc": "doc_licenses", "page": 1, "row": "lic_tot"},
               {"label": "Employer payroll taxes", "value": 93_020.00,
                "doc": "doc_licenses", "page": 2, "row": "tax_payroll"},
               {"label": "Personal property tax", "value": 18_400.00,
                "doc": "doc_licenses", "page": 2, "row": "tax_prop"},
           ]},
       rationale="Excise tax of $1,684,200 was deliberately EXCLUDED. It is collected "
                 "from customers and remitted to the state, so it is not an expense of "
                 "the Company. Flagged for approval because the exclusion is large and "
                 "the client's books present it inconsistently.",
       evidence=[
           {"doc": "doc_licenses", "page": 2, "note": "Document note confirms excise is collected on behalf of the state"},
           {"doc": "doc_pl_2025", "page": 1, "note": "P&L also presents excise net of revenue"},
       ],
       conflicts=[{
           "competing_value": 1_914_220.00, "competing_doc": "doc_licenses",
           "competing_page": 2, "competing_row": "tax_excise", "delta": 1_684_200.00,
           "explanation": "If excise tax were treated as a deductible tax rather than a "
                          "pass-through collection, this line would be $1,914,220. That "
                          "treatment would be aggressive and is inconsistent with how "
                          "revenue is presented on the P&L. Confirm before filing.",
       }]),

    _f("f_interest", "Deductions", "18", "Interest expense",
       47_300.00, "extracted", "editable", 0.93,
       doc="doc_bank_stmt", page=24, row="bk24_int",
       excerpt="Total interest charged YTD · 47,300.00",
       rationale="Extracted from the year-end bank summary.",
       evidence=[{"doc": "doc_bank_stmt", "page": 23, "note": "December charge of $3,940 consistent with monthly run rate"}]),

    _f("f_charitable", "Deductions", "19", "Charitable contributions",
       12_000.00, "extracted", "ai_suggested", 0.79,
       doc="doc_vendor", page=3, row="vn_charity",
       excerpt="Community Health Fdn · Charitable contribution · 12,000.00",
       rationale="Extracted from the vendor recap. The 10% taxable income limitation has "
                 "not been applied, and Sec. 280E may disallow this entirely for a "
                 "trafficking business.",
       evidence=[{"doc": "doc_vendor", "page": 3, "note": "Single contribution; no substantiation letter in the file"}]),

    _f("f_depreciation", "Deductions", "20", "Depreciation",
       96_450.00, "extracted", "ai_suggested", 0.84,
       doc="doc_fixed_assets", page=1, row="fa_combined",
       excerpt="TOTAL D&A · 96,450.00",
       rationale="Extracted from the fixed asset schedule. The schedule combines "
                 "depreciation ($96,198) with license amortization ($252). If the return "
                 "needs them split, line 20 should carry only the depreciation portion.",
       evidence=[
           {"doc": "doc_fixed_assets", "page": 1, "note": "Depreciation subtotal $96,198; amortization $252"},
           {"doc": "doc_fixed_assets", "page": 2, "note": "No Sec. 179 election; elected out of bonus"},
           {"doc": "doc_fixed_assets", "page": 2, "note": "No production-allocable assets, so none moves to COGS"},
       ]),

    _f("f_advertising", "Deductions", "22", "Advertising",
       42_150.00, "extracted", "verified", 0.95,
       doc="doc_vendor", page=3, row="vn_advtot",
       excerpt="TOTAL ADVERTISING · 42,150.00",
       rationale="Extracted from the vendor recap; agrees to the P&L operating expense line.",
       evidence=[{"doc": "doc_pl_2025", "page": 3, "note": "P&L advertising line agrees exactly"}]),

    _f("f_pension", "Deductions", "23", "Pension and profit-sharing plans",
       22_400.00, "extracted", "editable", 0.91,
       doc="doc_payroll", page=4, row="pr4_pension",
       excerpt="RETIREMENT PLAN CONTRIBUTIONS · 22,400.00",
       rationale="Extracted from the payroll register annual totals.",
       evidence=[{"doc": "doc_pl_2025", "page": 3, "note": "Agrees to P&L retirement contribution line"}]),

    _f("f_benefits", "Deductions", "24", "Employee benefit programs",
       61_480.00, "extracted", "editable", 0.92,
       doc="doc_payroll", page=4, row="pr4_benefits",
       excerpt="EMPLOYEE BENEFIT PROGRAMS · 61,480.00",
       rationale="Extracted from the payroll register annual totals.",
       evidence=[{"doc": "doc_pl_2025", "page": 3, "note": "Agrees to P&L benefits line"}]),

    _f("f_insurance", "Deductions", "26a", "Insurance",
       58_900.00, "extracted", "verified", 0.97,
       doc="doc_insurance", page=1, row="ins_tot",
       excerpt="TOTAL PREMIUMS · 58,900.00",
       rationale="Extracted from the insurance policy summary. All four policies are in "
                 "force for the full 12-month term with no short-period proration.",
       evidence=[{"doc": "doc_insurance", "page": 1, "note": "Four policies, all 12-month terms"}]),

    _f("f_security", "Deductions", "26b", "Security services",
       96_400.00, "extracted", "ai_suggested", 0.89,
       doc="doc_vendor", page=1, row="vn_sec",
       excerpt="Sentinel Protective Svcs · Security & monitoring · 96,400.00",
       rationale="Extracted from the vendor recap. Worth noting: security is mandated by "
                 "state licensing, but Sec. 280E still disallows it because it is not an "
                 "inventory cost under Sec. 471.",
       evidence=[{"doc": "doc_pl_2025", "page": 3, "note": "P&L security line agrees"}]),

    _f("f_utilities", "Deductions", "26c", "Utilities",
       74_820.00, "extracted", "verified", 0.94,
       doc="doc_vendor", page=1, row="vn_utiltot",
       excerpt="TOTAL UTILITIES · 74,820.00",
       rationale="Sum of the three utility vendors on the recap; agrees to the P&L.",
       evidence=[{"doc": "doc_pl_2025", "page": 3, "note": "P&L utilities line agrees"}]),

    _f("f_professional", "Deductions", "26d", "Professional fees",
       67_300.00, "extracted", "editable", 0.93,
       doc="doc_vendor", page=2, row="vn_proftot",
       excerpt="TOTAL PROFESSIONAL FEES · 67,300.00",
       rationale="Extracted from the vendor recap. Includes both regulatory legal work "
                 "and prior-firm accounting fees.",
       evidence=[{"doc": "doc_vendor", "page": 2, "note": "Legal $38,400 + accounting $28,900"}]),

    _f("f_licenses_ded", "Deductions", "26e", "Licenses and permits",
       118_600.00, "extracted", "verified", 0.98,
       doc="doc_licenses", page=1, row="lic_tot",
       excerpt="TOTAL LICENSES, PERMITS & FEES · 118,600.00",
       rationale="Extracted from the regulatory fee schedule. Six separate authorities, "
                 "all documented.",
       evidence=[{"doc": "doc_licenses", "page": 1, "note": "Six line items with authority and period"}]),

    _f("f_office", "Deductions", "26f", "Office expense and software",
       27_940.00, "extracted", "editable", 0.90,
       doc="doc_vendor", page=2, row="vn_offtot",
       excerpt="TOTAL OFFICE & SOFTWARE · 27,940.00",
       rationale="Extracted from the vendor recap.",
       evidence=[{"doc": "doc_vendor", "page": 2, "note": "Seed-to-sale platform is the largest component"}]),

    _f("f_bank_fees", "Deductions", "26g", "Bank and merchant processing fees",
       51_330.00, "extracted", "ai_suggested", 0.87,
       doc="doc_bank_stmt", page=24, row="bk24_fees",
       excerpt="Bank & merchant processing fees · 51,330.00",
       rationale="Extracted from the bank year-end summary. Cash-intensive cannabis "
                 "operations carry elevated banking costs; this figure is consistent with "
                 "the deposit volume.",
       evidence=[{"doc": "doc_pl_2025", "page": 3, "note": "P&L bank fee line agrees"}]),

    _f("f_waste", "Deductions", "26h", "Regulated waste disposal",
       12_800.00, "extracted", "editable", 0.91,
       doc="doc_vendor", page=1, row="vn_waste",
       excerpt="Compliant Disposal Inc · Regulated waste disposal · 12,800.00",
       rationale="Extracted from the vendor recap. Required by state regulation.",
       evidence=[{"doc": "doc_vendor", "page": 1, "note": "Single vendor, monthly service"}]),

    _f("f_misc", "Deductions", "26i", "Miscellaneous",
       14_600.00, "extracted", "ai_suggested", 0.64,
       doc="doc_vendor", page=3, row="vn_misc",
       excerpt="Various · Miscellaneous · 14,600.00",
       rationale="Extracted from the vendor recap, but the line is aggregated as "
                 "'Various' with no vendor detail. Low confidence: an unexplained "
                 "miscellaneous balance of this size is an audit flag and should be "
                 "broken out before filing.",
       evidence=[{"doc": "doc_vendor", "page": 3, "note": "No vendor-level detail provided for this line"}]),

    _f("f_total_deductions", "Deductions", "27", "Total deductions",
       1_925_990.00, "calculated", "locked", None,
       transformation={
           "formula": "Sum of lines 12 through 26",
           "steps": [
               {"label": "Compensation of officers (Ln 12)", "value": 185_000.00},
               {"label": "Salaries and wages (Ln 13)", "value": 704_200.00},
               {"label": "Rents (Ln 16)", "value": 288_000.00},
               {"label": "Taxes and licenses (Ln 17)", "value": 230_020.00},
               {"label": "Depreciation (Ln 20)", "value": 96_450.00},
               {"label": "All other deductions (Ln 14–26)", "value": 422_320.00},
           ]},
       rationale="Sum of all deduction lines before the Sec. 280E adjustment.",
       lock="Derived field. Change any deduction line to affect this value."),

    # ═══════════════════════════ 280E ADJUSTMENT ════════════════════════════
    _f("f_280e_disallowed", "Sec. 280E Adjustment", "27 (adj)",
       "Sec. 280E disallowed deductions",
       1_925_990.00, "calculated", "locked", None,
       transformation={
           "formula": "Total deductions − deductions allocable to non-trafficking activity",
           "steps": [
               {"label": "Total deductions (Ln 27)", "value": 1_925_990.00},
               {"label": "Allocable to non-trafficking activity", "value": 0.00},
           ]},
       rationale="Sec. 280E disallows every deduction other than cost of goods sold for "
                 "a business trafficking in a Schedule I controlled substance. The "
                 "Company reported $181,800 of accessory sales, but no expenses were "
                 "separately allocated to that activity, so no deductions survive. "
                 "Allocating a portion would require a documented, defensible basis.",
       evidence=[
           {"doc": "doc_pl_2025", "page": 1, "note": "Accessories & non-cannabis retail: $181,800"},
           {"doc": "doc_prior_return", "page": 1, "note": "Prior year used a different allocation basis"},
       ],
       lock="Derived field. Allocate expenses to a separate non-trafficking trade or "
            "business to reduce the disallowance."),

    _f("f_taxable_income", "Sec. 280E Adjustment", "30", "Taxable income",
       1_834_940.00, "calculated", "locked", None,
       transformation={
           "formula": "Total income − allowable deductions after Sec. 280E",
           "steps": [
               {"label": "Total income (Ln 11)", "value": 1_834_940.00},
               {"label": "Deductions allowed after Sec. 280E", "value": 0.00},
           ]},
       rationale="Because Sec. 280E disallows all operating deductions, taxable income "
                 "equals gross profit plus other income. That mechanic is exactly why the "
                 "COGS allocation on line 2 is the highest-stakes number on this return.",
       evidence=[{"doc": "doc_prior_return", "page": 1, "note": "Prior year taxable income: $1,112,640"}],
       lock="Derived field. Change line 2 or the Sec. 280E allocation to affect this value."),

    _f("f_total_tax", "Sec. 280E Adjustment", "31", "Total tax",
       385_337.00, "calculated", "ai_suggested", 0.82,
       transformation={
           "formula": "Taxable income × 21% federal corporate rate",
           "steps": [
               {"label": "Taxable income (Ln 30)", "value": 1_834_940.00},
               {"label": "Federal corporate rate (21%)", "value": 0.21},
           ]},
       rationale="Flat 21% applied to taxable income. State tax, estimated payments, and "
                 "any credits are not yet reflected.",
       evidence=[{"doc": "doc_prior_return", "page": 1, "note": "Prior year effective rate consistent with 21% flat"}]),
]


# ---------------------------------------------------------------------------
# AFFORDANCE SYSTEM (Challenge 08)
# Defined once, consumed by every screen, so the visual language cannot drift.
# ---------------------------------------------------------------------------

STATES = {
    "needs_approval": {
        "label": "Needs approval",
        "meaning": "AI found a conflict it cannot resolve. Requires a decision.",
        "editable": True,
        "border": "border-l-4 border-rose-400",
        "chip_bg": "bg-rose-50 text-rose-800 ring-rose-200",
    },
    "ai_suggested": {
        "label": "AI suggested",
        "meaning": "Generated by AI. Not yet reviewed by a human.",
        "editable": True,
        "border": "border-l-4 border-amber-400",
        "chip_bg": "bg-amber-50 text-amber-800 ring-amber-200",
    },
    "editable": {
        "label": "Editable",
        "meaning": "Standard field. Extracted with high confidence, open to edit.",
        "editable": True,
        "border": "border-l-4 border-slate-200",
        "chip_bg": "bg-slate-50 text-slate-600 ring-slate-200",
    },
    "verified": {
        "label": "Verified",
        "meaning": "Reviewed and confirmed by a human preparer.",
        "editable": True,
        "border": "border-l-4 border-emerald-400",
        "chip_bg": "bg-emerald-50 text-emerald-800 ring-emerald-200",
    },
    "locked": {
        "label": "Locked",
        "meaning": "Derived from other fields. Cannot be edited directly.",
        "editable": False,
        "border": "border-l-4 border-slate-400",
        "chip_bg": "bg-slate-100 text-slate-700 ring-slate-300",
    },
}

SECTIONS = ["Income", "Deductions", "Sec. 280E Adjustment"]


def confidence_band(c):
    """Coarse bands. Exposing '0.6134' to a CPA implies a precision the model
    does not have, and reviewers anchor hard on decimals."""
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
    """Ranking stub -- the 'small script that fakes the logic' the brief allows.
    Orders by decision urgency, not by form line number."""
    priority = {"needs_approval": 0, "ai_suggested": 1, "editable": 2,
                "verified": 3, "locked": 4}
    return sorted(
        FIELDS,
        key=lambda f: (priority[f["state"]],
                       f["confidence"] if f["confidence"] is not None else 1.0),
    )


def fields_by_section():
    return [(s, [f for f in FIELDS if f["section"] == s]) for s in SECTIONS]


def summary_counts():
    counts = {k: 0 for k in STATES}
    for f in FIELDS:
        counts[f["state"]] += 1
    return counts


def open_items():
    return sum(1 for f in FIELDS if f["state"] in ("needs_approval", "ai_suggested"))


def get_page(doc_id, page_no):
    """Authored page content, or None if that page was not indexed.
    Unindexed pages are shown honestly rather than faked."""
    doc = DOCUMENTS.get(doc_id)
    if not doc:
        return None
    return doc["pages"].get(int(page_no))
