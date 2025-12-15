import os
import datetime

# --- CONFIGURATION ---
BASE_URL = "https://holosec.tech"
TODAY = datetime.date.today().isoformat()

def main():
    print("[*] Initializing Cartography Sequence...")
    
    # 1. Start the XML structure
    sitemap_content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    # 2. Add Main Pages
    core_pages = ["", "transmissions.html"] 
    for page in core_pages:
        url = f"{BASE_URL}/{page}"
        if page == "": url = BASE_URL 
        
        entry = f"""    <url>
        <loc>{url}</loc>
        <lastmod>{TODAY}</lastmod>
        <priority>1.0</priority>
    </url>"""
        sitemap_content.append(entry)

    # 3. Add the 100 Transmissions
    folder = "transmissions"
    if os.path.exists(folder):
        files = [f for f in os.listdir(folder) if f.endswith('.html')]
        files.sort()
        
        print(f"[*] Mapping {len(files)} transmission routes...")
        
        for filename in files:
            url = f"{BASE_URL}/transmissions/{filename}"
            entry = f"""    <url>
        <loc>{url}</loc>
        <lastmod>{TODAY}</lastmod>
        <priority>0.8</priority>
    </url>"""
            sitemap_content.append(entry)

    # 4. Close and Save
    sitemap_content.append('</urlset>')
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_content))
        
    print(f"[SUCCESS] sitemap.xml generated. The Map is ready.")

if __name__ == "__main__":
    main()