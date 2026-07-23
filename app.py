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
        return "—"
    neg = v < 0
    s = f"${abs(v):,.2f}"
    return f"({s})" if neg else s


@app.route("/")
def index():
    return redirect(url_for("review"))


@app.route("/review")
def review():
    """Challenge 01 + 08: the return review screen with side-by-side tracing."""
    return render_template(
        "review.html",
        fields=md.FIELDS,
        queue=md.review_queue(),
        counts=md.summary_counts(),
        active_page="review",
    )


@app.route("/queue")
def queue():
    """Second surface proving the affordance system holds across screens
    (Challenge 08 explicitly asks for more than one context)."""
    return render_template(
        "queue.html",
        queue=md.review_queue(),
        counts=md.summary_counts(),
        active_page="queue",
    )


@app.route("/legend")
def legend():
    """The interaction system documented as a living reference."""
    return render_template("legend.html", active_page="legend")


@app.route("/api/field/<field_id>")
def api_field(field_id):
    """Powers the trace panel. In a real build this would join return fields
    against an extraction store; here it reads a Python dict."""
    f = md.get_field(field_id)
    if not f:
        return jsonify({"error": "not found"}), 404
    out = dict(f)
    out["band"] = md.confidence_band(f["confidence"])
    out["state_meta"] = md.STATES[f["state"]]
    if f["source_doc"]:
        out["doc_meta"] = md.DOCUMENTS[f["source_doc"]]
    for e in out.get("evidence", []):
        e["doc_name"] = md.DOCUMENTS[e["doc"]]["name"] if e.get("doc") else None
    for c in out.get("conflicts", []):
        c["competing_doc_name"] = md.DOCUMENTS[c["competing_doc"]]["name"]
    if out.get("transformation"):
        for s in out["transformation"]["steps"]:
            s["doc_name"] = md.DOCUMENTS[s["doc"]]["name"] if s.get("doc") else None
    return jsonify(out)


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
    new_value = float(payload.get("value", f["value"]))
    reason = (payload.get("reason") or "").strip() or "No reason provided."

    f["override_history"].append({
        "from": f["value"],
        "to": new_value,
        "by": "You (Preparer)",
        "at": "just now",
        "reason": reason,
    })
    f["value"] = new_value
    f["source_type"] = "manual"
    f["state"] = "verified"
    f["confidence"] = None
    return jsonify({"ok": True, "counts": md.summary_counts()})


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
    return jsonify({"ok": True, "counts": md.summary_counts()})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
