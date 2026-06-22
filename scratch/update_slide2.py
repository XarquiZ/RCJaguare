import re

with open("index.html", "r") as f:
    content = f.read()

# 1. Replace CSS
new_css = """    <style>
        /* Fundo e Orbs Decorativos */
        .slide2-bg-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(80px);
            opacity: 0.5;
            z-index: 1;
        }
        .orb-1 {
            top: -20%; left: -10%;
            width: 500px; height: 500px;
            background: rgba(147, 51, 234, 0.6);
        }
        .orb-2 {
            bottom: -20%; right: -10%;
            width: 600px; height: 600px;
            background: rgba(245, 158, 11, 0.4);
        }

        /* Container principal */
        .slide2-wrapper {
            display: flex;
            gap: 40px;
            align-items: center;
            width: 100%;
            max-width: 1280px;
            margin: 0 auto;
            padding: 20px 0;
            z-index: 2;
        }

        /* Colunas */
        .slide2-col-left {
            flex: 1 1 55%;
            display: flex;
            flex-direction: column;
            gap: 20px;
            justify-content: center;
        }
        .slide2-col-right {
            flex: 1 1 45%;
            display: flex;
            justify-content: flex-end;
            align-items: center;
        }

        /* Badge Superior */
        .slide2-badge {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: rgba(255, 204, 51, 0.15);
            border: 1px solid rgba(255, 204, 51, 0.3);
            color: #FFCC33;
            padding: 8px 20px;
            border-radius: 100px;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 0.85rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            width: fit-content;
            box-shadow: 0 4px 15px rgba(255, 204, 51, 0.1);
        }
        .slide2-badge-dot {
            width: 8px;
            height: 8px;
            background: #FFCC33;
            border-radius: 50%;
            box-shadow: 0 0 10px #FFCC33, 0 0 20px #FFCC33;
            animation: pulse-dot 2s infinite;
        }
        @keyframes pulse-dot {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(1.5); }
        }

        /* Título e Subtítulo */
        .slide2-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: clamp(2rem, 3.5vw, 3rem);
            color: #ffffff;
            line-height: 1.1;
            margin: 0;
            text-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }
        .slide2-title .highlight {
            color: #FFCC33;
            position: relative;
            display: inline-block;
        }
        .slide2-title .highlight::after {
            content: '';
            position: absolute;
            bottom: 2px;
            left: 0;
            width: 100%;
            height: 6px;
            background: rgba(255, 204, 51, 0.4);
            border-radius: 4px;
            z-index: -1;
        }
        .slide2-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 1.05rem;
            color: rgba(255, 255, 255, 0.9);
            line-height: 1.5;
            margin: 0;
            max-width: 540px;
        }

        /* Cloud de Tags de Cursos */
        .slide2-tags-cloud {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 5px;
        }
        .slide2-tag {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #fff;
            padding: 8px 16px;
            border-radius: 100px;
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.3s ease;
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            display: inline-flex;
            align-items: center;
            cursor: default;
        }
        .slide2-tag:hover {
            background: rgba(255, 204, 51, 0.2);
            border-color: rgba(255, 204, 51, 0.5);
            color: #FFCC33;
            transform: translateY(-2px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.15);
        }

        /* Botões */
        .slide2-actions {
            display: flex;
            gap: 16px;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        .slide2-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            padding: 14px 28px;
            border-radius: 12px;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: none;
        }
        .slide2-btn-solid {
            background: #FFCC33;
            color: #1a1a1a;
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
        }
        .slide2-btn-solid:hover {
            background: #ffe066;
            transform: translateY(-3px);
            box-shadow: 0 12px 30px rgba(245, 158, 11, 0.6);
        }
        .slide2-btn-outline {
            background: rgba(255, 255, 255, 0.05);
            color: #fff;
            border: 2px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
        }
        .slide2-btn-outline:hover {
            background: rgba(255, 255, 255, 0.15);
            border-color: #fff;
            transform: translateY(-3px);
        }

        /* Premium Glass Card */
        .slide2-glass-card {
            background: rgba(20, 15, 45, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 28px;
            width: 100%;
            max-width: 440px;
            box-shadow: 0 24px 50px rgba(0, 0, 0, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            display: flex;
            flex-direction: column;
            gap: 20px;
            position: relative;
            overflow: hidden;
        }
        .slide2-glass-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
            background: linear-gradient(90deg, #FFCC33, #f59e0b, #db2777);
        }
        .glass-card-header {
            display: flex;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            padding-bottom: 16px;
        }
        .glass-card-header h3 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.2rem;
            color: #fff;
            margin: 0;
            letter-spacing: 0.02em;
        }
        .glass-benefits-list {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .glass-benefit-item {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .benefit-icon-box {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            flex-shrink: 0;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        .benefit-icon-box.morning { background: rgba(245, 158, 11, 0.15); box-shadow: 0 0 15px rgba(245, 158, 11, 0.2); }
        .benefit-icon-box.afternoon { background: rgba(56, 189, 248, 0.15); box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }
        .benefit-icon-box.night { background: rgba(168, 85, 247, 0.15); box-shadow: 0 0 15px rgba(168, 85, 247, 0.2); }
        
        .benefit-content {
            display: flex;
            flex-direction: column;
            gap: 4px;
        }
        .benefit-content h4 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 0.95rem;
            color: #fff;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .benefit-content h4 span {
            font-weight: 400;
            font-size: 0.8rem;
            color: rgba(255,255,255,0.6);
            background: rgba(255,255,255,0.1);
            padding: 2px 8px;
            border-radius: 4px;
        }
        .benefit-content p {
            font-family: 'Inter', sans-serif;
            font-size: 0.85rem;
            color: rgba(255,255,255,0.8);
            margin: 0;
        }
        .glass-card-footer {
            margin-top: 4px;
            padding-top: 16px;
            border-top: 1px dashed rgba(255,255,255,0.15);
        }
        .footer-highlight {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: rgba(255, 204, 51, 0.15);
            color: #FFCC33;
            padding: 12px;
            border-radius: 10px;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 0.85rem;
        }

        /* Responsividade */
        @media (max-width: 1024px) {
            .slide2-wrapper {
                flex-direction: column;
                gap: 40px;
                padding: 40px 5% 80px;
                text-align: center;
            }
            .slide2-col-left {
                align-items: center;
            }
            .slide2-tags-cloud {
                justify-content: center;
            }
            .slide2-actions {
                justify-content: center;
            }
            .slide2-glass-card {
                max-width: 500px;
            }
            .benefit-content {
                text-align: left;
            }
            .orb-1 { width: 300px; height: 300px; }
            .orb-2 { width: 400px; height: 400px; }
        }

        @media (max-width: 640px) {
            .slide2-title {
                font-size: 2rem;
            }
            .slide2-subtitle {
                font-size: 0.95rem;
            }
            .slide2-actions {
                flex-direction: column;
                width: 100%;
            }
            .slide2-btn {
                width: 100%;
            }
            .slide2-glass-card {
                padding: 20px;
            }
            .glass-benefit-item {
                gap: 12px;
            }
            .benefit-content h4 {
                flex-direction: column;
                align-items: flex-start;
                gap: 4px;
            }
            .benefit-content h4 span {
                margin-left: 0;
            }
        }
    </style>"""

