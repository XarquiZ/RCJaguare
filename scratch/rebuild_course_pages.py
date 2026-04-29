#!/usr/bin/env python3
"""
rebuild_course_pages.py — 9 course pages with unique palettes +
per-course orbital logo animation system.
"""
import os, math

BASE = "/Users/wellintonbatista/Documents/projetos/RCJaguare/cursos"

# ══════════════════════════════════════════════════════════════
# ORBITAL SYSTEM GENERATOR
# ══════════════════════════════════════════════════════════════

def make_orbit(hero_logos, accent, accent_rgb):
    """
    Generates the orbit visual HTML + per-logo CSS keyframes.
    Inner orbit (R=110px, 10s CW) and outer orbit (R=175px, 17s CCW).
    Uses translate-only animation so logos stay perfectly upright.
    """
    n = len(hero_logos)
    if n <= 2:
        inner, outer = hero_logos, []
    elif n <= 4:
        inner, outer = hero_logos[:2], hero_logos[2:]
    else:
        inner, outer = hero_logos[:2], hero_logos[2:5]

    keyframes = []
    logos_html = []

    def add(lf, la, radius, period, phase_deg, direction):
        ph = math.radians(phase_deg)
        pts = {}
        for p in [0, 25, 50, 75, 100]:
            a = ph + direction * math.radians(p / 100 * 360)
            pts[p] = (round(radius * math.sin(a), 1), round(-radius * math.cos(a), 1))
        safe = lf.replace(".", "_").replace("-", "_")
        d = "cw" if direction > 0 else "ccw"
        name = f"orb_{safe}_{int(phase_deg)}_{d}"
        kf = f"@keyframes {name} {{\n"
        for p, (x, y) in pts.items():
            kf += f"    {p}% {{ transform: translate({x}px, {y}px); }}\n"
        kf += "}"
        keyframes.append(kf)
        logos_html.append(
            f'            <div class="o-logo" style="animation:{name} {period}s linear infinite;">'
            f'<img src="logos/{lf}" alt="{la}"></div>'
        )

    for i, (lf, la) in enumerate(inner):
        add(lf, la, 110, 10, i * (360 / max(len(inner), 1)), 1)
    for i, (lf, la) in enumerate(outer):
        add(lf, la, 175, 17, i * (360 / max(len(outer), 1)), -1)

    html = (
        '            <div class="orbit-system">\n'
        '                <div class="o-ring o-ring-inner"></div>\n'
        '                <div class="o-ring o-ring-outer"></div>\n'
        '                <div class="o-core"></div>\n'
        + "\n".join(logos_html) + "\n"
        '            </div>'
    )
    return html, "\n\n".join(keyframes)


# ══════════════════════════════════════════════════════════════
# SHARED CSS
# ══════════════════════════════════════════════════════════════

