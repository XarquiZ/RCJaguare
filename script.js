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

    // ===== CONTADOR ANIMADO NO HERO =====
    const counterElement = document.querySelector('.impact-number');
    if (counterElement) {
        const target = parseInt(counterElement.getAttribute('data-target'));
        const duration = 2000; // 2 segundos
        let started = false;

        const startCounter = () => {
            let startTimestamp = null;
            const step = (timestamp) => {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                const currentCount = Math.floor(progress * target);
                
                // Formata com ponto (ex: 7.000)
                counterElement.textContent = currentCount.toLocaleString('pt-BR');
                
                if (progress < 1) {
                    window.requestAnimationFrame(step);
                } else {
                    counterElement.textContent = target.toLocaleString('pt-BR');
                }
            };
            window.requestAnimationFrame(step);
        };

        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !started) {
                    started = true;
                    setTimeout(startCounter, 500); // Pequeno delay para suavidade
                }
            });
        }, { threshold: 0.5 });

        counterObserver.observe(counterElement);
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
});
