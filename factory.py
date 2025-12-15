import os
import google.generativeai as genai
import time

# --- CONFIGURATION ---
# !!! PASTE YOUR API KEY HERE !!!
API_KEY = "PASTE_YOUR_KEY_HERE" 

# Set this to 100 when you are ready for the full flood.
TOTAL_POSTS = 10 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

# --- THE ENCYCLOPEDIA (GOD MODE DATA) ---

PRODUCT_SPECS = """
PRODUCT NAME: HoloSec // The Digital Fortress
TYPE: Quantum-Resistant, Air-Gapped Encryption Suite.
ARCHITECT: The Vortex (VortexFractmatics).

CORE ENGINES:
1. "Dynamic Geometry": Keys are not static strings; they are rotating geometric constructs.
2. "Swarm Entropy": Uses biological mouse movement + atmospheric noise to generate keys.
3. "The Void Protocol": Data is not just encrypted; it is obfuscated to look like random white noise.

ADVANCED DEFENSE FEATURES:
- "Duress Mode": If forced to unlock your vault at gunpoint, type your 'Duress Password'. It opens a fake, empty vault.
- "Steganographic Injection": Hide sensitive text files inside innocent-looking JPG images.
- "Dead Man's Switch": If the vault isn't opened for X days, it self-incinerates (optional).
- "Key Sharding": Split your master key into 5 QR codes. You need 3 to unlock. (Shamir's Secret Sharing).
- "Decoy Containers": Create dummy volumes to distract forensic analysis.
- "Panic Button": One-click lockdown that unmounts all drives and clears RAM instantly.
- "Plausible Deniability": The encrypted volume has no file header. It looks like empty disk space.

USE CASES (TARGET MARKETS):
- CRYPTO WHALES: Cold storage for seed phrases. No cloud leaks.
- JOURNALISTS: Protecting sources. Transporting leaks across borders.
- ENGINEERS: Securing IP, blueprints, and CAD files from corporate espionage.
- LAWYERS/DOCTORS: HIPAA/GDPR compliance without trusting Microsoft/Google.
- DEVELOPERS: Storing API keys and .env files locally.
- SOUND DESIGNERS: Protecting unreleased stems and "Magnum Opus" projects.
- PREPPERS: Digital survival kits (maps, manuals, IDs) on a USB drive.

THE COMPETITIVE EDGE:
- BitLocker has a backdoor for recovery. We do not.
- Cloud storage (Dropbox/Drive) scans your files. We do not.
- Password Managers (LastPass) get hacked. We are offline.
"""

MANIFESTO = """
PHILOSOPHY:
We are building the 'Ark' for the digital flood.
Sovereignty is not given; it is encrypted.
The user is the only admin. There is no 'Forgot Password'. There is no help desk.
There is only Mathematics and Willpower.
"""

CSS = """
<style>
    body { background-color: #050505; color: #e0e0e0; font-family: 'Courier New', monospace; padding: 20px; }
    h1 { color: #00FF41; text-transform: uppercase; border-bottom: 1px solid #333; padding-bottom: 10px; }
    .terminal-box { border: 1px solid #333; padding: 20px; background: rgba(10,10,10,0.8); max-width: 800px; margin: 0 auto; }
    a { color: #00FF41; text-decoration: none; font-weight: bold; }
    a:hover { background: #00FF41; color: black; }
    .meta { color: #555; font-size: 0.8rem; margin-bottom: 20px; }
    .content { line-height: 1.6; }
    .spec-box { border: 1px dashed #555; padding: 10px; margin-top: 20px; background: #111; font-size: 0.9em; }
    li { margin-bottom: 10px; }
</style>
"""

def generate_topics(count):
    print(f"[*] Asking Gemini to access the HoloSec Encyclopedia...")
    prompt = f"""
    Read these EXTENSIVE Product Specs:
    {PRODUCT_SPECS}
    
    Generate {count} unique, highly specific blog post titles that show off the diversity of this tool.
    Mix it up:
    - Some for "Paranoid Preppers" (Dead Man's Switch).
    - Some for "Corporate Spies" (Steganography).
    - Some for "Crypto Traders" (Key Sharding).
    - Some purely technical (Dynamic Geometry).
    
    Format: Just the titles, one per line.
    """
    response = model.generate_content(prompt)
    return response.text.strip().split('\n')