def make_css(hero_grad, accent, accent_rgb, accent_light, extra_keyframes):
    return f"""        /* ── Course tokens ── */
        :root {{--c-accent:{accent};--c-rgb:{accent_rgb};--c-light:{accent_light};}}

        /* ── HERO ── */
        .course-hero {{
            background:{hero_grad};
            padding:150px 0 0; position:relative; overflow:hidden;
        }}
        .course-hero::after {{
            content:''; position:absolute; inset:0; pointer-events:none;
            background:radial-gradient(ellipse 80% 55% at 80% 20%,rgba(255,255,255,0.07),transparent 70%),
                       radial-gradient(ellipse 50% 70% at 10% 85%,rgba(0,0,0,0.18),transparent 60%);
        }}
        .hero-grid {{
            display:grid; grid-template-columns:1fr 1fr; gap:60px;
            align-items:center; position:relative; z-index:2; padding-bottom:90px;
        }}

        /* eyebrow — SENAI badge */
        .hero-eyebrow {{
            display:inline-flex; align-items:center; gap:10px;
            background:rgba(255,255,255,0.15); backdrop-filter:blur(10px);
            border:1px solid rgba(255,255,255,0.3);
            padding:8px 20px; border-radius:40px; margin-bottom:28px;
            font-size:0.8rem; font-weight:700; color:white;
            letter-spacing:0.08em; text-transform:uppercase;
        }}
        .hero-eyebrow .senai-img {{
            height:22px; background:white;
            padding:3px 6px; border-radius:6px;
            display:block; object-fit:contain;
        }}

        .course-title {{
            font-size:clamp(2.8rem,5vw,4.4rem);
            font-weight:900; line-height:1.05; margin-bottom:24px;
            color:white; letter-spacing:-0.02em;
        }}
        .course-title .accent{{color:#FFD166;}}
        .course-desc {{
            font-size:1.12rem; line-height:1.78;
            color:rgba(255,255,255,0.88); margin-bottom:40px; max-width:500px;
        }}
        .hero-pills{{display:flex; gap:14px; flex-wrap:wrap;}}
        .hero-pill {{
            display:flex; align-items:center; gap:10px;
            padding:12px 24px; border-radius:50px;
            background:rgba(255,255,255,0.12); border:1.5px solid rgba(255,255,255,0.25);
            font-weight:700; font-size:0.9rem; color:white; backdrop-filter:blur(6px);
        }}
        .hero-pill .pill-value{{font-size:1.1rem; font-weight:900; color:#FFD166; margin-right:2px;}}

        /* ── ORBITAL SYSTEM ── */
        .hero-visual {{
            position:relative; display:flex;
            align-items:center; justify-content:center; min-height:380px;
        }}
        .orbit-system {{
            position:relative; width:380px; height:380px;
            display:flex; align-items:center; justify-content:center;
        }}
        .o-ring {{
            position:absolute; border-radius:50%;
            border:1px solid rgba(255,255,255,0.1);
        }}
        .o-ring-inner {{width:220px; height:220px;}}
        .o-ring-outer {{
            width:350px; height:350px;
            border-style:dashed; border-color:rgba(255,255,255,0.06);
        }}
        .o-core {{
            position:absolute; width:88px; height:88px; border-radius:50%;
            background:radial-gradient(circle at 35% 35%, rgba(255,255,255,0.35), {accent});
            box-shadow:0 0 0 14px rgba({accent_rgb},0.18), 0 0 50px rgba({accent_rgb},0.5);
            animation:corePulse 3.5s ease-in-out infinite;
        }}
        @keyframes corePulse {{
            0%,100% {{transform:scale(1); box-shadow:0 0 0 14px rgba({accent_rgb},0.18),0 0 50px rgba({accent_rgb},0.5);}}
            50%  {{transform:scale(1.1); box-shadow:0 0 0 20px rgba({accent_rgb},0.12),0 0 70px rgba({accent_rgb},0.7);}}
        }}
        .o-logo {{
            position:absolute; top:50%; left:50%;
            margin:-32px 0 0 -32px;
            width:64px; height:64px;
            background:white; border-radius:18px; padding:10px;
            display:flex; align-items:center; justify-content:center;
            box-shadow:0 8px 28px rgba(0,0,0,0.25);
        }}
        .o-logo img{{width:100%; height:100%; object-fit:contain;}}

        /* per-logo orbit keyframes */
        {extra_keyframes}

        /* ── SCROLL HINT ── */
        .scroll-hint {{
            position:absolute; bottom:28px; left:50%;
            transform:translateX(-50%); z-index:4;
            display:flex; flex-direction:column; align-items:center; gap:8px;
            color:rgba(255,255,255,0.6); cursor:pointer;
            animation:scrollFade 2s ease-in-out infinite;
            text-decoration:none;
        }}
        .scroll-hint span {{
            font-size:0.72rem; font-weight:700;
            letter-spacing:0.15em; text-transform:uppercase;
        }}
        .scroll-hint-dots {{
            display:flex; flex-direction:column; align-items:center; gap:4px;
        }}
        .scroll-hint-dots i {{
            width:6px; height:6px; border-radius:50%;
            background:rgba(255,255,255,0.5);
            animation:dotBounce 1.4s ease-in-out infinite;
        }}
        .scroll-hint-dots i:nth-child(2) {{ animation-delay:0.2s; }}
        .scroll-hint-dots i:nth-child(3) {{ animation-delay:0.4s; }}
        @keyframes dotBounce {{
            0%,100% {{ opacity:0.3; transform:scaleY(0.6); }}
            50%      {{ opacity:1;   transform:scaleY(1.4); }}
        }}
        @keyframes scrollFade {{
            0%,100% {{ opacity:0.5; transform:translateX(-50%) translateY(0); }}
            50%      {{ opacity:1;   transform:translateX(-50%) translateY(6px); }}
        }}

        /* ── DIVIDER ── */
        .hero-divider {{
            height:65px; background:white;
            clip-path:ellipse(54% 100% at 50% 100%); margin-top:-1px;
        }}

        /* ── HIGHLIGHTS BRIDGE ── */
        .course-highlights {{
            background:white;
            padding:0 0 2px;
        }}
        .highlights-strip {{
            display:grid; grid-template-columns:repeat(4,1fr);
            border-radius:24px; overflow:hidden;
            box-shadow:0 4px 30px rgba(0,0,0,0.08);
            border:1px solid #f0f0f0;
            margin-bottom:0;
        }}
        .hl-item {{
            padding:32px 28px; display:flex;
            align-items:center; gap:18px;
            background:white; position:relative;
            transition:background 0.25s ease;
        }}
        .hl-item:not(:last-child)::after {{
            content:''; position:absolute; right:0; top:20%; height:60%;
            width:1px; background:#f0f0f0;
        }}
        .hl-item:hover {{ background:var(--c-light); }}
        .hl-icon {{
            width:52px; height:52px; border-radius:16px; flex-shrink:0;
            background:linear-gradient(135deg,{accent},rgba({accent_rgb},0.5));
            display:flex; align-items:center; justify-content:center;
            font-size:1.4rem; box-shadow:0 4px 14px rgba({accent_rgb},0.3);
        }}
        .hl-text {{ display:flex; flex-direction:column; }}
        .hl-value {{
            font-size:1.2rem; font-weight:900; color:var(--dark); line-height:1.1;
        }}
        .hl-label {{
            font-size:0.82rem; color:var(--text-muted); font-weight:500; margin-top:3px;
        }}
        @media (max-width:900px) {{
            .highlights-strip {{ grid-template-columns:repeat(2,1fr); }}
            .hl-item:nth-child(2)::after {{ display:none; }}
        }}
        @media (max-width:560px) {{
            .highlights-strip {{ grid-template-columns:1fr 1fr; }}
            .hl-item {{ padding:24px 18px; gap:12px; }}
        }}

        /* ── BODY ── */
        .course-body{{background:var(--bg-light);}}

        /* ── SECTION HEADER ── */
        .c-section-header{{text-align:center; margin-bottom:60px;}}
        .c-section-tag {{
            display:inline-block; padding:6px 18px; border-radius:40px;
            background:rgba({accent_rgb},0.1); border:1.5px solid rgba({accent_rgb},0.25);
            color:{accent}; font-size:0.78rem; font-weight:800;
            letter-spacing:0.12em; text-transform:uppercase; margin-bottom:16px;
        }}
        .c-section-title{{font-size:2.2rem; font-weight:900; color:var(--dark); line-height:1.15; letter-spacing:-0.01em;}}
        .c-section-sub{{color:var(--text-muted); font-size:1.05rem; margin-top:12px;}}

        /* ── VIDEO ── */
        .c-video-section{{background:white; padding:80px 0;}}
        .c-video-wrap{{max-width:880px; margin:0 auto;}}
        .c-video-placeholder {{
            width:100%; aspect-ratio:16/9;
            background:linear-gradient(135deg,#0f0f1e 0%,#1a102e 100%);
            border-radius:24px; display:flex; flex-direction:column;
            align-items:center; justify-content:center; gap:20px;
            box-shadow:0 25px 60px rgba(0,0,0,0.2); cursor:pointer;
            border:1px solid rgba(255,255,255,0.06); position:relative; overflow:hidden;
            transition:transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .c-video-placeholder::before {{
            content:''; position:absolute; inset:0;
            background:radial-gradient(ellipse at 50% 50%,rgba({accent_rgb},0.18),transparent 70%);
        }}
        .c-video-placeholder:hover{{transform:translateY(-4px); box-shadow:0 35px 70px rgba(0,0,0,0.28);}}
        .c-play-btn {{
            width:84px; height:84px; border-radius:50%; background:{accent};
            box-shadow:0 0 0 14px rgba({accent_rgb},0.2);
            display:flex; align-items:center; justify-content:center;
            transition:all 0.3s ease; position:relative; z-index:1;
        }}
        .c-play-btn svg{{width:32px; height:32px; fill:white; margin-left:6px;}}
        .c-video-placeholder:hover .c-play-btn{{transform:scale(1.1); box-shadow:0 0 0 20px rgba({accent_rgb},0.12);}}
        .c-video-label{{
            color:rgba(255,255,255,0.4); font-size:0.82rem;
            font-weight:600; letter-spacing:0.12em; text-transform:uppercase;
            position:relative; z-index:1;
        }}

        /* ── MODULES ── */
        .c-modules-section{{background:var(--c-light); padding:90px 0;}}
        .c-modules{{display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:28px;}}
        .c-module {{
            background:white; border-radius:20px; padding:36px 32px 32px;
            box-shadow:0 4px 24px rgba(0,0,0,0.06);
            border:1px solid rgba(0,0,0,0.05);
            position:relative; overflow:hidden;
            transition:transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .c-module::before {{
            content:''; position:absolute;
            top:0; left:0; right:0; height:5px;
            background:linear-gradient(90deg,{accent},#FFD166);
        }}
        .c-module:hover{{transform:translateY(-8px); box-shadow:0 20px 50px rgba({accent_rgb},0.18);}}
        .c-module-num {{
            font-size:5rem; font-weight:900; line-height:1;
            color:rgba({accent_rgb},0.07); position:absolute; top:14px; right:22px; user-select:none;
        }}
        .c-module h3{{font-size:1.2rem; font-weight:800; color:var(--dark); margin-bottom:14px; position:relative;}}
        .c-module p{{color:var(--text-muted); font-size:0.97rem; line-height:1.75; position:relative;}}

        /* ── TOOLS ── */
        .c-tools-section{{background:white; padding:90px 0;}}
        .c-tools-grid{{display:flex; flex-wrap:wrap; justify-content:center; gap:16px;}}
        .c-tool {{
            background:#f8fafc; border-radius:16px; padding:18px 28px;
            display:flex; align-items:center; gap:14px;
            border:1.5px solid #eef2f7; transition:all 0.25s ease; cursor:default;
        }}
        .c-tool:hover{{
            background:white; border-color:{accent};
            box-shadow:0 8px 30px rgba({accent_rgb},0.15); transform:translateY(-4px);
        }}
        .c-tool-icon{{width:38px; height:38px; display:flex; align-items:center; justify-content:center; flex-shrink:0;}}
        .c-tool-icon img{{width:100%; height:100%; object-fit:contain;}}
        .c-tool-name{{font-weight:700; color:var(--dark); font-size:0.97rem; white-space:nowrap;}}

        /* ── CTA ── */
        .c-cta-section{{padding:60px 0 100px; background:var(--bg-light);}}
        .c-cta {{
            background:{hero_grad};
            border-radius:32px; padding:90px 40px; text-align:center;
            position:relative; overflow:hidden;
            box-shadow:0 20px 60px rgba(0,0,0,0.22);
        }}
        .c-cta::after {{
            content:''; position:absolute; inset:0;
            background:radial-gradient(ellipse 70% 60% at 80% 30%,rgba(255,255,255,0.08),transparent 70%);
        }}
        .c-cta-inner{{position:relative; z-index:2;}}
        .c-cta h2{{font-size:2.8rem; font-weight:900; margin-bottom:18px; color:white; letter-spacing:-0.02em;}}
        .c-cta p{{font-size:1.2rem; color:rgba(255,255,255,0.87); margin:0 auto 44px; max-width:580px;}}
        .c-cta-btns{{display:flex; gap:20px; justify-content:center; flex-wrap:wrap;}}
        .btn-cta-primary {{
            padding:18px 48px; border-radius:50px; background:#FFD166; color:#1a1a1a;
            font-weight:900; font-size:1rem; letter-spacing:0.02em;
            text-decoration:none; transition:all 0.3s;
            box-shadow:0 10px 30px rgba(255,209,102,0.4); display:inline-block;
        }}
        .btn-cta-primary:hover{{transform:translateY(-3px); box-shadow:0 16px 40px rgba(255,209,102,0.6);}}
        .btn-cta-outline {{
            padding:18px 48px; border-radius:50px;
            background:rgba(255,255,255,0.12); color:white; font-weight:700; font-size:1rem;
            text-decoration:none; border:2px solid rgba(255,255,255,0.4);
            transition:all 0.3s; backdrop-filter:blur(8px); display:inline-block;
        }}
        .btn-cta-outline:hover{{background:rgba(255,255,255,0.22); border-color:white; transform:translateY(-3px);}}

        /* ── RESPONSIVE ── */
        @media (max-width:768px){{
            .hero-grid{{grid-template-columns:1fr; gap:24px; padding-bottom:50px;}}
            .hero-visual{{min-height:260px;}}
            .orbit-system{{transform:scale(0.68); transform-origin:center;}}
            .course-title{{font-size:2.6rem;}}
            .c-cta h2{{font-size:2.1rem;}}
        }}"""


