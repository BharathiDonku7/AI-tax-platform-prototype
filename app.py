"""
GreenGrowth CPAs - AI Engineer Case Study
Challenges 01 (Source Document Traceability), 08 (Clickable vs. Editable),
and 10 (Trustworthy AI).

Flask + Jinja2 + Tailwind + Alpine.js, chosen to match the Python/Flask/
PostgreSQL monolith described in the role.

Nothing here is a real system. See mock_data.py and README.md.
"""

from flask import Flask, render_template, jsonify, request, redirect, url_for
import mock_data as md

app = Flask(__name__)


@app.context_processor
def inject_globals():
    return {
        "STATES": md.STATES,
        "DOCUMENTS": md.DOCUMENTS,
        "confidence_band": md.confidence_band,
    }


@app.template_filter("money")
def money(v):
    if v is None:
        return "\u2014"
    neg = v < 0
    s = f"${abs(v):,.2f}"
    return f"({s})" if neg else s


def _enrich(f):
    """Attach everything the trust panel and viewer need for one field."""
    out = dict(f)
    out["band"] = md.confidence_band(f["confidence"])
    out["state_meta"] = md.STATES[f["state"]]

    if f["source_doc"]:
        doc = md.DOCUMENTS[f["source_doc"]]
        out["doc_meta"] = {k: doc[k] for k in
                           ("id", "name", "kind", "uploaded_by", "uploaded_at", "page_count")}
        out["doc_meta"]["indexed_pages"] = sorted(doc["pages"].keys())
        out["doc_short"] = doc["short"]

    for e in out.get("evidence", []):
        e["doc_name"] = md.DOCUMENTS[e["doc"]]["name"] if e.get("doc") else None

    for c in out.get("conflicts", []):
        cd = md.DOCUMENTS[c["competing_doc"]]
        c["competing_doc_name"] = cd["name"]
        c["competing_doc_short"] = cd["short"]

    if out.get("transformation"):
        for s in out["transformation"]["steps"]:
            s["doc_name"] = md.DOCUMENTS[s["doc"]]["name"] if s.get("doc") else None
    return out


@app.route("/")
def index():
    return redirect(url_for("review"))


@app.route("/review")
def review():
    """Challenges 01 + 08: return review with row-level source tracing."""
    index = [{"id": f["id"], "state": f["state"], "section": f["section"],
              "hay": (f["label"] + " " + f["line"] + " " + f["section"]).lower()}
             for f in md.FIELDS]
    return render_template(
        "review.html",
        field_index=index,
        sections=md.fields_by_section(),
        counts=md.summary_counts(),
        open_items=md.open_items(),
        total_fields=len(md.FIELDS),
        doc_count=len(md.DOCUMENTS),
        active_page="review",
    )


@app.route("/queue")
def queue():
    """Second surface proving the affordance system holds across contexts --
    Challenge 08 explicitly asks for more than one screen."""
    return render_template(
        "queue.html",
        queue=md.review_queue(),
        counts=md.summary_counts(),
        active_page="queue",
    )


@app.route("/legend")
def legend():
    return render_template("legend.html", active_page="legend")


@app.route("/api/field/<field_id>")
def api_field(field_id):
    f = md.get_field(field_id)
    if not f:
        return jsonify({"error": "not found"}), 404
    return jsonify(_enrich(f))


@app.route("/api/doc/<doc_id>/page/<int:page_no>")
def api_doc_page(doc_id, page_no):
    """Serves one rendered page of a source document.

    In a real build this would return page geometry from an extraction store.
    Here it returns hand-authored rows. Pages outside the authored set return
    indexed=False so the UI can say so honestly instead of faking content.
    """
    doc = md.DOCUMENTS.get(doc_id)
    if not doc:
        return jsonify({"error": "not found"}), 404
    page = md.get_page(doc_id, page_no)
    return jsonify({
        "doc_id": doc_id,
        "doc_name": doc["name"],
        "doc_kind": doc["kind"],
        "uploaded_at": doc["uploaded_at"],
        "page_count": doc["page_count"],
        "page_no": page_no,
        "indexed": page is not None,
        "indexed_pages": sorted(doc["pages"].keys()),
        "page": page,
    })


@app.route("/api/field/<field_id>/override", methods=["POST"])
def api_override(field_id):
    """Challenge 10: correcting the AI without losing what it originally said.

    The override is appended to history and the field flips to 'verified'.
    The AI's original value and rationale are never deleted -- that record is
    the audit trail, and under Sec. 280E scrutiny it is the whole point.
    Mutates an in-memory dict; resets on restart.
    """
    f = md.get_field(field_id)
    if not f:
        return jsonify({"error": "not found"}), 404
    if f["state"] == "locked":
        return jsonify({"error": "locked", "reason": f["lock_reason"]}), 409

    payload = request.get_json(force=True)
    try:
        new_value = float(payload.get("value", f["value"]))
    except (TypeError, ValueError):
        return jsonify({"error": "invalid value"}), 400
    reason = (payload.get("reason") or "").strip() or "No reason provided."

    f["override_history"].append({
        "from": f["value"], "to": new_value, "by": "You (Preparer)",
        "at": "just now", "reason": reason,
    })
    f["value"] = new_value
    f["source_type"] = "manual"
    f["state"] = "verified"
    f["confidence"] = None
    return jsonify({"ok": True, "counts": md.summary_counts(),
                    "open_items": md.open_items(), "field": _enrich(f)})


@app.route("/api/field/<field_id>/resolve", methods=["POST"])
def api_resolve(field_id):
    """Conflict resolution: accept one of the competing values."""
    f = md.get_field(field_id)
    if not f or not f["conflicts"]:
        return jsonify({"error": "no conflict"}), 400
    payload = request.get_json(force=True)
    chosen = float(payload["value"])
    note = payload.get("reason", "Conflict resolved by preparer.")
    f["override_history"].append({
        "from": f["value"], "to": chosen, "by": "You (Preparer)",
        "at": "just now", "reason": note,
    })
    f["value"] = chosen
    f["state"] = "verified"
    f["conflicts"] = []
    f["confidence"] = None
    f["source_type"] = "manual"
    return jsonify({"ok": True, "counts": md.summary_counts(),
                    "open_items": md.open_items(), "field": _enrich(f)})


@app.route("/api/field/<field_id>/accept", methods=["POST"])
def api_accept(field_id):
    """Accept the AI's value as-is. A preparer doing this two hundred times a
    day needs one click, not a dialog."""
    f = md.get_field(field_id)
    if not f:
        return jsonify({"error": "not found"}), 404
    if f["state"] == "locked":
        return jsonify({"error": "locked", "reason": f["lock_reason"]}), 409
    if f["conflicts"]:
        return jsonify({"error": "resolve conflict first"}), 409
    f["state"] = "verified"
    return jsonify({"ok": True, "counts": md.summary_counts(),
                    "open_items": md.open_items(), "field": _enrich(f)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
