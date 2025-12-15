import os
import re

# CONFIGURATION
FOLDER = "transmissions"

def extract_title(filepath):
    # This grabs the text inside the <h1> tag so the link looks nice
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'<h1>(.*?)</h1>', content)
            if match:
                return match.group(1)
    except:
        pass
    return None

def main():
    print("[*] SCANNING FOR SURVIVORS...")
    
    # 1. FIND ONLY THE FILES THAT ACTUALLY EXIST
    files = [f for f in os.listdir(FOLDER) if f.endswith('.html')]
    files.sort()
    
    print(f"   > Found {len(files)} actual files. (These will be your menu)")

    # 2. BUILD THE NEW MENU LINKS
    menu_links = []
    for filename in files:
        # Get the ID number (e.g., 042)
        try:
            id_num = filename.split('_')[1].split('.')[0]
        except:
            id_num = "???"
            
        # Get the Title from inside the file
        filepath = os.path.join(FOLDER, filename)
        real_title = extract_title(filepath)
        display_title = real_title if real_title else f"Transmission_{id_num}"
        
        # Make the link
        link = f'<div class="log-entry"><span style="color:#555">[{id_num}]</span> <a href="transmissions/{filename}">{display_title}</a></div>'
        menu_links.append(link)

    # 3. OVERWRITE THE OLD MENU FILE
    menu_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>HoloSec // Archives</title>
    <link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <script src="https://gumroad.com/js/gumroad.js"></script>
    <style>
        body {{ background-color: #050505; color: #00FF41; font-family: 'Share Tech Mono', monospace; padding: 5%; }}
        h1 {{ font-size: 3rem; margin-bottom: 40px; border-bottom: 2px solid #222; padding-bottom: 20px; }}
        .log-entry {{ margin-bottom: 12px; border-bottom: 1px solid #111; padding: 8px; transition: 0.2s; }}
        .log-entry:hover {{ background: #111; padding-left: 15px; }}
        a {{ color: #e0e0e0; text-decoration: none; font-size: 1.1rem; }}
        a:hover {{ color: #00FF41; }}
        .back-btn {{ position: fixed; top: 20px; right: 20px; border: 1px solid #00FF41; padding: 10px; background: #000; color: #00FF41; text-decoration: none; }}
        .back-btn:hover {{ background: #00FF41; color: #000; }}
        .stats {{ color: #444; margin-bottom: 40px; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <a href="index.html" class="back-btn">RETURN TO ENGINE</a>
    <h1>// KNOWLEDGE_BASE</h1>
    <div class="stats">
        SECTORS_ACTIVE: {len(files)}<br>
        SECURITY_LEVEL: MAXIMUM
    </div>
    
    {''.join(menu_links)}
    
    <br><br>
    <div style="text-align:center; color:#333; margin-top:50px;">
        HOLOSEC SECURE ARCHIVE // END OF LINE
    </div>
</body>
</html>
"""
    with open("transmissions.html", "w", encoding="utf-8") as f:
        f.write(menu_html)
    print(f"   > SUCCESS. Menu updated to match the {len(files)} files.")

if __name__ == "__main__":
    main()