# ══════════════════════════════════════════════════════════════
# SHARED PARTIALS
# ══════════════════════════════════════════════════════════════

def ticker():
    t = "Quebrando barreiras, mudando destinos"
    return f'    <div class="ticker-wrap"><div class="ticker">{"".join(f"""<span class="ticker-item">{t}</span>""" for _ in range(8))}</div></div>'

def nav():
    return """    <nav class="navbar" id="navbar">
        <div class="nav-container">
            <a href="../index.html" class="nav-logo"><img src="../images/logo_rede_comunita.png" alt="CEDESP" class="logo-icon-crop"><span class="logo-text-cedesp">CEDESP</span><span class="logo-wrapper"><span class="logo-highlight">Jaguaré</span></span></a>
            <div class="nav-links"><a href="../historia.html">Nossa História</a><a href="../cursos.html">Cursos</a><a href="../eventos.html">Eventos</a><a href="../calendario.html">Calendário</a></div>
            <div class="nav-actions"><a href="https://wa.me/5511972423702" target="_blank" class="btn btn-primary btn-caps">MATRICULE-SE</a></div>
        </div>
    </nav>"""

def footer():
    return """    <footer class="footer">
        <div class="container footer-grid">
            <div class="footer-brand"><div class="footer-brand-container"><div class="footer-logo-row"><img src="../images/logo_rede_comunita.png" alt="Rede Comunitá" class="logo-img"><span class="footer-text-cedesp">CEDESP</span></div><div class="footer-logo-subtitle"><span class="logo-wrapper"><span class="logo-highlight">Jaguaré</span></span></div></div><p>Transformando vidas na região do Jaguaré.</p></div>
            <div class="footer-links"><h4>Links</h4><a href="../historia.html">Nossa História</a><a href="../index.html#programas">Programas</a></div>
            <div class="footer-contact"><h4>Contato</h4><p>R. Floresto Bandecchi, 156 - Jaguaré, SP</p><a href="https://wa.me/5511972423702" class="btn btn-whatsapp" target="_blank">Falar no WhatsApp</a></div>
        </div>
        <div class="footer-bottom"><p>&copy; 2026 Rede Comunitá Jaguaré.</p></div>
    </footer>"""


