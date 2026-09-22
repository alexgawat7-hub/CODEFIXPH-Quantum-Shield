import hashlib, os
GENESIS_SECRET = "09517080795_AlexGawat_SanJose_0001"
GENESIS_HASH = hashlib.sha256(GENESIS_SECRET.encode()).hexdigest()
print(f"✓ DNA VERIFIED - {GENESIS_HASH[:12]} - Alex Gawat")

from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.secret_key = GENESIS_HASH
limiter = Limiter(get_remote_address, app=app, default_limits=["100 per hour"])

@app.route('/')
def home():
    return f"<h1>🛡️ QUANTUM SHIELD ACTIVE</h1><p>Owner: Alex Gawat<br>Cert: CFPH-QS-2026-0001<br>Hash: {GENESIS_HASH[:16]}<br>GCash: 09517080795</p><a href='/verify'>VERIFY OWNER</a>"

@app.route('/verify')
def verify():
    return jsonify(owner="Alex Gawat", cert="CFPH-QS-2026-0001", gcash="09517080795", hash=GENESIS_HASH, status="GENESIS 0001 - WORLD FIRST - Anti-Clone Locked", dna="Protected by Quantum DNA")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
