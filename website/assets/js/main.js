/**
 * LangkahKampus - Main JavaScript
 * Core functionality: navbar, particles, counters, scroll effects, mobile menu
 */

document.addEventListener('DOMContentLoaded', function() {
    initNavbar();
    initMobileMenu();
    initSmoothScroll();
    initScrollAnimations();
    initCounterAnimation();
    initParticleBackground();
    initTestimonialCarousel();
    initToastAutoHide();
});

/* === Navbar Scroll Effect === */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });
}

/* === Mobile Menu === */
function initMobileMenu() {
    const toggle = document.getElementById('navToggle');
    const menu = document.getElementById('navMenu');

    if (!toggle || !menu) return;

    toggle.addEventListener('click', function() {
        toggle.classList.toggle('active');
        menu.classList.toggle('active');
        document.body.style.overflow = menu.classList.contains('active') ? 'hidden' : '';
    });

    // Close menu on link click
    const links = menu.querySelectorAll('.nav-link');
    links.forEach(function(link) {
        link.addEventListener('click', function() {
            toggle.classList.remove('active');
            menu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // Close menu on outside click
    document.addEventListener('click', function(e) {
        if (!menu.contains(e.target) && !toggle.contains(e.target) && menu.classList.contains('active')) {
            toggle.classList.remove('active');
            menu.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
}

/* === Smooth Scroll === */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                const navbarHeight = document.getElementById('navbar').offsetHeight;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/* === Scroll Animations (Intersection Observer) === */
function initScrollAnimations() {
    const elements = document.querySelectorAll('.animate-on-scroll, [data-aos]');

    if (!('IntersectionObserver' in window)) {
        elements.forEach(function(el) {
            el.classList.add('visible');
        });
        return;
    }

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    elements.forEach(function(el) {
        observer.observe(el);
    });
}

/* === Counter Animation === */
function initCounterAnimation() {
    const counters = document.querySelectorAll('[data-counter]');

    if (!counters.length) return;

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(function(counter) {
        observer.observe(counter);
    });
}

function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-counter'));
    const suffix = element.getAttribute('data-suffix') || '';
    const prefix = element.getAttribute('data-prefix') || '';
    const duration = 2000;
    const steps = 60;
    const increment = target / steps;
    let current = 0;
    const stepTime = duration / steps;

    const timer = setInterval(function() {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }

        element.textContent = prefix + formatNumber(Math.floor(current)) + suffix;
    }, stepTime);
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}

/* === Particle Background === */
function initParticleBackground() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationId;

    function resizeCanvas() {
        canvas.width = canvas.parentElement.offsetWidth;
        canvas.height = canvas.parentElement.offsetHeight;
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // Create particles
    const particleCount = Math.min(80, Math.floor((canvas.width * canvas.height) / 15000));

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            radius: Math.random() * 2 + 1,
            opacity: Math.random() * 0.5 + 0.2
        });
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Update and draw particles
        particles.forEach(function(p, i) {
            p.x += p.vx;
            p.y += p.vy;

            // Wrap around
            if (p.x < 0) p.x = canvas.width;
            if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            if (p.y > canvas.height) p.y = 0;

            // Draw particle
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(255, 255, 255, ' + p.opacity + ')';
            ctx.fill();

            // Connect nearby particles
            for (let j = i + 1; j < particles.length; j++) {
                var p2 = particles[j];
                var dx = p.x - p2.x;
                var dy = p.y - p2.y;
                var dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(p.x, p.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = 'rgba(255, 255, 255, ' + (0.15 * (1 - dist / 120)) + ')';
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        });

        animationId = requestAnimationFrame(animate);
    }

    animate();

    // Cleanup on page hide
    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            cancelAnimationFrame(animationId);
        } else {
            animate();
        }
    });
}

/* === Testimonial Carousel === */
function initTestimonialCarousel() {
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.testimonial-dot');

    if (!slides.length) return;

    let current = 0;
    let interval;

    function showSlide(index) {
        slides.forEach(function(s) { s.classList.remove('active'); });
        dots.forEach(function(d) { d.classList.remove('active'); });

        slides[index].classList.add('active');
        if (dots[index]) dots[index].classList.add('active');
        current = index;
    }

    function nextSlide() {
        showSlide((current + 1) % slides.length);
    }

    // Auto-advance
    interval = setInterval(nextSlide, 5000);

    // Click dots
    dots.forEach(function(dot, index) {
        dot.addEventListener('click', function() {
            clearInterval(interval);
            showSlide(index);
            interval = setInterval(nextSlide, 5000);
        });
    });
}

/* === Toast Auto-Hide === */
function initToastAutoHide() {
    const toast = document.getElementById('flashToast');
    if (!toast) return;

    setTimeout(function() {
        toast.style.animation = 'slideInRight 0.3s ease reverse forwards';
        setTimeout(function() {
            toast.remove();
        }, 300);
    }, 5000);
}

/* === Typing Effect === */
function initTypingEffect(element, texts, speed) {
    if (!element) return;

    speed = speed || 80;
    let textIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
        var currentText = texts[textIndex];
        var displayText;

        if (isDeleting) {
            displayText = currentText.substring(0, charIndex - 1);
            charIndex--;
        } else {
            displayText = currentText.substring(0, charIndex + 1);
            charIndex++;
        }

        element.innerHTML = displayText + '<span class="cursor">|</span>';

        var typeSpeed = isDeleting ? speed / 2 : speed;

        if (!isDeleting && charIndex === currentText.length) {
            typeSpeed = 2000; // Pause at end
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            textIndex = (textIndex + 1) % texts.length;
            typeSpeed = 500;
        }

        setTimeout(type, typeSpeed);
    }

    type();
}