# ══════════════════════════════════════════════════════════════
# PAGE BUILDER
# ══════════════════════════════════════════════════════════════

def build_page(
    filename, title, meta_desc,
    hero_grad, accent, accent_rgb, accent_light,
    h1_main, h1_accent,
    desc, hours,
    hero_logos, modules, tools,
    cta_h2, cta_p, wa_msg,
):
    orbit_html, orbit_keyframes = make_orbit(hero_logos, accent, accent_rgb)
    css = make_css(hero_grad, accent, accent_rgb, accent_light, orbit_keyframes)

    mods = ""
    for i, (mt, mb) in enumerate(modules, 1):
        num = f"0{i}" if i < 10 else str(i)
        mods += f"""            <div class="c-module animate-on-scroll">
                <span class="c-module-num">{num}</span>
                <h3>{mt}</h3>
                <p>{mb}</p>
            </div>\n"""

    tool_items = ""
    for lf, la, name in tools:
        tool_items += f"""            <div class="c-tool">
                <div class="c-tool-icon"><img src="logos/{lf}" alt="{la}"></div>
                <span class="c-tool-name">{name}</span>
            </div>\n"""

    wa_enc = wa_msg.replace(" ", "+")

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Rede Comunitá Jaguaré</title>
    <meta name="description" content="{meta_desc}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../styles.css">
    <style>
{css}
    </style>
</head>
<body>
{ticker()}

