import os

cursos_dir = "/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos"

target_block = """        @media (max-width:560px) {
            .highlights-strip { grid-template-columns:1fr; }
            .hl-item { padding:20px 24px; gap:16px; border-bottom:1px solid #f0f0f0; }
            .hl-item:last-child { border-bottom:none; }
            .hl-item::after { display:none; }
            .course-title { font-size:1.8rem; }
            .trust-badges { flex-direction:column !important; align-items:center !important; gap:10px !important; transform:scale(0.85); }
        }"""

replacement_block = """        @media (max-width:560px) {
            .highlights-strip { grid-template-columns:1fr; }
            .hl-item { padding:20px 24px; gap:16px; border-bottom:1px solid #f0f0f0; }
            .hl-item:last-child { border-bottom:none; }
            .hl-item::after { display:none; }
            .course-title { font-size:1.8rem; }
            .trust-badges { flex-direction:column !important; align-items:center !important; gap:10px !important; transform:scale(0.85); }
        }

        /* Optimization for ultra-compact mobile screens (iPhone SE & smaller) */
        @media (max-width:375px) {
            .course-title { font-size:1.6rem !important; }
            .trust-badges { gap:8px !important; width: 100% !important; align-items: center !important; }
            .trust-badge {
                padding: 6px 12px 6px 6px !important;
                border-radius: 16px !important;
                width: 100% !important;
                max-width: 280px !important;
                justify-content: flex-start !important;
                margin: 0 auto !important;
            }
            .badge-logo-container {
                width: 40px !important;
                height: 40px !important;
                border-radius: 10px !important;
                padding: 6px !important;
            }
            .badge-title { font-size: 0.75rem !important; }
            .badge-sub { font-size: 0.65rem !important; }
            .hero-pill { padding: 10px 18px !important; font-size: 0.8rem !important; }
        }"""

for filename in os.listdir(cursos_dir):
    if filename.endswith(".html"):
        filepath = os.path.join(cursos_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        modified = False
        if target_block in content:
            content = content.replace(target_block, replacement_block)
            modified = True
        else:
            print(f"Target block not found in {filename}")
            
        if modified:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Successfully applied iPhone SE optimizations to {filename}")
        else:
            print(f"No changes made to {filename}")
