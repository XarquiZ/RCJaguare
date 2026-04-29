import os
import re

social_html = """                <div class="nav-social">
                    <a href="https://www.instagram.com/cedespjaguare/" target="_blank" class="nav-social-link" aria-label="Instagram">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="nav-social-icon"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg>
                    </a>
                    <a href="https://www.tiktok.com/@cedesp.jaguar?_r=1&_t=ZS-95mfSbp6soq" target="_blank" class="nav-social-link" aria-label="TikTok">
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" class="nav-social-icon" viewBox="0 0 16 16">
                            <path d="M9 0h1.98c.144.715.54 1.617 1.235 2.512C12.895 3.389 13.797 4 15 4v2c-1.753 0-3.07-.814-4-1.829V11a5 5 0 1 1-5-5v2a3 3 0 1 0 3 3V0Z"/>
                        </svg>
                    </a>
                </div>
"""

footer_social_html = """                <div class="footer-social" style="display: flex; gap: 15px; margin: 15px 0;">
                    <a href="https://www.instagram.com/cedespjaguare/" target="_blank" aria-label="Instagram" style="color: white; opacity: 0.8; transition: 0.3s;"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line></svg></a>
                    <a href="https://www.tiktok.com/@cedesp.jaguar?_r=1&_t=ZS-95mfSbp6soq" target="_blank" aria-label="TikTok" style="color: white; opacity: 0.8; transition: 0.3s;"><svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" fill="currentColor" viewBox="0 0 16 16"><path d="M9 0h1.98c.144.715.54 1.617 1.235 2.512C12.895 3.389 13.797 4 15 4v2c-1.753 0-3.07-.814-4-1.829V11a5 5 0 1 1-5-5v2a3 3 0 1 0 3 3V0Z"/></svg></a>
                </div>
"""

def update_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Avoid duplicate additions
    if 'class="nav-social"' in content:
        return

    # Navbar Actions
    if '<div class="nav-actions">' in content:
        new_content = content.replace('<div class="nav-actions">', '<div class="nav-actions">\n' + social_html)
        
        # Footer Actions (different versions might exist)
        if '<div class="footer-social"' in new_content:
             # Replace existing footer social
             new_content = re.sub(r'<div class="footer-social".*?</div>', footer_social_html, new_content, flags=re.DOTALL)
        else:
             # Add if missing (before WhatsApp button)
             if 'class="btn btn-whatsapp"' in new_content:
                 new_content = new_content.replace('<a href="https://wa.me/5511972423702', footer_social_html + '                <a href="https://wa.me/5511972423702')

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {file_path}")

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".html"):
            update_file(os.path.join(root, file))
