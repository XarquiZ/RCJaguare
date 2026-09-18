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

    // ===== LÓGICA DE FILTROS DA PÁGINA DE EVENTOS =====
    const categoryBtns = document.querySelectorAll('.event-filter-btn');
    const yearSelect = document.getElementById('yearSelect');
    const eventCards = document.querySelectorAll('.event-card');
    const noEventsMessage = document.getElementById('noEventsMessage');

    if (categoryBtns.length > 0 && eventCards.length > 0) {
        
        let currentCategory = 'all';
        let currentYear = 'all';

        const filterEvents = () => {
            let visibleCount = 0;

            eventCards.forEach(card => {
                const cardCategory = card.getAttribute('data-category');
                const cardYear = card.getAttribute('data-year');

                // Condição de Match
                const matchCategory = currentCategory === 'all' || cardCategory === currentCategory;
                const matchYear = currentYear === 'all' || cardYear === currentYear;

                if (matchCategory && matchYear) {
                    // Mostrar com animação
                    card.style.display = 'flex';
                    setTimeout(() => {
                        card.classList.remove('hiding');
                    }, 50);
                    visibleCount++;
                } else {
                    // Esconder com animação
                    card.classList.add('hiding');
                    setTimeout(() => {
                        if (card.classList.contains('hiding')) {
                            card.style.display = 'none';
                        }
                    }, 400); // Tempo igual a transição do CSS
                }
            });

            // Mostra ou esconde mensagem "nenhum evento"
            if (noEventsMessage) {
                setTimeout(() => {
                    noEventsMessage.style.display = visibleCount === 0 ? 'block' : 'none';
                }, 400);
            }
        };

        // Event Listeners Category
        categoryBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                // Atualiza UI dos bots
                categoryBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                currentCategory = btn.getAttribute('data-filter');
                filterEvents();
            });
        });

        // Event Listener Year
        if (yearSelect) {
            yearSelect.addEventListener('change', (e) => {
                currentYear = e.target.value;
                filterEvents();
            });
        }
    }

    // ===== LÓGICA DO LIGHTBOX DE ÁLBUNS =====
    const lightboxOverlay = document.getElementById('albumLightbox');
    if (lightboxOverlay && typeof ALBUMS_DATA !== 'undefined') {
        const titleEl = document.getElementById('lightboxTitle');
        const gridView = document.getElementById('lightboxGrid');
        const fullView = document.getElementById('lightboxFullscreen');
        const fullscreenImg = document.getElementById('fullscreenImage');
        const currentImgNum = document.getElementById('currentImgNum');
        const totalImgNum = document.getElementById('totalImgNum');
        const closeBtn = document.querySelector('.lightbox-close');
        
        let currentAlbum = null;
        let currentIndex = 0;

        // Abrir o álbum a partir dos cartões (toda a área do card)
        const albumCards = document.querySelectorAll('.event-card[data-album]');
        albumCards.forEach(card => {
            card.addEventListener('click', (e) => {
                e.preventDefault();
                const albumId = card.getAttribute('data-album');
                if(ALBUMS_DATA[albumId]) {
                    openAlbum(albumId);
                }
            });
        });

        function openAlbum(albumId) {
            currentAlbum = ALBUMS_DATA[albumId];
            titleEl.textContent = currentAlbum.title;
            
            // Limpa o grid antigo e monta o novo
            gridView.innerHTML = '';
            
            currentAlbum.images.forEach((imgName, idx) => {
                const img = document.createElement('img');
                img.src = `${currentAlbum.path}thumb/${imgName}`;
                img.classList.add('lightbox-thumb');
                img.loading = 'lazy';
                img.style.animationDelay = `${(idx % 15) * 0.05}s`;
                
                img.onload = () => img.classList.add('loaded');
                
                img.addEventListener('click', () => {
                    openFullscreen(idx);
                });
                
                gridView.appendChild(img);
            });

            // Reseta Views
            gridView.style.display = 'grid';
            fullView.style.display = 'none';
            lightboxOverlay.classList.add('active');
            document.body.style.overflow = 'hidden'; // Evita scroll do site atrás do modal
        }

        // Navegação Tela Cheia
        function openFullscreen(index) {
            currentIndex = index;
            const imgName = currentAlbum.images[currentIndex];
            fullscreenImg.src = `${currentAlbum.path}full/${imgName}`;
            
            totalImgNum.textContent = currentAlbum.images.length;
            currentImgNum.textContent = currentIndex + 1;
            
            gridView.style.display = 'none';
            fullView.style.display = 'flex';
        }

        function showNext() {
            if(currentIndex < currentAlbum.images.length - 1) {
                openFullscreen(currentIndex + 1);
            }
        }

        function showPrev() {
            if(currentIndex > 0) {
                openFullscreen(currentIndex - 1);
            }
        }

        document.querySelector('.next-btn')?.addEventListener('click', showNext);
        document.querySelector('.prev-btn')?.addEventListener('click', showPrev);

        // Suporte a Setas do Teclado e Esc para fechar
        document.addEventListener('keydown', (e) => {
            if(!lightboxOverlay.classList.contains('active')) return;
            
            if(e.key === 'Escape') {
                if(fullView.style.display === 'flex') {
                    // Se estava tela cheia, volta pra grade
                    fullView.style.display = 'none';
                    gridView.style.display = 'grid';
                } else {
                    // Fecha o modal inteiro
                    closeLightbox();
                }
            }
            if(e.key === 'ArrowRight' && fullView.style.display === 'flex') showNext();
            if(e.key === 'ArrowLeft' && fullView.style.display === 'flex') showPrev();
        });

        function closeLightbox() {
            lightboxOverlay.classList.remove('active');
            document.body.style.overflow = '';
            // Limpa fonte d'água grande após animação
            setTimeout(() => { fullscreenImg.src = ''; }, 400); 
        }

        closeBtn.addEventListener('click', () => {
            if (fullView.style.display === 'flex') {
                // Se estava tela cheia, volta pra grade
                fullView.style.display = 'none';
                gridView.style.display = 'grid';
            } else {
                // Fecha o modal inteiro
                closeLightbox();
            }
        });
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
