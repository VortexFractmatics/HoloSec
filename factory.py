import os
import google.generativeai as genai
import time

# --- CONFIGURATION ---
# !!! PASTE YOUR API KEY INSIDE THE QUOTES BELOW !!!
API_KEY = "AIzaSyBjeQhHQ_uH4oyTvDJgbFU52k1WT7TIa8A" 

# The Tesla Number. 
TOTAL_POSTS = 369 

# Safety Delay: 4 seconds between requests prevents Google from blocking you.
# Do not lower this number for a batch this size.
SLEEP_TIMER = 4

genai.configure(api_key=API_KEY)
# Using the high-speed Flash engine
model = genai.GenerativeModel('gemini-2.5-flash')

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

# NOTE: Gumroad script is injected here for every page
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
    .gumroad-button { 
        background-color: transparent !important; 
        color: #00FF41 !important; 
        border: 1px solid #00FF41 !important;
        font-family: 'Courier New', monospace !important;
    }
    .gumroad-button:hover {
        background-color: #00FF41 !important;
        color: #000 !important;
        box-shadow: 0 0 15px #00FF41;
    }
</style>
"""

def generate_topics(count):
    print(f"[*] Asking Gemini to access the HoloSec Encyclopedia for {count} topics...")
    # We ask for batches to handle the large number
    topics = []
    batch_size = 20
    
    for i in range(0, count, batch_size):
        print(f"   > Generating batch {i} to {i+batch_size}...")
        prompt = f"""
        Read these EXTENSIVE Product Specs:
        {PRODUCT_SPECS}
        
        Generate {batch_size} unique, highly specific, "click-worthy" blog post titles. 
        Focus on specific user problems (e.g. "How to hide blueprints", "The truth about Bitlocker").
        Format: Just the titles, one per line. No numbers.
        """
        try:
            response = model.generate_content(prompt)
            batch_topics = response.text.strip().split('\n')
            topics.extend(batch_topics)
            time.sleep(2) # Short pause between topic batches
        except Exception as e:
            print(f"Error generating topics: {e}")
            
    return topics[:count] # Ensure we return exactly the requested amount

def write_article(title):
    print(f"[*] Compiling Data for: {title}...")
    prompt = f"""
    ROLE: You are the Lead Architect of HoloSec.
    INPUT DATA: {PRODUCT_SPECS} {MANIFESTO}
    TASK: Write a 'Deep Dive' transmission about "{title}".
    REQUIREMENTS:
    1. BE SPECIFIC: Explain HOW HoloSec solves this specific problem using the specs.
    2. THE ENEMY: Explain why Cloud/Big Tech fails here.
    3. CALL TO ACTION: Tell them to secure their data now.
    OUTPUT FORMAT: HTML body content only (use <h2>, <p>, <ul>).
    """
    try:
        # THE SAFETY DELAY
        time.sleep(SLEEP_TIMER) 
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

    print(f"[*] Starting Production Run: {len(topics)} Articles.")

    for i, topic in enumerate(topics):
        if not topic.strip(): continue
        
        filename = f"log_{i+1:03d}.html"
        content = write_article(topic)
        
        # HTML Template with Gumroad Script injected in HEAD
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>HoloSec // {topic}</title>
            {CSS}
            <script src="https://gumroad.com/js/gumroad.js"></script>
        </head>
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
                <center>
                    <a class="gumroad-button" href="https://holosec.gumroad.com/l/oemsfb?wanted=true" target="_blank" style="font-size:1.2em; padding:15px; display:inline-block; text-decoration:none;">
                        [ ACCESS THE FORTRESS ]
                    </a>
                </center>
            </div>
        </body>
        </html>
        """
        
        with open(f"transmissions/{filename}", "w", encoding="utf-8") as f:
            f.write(html)
        
        links.append(f'<div class="log-entry"><span style="color:#555">[{i+1:03d}]</span> <a href="transmissions/{filename}">{topic}</a></div>')
        
        # Progress update every 10 posts
        if (i+1) % 10 == 0:
            print(f"   >>> {i+1}/{TOTAL_POSTS} Completed.")

    # Hub Template with Gumroad Script
    hub_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>HoloSec // Transmissions</title>
        <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
        <script src="https://gumroad.com/js/gumroad.js"></script>
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
        <p>TOTAL_RECORDS: {len(links)}</p>
        <br>
        {''.join(links)}
    </body>
    </html>
    """
    
    with open("transmissions.html", "w", encoding="utf-8") as f:
        f.write(hub_html)

    print(f"\n[SUCCESS] The Universe Key (369) is generated. Deployment ready.")

if __name__ == "__main__":
    main()