/* === AJAX Helper === */
function ajaxRequest(url, method, data, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            var response;
            try {
                response = JSON.parse(xhr.responseText);
            } catch (e) {
                response = { error: 'Invalid response' };
            }

            if (xhr.status >= 200 && xhr.status < 300) {
                callback(null, response);
            } else {
                callback(response.error || 'Request failed', null);
            }
        }
    };

    if (data) {
        xhr.send(JSON.stringify(data));
    } else {
        xhr.send();
    }
}

/* === Toast Notification System === */
function showToast(type, message, duration) {
    duration = duration || 4000;

    var iconMap = {
        success: 'fa-check-circle',
        danger: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };

    var toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.innerHTML = '<i class="fas ' + (iconMap[type] || iconMap.info) + '"></i>' +
        '<span>' + message + '</span>' +
        '<button class="toast-close" onclick="this.parentElement.remove()"><i class="fas fa-times"></i></button>';

    document.body.appendChild(toast);

    setTimeout(function() {
        toast.style.animation = 'slideInRight 0.3s ease reverse forwards';
        setTimeout(function() {
            if (toast.parentElement) toast.remove();
        }, 300);
    }, duration);
}

/* === Form Validation Helper === */
function validateForm(form) {
    var isValid = true;
    var requiredFields = form.querySelectorAll('[required]');

    // Clear previous errors
    form.querySelectorAll('.form-error').forEach(function(el) { el.remove(); });
    form.querySelectorAll('.error').forEach(function(el) { el.classList.remove('error'); });

    requiredFields.forEach(function(field) {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('error');

            var errorMsg = document.createElement('div');
            errorMsg.className = 'form-error';
            errorMsg.textContent = 'Field ini wajib diisi';
            field.parentNode.appendChild(errorMsg);
        }
    });

    // Email validation
    var emailFields = form.querySelectorAll('input[type="email"]');
    emailFields.forEach(function(field) {
        if (field.value && !isValidEmail(field.value)) {
            isValid = false;
            field.classList.add('error');

            var errorMsg = document.createElement('div');
            errorMsg.className = 'form-error';
            errorMsg.textContent = 'Format email tidak valid';
            field.parentNode.appendChild(errorMsg);
        }
    });

    return isValid;
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
