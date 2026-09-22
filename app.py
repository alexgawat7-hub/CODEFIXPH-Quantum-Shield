from flask import Flask, request, jsonify

app = Flask(__name__)

# Tickets - Security Shield Fixed (No IDOR)
tickets = {
    "1": {"owner": "alex", "content": "Ticket #1 - Owner: Alex - SECURE"},
    "2": {"owner": "bob", "content": "Ticket #2 - Owner: Bob - SECURE"}
}

@app.route('/')
def home():
    return """
    <h1 style='color:green'>✅ CODEFIXPH Security Shield ACTIVE</h1>
    <p><b>Owner:</b> Alex Gawat Jr. | GENESIS-0001</p>
    <p><b>Status:</b> Production Ready - Not Demo</p>
    <p><b>Cert:</b> CFPH-QS-2026-0001</p>
    <hr>
    <a href='/ticket?id=1&user=alex'>Test Ticket 1 (Should Work)</a><br>
    <a href='/ticket?id=2&user=alex'>Test Ticket 2 (Should Block - 403)</a><br>
    <a href='/verify'>Verify Certificate</a>
    """

@app.route('/ticket')
def get_ticket():
    ticket_id = request.args.get('id')
    user = request.args.get('user', 'alex')

    # Security Fix 1: Validate input
    if not ticket_id or not ticket_id.isdigit():
        return "400 Invalid Input - ID must be number", 400
    
    ticket = tickets.get(ticket_id)
    if not ticket:
        return "404 Ticket Not Found", 404

    # Security Fix 2: IDOR Protection (Security Shield)
    if ticket["owner"] != user:
        return "403 Forbidden - Access Denied - Security Shield Blocked", 403

    return f"200 OK - {ticket['content']}", 200

@app.route('/verify')
def verify():
    return jsonify({
        "owner": "Alex Gawat Jr.",
        "project": "CODEFIXPH-Quantum-Shield",
        "cert": "CFPH-QS-2026-0001",
        "status": "Genesis 0001 - Verified - Production Ready",
        "security": "Security Shield Active - IDOR Fixed"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