{nav()}

    <!-- ── HERO ── -->
    <header class="course-hero">
        <div class="container">
            <div class="hero-grid">
                <div class="hero-text animate-on-scroll is-visible">
                    <div class="hero-eyebrow">
                        <img class="senai-img" src="../images/logo_senai.png" alt="SENAI">
                        <span>Certificação SENAI Oficial</span>
                    </div>
                    <h1 class="course-title">{h1_main}<br><span class="accent">{h1_accent}</span></h1>
                    <p class="course-desc">{desc}</p>
                    <div class="hero-pills">
                        <div class="hero-pill"><span class="pill-value">{hours}</span>Carga horária</div>
                        <div class="hero-pill"><span class="pill-value">SENAI</span>Certificação</div>
                        <div class="hero-pill"><span class="pill-value">100%</span>Gratuito</div>
                    </div>
                </div>
                <div class="hero-visual">
{orbit_html}
                </div>
            </div>
        </div>
        <!-- scroll indicator -->
        <a class="scroll-hint" href="#course-highlights">
            <span>Descubra o curso</span>
            <div class="scroll-hint-dots"><i></i><i></i><i></i></div>
        </a>
    </header>
    <div class="hero-divider"></div>

    <!-- ── HIGHLIGHTS BRIDGE ── -->
    <section class="course-highlights" id="course-highlights">
        <div class="container">
            <div class="highlights-strip animate-on-scroll is-visible">
                <div class="hl-item">
                    <div class="hl-icon">🏆</div>
                    <div class="hl-text">
                        <span class="hl-value">Certificação SENAI</span>
                        <span class="hl-label">Reconhecida em todo o Brasil</span>
                    </div>
                </div>
                <div class="hl-item">
                    <div class="hl-icon">⏱️</div>
                    <div class="hl-text">
                        <span class="hl-value">{hours} de curso</span>
                        <span class="hl-label">Formação prática e completa</span>
                    </div>
                </div>
                <div class="hl-item">
                    <div class="hl-icon">💰</div>
                    <div class="hl-text">
                        <span class="hl-value">100% Gratuito</span>
                        <span class="hl-label">Sem mensalidades ou taxas</span>
                    </div>
                </div>
                <div class="hl-item">
                    <div class="hl-icon">💼</div>
                    <div class="hl-text">
                        <span class="hl-value">Alta Empregabilidade</span>
                        <span class="hl-label">Profissionais em alta demanda</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <main class="course-body">

        <!-- ── VÍDEO ── -->
        <section class="c-video-section">
            <div class="container">
                <div class="c-section-header animate-on-scroll">
                    <div class="c-section-tag">🎥 Conheça o Curso</div>
                    <h2 class="c-section-title">O professor apresenta</h2>
                    <p class="c-section-sub">Assista e descubra o que este curso tem a oferecer para a sua carreira</p>
                </div>
                <div class="c-video-wrap">
                    <div class="c-video-placeholder animate-on-scroll">
                        <div class="c-play-btn"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></div>
                        <span class="c-video-label">Vídeo de apresentação</span>
                    </div>
                </div>
            </div>
        </section>

        <!-- ── MÓDULOS ── -->
        <section class="c-modules-section">
            <div class="container">
                <div class="c-section-header animate-on-scroll">
                    <div class="c-section-tag">📚 Conteúdo Programático</div>
                    <h2 class="c-section-title">O que você vai aprender</h2>
                    <p class="c-section-sub">Conteúdo baseado no plano de ensino oficial do SENAI</p>
                </div>
                <div class="c-modules">
{mods}                </div>
            </div>
        </section>

        <!-- ── FERRAMENTAS ── -->
        <section class="c-tools-section">
            <div class="container">
                <div class="c-section-header animate-on-scroll">
                    <div class="c-section-tag">🛠️ Ferramentas na Prática</div>
                    <h2 class="c-section-title">Tecnologias que você vai dominar</h2>
                    <p class="c-section-sub">Softwares e plataformas usadas no mercado de trabalho</p>
                </div>
                <div class="c-tools-grid">
{tool_items}                </div>
            </div>
        </section>

        <!-- ── CTA ── -->
        <section class="c-cta-section">
            <div class="container">
                <div class="c-cta animate-on-scroll">
                    <div class="c-cta-inner">
                        <h2>{cta_h2}</h2>
                        <p>{cta_p}</p>
                        <div class="c-cta-btns">
                            <a href="https://wa.me/5511972423702?text=Olá+quero+me+matricular+no+curso+de+{wa_enc}!" target="_blank" class="btn-cta-primary">FALAR COM A SECRETARIA</a>
                            <a href="../cursos.html" class="btn-cta-outline">Ver Todos os Cursos</a>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>

{footer()}
    <script src="../script.js"></script>