def write_article(title):
    print(f"[*] Compiling Data for: {title}...")
    prompt = f"""
    ROLE: You are the Lead Architect of HoloSec.
    
    INPUT DATA:
    {PRODUCT_SPECS}
    {MANIFESTO}
    
    TASK: Write a 'Deep Dive' transmission about "{title}".
    
    REQUIREMENTS:
    1. BE SPECIFIC: Don't just say "it's secure." Explain HOW (e.g., "The Duress Mode creates a cryptographic fork...").
    2. USE THE FEATURES: Reference the specific features in the specs (Decoys, Sharding, Geometry).
    3. THE ENEMY: Explain why the "Old World" (Cloud, Big Tech) cannot do this.
    
    OUTPUT FORMAT: HTML body content only (use <h2>, <p>, <ul>).
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[!] Error: {e}")
        return "<p>Signal Lost.</p>"

def main():
    if not os.path.exists("transmissions"):
        os.makedirs("transmissions")

    topics = generate_topics(TOTAL_POSTS)
    links = []

    for i, topic in enumerate(topics):
        if not topic.strip(): continue
        filename = f"log_{i+1:03d}.html"
        content = write_article(topic)
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head><title>HoloSec // {topic}</title>{CSS}</head>
        <body>
            <div class="nav"><a href="../index.html"><< RETURN TO ROOT</a></div>
            <br><br>
            <div class="terminal-box">
                <h1>{topic}</h1>
                <div class="meta">ID: {i+1:03d} // CLEARANCE: BLACK_BOX</div>
                <div class="content">
                    {content}
                    <div class="spec-box">
                        <strong>ARCHIVE DATA:</strong><br>
                        > MODULE: {topic.split(':')[0]}<br>
                        > PROTOCOL: Zero-Knowledge<br>
                        > STATUS: <span style="color:#00FF41">ACTIVE</span>
                    </div>
                </div>
                <br><br>
                <center><a href="https://holosec.gumroad.com/l/oemsfb" style="font-size:1.2em; border:2px solid #00FF41; padding:15px; display:inline-block;">ACCESS THE FORTRESS</a></center>
            </div>
        </body>
        </html>
        """
        with open(f"transmissions/{filename}", "w", encoding="utf-8") as f:
            f.write(html)
        links.append(f'<div class="log-entry"><span style="color:#555">[{i+1:03d}]</span> <a href="transmissions/{filename}">{topic}</a></div>')
        time.sleep(2)

    hub_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>HoloSec // Transmissions</title>
        <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
        <style>
            body {{ background-color: #050505; color: #00FF41; font-family: 'Share Tech Mono', monospace; padding: 5%; }}
            h1 {{ font-size: 3rem; margin-bottom: 40px; }}
            .log-entry {{ margin-bottom: 10px; border-bottom: 1px solid #222; padding: 5px; }}
            a {{ color: #e0e0e0; text-decoration: none; }}
            a:hover {{ color: #00FF41; background: #111; }}
            .back-btn {{ position: fixed; top: 20px; right: 20px; border: 1px solid #00FF41; padding: 10px; }}
        </style>
    </head>
    <body>
        <a href="index.html" class="back-btn">RETURN TO ENGINE</a>
        <h1>// KNOWLEDGE_BASE</h1>
        <p>THE COMPLETE ARCHIVE OF DIGITAL SOVEREIGNTY.</p>
        <br>
        {''.join(links)}
    </body>
    </html>
    """
    with open("transmissions.html", "w", encoding="utf-8") as f:
        f.write(hub_html)
    print(f"\n[SUCCESS] Encyclopedia Generated. {len(links)} entries created.")

if __name__ == "__main__":
    main()