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
    const logoHighlights = document.querySelectorAll('.logo-highlight');
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
        'Operador de Microcomputador': 'informatica',
        'Web Designer': 'informatica',
        'Assistente de TI': 'informatica',
        'Controle de Qualidade': 'administracao',
        'Recursos Humanos (RH)': 'administracao',
        'Auxiliar Administrativo': 'administracao'
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
});