# Find the css block
css_pattern = re.compile(r'    <style>\n        /\* Container principal do slide 2 \*/.*?    </style>', re.DOTALL)
content = css_pattern.sub(new_css, content)

# 2. Replace HTML
new_html = """            <div class="hero-slide"
                style="background: linear-gradient(135deg, #1e1b4b 0%, #3b0764 45%, #9333ea 80%, #f59e0b 115%); overflow: hidden; position: relative;">
                
                <!-- Abstract glowing orbs for background depth -->
                <div class="slide2-bg-orb orb-1"></div>
                <div class="slide2-bg-orb orb-2"></div>

                <div class="hero-main-row" style="padding: 0; position: relative; z-index: 2;">
                    <div class="slide2-wrapper">
                        
                        <!-- COLUNA ESQUERDA: Textos principais, tags de cursos e botões -->
                        <div class="slide2-col-left">
                            <div class="slide2-badge animate-on-scroll delay-1">
                                <span class="slide2-badge-dot"></span> INSCRIÇÕES ABERTAS
                            </div>
                            
                            <h1 class="slide2-title animate-on-scroll delay-1">
                                Capacitação <span class="highlight">Gratuita</span><br> Padrão SENAI
                            </h1>
                            
                            <p class="slide2-subtitle animate-on-scroll delay-2">
                                Transforme seu futuro! Garanta sua pré-inscrição com vagas limitadas e 100% gratuitas para a comunidade do Jaguaré.
                            </p>

                            <!-- Grade de Cursos como Tags Modernas -->
                            <div class="slide2-tags-cloud animate-on-scroll delay-2">
                                <span class="slide2-tag">💻 Tecnologia da Informação</span>
                                <span class="slide2-tag">🎨 Web Designer</span>
                                <span class="slide2-tag">🖥️ Informática Básica</span>
                                <span class="slide2-tag">⚡ Eletricista Instalador</span>
                                <span class="slide2-tag">⚙️ Ajustador Mecânico</span>
                                <span class="slide2-tag">❄️ Reparador Linha Branca</span>
                                <span class="slide2-tag">📊 Administração & RH</span>
                            </div>

                            <!-- Botões Lado a Lado -->
                            <div class="slide2-actions animate-on-scroll delay-3">
                                <a href="https://wa.me/5511972423702?text=Ol%C3%A1%20quero%20me%20matricular%20!" target="_blank" class="slide2-btn slide2-btn-solid">
                                    MATRICULE-SE JÁ
                                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                                    </svg>
                                </a>
                                <a href="cursos.html#filtros-cursos" class="slide2-btn slide2-btn-outline">
                                    Ver Cursos Ofertados
                                </a>
                            </div>
                        </div>

                        <!-- COLUNA DIREITA: Card Glassmorphism Premium de Benefícios -->
                        <div class="slide2-col-right animate-on-scroll delay-3">
                            <div class="slide2-glass-card">
                                <div class="glass-card-header">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FFCC33" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                                    </svg>
                                    <h3>Turnos & Benefícios</h3>
                                </div>

                                <div class="glass-benefits-list">
                                    <div class="glass-benefit-item">
                                        <div class="benefit-icon-box morning">🌅</div>
                                        <div class="benefit-content">
                                            <h4>MANHÃ <span>08h00 - 11h15</span></h4>
                                            <p>Café da manhã e almoço inclusos</p>
                                        </div>
                                    </div>
                                    <div class="glass-benefit-item">
                                        <div class="benefit-icon-box afternoon">☀️</div>
                                        <div class="benefit-content">
                                            <h4>TARDE <span>13h00 - 16h50</span></h4>
                                            <p>Almoço e café da tarde inclusos</p>
                                        </div>
                                    </div>
                                    <div class="glass-benefit-item">
                                        <div class="benefit-icon-box night">🌙</div>
                                        <div class="benefit-content">
                                            <h4>NOITE <span>19h00 - 21h30</span></h4>
                                            <p>Jantar no local incluso</p>
                                        </div>
                                    </div>
                                </div>

                                <div class="glass-card-footer">
                                    <div class="footer-highlight">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                            <path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/>
                                        </svg>
                                        100% Gratuito (Cursos e Refeições)
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>"""

html_pattern = re.compile(r'            <div class="hero-slide"\n                style="background: linear-gradient\(110deg, #1e1b4b 0%, #4c1d95 38%, #7c3aed 65%, #f59e0b 100%\);.*?            </div>\n            <!-- ================================================================ -->\n            <!-- FIM DO SLIDE 2 REDESENHADO -->', re.DOTALL)
content = html_pattern.sub(new_html + '\n            <!-- ================================================================ -->\n            <!-- FIM DO SLIDE 2 REDESENHADO -->', content)

with open("index.html", "w") as f:
    f.write(content)

print("Done replacing.")
