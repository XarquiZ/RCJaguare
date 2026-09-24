document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
        });

        // Close menu when a link is clicked
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
            });
        });
    }

    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target); // Stop observing once visible
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    animatedElements.forEach(el => observer.observe(el));

    // Timeline items also animate on scroll
    const timelineItems = document.querySelectorAll('.timeline-item');
    timelineItems.forEach(el => observer.observe(el));

    // ===== SLIDESHOW AUTOMÁTICO =====
    document.querySelectorAll('.timeline-slideshow').forEach(slideshow => {
        const slides = slideshow.querySelectorAll('.slide');
        const dotsContainer = slideshow.querySelector('.slideshow-dots');
        if (slides.length <= 1) return;

        let currentIndex = 0;

        // Cria dots
        slides.forEach((_, i) => {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToSlide(i));
            dotsContainer.appendChild(dot);
        });

        function goToSlide(index) {
            slides[currentIndex].classList.remove('active');
            dotsContainer.children[currentIndex].classList.remove('active');
            currentIndex = index;
            slides[currentIndex].classList.add('active');
            dotsContainer.children[currentIndex].classList.add('active');
        }

        function nextSlide() {
            goToSlide((currentIndex + 1) % slides.length);
        }

        setInterval(nextSlide, 4000);
    });

    // ===== HERO BANNER SLIDESHOW AUTOMÁTICO =====
    const heroSlider = document.querySelector('.hero-slider');
    if (heroSlider) {
        const slides = heroSlider.querySelectorAll('.hero-slide');
        const dotsContainer = document.querySelector('.hero-dots');
        const prevBtn = document.querySelector('.hero-prev');
        const nextBtn = document.querySelector('.hero-next');
        
        if (slides.length > 1) {
            let currentIndex = 0;
            let slideInterval;
            const intervalTime = 5000; // 5 segundos por banner

            // Cria dots
            slides.forEach((_, i) => {
                const dot = document.createElement('span');
                dot.classList.add('hero-dot');
                if (i === 0) dot.classList.add('active');
                dot.addEventListener('click', () => {
                    goToSlide(i);
                    resetTimer();
                });
                dotsContainer.appendChild(dot);
            });

            let isAnimating = false;
            const animDuration = 850; // ms, slightly longer than CSS 0.8s

            function goToSlide(index, direction = 'next') {
                if (index === currentIndex || isAnimating) return;
                isAnimating = true;

                const outgoing = slides[currentIndex];
                const incoming = slides[index];

                // Update dots
                if (dotsContainer && dotsContainer.children[currentIndex]) {
                    dotsContainer.children[currentIndex].classList.remove('active');
                }
                if (dotsContainer && dotsContainer.children[index]) {
                    dotsContainer.children[index].classList.add('active');
                }

                // Make incoming visible but transparent
                incoming.style.opacity = '0';
                incoming.style.visibility = 'visible';
                incoming.style.zIndex = '3';
                incoming.classList.add('active');

                // Force reflow
                incoming.offsetHeight;

                // Crossfade
                incoming.style.transition = 'opacity 0.7s ease';
                incoming.style.opacity = '1';
                outgoing.style.transition = 'opacity 0.7s ease';
                outgoing.style.opacity = '0';

                // Cleanup after animation completes
                setTimeout(() => {
                    outgoing.classList.remove('active');
                    outgoing.style.opacity = '';
                    outgoing.style.visibility = '';
                    outgoing.style.zIndex = '';
                    outgoing.style.transition = '';
                    incoming.style.opacity = '';
                    incoming.style.visibility = '';
                    incoming.style.zIndex = '';
                    incoming.style.transition = '';
                    currentIndex = index;
                    isAnimating = false;
                }, 750);
            }

            function nextSlide() {
                goToSlide((currentIndex + 1) % slides.length, 'next');
            }

            function prevSlide() {
                goToSlide((currentIndex - 1 + slides.length) % slides.length, 'prev');
            }

            // Swipe Detection Mobile com Trava de Ângulo Direcional
            let touchStartX = 0;
            let touchStartY = 0;
            const swipeThreshold = 35; // pixels otimizado para celulares

            heroSlider.addEventListener('touchstart', e => {
                if (e.touches && e.touches.length > 0) {
                    touchStartX = e.touches[0].clientX;
                    touchStartY = e.touches[0].clientY;
                }
            }, { passive: true });

            heroSlider.addEventListener('touchend', e => {
                if (!e.changedTouches || e.changedTouches.length === 0) return;
                const touchEndX = e.changedTouches[0].clientX;
                const touchEndY = e.changedTouches[0].clientY;
                const diffX = touchStartX - touchEndX;
                const diffY = touchStartY - touchEndY;

                // Só avança o slide se o movimento foi predominantemente horizontal
                if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > swipeThreshold) {
                    if (diffX > 0) {
                        // swipe para a esquerda -> próximo slide
                        nextSlide();
                        resetTimer();
                    } else {
                        // swipe para a direita -> slide anterior
                        prevSlide();
                        resetTimer();
                    }
                }
            }, { passive: true });
            // Optional mouse drag for desktop
            let mouseDownX = 0;
            heroSlider.addEventListener('mousedown', e => {
                mouseDownX = e.clientX;
            });
            heroSlider.addEventListener('mouseup', e => {
                const mouseUpX = e.clientX;
                const diffX = mouseDownX - mouseUpX;
                if (Math.abs(diffX) > swipeThreshold) {
                    if (diffX > 0) { nextSlide(); } else { prevSlide(); }
                    resetTimer();
                }
            });

            // Click Handlers para setas
            if (prevBtn) {
                prevBtn.addEventListener('click', () => {
                    prevSlide();
                    resetTimer();
                });
            }
            if (nextBtn) {
                nextBtn.addEventListener('click', () => {
                    nextSlide();
                    resetTimer();
                });
            }

            // Inicia o timer
            function startTimer() {
                slideInterval = setInterval(nextSlide, intervalTime);
            }

            // Reseta o timer ao interagir
            function resetTimer() {
                clearInterval(slideInterval);
                startTimer();
            }

            startTimer();
        }
    }

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Logo Typing Animation - Looping
    const logoHighlights = document.querySelectorAll('.nav-logo .logo-highlight');
    if (logoHighlights.length > 0) {
        logoHighlights.forEach(el => {
            const text = "Jaguaré";
            let charIndex = 0;
            let isDeleting = false;

            const type = () => {
                const currentText = isDeleting 
                    ? text.substring(0, charIndex--) 
                    : text.substring(0, charIndex++);
                
                el.textContent = currentText;

                let nextSpeed = isDeleting ? 100 : 200;

                if (!isDeleting && charIndex > text.length) {
                    isDeleting = true;
                    nextSpeed = 2000; // Pause at end
                } else if (isDeleting && charIndex < 0) {
                    isDeleting = false;
                    charIndex = 0;
                    nextSpeed = 500; // Pause before restarting
                }

                setTimeout(type, nextSpeed);
            };
            
            setTimeout(type, 1000);
        });
    }

    // Course Categories Logic
    const courseCategories = {
        'Ajustador Mecânico': 'manutencao',
        'Reparador de Linha Branca': 'manutencao',
        'Eletricista Instalador': 'manutencao',
        'Informática Básica': 'tecnologia',
        'Web Designer': 'tecnologia',
        'Tecnologia da Informação (TI)': 'tecnologia',
        'Logística': 'administracao',
        'Recursos Humanos (RH)': 'administracao',
        'Administração': 'administracao'
    };

    // Initialize course categories on sections
    const courseSections = document.querySelectorAll('main > section');
    courseSections.forEach(section => {
        const h2 = section.querySelector('h2');
        if (h2) {
            const courseName = h2.textContent.trim();
            if (courseCategories[courseName]) {
                section.setAttribute('data-category', courseCategories[courseName]);
            }
        }
    });

    // Handle course filtering
    const filterBtns = document.querySelectorAll('.filter-btn');
    if (filterBtns.length > 0) {
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active state
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const filter = btn.getAttribute('data-filter');
                let firstVisibleSection = null;

                courseSections.forEach(section => {
                    const category = section.getAttribute('data-category');
                    if (filter === 'todos' || category === filter) {
                        section.style.display = 'block';
                        section.style.animation = 'none';
                        section.offsetHeight; /* trigger reflow */
                        section.style.animation = 'fadeInFilter 0.5s ease-out forwards';

                        if (!firstVisibleSection) {
                            firstVisibleSection = section;
                        }
                    } else {
                        section.style.display = 'none';
                    }
                });

                if (firstVisibleSection) {
                    setTimeout(() => {
                        const yOffset = -90; // Fixed navbar offset space
                        const y = firstVisibleSection.getBoundingClientRect().top + window.scrollY + yOffset;
                        window.scrollTo({top: y, behavior: 'smooth'});
                    }, 50);
                }
            });
        });
    }
    // Calendar logic with month filters and past events hiding
    const calendarItems = document.querySelectorAll('.calendar-item');
    const calFilterBtns = document.querySelectorAll('.cal-filter-btn');
    
    if (calendarItems.length > 0) {
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        let currentMonth = (today.getMonth() + 1).toString();
        
        let hasCurrentMonthBtn = false;
        if (calFilterBtns.length > 0) {
            calFilterBtns.forEach(btn => {
                btn.classList.remove('active');
                if (btn.getAttribute('data-month') === currentMonth) {
                    hasCurrentMonthBtn = true;
                    btn.classList.add('active');
                }
            });
            if (!hasCurrentMonthBtn) {
                currentMonth = 'todos';
                calFilterBtns[0].classList.add('active');
            }
        }

        const filterCalendar = (monthFilter) => {
            let visibleCount = 0;
            calendarItems.forEach(item => {
                const dateStr = item.getAttribute('data-date');
                if (dateStr) {
                    const parts = dateStr.split('-');
                    if (parts.length === 3) {
                        const year = parseInt(parts[0], 10);
                        const itemMonthNum = parseInt(parts[1], 10);
                        const day = parseInt(parts[2], 10);
                        const eventDate = new Date(year, itemMonthNum - 1, day);
                        
                        const isPast = eventDate < today;
                        const matchesMonth = monthFilter === 'todos' || itemMonthNum.toString() === monthFilter;
                        
                        if (!matchesMonth) {
                            // Oculta apenas se não bater com o filtro de mês
                            item.style.display = 'none';
                            item.classList.remove('is-past');
                        } else {
                            item.style.display = 'flex';
                            item.style.animation = 'none';
                            item.offsetHeight; // trigger reflow
                            item.style.animation = 'fadeInFilter 0.4s ease-out forwards';
                            
                            if (isPast) {
                                // Evento passado: mostra acinzentado
                                item.classList.add('is-past');
                            } else {
                                item.classList.remove('is-past');
                                visibleCount++;
                            }
                        }
                    }
                }
            });

            const noEventsMsg = document.getElementById('no-events-msg');
            if (noEventsMsg) {
                noEventsMsg.style.display = visibleCount === 0 ? 'block' : 'none';
            }
        };

        // Initial load
        filterCalendar(currentMonth);

        // Filter clicks
        if (calFilterBtns.length > 0) {
            calFilterBtns.forEach(btn => {
                btn.addEventListener('click', () => {
                    calFilterBtns.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    filterCalendar(btn.getAttribute('data-month'));
                });
            });
        }
    }

    // ===== CONTADOR ANIMADO NOS NÚMEROS DE IMPACTO =====
    const counterElements = document.querySelectorAll('.impact-number[data-target]');
    if (counterElements.length > 0) {
        const duration = 2000; // 2 segundos

        const startCounter = (el) => {
            const rawTarget = el.getAttribute('data-target');
            const target = parseInt(rawTarget, 10);
            if (isNaN(target)) return;

            const prefix = el.getAttribute('data-prefix') || '+';
            let startTimestamp = null;

            const step = (timestamp) => {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                const currentCount = Math.floor(progress * target);

                el.textContent = `${prefix}${currentCount.toLocaleString('pt-BR')}`;

                if (progress < 1) {
                    window.requestAnimationFrame(step);
                } else {
                    el.textContent = `${prefix}${target.toLocaleString('pt-BR')}`;
                }
            };
            window.requestAnimationFrame(step);
        };

        const counterObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const el = entry.target;
                    startCounter(el);
                    observer.unobserve(el);
                }
            });
        }, { threshold: 0.3 });

        counterElements.forEach(el => counterObserver.observe(el));
    }

    // ===== SINCRONIZAÇÃO DINÂMICA DE EVENTOS (GOOGLE DRIVE ESPELHO) =====
    const GOOGLE_DRIVE_EVENTS_URL = "https://script.google.com/macros/s/AKfycbwuRr3KOATyHEOl8Nf-ZaNC7dGUm2XHVKI52cYfaJpYe7I7BspR_lnLjeC3riIvSTvs/exec";
    const eventsGrid = document.getElementById('eventsGrid');
    const categoryFiltersContainer = document.getElementById('categoryFilters');
    const yearFiltersWrapper = document.getElementById('yearFiltersWrapper');
    const yearSelect = document.getElementById('yearSelect');
    const noEventsMessage = document.getElementById('noEventsMessage');
    const loadingState = document.getElementById('eventsLoadingState');
    const lightboxOverlay = document.getElementById('albumLightbox');

    if (eventsGrid && lightboxOverlay) {
        let driveAlbums = [];
        let currentFilter = 'all';
        let currentYear = 'all';

        // Elementos do Lightbox
        const titleEl = document.getElementById('lightboxTitle');
        const gridView = document.getElementById('lightboxGrid');
        const fullView = document.getElementById('lightboxFullscreen');
        const fullscreenImg = document.getElementById('fullscreenImage');
        const currentImgNum = document.getElementById('currentImgNum');
        const totalImgNum = document.getElementById('totalImgNum');
        const closeBtn = document.querySelector('.lightbox-close');

        let activeAlbum = null;
        let activePhotoIdx = 0;

        // Carregamento inicial zero milissegundo (usando pré-carga estática se houver, ou cache do localStorage)
        let hasRendered = false;
        try {
            if (typeof DRIVE_INITIAL_ALBUMS !== 'undefined' && Array.isArray(DRIVE_INITIAL_ALBUMS) && DRIVE_INITIAL_ALBUMS.length > 0) {
                driveAlbums = DRIVE_INITIAL_ALBUMS;
                renderPage();
                hasRendered = true;
            }
        } catch (e) {}

        // 1. Função para buscar os dados do Google Apps Script com Cache Inteligente (Stale-While-Revalidate)
        const fetchDriveEvents = async () => {
            let hasCachedData = hasRendered;

            try {
                // Carrega do localStorage para manter atualização da última visita
                const cached = localStorage.getItem('cedesp_drive_albums_v2');
                if (cached) {
                    const parsed = JSON.parse(cached);
                    if (Array.isArray(parsed) && parsed.length > 0) {
                        driveAlbums = parsed;
                        hasCachedData = true;
                        renderPage(); // Instantâneo!
                    }
                }
            } catch (e) {
                console.warn('Erro ao ler cache local:', e);
            }

            try {
                // Busca atualização do Drive em segundo plano
                const res = await fetch(GOOGLE_DRIVE_EVENTS_URL);
                const data = await res.json();

                if (data.status === 'success' && Array.isArray(data.albums)) {
                    const freshDataStr = JSON.stringify(data.albums);
                    const oldDataStr = JSON.stringify(driveAlbums);

                    // Só re-renderiza se houver novidade/diferença
                    if (freshDataStr !== oldDataStr || !hasCachedData) {
                        driveAlbums = data.albums;
                        try {
                            localStorage.setItem('cedesp_drive_albums_v2', freshDataStr);
                        } catch(e) {}
                        renderPage();
                    }
                } else {
                    throw new Error(data.message || 'Dados inválidos do Drive');
                }
            } catch (err) {
                console.error('Erro na sincronização em segundo plano:', err);
                if (!hasCachedData && driveAlbums.length === 0) {
                    if (loadingState) loadingState.style.display = 'none';
                    if (noEventsMessage) {
                        noEventsMessage.style.display = 'block';
                        noEventsMessage.innerHTML = '<p>Não foi possível carregar as fotos no momento. Tente recarregar a página.</p>';
                    }
                }
            }
        };

        // 2. Renderiza Categorias e Cards
        const renderPage = () => {
            if (loadingState) loadingState.style.display = 'none';

            if (!driveAlbums || driveAlbums.length === 0) {
                eventsGrid.innerHTML = '';
                if (noEventsMessage) {
                    noEventsMessage.style.display = 'block';
                    noEventsMessage.innerHTML = '<p>Nenhum álbum encontrado no Google Drive.</p>';
                }
                return;
            }

            // A) Classificação Inteligente de Categoria e Ano
            const uniqueYears = new Set();
            const categoryGroups = new Map(); // categoryKey -> { label, albums: [] }

            // Helper para identificar a categoria a partir do título do álbum
            const detectCategory = (title) => {
                const lower = (title || '').toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
                if (lower.includes('palestra') || lower.includes('workshop') || lower.includes('seminario')) {
                    return { key: 'palestras', label: 'Palestras', tag: 'Palestra' };
                }
                if (lower.includes('feira') || lower.includes('profiss')) {
                    return { key: 'feiras', label: 'Feiras & Profissões', tag: 'Feira' };
                }
                if (lower.includes('formatura') || lower.includes('certificad') || lower.includes('conclus')) {
                    return { key: 'formaturas', label: 'Formaturas', tag: 'Formatura' };
                }
                if (lower.includes('visita') || lower.includes('empresa') || lower.includes('tecnica')) {
                    return { key: 'visitas', label: 'Visitas Técnicas', tag: 'Visita Técnica' };
                }
                if (lower.includes('comemorac') || lower.includes('festa') || lower.includes('dia d') || lower.includes('confraternizacao')) {
                    return { key: 'comemoracoes', label: 'Comemorações', tag: 'Comemoração' };
                }
                return { key: 'eventos-gerais', label: 'Outros Eventos', tag: 'Evento' };
            };

            // Gerador automático de descrições enriquecidas que elevam o valor pedagógico e profissional
            const generateEnrichedDescription = (title, categoryKey) => {
                const cleanTitle = (title || '').replace(/\b(20\d{2})\b/g, '').trim();
                const lower = cleanTitle.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");

                // 1. Temas frequentes em Palestras
                if (lower.includes('ansiedade') || lower.includes('saude mental') || lower.includes('emocional') || lower.includes('psico')) {
                    return 'Encontro formativo focado em inteligência emocional e saúde mental, proporcionando aos alunos ferramentas indispensáveis para o bem-estar e o equilíbrio profissional.';
                }
                if (lower.includes('marketing') || lower.includes('digital') || lower.includes('midias') || lower.includes('redes sociais')) {
                    return 'Imersão em estratégias digitais contemporâneas, preparando nossos jovens para posicionamento de marca, inovação comercial e oportunidades na economia conectada.';
                }
                if (lower.includes('financeira') || lower.includes('financ') || lower.includes('dinheiro') || lower.includes('orcamento')) {
                    return 'Capacitação prática em gestão financeira e planejamento pessoal, essencial para a autonomia socioeconômica, consumo consciente e futuro sustentável dos educandos.';
                }
                if (lower.includes('sexualidade') || lower.includes('afetividade') || lower.includes('saude sexual')) {
                    return 'Espaço de acolhimento e conscientização com base científica e respeito, abordando autocuidado, prevenção e cidadania responsável para a juventude.';
                }
                if (lower.includes('violencia') || lower.includes('mulher') || lower.includes('genero') || lower.includes('direitos')) {
                    return 'Roda de reflexão e fortalecimento da cidadania sobre os direitos da mulher e combate à violência, estimulando uma postura ética, crítica e transformadora na comunidade.';
                }
                if (lower.includes('carreira') || lower.includes('entrevista') || lower.includes('trabalho') || lower.includes('curriculo') || lower.includes('empregabilidade')) {
                    return 'Orientações práticas de postura profissional, elaboração de currículo e preparação para processos seletivos em grandes empresas parceiras.';
                }
                if (lower.includes('lideranca') || lower.includes('etica') || lower.includes('comunicacao')) {
                    return 'Desenvolvimento de soft skills, protagonismo e comunicação assertiva, capacitando os estudantes a liderarem suas próprias trajetórias profissionais.';
                }

                // 2. Palestras com qualquer outro tema não mapeado (extrai o assunto principal do título)
                if (categoryKey === 'palestras' || lower.includes('palestra') || lower.includes('workshop')) {
                    const subject = cleanTitle.replace(/^(Palestra|Workshop|Semin[aá]rio)\s*(sobre|de|da|do|para)?\s*/i, '').trim();
                    if (subject) {
                        return `Encontro de desenvolvimento integral dedicado a ${subject}, conectando os alunos a especialistas e referências fundamentais para sua evolução pessoal e profissional.`;
                    }
                    return 'Encontro enriquecedor com profissionais convidados, ampliando a visão de mundo e preparando os alunos com competências essenciais para o mercado de trabalho.';
                }

                // 3. Outras Categorias de Eventos
                if (categoryKey === 'feiras') {
                    return 'Mostra de talentos e conexão direta com o universo produtivo, evidenciando o potencial técnico e criativo dos estudantes em projetos reais.';
                }
                if (categoryKey === 'formaturas') {
                    return 'Celebração da conquista de um marco na trajetória acadêmica e profissional de quem concluiu seu curso com excelência e dedicação.';
                }
                if (categoryKey === 'visitas') {
                    return 'Experiência prática in loco no ecossistema corporativo, aproximando a teoria da sala de aula da rotina real das indústrias e empresas.';
                }

                return `Momento marcante vivenciado pela comunidade do CEDESP Jaguaré, celebrando o aprendizado coletivo e o impacto positivo na formação dos jovens.`;
            };

            driveAlbums.forEach(album => {
                const yearMatch = album.title.match(/\b(20\d{2})\b/);
                if (yearMatch) {
                    album.year = yearMatch[1];
                    uniqueYears.add(yearMatch[1]);
                } else {
                    album.year = 'Recente';
                }

                const catInfo = detectCategory(album.title);
                album.categoryKey = catInfo.key;
                album.categoryLabel = catInfo.label;
                album.categoryTag = catInfo.tag;

                if (!categoryGroups.has(catInfo.key)) {
                    categoryGroups.set(catInfo.key, {
                        key: catInfo.key,
                        label: catInfo.label,
                        count: 0
                    });
                }
                categoryGroups.get(catInfo.key).count++;
            });

            // Popula os botões de filtros por Categoria
            if (categoryFiltersContainer) {
                categoryFiltersContainer.innerHTML = '<button class="event-filter-btn active" data-filter="all">Todos os Eventos</button>';
                
                // Prioriza "Palestras" logo após "Todos" se existir
                const sortedCategories = Array.from(categoryGroups.values()).sort((a, b) => {
                    if (a.key === 'palestras') return -1;
                    if (b.key === 'palestras') return 1;
                    return a.label.localeCompare(b.label);
                });

                sortedCategories.forEach(cat => {
                    const btn = document.createElement('button');
                    btn.className = 'event-filter-btn';
                    btn.setAttribute('data-filter', cat.key);
                    btn.innerHTML = `${cat.label} <span class="filter-count">(${cat.count})</span>`;
                    btn.addEventListener('click', () => {
                        document.querySelectorAll('.event-filter-btn').forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');
                        currentFilter = cat.key;
                        applyFilter();
                    });
                    categoryFiltersContainer.appendChild(btn);
                });

                const allBtn = categoryFiltersContainer.querySelector('[data-filter="all"]');
                if (allBtn) {
                    allBtn.innerHTML = `Todos os Eventos <span class="filter-count">(${driveAlbums.length})</span>`;
                    allBtn.addEventListener('click', () => {
                        document.querySelectorAll('.event-filter-btn').forEach(b => b.classList.remove('active'));
                        allBtn.classList.add('active');
                        currentFilter = 'all';
                        applyFilter();
                    });
                }
            }

            // Popula Dropdown de Anos
            if (uniqueYears.size > 0 && yearSelect && yearFiltersWrapper) {
                yearFiltersWrapper.style.display = 'flex';
                yearSelect.innerHTML = '<option value="all">Todos os Anos</option>';
                Array.from(uniqueYears).sort().reverse().forEach(yr => {
                    const opt = document.createElement('option');
                    opt.value = yr;
                    opt.textContent = yr;
                    yearSelect.appendChild(opt);
                });
                yearSelect.onchange = (e) => {
                    currentYear = e.target.value;
                    applyFilter();
                };
            }

            // B) Renderizar os Cards de Álbuns
            eventsGrid.innerHTML = '';
            driveAlbums.forEach((album, idx) => {
                const card = document.createElement('div');
                card.className = 'event-card animate-on-scroll';
                card.setAttribute('data-album-id', album.id);
                card.setAttribute('data-category', album.categoryKey || 'outros');
                card.setAttribute('data-year', album.year || 'all');
                card.style.animationDelay = `${(idx + 1) * 0.08}s`;

                const cover = album.coverUrl || (album.images && album.images[0] ? album.images[0].thumbUrl : '');
                const enrichedDescription = generateEnrichedDescription(album.title, album.categoryKey);

                card.innerHTML = `
                    <div class="event-image-wrap">
                        <div class="image-placeholder" style="background: linear-gradient(135deg,rgba(0,0,0,0.6), rgba(0,0,0,0.15)), url('${cover}') center/cover no-repeat;">
                        </div>
                        <span class="event-category-badge ${album.categoryKey}">${album.categoryTag}</span>
                        <div class="event-year-tag">${album.photoCount} fotos</div>
                    </div>
                    <div class="event-content">
                        <span class="event-date">${album.categoryLabel} • CEDESP</span>
                        <h3>${album.title}</h3>
                        <p class="event-enriched-desc">${enrichedDescription}</p>
                        <a href="#" class="view-album-btn">Ver Fotos <span>→</span></a>
                    </div>
                `;

                card.addEventListener('click', (e) => {
                    e.preventDefault();
                    openAlbum(album);
                });

                eventsGrid.appendChild(card);
            });

            applyFilter();
        };

        // 3. Filtragem de Cards
        const applyFilter = () => {
            const cards = eventsGrid.querySelectorAll('.event-card');
            let countVisible = 0;

            cards.forEach(card => {
                const cardCategory = card.getAttribute('data-category');
                const cardYear = card.getAttribute('data-year');

                const matchCategory = (currentFilter === 'all' || cardCategory === currentFilter);
                const matchYear = (currentYear === 'all' || cardYear === currentYear);

                if (matchCategory && matchYear) {
                    card.style.display = 'flex';
                    card.classList.remove('hiding');
                    countVisible++;
                } else {
                    card.classList.add('hiding');
                    card.style.display = 'none';
                }
            });

            if (noEventsMessage) {
                noEventsMessage.style.display = (countVisible === 0) ? 'block' : 'none';
            }
        };

        // ================================================================
        // 4. MODAL COM ORIGINKIT SMOOTH SCROLL GALLERY SLIDER
        // ================================================================
        const sliderViewport = document.getElementById('albumSliderViewport');
        const counterCurrent = document.getElementById('originkitCurrentNum');
        const counterTotal = document.getElementById('originkitTotalNum');
        const prevBtn = document.getElementById('albumSliderPrev');
        const nextBtn = document.getElementById('albumSliderNext');

        let activeSliderRaf = null;
        let cleanupSliderEvents = null;

        const openAlbum = (album) => {
            activeAlbum = album;
            titleEl.textContent = album.title;
            if (counterTotal) counterTotal.textContent = album.images.length;
            if (counterCurrent) counterCurrent.textContent = '1';

            lightboxOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';

            // Aguarda o próximo frame para garantir que as dimensões do modal (width/height) estejam calculadas
            requestAnimationFrame(() => {
                initOriginkitGallery(album);
            });
        };

        const closeLightbox = () => {
            if (activeSliderRaf) {
                cancelAnimationFrame(activeSliderRaf);
                activeSliderRaf = null;
            }
            if (cleanupSliderEvents) {
                cleanupSliderEvents();
                cleanupSliderEvents = null;
            }
            if (sliderViewport) sliderViewport.innerHTML = '';
            lightboxOverlay.classList.remove('active');
            document.body.style.overflow = '';
        };

        closeBtn?.addEventListener('click', closeLightbox);

        // Suporte a teclado
        document.addEventListener('keydown', (e) => {
            if (!lightboxOverlay.classList.contains('active')) return;
            if (e.key === 'Escape') closeLightbox();
        });

        // Motor Originkit Smooth Scroll Slider adaptado fielmente do código base
        const initOriginkitGallery = (album) => {
            if (!sliderViewport || !album.images || album.images.length === 0) return;

            // Limpa instâncias e animações anteriores
            if (activeSliderRaf) {
                cancelAnimationFrame(activeSliderRaf);
                activeSliderRaf = null;
            }
            if (cleanupSliderEvents) {
                cleanupSliderEvents();
                cleanupSliderEvents = null;
            }
            sliderViewport.innerHTML = '';

            const images = album.images;
            const isMobile = window.innerWidth <= 768;
            const isNarrow = window.innerWidth <= 380;

            // Originkit Defaults:
            // "smoothness": 0, "background": "#000000", "sensitivity": 5.1, slideWidth: 400, slideHeight: 400
            const slideWidth = isNarrow ? 260 : (isMobile ? 310 : 400);
            const slideHeight = isNarrow ? 260 : (isMobile ? 310 : 400);
            const spacing = 2;
            const direction = "right";
            const smoothness = 0; // Preset Originkit
            const background = "#000000";
            const radius = 16;
            const dim = 10;
            const sensitivity = 5.1; // Preset Originkit
            const loop = images.length > 2;

            // Escala ideal: centro com destaque (1.35x) e laterais visíveis e elegantes (0.7x)
            const MAX_SCALE = isMobile ? 1.15 : 1.35;
            const MIN_SCALE = isMobile ? 0.65 : 0.7;

            const wrap = (value, span) => ((value % span) + span) % span;
            const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

            const step = slideWidth + clamp(spacing, 0, 10) * 20;
            const ease = 0.15 - (clamp(smoothness, 0, 10) / 10) * 0.13;
            const dimAmount = (clamp(dim, 0, 10) / 10) * 0.85;
            const wheelMultiplier = 0.4 + (clamp(sensitivity, 0, 10) / 10) * 1.2;
            const dragMultiplier = 0.6 + (clamp(sensitivity, 0, 10) / 10) * 1.8;
            const flip = direction === "left";

            // Largura inicial do container
            let containerWidth = sliderViewport.getBoundingClientRect().width || sliderViewport.clientWidth || window.innerWidth;
            if (containerWidth <= 0) containerWidth = window.innerWidth;

            const repeats = (!loop || containerWidth <= 0 || step <= 0)
                ? 1
                : Math.max(1, Math.ceil((containerWidth + step * 2) / (images.length * step)));

            const slides = [];
            for (let r = 0; r < repeats; r++) {
                images.forEach((imgObj, originalIdx) => {
                    slides.push({
                        src: imgObj.fullUrl || imgObj.thumbUrl,
                        offsetY: 0,
                        originalIdx,
                        alt: imgObj.name || album.title
                    });
                });
            }

            // Cria nós DOM com estilos idênticos ao React
            const nodes = slides.map((slide, i) => {
                const el = document.createElement('div');
                el.className = 'originkit-slide-item';
                el.style.position = 'absolute';
                el.style.top = '50%';
                el.style.left = '0px';
                el.style.width = `${slideWidth}px`;
                el.style.height = `${slideHeight}px`;
                el.style.borderRadius = `${radius}px`;
                el.style.overflow = 'hidden';
                el.style.background = '#111';
                el.style.willChange = 'transform, filter';
                el.style.transform = 'translate3d(0, -50%, 0)';
                el.style.pointerEvents = 'none';

                if (slide.src) {
                    const img = document.createElement('img');
                    img.alt = slide.alt;
                    img.draggable = false;
                    img.src = slide.src;
                    img.style.width = '100%';
                    img.style.height = '100%';
                    img.style.objectFit = 'cover';
                    img.style.objectPosition = `50% calc(50% + ${slide.offsetY}px)`;
                    img.style.display = 'block';
                    img.style.userSelect = 'none';
                    el.appendChild(img);
                }

                sliderViewport.appendChild(el);
                return { el, originalIdx: slide.originalIdx };
            });

            sliderViewport.style.opacity = '1';

            const count = slides.length;
            const span = count * step;

            let targetX = 0;
            let currentX = 0;
            let lastTime = 0;

            const tick = (now) => {
                activeSliderRaf = requestAnimationFrame(tick);
                const delta = lastTime ? Math.min((now - lastTime) / 1000, 0.1) : 1 / 60;
                lastTime = now;

                // Medição dinâmica para evitar que containerWidth seja 0 ou incorreto
                const currentWidth = sliderViewport.getBoundingClientRect().width || sliderViewport.clientWidth || window.innerWidth;
                if (currentWidth > 0) containerWidth = currentWidth;

                if (!count || step <= 0 || containerWidth <= 0) return;

                if (loop) {
                    if (currentX > span || currentX < -span) {
                        const shift = Math.trunc(currentX / span) * span;
                        currentX -= shift;
                        targetX -= shift;
                    }
                } else {
                    targetX = clamp(targetX, 0, (count - 1) * step);
                }

                const k = 1 - Math.pow(1 - ease, delta * 60);
                currentX += (targetX - currentX) * k;

                const pad = (containerWidth - slideWidth) / 2;
                const half = containerWidth / 2;

                let closestDist = Infinity;
                let closestIdx = 0;

                for (let i = 0; i < count; i++) {
                    const node = nodes[i];
                    if (!node) continue;

                    const raw = i * step - currentX + pad;
                    const x = loop ? wrap(raw + step, span) - step : raw;

                    const distance = x + slideWidth / 2 - half;
                    const absDist = Math.abs(distance);

                    if (absDist < closestDist) {
                        closestDist = absDist;
                        closestIdx = node.originalIdx;
                    }

                    // A imagem central tem distance = 0 (absDist = 0) e deve ser a MAIOR.
                    // Conforme se afasta do centro para a esquerda ou direita, o scale diminui suavemente.
                    const normDist = clamp(absDist / (containerWidth * 0.5), 0, 1);
                    const scale = MAX_SCALE - normDist * (MAX_SCALE - MIN_SCALE);

                    const left = flip ? containerWidth - slideWidth - x : x;
                    node.el.style.transform = `translate3d(${left}px, -50%, 0) scale(${scale})`;

                    if (dimAmount > 0) {
                        const t = normDist;
                        node.el.style.filter = `brightness(${1 - t * dimAmount})`;
                    } else {
                        node.el.style.filter = 'none';
                    }

                    node.el.style.zIndex = Math.round(1000 - absDist);
                }

                if (counterCurrent) {
                    counterCurrent.textContent = (closestIdx + 1);
                }
            };

            activeSliderRaf = requestAnimationFrame(tick);

            // ==================== INTERAÇÕES DE POINTER E WHEEL (ORIGINKIT ORIGINAL) ====================
            let pointerId = null;
            let lastPointerX = 0;

            const onPointerDown = (event) => {
                if (pointerId !== null) return;
                pointerId = event.pointerId;
                lastPointerX = event.clientX;
                try {
                    sliderViewport.setPointerCapture(event.pointerId);
                } catch (err) {}
            };

            const onPointerMove = (event) => {
                if (pointerId !== event.pointerId) return;
                const dx = event.clientX - lastPointerX;
                lastPointerX = event.clientX;
                targetX += (flip ? dx : -dx) * dragMultiplier;
            };

            const onPointerUp = (event) => {
                if (pointerId !== event.pointerId) return;
                pointerId = null;
                try {
                    if (sliderViewport.hasPointerCapture(event.pointerId)) {
                        sliderViewport.releasePointerCapture(event.pointerId);
                    }
                } catch (err) {}
            };

            sliderViewport.addEventListener('pointerdown', onPointerDown);
            sliderViewport.addEventListener('pointermove', onPointerMove);
            sliderViewport.addEventListener('pointerup', onPointerUp);
            sliderViewport.addEventListener('pointercancel', onPointerUp);

            // Wheel listener
            const onWheel = (event) => {
                event.preventDefault();
                const dominant = Math.abs(event.deltaX) > Math.abs(event.deltaY)
                    ? event.deltaX
                    : event.deltaY;
                targetX += dominant * wheelMultiplier;
            };
            sliderViewport.addEventListener('wheel', onWheel, { passive: false });

            // Botões Next / Prev
            const onNextClick = (e) => {
                e.preventDefault();
                targetX += step;
            };
            const onPrevClick = (e) => {
                e.preventDefault();
                targetX -= step;
            };

            nextBtn?.addEventListener('click', onNextClick);
            prevBtn?.addEventListener('click', onPrevClick);

            // Resize observer
            const resizeObserver = new ResizeObserver((entries) => {
                if (entries[0]) {
                    containerWidth = entries[0].contentRect.width;
                }
            });
            resizeObserver.observe(sliderViewport);

            // Cleanup
            cleanupSliderEvents = () => {
                sliderViewport.removeEventListener('pointerdown', onPointerDown);
                sliderViewport.removeEventListener('pointermove', onPointerMove);
                sliderViewport.removeEventListener('pointerup', onPointerUp);
                sliderViewport.removeEventListener('pointercancel', onPointerUp);
                sliderViewport.removeEventListener('wheel', onWheel);
                nextBtn?.removeEventListener('click', onNextClick);
                prevBtn?.removeEventListener('click', onPrevClick);
                resizeObserver.disconnect();
            };
        };

        // Inicia a sincronização ao carregar a página
        fetchDriveEvents();
    }

    // ===== REMOVER MARCA D'ÁGUA DO BEHOLD (DENTRO DO SHADOW DOM) =====
    const hideBeholdWatermark = () => {
        const beholdWidget = document.querySelector('behold-widget');
        if (beholdWidget && beholdWidget.shadowRoot) {
            // Remove o link de marca d'água se já tiver sido renderizado no DOM
            const links = beholdWidget.shadowRoot.querySelectorAll('a');
            links.forEach(link => {
                if (link.href && (link.href.includes('behold.so') || link.innerText.toLowerCase().includes('behold'))) {
                    link.style.setProperty('display', 'none', 'important');
                    link.style.setProperty('visibility', 'hidden', 'important');
                    link.style.setProperty('height', '0', 'important');
                    link.style.setProperty('opacity', '0', 'important');
                    link.style.setProperty('pointer-events', 'none', 'important');
                    
                    if (link.parentElement) {
                        link.parentElement.style.setProperty('display', 'none', 'important');
                        link.parentElement.style.setProperty('visibility', 'hidden', 'important');
                        link.parentElement.style.setProperty('height', '0', 'important');
                    }
                }
            });

            // Injeta o estilo preventivo para o caso de novas renderizações
            if (!beholdWidget.shadowRoot.querySelector('#hide-behold-style')) {
                const style = document.createElement('style');
                style.id = 'hide-behold-style';
                style.textContent = `
                    a[href*="behold.so"], 
                    div[class*="watermark"], 
                    [class*="branding"],
                    div[style*="justify-content: center"] > a { 
                        display: none !important; 
                        visibility: hidden !important; 
                        opacity: 0 !important; 
                        height: 0 !important; 
                        pointer-events: none !important;
                    }
                `;
                beholdWidget.shadowRoot.appendChild(style);
            }
        }
    };

    // Roda de forma contínua no início para pegar o delay do carregamento
    const beholdInterval = setInterval(hideBeholdWatermark, 150);
    // Limpa o interval após 10 segundos para economizar processamento do navegador
    setTimeout(() => clearInterval(beholdInterval), 10000);

    // ================================================================
    // ORIGINKIT SMOOTH SCROLL SLIDER MOTOR — CEDESP JAGUARÉ
    // ================================================================
    const sliderContainer = document.getElementById('smoothScrollSlider');
    if (sliderContainer) {
        const slideData = [
            {
                title: "CCA Jaguaré",
                category: "Desenvolvimento Infantil",
                desc: "Atendimento social diário, oficinas culturais e acompanhamento nutricional para crianças e adolescentes.",
                img: "images/fotos/4.jpg",
                link: "historia.html#cca",
                btnText: "Conhecer o CCA"
            },
            {
                title: "Projetos da Casa",
                category: "Cultura & Comunidade",
                desc: "Iniciativas socioculturais, bazares comunitários e ações de acolhimento para fortalecer famílias locais.",
                img: "images/fotos/5.webp",
                link: "eventos.html",
                btnText: "Ver Projetos & Eventos"
            },
            {
                title: "Cursos SENAI Gratuitos",
                category: "Qualificação Profissional",
                desc: "Formação técnica com certificação padrão SENAI nas áreas de TI, Mecânica, Linha Branca e Gestão.",
                img: "images/fotos/6.jpg",
                link: "cursos.html#filtros-cursos",
                btnText: "Explorar Cursos"
            },
            {
                title: "Parceria RD Saúde",
                category: "Saúde & Farmácia",
                desc: "Palestras técnicas, atividades sociais e orientação profissional especializada dentro do CEDESP Jaguaré.",
                img: "images/rd_saude_banner.jpg",
                link: "https://rdsaude.com.br",
                btnText: "Saiba Mais"
            },
            {
                title: "Faça Parte da Mudança",
                category: "Voluntariado & Doações",
                desc: "Apoie nossos projetos sociais através do voluntariado, parcerias ou participando ativamente.",
                img: "images/fotos/1.jpg",
                link: "https://wa.me/5511972423702?text=Ol%C3%A1%20quero%20apoiar%20os%20projetos%20do%20CEDESP%20Jaguar%C3%A9!",
                btnText: "Falar no WhatsApp"
            },
            {
                title: "Visite Nosso Bazar",
                category: "Bazar Beneficente",
                desc: "Roupas, calçados e utensílios com valores simbólicos cuja renda apoia integralmente nossos atendidos.",
                img: "images/fotos/2.jpg",
                link: "https://redecomunita.org.br/bazar",
                btnText: "Visitar Bazar"
            },
            {
                title: "Parceria LOGA",
                category: "Sustentabilidade",
                desc: "Educação ambiental e conscientização sobre reciclagem para um Jaguaré mais limpo e sustentável.",
                img: "images/loga_equipe.jpg",
                link: "https://www.loga.com.br",
                btnText: "Conhecer Parceria"
            },
            {
                title: "Nossa Trajetória",
                category: "História & Legado",
                desc: "Mais de 70 anos de dedicação contínua transformando destinos na Zona Oeste de São Paulo.",
                img: "images/fotos/3.JPG",
                link: "historia.html",
                btnText: "Ler Nossa História"
            }
        ];

        // Constantes da física Originkit
        const isMobile = () => window.innerWidth <= 992;
        const isNarrowMobile = () => window.innerWidth <= 375;
        const getSlideWidth = () => isNarrowMobile() ? 245 : (isMobile() ? 275 : 460);
        const getSlideHeight = () => isNarrowMobile() ? 330 : (isMobile() ? 360 : 500);
        const getMaxScale = () => isMobile() ? 1.15 : 1.35;
        const MIN_SCALE = 0.55;
        const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
        const wrap = (val, span) => ((val % span) + span) % span;

        // Configuração
        let slideWidth = getSlideWidth();
        const spacing = 2;
        let step = slideWidth + clamp(spacing, 0, 10) * (isMobile() ? 14 : 20);
        const smoothness = 8;
        const ease = 0.15 - (clamp(smoothness, 0, 10) / 10) * 0.13;
        const dimAmount = 0.55;
        const wheelMultiplier = 1.35;
        const loop = true;

        let width = sliderContainer.getBoundingClientRect().width || window.innerWidth;
        let repeats = Math.max(1, Math.ceil((width + step * 2) / (slideData.length * step))) + 1;

        // Monta slides repetidos para loop contínuo
        const allSlides = [];
        for (let r = 0; r < repeats; r++) {
            allSlides.push(...slideData);
        }

        // Renderiza elementos no DOM
        sliderContainer.innerHTML = '';
        const nodes = allSlides.map((item, i) => {
            const el = document.createElement('a');
            el.className = 'smooth-slide-node';
            el.href = item.link;
            if (item.link.startsWith('http')) {
                el.target = '_blank';
                el.rel = 'noopener noreferrer';
            }

            el.innerHTML = `
                <img src="${item.img}" alt="${item.title}" class="smooth-slide-img" draggable="false" loading="lazy">
                <div class="smooth-slide-overlay">
                    <span class="smooth-slide-category">${item.category}</span>
                    <h3 class="smooth-slide-title">${item.title}</h3>
                    <p class="smooth-slide-desc">${item.desc}</p>
                    <div class="smooth-slide-btn">
                        <span>${item.btnText}</span>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="5" y1="12" x2="19" y2="12"></line>
                            <polyline points="12 5 19 12 12 19"></polyline>
                        </svg>
                    </div>
                </div>
            `;
            sliderContainer.appendChild(el);
            return el;
        });

        // Estado do motor de física
        let targetX = 0;
        let currentX = 0;
        const count = allSlides.length;

        // Resize observer para recalibrar nos diferentes iPhones
        const resizeObserver = new ResizeObserver(entries => {
            if (entries[0]) {
                width = entries[0].contentRect.width;
                slideWidth = getSlideWidth();
                step = slideWidth + clamp(spacing, 0, 10) * (isMobile() ? 14 : 20);
            }
        });
        resizeObserver.observe(sliderContainer);

        // Animação RAF
        let lastTime = 0;
        let isDragging = false;
        let startPointerX = 0;
        let startPointerY = 0;
        let lastPointerX = 0;
        let pointerDeltaAccum = 0;
        let isHorizontalGesture = null;
        let velocityX = 0;
        let lastDragTime = 0;

        // Elemento da thumb bar mobile
        const thumbBar = document.getElementById('smoothThumbBar');

        const tick = (now) => {
            requestAnimationFrame(tick);
            const delta = lastTime ? Math.min((now - lastTime) / 1000, 0.1) : 1 / 60;
            lastTime = now;

            if (!count || step <= 0 || width <= 0) return;

            const span = count * step;

            // Loop wrapping
            if (loop) {
                if (currentX > span || currentX < -span) {
                    const shift = Math.trunc(currentX / span) * span;
                    currentX -= shift;
                    targetX -= shift;
                }
            } else {
                targetX = clamp(targetX, 0, (count - 1) * step);
            }

            // Suavização do movimento (Easing)
            const k = 1 - Math.pow(1 - ease, delta * 60);
            currentX += (targetX - currentX) * k;

            // Se não estiver arrastando, adiciona sutil avanço automático contínuo
            if (!isDragging) {
                targetX += 0.35;
            }

            // Atualiza barra de progresso mobile
            if (thumbBar) {
                const totalCycle = slideData.length * step;
                const normalized = wrap(currentX, totalCycle) / totalCycle;
                const maxLeft = 70; // percentual restante
                thumbBar.style.left = `${normalized * maxLeft}%`;
            }

            const pad = (width - slideWidth) / 2;
            const half = width / 2;
            const maxScale = getMaxScale();

            for (let i = 0; i < count; i++) {
                const node = nodes[i];
                if (!node) continue;

                const raw = i * step - currentX + pad;
                const x = loop ? wrap(raw + step, span) - step : raw;

                const distance = x + slideWidth / 2 - half;
                let scale;
                let push;

                if (distance > 0) {
                    scale = Math.min(maxScale, 1 + distance / width);
                    push = (scale - 1) * slideWidth * (isMobile() ? 0.45 : 0.75);
                } else {
                    scale = Math.max(MIN_SCALE, 1 + distance / width);
                    push = 0;
                }

                const left = x + push;
                node.style.transform = `translate3d(${left}px, -50%, 0) scale(${scale})`;

                // Ajuste de brilho/dimming nas bordas
                if (dimAmount > 0 && scale < 1) {
                    const t = (1 - scale) / Math.max(0.001, 1 - MIN_SCALE);
                    node.style.filter = `brightness(${1 - t * dimAmount})`;
                } else {
                    node.style.filter = 'none';
                }

                // Z-index baseado na proximidade do centro
                const centerDist = Math.abs(distance);
                node.style.zIndex = Math.round(1000 - centerDist);
            }
        };
        requestAnimationFrame(tick);

        // ================================================================
        // COMANDOS DE CELULAR: TOUCH / DRAG COM FÍSICA E MOMENTUM
        // ================================================================
        const onPointerDown = (e) => {
            if (e.pointerType === 'mouse' && e.button !== 0) return;
            isDragging = true;
            startPointerX = e.clientX;
            startPointerY = e.clientY;
            lastPointerX = e.clientX;
            lastDragTime = performance.now();
            pointerDeltaAccum = 0;
            isHorizontalGesture = null;
            velocityX = 0;
            sliderContainer.setPointerCapture(e.pointerId);
        };

        const onPointerMove = (e) => {
            if (!isDragging) return;

            const dx = e.clientX - lastPointerX;
            const totalDx = e.clientX - startPointerX;
            const totalDy = e.clientY - startPointerY;

            // Determina direção primária do gesto para não bloquear scroll vertical
            if (isHorizontalGesture === null) {
                if (Math.abs(totalDx) > 8 || Math.abs(totalDy) > 8) {
                    isHorizontalGesture = Math.abs(totalDx) >= Math.abs(totalDy);
                }
            }

            if (isHorizontalGesture) {
                if (e.cancelable) e.preventDefault();
                pointerDeltaAccum += Math.abs(dx);
                targetX -= dx * 1.35;

                const now = performance.now();
                const dt = Math.max(1, now - lastDragTime);
                velocityX = (dx / dt) * 16;
                lastDragTime = now;
            }

            lastPointerX = e.clientX;
        };

        const onPointerUp = (e) => {
            if (!isDragging) return;
            isDragging = false;

            try {
                sliderContainer.releasePointerCapture(e.pointerId);
            } catch (err) {}

            // Aplica inércia de deslize (momentum)
            if (isHorizontalGesture && Math.abs(velocityX) > 2) {
                targetX -= velocityX * 18;
            }

            // Se arrastou intencionalmente, impede que o clique abra o link acidentalmente
            if (pointerDeltaAccum > 12) {
                const preventClick = (ev) => {
                    ev.preventDefault();
                    ev.stopPropagation();
                    window.removeEventListener('click', preventClick, true);
                };
                window.addEventListener('click', preventClick, true);
            }

            isHorizontalGesture = null;
        };

        sliderContainer.addEventListener('pointerdown', onPointerDown, { passive: true });
        sliderContainer.addEventListener('pointermove', onPointerMove, { passive: false });
        sliderContainer.addEventListener('pointerup', onPointerUp, { passive: true });
        sliderContainer.addEventListener('pointercancel', onPointerUp, { passive: true });

        // ================================================================
        // COMANDOS DE CELULAR: BOTÕES DE AVANÇAR E RETROCEDER (SLIDER)
        // ================================================================
        const prevBtn = document.getElementById('smoothPrevBtn');
        const nextBtn = document.getElementById('smoothNextBtn');

        if (prevBtn) {
            prevBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const currentStep = step || 280;
                targetX -= currentStep * 1.05;
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const currentStep = step || 280;
                targetX += currentStep * 1.05;
            });
        }

        // Scroll do mouse (Só intercepta e passa o slider quando os cards estiverem centralizados na tela)
        sliderContainer.addEventListener('wheel', (e) => {
            // Se for scroll horizontal (shift + wheel ou touchpad horizontal), sempre permite passar o slider
            if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
                e.preventDefault();
                targetX += e.deltaX * wheelMultiplier;
                return;
            }

            // Para scroll vertical: verifica se a seção/cards estão centralizados no meio da viewport
            const rect = sliderContainer.getBoundingClientRect();
            const sliderCenter = rect.top + rect.height / 2;
            const viewportCenter = window.innerHeight / 2;
            const tolerance = Math.min(160, rect.height * 0.35); // Faixa de centralização confortável

            const isCentered = Math.abs(sliderCenter - viewportCenter) <= tolerance;

            if (isCentered) {
                // Está centralizado: intercepta e faz o slider avançar/retroceder
                e.preventDefault();
                targetX += e.deltaY * wheelMultiplier;
            }
            // Caso NÃO esteja centralizado na tela, NÃO chama preventDefault(): a página rola normalmente até centralizar
        }, { passive: false });
    }

    // ================================================================
    // ORIGINKIT RADIAL REVEAL BUTTON MOTOR (POINTER-ANCHORED EXPANSION)
    // ================================================================
    const radialButtons = document.querySelectorAll('.originkit-radial-btn');
    radialButtons.forEach(btn => {
        const overlay = btn.querySelector('.overlay-face');
        if (!overlay) return;

        let isHovered = false;

        function updateCircle(xPct, yPct, radiusPct) {
            const clip = `circle(${radiusPct}% at ${xPct}% ${yPct}%)`;
            overlay.style.clipPath = clip;
            overlay.style.webkitClipPath = clip;
        }

        btn.addEventListener('pointerenter', e => {
            isHovered = true;
            const rect = btn.getBoundingClientRect();
            const px = e.clientX - rect.left;
            const py = e.clientY - rect.top;

            const xPct = (px / rect.width) * 100;
            const yPct = (py / rect.height) * 100;

            // Calcula o ponto mais distante para garantir que o círculo cubra todo o botão
            const far = Math.max(
                Math.hypot(px, py),
                Math.hypot(rect.width - px, py),
                Math.hypot(px, rect.height - py),
                Math.hypot(rect.width - px, rect.height - py)
            );
            const unit = Math.hypot(rect.width, rect.height) / Math.SQRT2;
            const maxRadiusPct = (far / unit) * 100 + 10;

            // Inicia do ponto onde o mouse entrou com raio zero
            overlay.style.transition = 'none';
            updateCircle(xPct, yPct, 0);

            // Força repaint para transição suave
            void overlay.offsetHeight;

            // Expande radialmente
            overlay.style.transition = 'clip-path 0.45s cubic-bezier(0.25, 1, 0.5, 1), -webkit-clip-path 0.45s cubic-bezier(0.25, 1, 0.5, 1)';
            updateCircle(xPct, yPct, maxRadiusPct);
        });

        btn.addEventListener('pointerleave', e => {
            isHovered = false;
            const rect = btn.getBoundingClientRect();
            const px = Math.max(0, Math.min(rect.width, e.clientX - rect.left));
            const py = Math.max(0, Math.min(rect.height, e.clientY - rect.top));

            const xPct = (px / rect.width) * 100;
            const yPct = (py / rect.height) * 100;

            // Retrai o círculo em direção ao ponto de saída
            overlay.style.transition = 'clip-path 0.35s cubic-bezier(0.25, 0.8, 0.25, 1), -webkit-clip-path 0.35s cubic-bezier(0.25, 0.8, 0.25, 1)';
            updateCircle(xPct, yPct, 0);
        });
    });
});