</body>
</html>"""


# ══════════════════════════════════════════════════════════════
# COURSE DEFINITIONS — Unique palette per course
# ══════════════════════════════════════════════════════════════

COURSES = [
    dict(
        filename="operador-de-microcomputador.html",
        title="Informática Básica",
        meta_desc="Curso gratuito de Informática Básica no CEDESP Jaguaré. Windows, Word, Excel e PowerPoint com certificação SENAI.",
        hero_grad="linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #2563eb 100%)",
        accent="#3b82f6", accent_rgb="59,130,246", accent_light="#f0f6ff",
        h1_main="Informática", h1_accent="Básica",
        desc="Dê o seu primeiro passo no mundo digital. Domine o computador, redija documentos profissionais e utilize planilhas eletrônicas como um especialista.",
        hours="400h",
        hero_logos=[("windows.svg","Windows"),("word.svg","Word"),("excel.svg","Excel"),("powerpoint.svg","PowerPoint"),("chrome.svg","Chrome")],
        modules=[
            ("Windows e Navegação","Navegação fluida pelo sistema operacional, organização de pastas e arquivos, personalização e atalhos essenciais de teclado para ganhar velocidade."),
            ("Editor de Texto Comercial","Criação e formatação de currículos, circulares, ofícios e relatórios. Estilos automáticos, índices e sumários no padrão ABNT."),
            ("Planilhas Eletrônicas","Transforme dados em decisões. Fórmulas essenciais, formatação condicional, tabelas e gráficos dinâmicos para análise profissional."),
            ("Segurança Digital","Navegação consciente, identificação de phishing, gestão de senhas seguras e netiqueta para o ambiente corporativo."),
        ],
        tools=[("windows.svg","Windows","Windows 11"),("word.svg","Word","Microsoft Word"),("excel.svg","Excel","Microsoft Excel"),("powerpoint.svg","PowerPoint","PowerPoint"),("chrome.svg","Chrome","Google Chrome")],
        cta_h2="Sua carreira digital começa aqui.", cta_p="Vagas gratuitas com certificação SENAI inclusa. Sem pré-requisitos.", wa_msg="Informática Básica",
    ),
    dict(
        filename="assistente-de-ti.html",
        title="Tecnologia da Informação (TI)",
        meta_desc="Curso gratuito de TI no CEDESP Jaguaré. Hardware, redes e suporte técnico com certificação SENAI.",
        hero_grad="linear-gradient(135deg, #020617 0%, #0c1a2e 50%, #0891b2 100%)",
        accent="#06b6d4", accent_rgb="6,182,212", accent_light="#f0fdff",
        h1_main="Tecnologia da", h1_accent="Informação (TI)",
        desc="Torne-se o profissional indispensável. Monte computadores, configure redes corporativas e ofereça suporte técnico de alto nível.",
        hours="800h",
        hero_logos=[("windows.svg","Windows"),("linux.svg","Linux"),("cisco.svg","Cisco"),("ubuntu.svg","Ubuntu"),("vscode.svg","VS Code")],
        modules=[
            ("Hardware e Montagem","Identificação e substituição de componentes, diagnóstico profissional de falhas, limpeza e manutenção preventiva e corretiva em computadores."),
            ("Sistemas Operacionais","Instalação, particionamento e configuração avançada do Windows 11 e Ubuntu Linux. Gerenciamento de usuários e permissões."),
            ("Redes de Computadores","Cabeamento Cat6, roteadores e switches, endereçamento IP (IPv4/IPv6), wireless, firewall e VPN corporativa."),
            ("Suporte Técnico e Helpdesk","Abertura de chamados, comunicação com usuários, SLA, escalação de incidentes e boas práticas ITIL para service desk."),
        ],
        tools=[("windows.svg","Windows","Windows 11"),("linux.svg","Linux","Linux / Ubuntu"),("cisco.svg","Cisco","Cisco Packet Tracer"),("ubuntu.svg","Ubuntu","Ubuntu Server"),("vscode.svg","VS Code","VS Code")],
        cta_h2="Domine a infraestrutura digital.", cta_p="Vagas gratuitas com certificação SENAI inclusa. Turmas com horários flexíveis.", wa_msg="Tecnologia da Informação TI",
    ),
    dict(
        filename="web-designer.html",
        title="Web Designer",
        meta_desc="Curso gratuito de Web Designer no CEDESP Jaguaré. HTML, CSS, JavaScript e Figma com certificação SENAI.",
        hero_grad="linear-gradient(135deg, #1e0035 0%, #4c1d95 50%, #7c3aed 100%)",
        accent="#7c3aed", accent_rgb="124,58,237", accent_light="#f5f0ff",
        h1_main="Web", h1_accent="Designer",
        desc="Crie sites modernos e experiências digitais incríveis. Da prototipagem no Figma ao código — construa sua presença no mercado digital.",
        hours="600h",
        hero_logos=[("html5.svg","HTML5"),("css3.svg","CSS3"),("javascript.svg","JavaScript"),("figma.svg","Figma"),("vscode.svg","VS Code")],
        modules=[
            ("HTML5 Semântico","Estruturação de páginas com tags semânticas, acessibilidade (ARIA), formulários avançados, multimídia e SEO on-page."),
            ("CSS3 e Design Responsivo","Flexbox, Grid Layout, animações CSS, media queries e metodologia BEM para criar interfaces em qualquer tela."),
            ("JavaScript Essencial","Manipulação do DOM, eventos, fetch API, validação de formulários e introdução a frameworks modernos."),
            ("UI/UX com Figma","Wireframes, protótipos navegáveis, sistemas de design e handoff para desenvolvimento — o workflow completo do designer."),
        ],
        tools=[("html5.svg","HTML5","HTML5"),("css3.svg","CSS3","CSS3"),("javascript.svg","JS","JavaScript"),("figma.svg","Figma","Figma"),("vscode.svg","VS Code","VS Code"),("wordpress.svg","WordPress","WordPress"),("chrome.svg","Chrome","Chrome DevTools")],
        cta_h2="Construa o futuro da web.", cta_p="Vagas gratuitas com certificação SENAI inclusa.", wa_msg="Web Designer",
    ),
    dict(
        filename="auxiliar-administrativo.html",
        title="Administração",
        meta_desc="Curso gratuito de Auxiliar Administrativo no CEDESP Jaguaré. Rotinas de escritório e gestão com certificação SENAI.",
        hero_grad="linear-gradient(135deg, #0c1445 0%, #1e2d78 50%, #3b5bdb 100%)",
        accent="#3b5bdb", accent_rgb="59,91,219", accent_light="#f0f2ff",
        h1_main="Administração", h1_accent="& Gestão",
        desc="Domine as rotinas que movem as empresas. Gerencie documentos, organize processos e opere sistemas administrativos com eficiência.",
        hours="600h",
        hero_logos=[("word.svg","Word"),("excel.svg","Excel"),("powerpoint.svg","PowerPoint"),("outlook.svg","Outlook"),("trello.svg","Trello")],
        modules=[
            ("Comunicação Empresarial","Redação de ofícios, atas, relatórios e e-mails corporativos. Protocolo profissional e técnicas de comunicação interna."),
            ("Gestão de Documentos","Arquivamento físico e digital, fluxo de documentos, normas ABNT e LGPD aplicadas ao ambiente administrativo."),
            ("Planilhas e Análise de Dados","Controle de custos, planilhas de fluxo de caixa, cálculos de indicadores e dashboards básicos em Excel."),
            ("Introdução a Sistemas ERP","Alimentação e consulta de dados em sistemas de gestão empresarial para contabilidade, estoque e RH."),
        ],
        tools=[("word.svg","Word","Microsoft Word"),("excel.svg","Excel","Microsoft Excel"),("powerpoint.svg","PowerPoint","PowerPoint"),("outlook.svg","Outlook","Microsoft Outlook"),("trello.svg","Trello","Trello")],
        cta_h2="Sua jornada profissional começa aqui.", cta_p="Vagas gratuitas com certificação SENAI inclusa.", wa_msg="Administração",
    ),
    dict(
        filename="controle-de-qualidade.html",
        title="Logística",
        meta_desc="Curso gratuito de Logística no CEDESP Jaguaré. Gestão de estoques, WMS e supply chain com certificação SENAI.",
        hero_grad="linear-gradient(135deg, #1c0a00 0%, #7c2d12 50%, #ea580c 100%)",
        accent="#ea580c", accent_rgb="234,88,12", accent_light="#fff7f0",
        h1_main="Logística &", h1_accent="Supply Chain",
        desc="Otimize o fluxo de produtos e informações. Aprenda a gerenciar estoques, coordenar cadeias de suprimento e garantir qualidade nas operações.",
        hours="600h",
        hero_logos=[("excel.svg","Excel"),("sap.svg","SAP"),("powerbi.svg","Power BI"),("googlemaps.svg","Google Maps")],
        modules=[
            ("Gestão de Estoque e Armazém","Tipos de armazenagem, curva ABC, FIFO/LIFO, endereçamento, movimentação segura de cargas e uso de sistemas WMS."),
            ("Transporte e Distribuição","Modal de transporte, roteirização inteligente, documentação fiscal (NF-e, CTRC) e rastreamento de frotas."),
            ("Controle de Qualidade","Ferramentas da qualidade (5S, PDCA, Ishikawa), inspeção de recebimento e gestão de indicadores KPI."),
            ("Sistemas e Tecnologia na Logística","ERPs logísticos, QR Code, planilhas inteligentes e introdução ao Power BI para relatórios gerenciais."),
        ],
        tools=[("excel.svg","Excel","Microsoft Excel"),("sap.svg","SAP","SAP ERP"),("powerbi.svg","Power BI","Power BI"),("googlemaps.svg","Maps","Google Maps")],
        cta_h2="Mova o mundo com eficiência.", cta_p="Vagas gratuitas com certificação SENAI inclusa.", wa_msg="Logística",
    ),
    dict(
        filename="rh.html",
        title="Recursos Humanos (RH)",
        meta_desc="Curso gratuito de RH no CEDESP Jaguaré. Recrutamento, DP e gestão de pessoas com certificação SENAI.",
        hero_grad="linear-gradient(135deg, #042f2e 0%, #065f46 50%, #059669 100%)",
        accent="#10b981", accent_rgb="16,185,129", accent_light="#f0fdf4",
        h1_main="Recursos", h1_accent="Humanos (RH)",
        desc="Seja a ponte entre as pessoas e os resultados. Domine o recrutamento, o departamento pessoal e as estratégias de desenvolvimento organizacional.",
        hours="600h",
        hero_logos=[("excel.svg","Excel"),("linkedin.svg","LinkedIn"),("teams.svg","Teams"),("outlook.svg","Outlook")],
        modules=[
            ("Recrutamento e Seleção","Atração de talentos, triagem de currículos, técnicas de entrevista, banco de talentos e onboarding estruturado."),
            ("Departamento Pessoal","Admissão, demissão, férias, folha de pagamento, encargos trabalhistas e obrigações legais (CLT, eSocial)."),
            ("Desenvolvimento Organizacional","Treinamentos, plano de carreira, avaliação de desempenho (PDR/PDI) e programas de engajamento."),
            ("Gestão de Clima e Cultura","Pesquisa de clima, gestão de conflitos, diversidade e inclusão e comunicação interna para ambientes saudáveis."),
        ],
        tools=[("excel.svg","Excel","Microsoft Excel"),("linkedin.svg","LinkedIn","LinkedIn Recruiter"),("teams.svg","Teams","Microsoft Teams"),("outlook.svg","Outlook","Microsoft Outlook")],
        cta_h2="Gerencie o ativo mais valioso.", cta_p="Vagas gratuitas com certificação SENAI inclusa.", wa_msg="Recursos Humanos",
    ),
    dict(
        filename="ajustador-mecanico.html",
        title="Ajustador Mecânico",
        meta_desc="Curso gratuito de Ajustador Mecânico no CEDESP Jaguaré. Usinagem e controle dimensional com certificação SENAI.",
        hero_grad="linear-gradient(135deg, #0f172a 0%, #1e3a5f 40%, #475569 100%)",
        accent="#64748b", accent_rgb="100,116,139", accent_light="#f8fafc",
        h1_main="Ajustador", h1_accent="Mecânico",
        desc="Seja o profissional que mantém a indústria em movimento. Domine as técnicas de ajuste, usinagem e controle dimensional com precisão industrial.",
        hours="800h",
        hero_logos=[("autocad.svg","AutoCAD"),("autodesk.svg","Autodesk"),("siemens.svg","Siemens"),("freecad.svg","FreeCAD")],
        modules=[
            ("Metrologia e Controle Dimensional","Uso de paquímetros, micrômetros e relógios comparadores. Leitura de tolerâncias GD&T e verificação de conformidade."),
            ("Ajuste e Usinagem Manual","Limagem, serramento, furação e roscagem em materiais metálicos. Montagem e desmontagem de conjuntos mecânicos."),
            ("Elementos de Máquinas","Identificação e seleção de rolamentos, chavetas, retentores, parafusos e molas. Lubrificação industrial."),
            ("Desenho Técnico e CAD","Leitura de projetos mecânicos, simbologia normalizada e introdução ao AutoCAD Mechanical para manutenção."),
        ],
        tools=[("autocad.svg","AutoCAD","AutoCAD Mechanical"),("autodesk.svg","Autodesk","Autodesk Inventor"),("siemens.svg","Siemens","Siemens NX"),("freecad.svg","FreeCAD","FreeCAD")],
        cta_h2="Precisão que move a indústria.", cta_p="Vagas gratuitas com certificação SENAI inclusa.", wa_msg="Ajustador Mecânico",
    ),
    dict(
        filename="eletricista-instalador.html",
        title="Eletricista Instalador",
        meta_desc="Curso gratuito de Eletricista Instalador no CEDESP Jaguaré. Instalações prediais e NR-10 com certificação SENAI.",
        hero_grad="linear-gradient(135deg, #1a1200 0%, #3d2e00 50%, #92400e 100%)",
        accent="#f59e0b", accent_rgb="245,158,11", accent_light="#fffbeb",
        h1_main="Eletricista", h1_accent="Instalador",
        desc="Domine a energia que move o mundo. Projete, monte e mantenha instalações elétricas prediais com total segurança, seguindo as normas NBR 5410 e NR-10.",
        hours="800h",
        hero_logos=[("autocad.svg","AutoCAD"),("siemens.svg","Siemens"),("schneider.svg","Schneider"),("arduino.svg","Arduino")],
        modules=[
            ("Fundamentos de Eletricidade","Lei de Ohm, circuitos série e paralelo, potência e energia elétrica, análise com multímetro digital e osciloscópio."),
            ("Instalações Prediais (NBR 5410)","Dimensionamento de condutores e eletrodutos, quadros de distribuição, DPS, DR e sistemas de aterramento."),
            ("NR-10 e Segurança Elétrica","Trabalho em baixa e alta tensão, EPIs obrigatórios, SEP e procedimentos de bloqueio e etiquetagem (LOTO)."),
            ("Automação e Programação de CLPs","Automação industrial, leitura de diagramas ladder e configuração básica de CLPs Siemens e Schneider."),
        ],
        tools=[("autocad.svg","AutoCAD","AutoCAD Electrical"),("siemens.svg","Siemens","Siemens Logo!"),("schneider.svg","Schneider","EcoStruxure"),("arduino.svg","Arduino","Arduino IDE")],
        cta_h2="Ilumine sua carreira com segurança.", cta_p="Vagas gratuitas com certificação SENAI inclusa.", wa_msg="Eletricista Instalador",
    ),
    dict(
        filename="reparador-de-linha-branca.html",
        title="Reparador de Linha Branca",
        meta_desc="Curso gratuito de Reparador de Linha Branca no CEDESP Jaguaré. Refrigeração, lavadoras e fogões com certificação SENAI.",
        hero_grad="linear-gradient(135deg, #012a4a 0%, #013a63 50%, #0284c7 100%)",
        accent="#0096c7", accent_rgb="0,150,199", accent_light="#f0fbff",
        h1_main="Reparador de", h1_accent="Linha Branca",
        desc="Especialize-se na manutenção de eletrodomésticos essenciais. Geladeiras, lavadoras e fogões — profissão de alta demanda e excelente retorno de mercado.",
        hours="800h",
        hero_logos=[("samsung.svg","Samsung"),("lg.svg","LG"),("whirlpool.svg","Whirlpool")],
        modules=[
            ("Refrigeração Doméstica","Princípios de termodinâmica, ciclo de refrigeração, gases refrigerantes (R-134a, R-600a), diagnóstico com manifold e recarga."),
            ("Máquinas de Lavar","Funcionamento eletromecânico, bombas de drenagem, falhas em placas eletrônicas de controle e troca de rolamentos."),
            ("Eletricidade Aplicada e Gás","Interpretação de esquemas elétricos, uso de multímetro e capacímetro, manuseio seguro de gás GLP."),
            ("Empreendedorismo Técnico","Como montar orçamentos, precificação de serviços, atendimento ao cliente e formalizar seu próprio negócio."),
        ],
        tools=[("samsung.svg","Samsung","Samsung Service"),("lg.svg","LG","LG ThinQ"),("whirlpool.svg","Whirlpool","Whirlpool Tech")],
        cta_h2="Seja a solução técnica que o mercado procura.", cta_p="Vagas gratuitas com certificação SENAI inclusa.", wa_msg="Reparador de Linha Branca",
    ),
]

# ══════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════
for c in COURSES:
    html = build_page(**c)
    path = os.path.join(BASE, c["filename"])
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅  {c['filename']}  accent={c['accent']}")

print(f"\n🎉 All 9 courses rebuilt with orbital animations + SENAI fix!")
