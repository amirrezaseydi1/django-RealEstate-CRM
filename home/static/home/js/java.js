// Real Estate CRM - Home Page JavaScript

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            navbar.classList.add('shadow');
        } else {
            navbar.classList.remove('shadow');
        }

        lastScroll = currentScroll;
    });

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));

            if (target) {
                const navbarHeight = navbar.offsetHeight;
                const targetPosition = target.offsetTop - navbarHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });

                // Close mobile menu if open
                const navbarCollapse = document.querySelector('.navbar-collapse');
                if (navbarCollapse.classList.contains('show')) {
                    navbarCollapse.classList.remove('show');
                }
            }
        });
    });

    // Intersection Observer for animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards
    const cards = document.querySelectorAll('.why-card, .property-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `all 0.6s ease ${index * 0.1}s`;
        observer.observe(card);
    });

    // CTA Button Click Handler
    const ctaButtons = document.querySelectorAll('.cta-button, .cta-contact-button');
    ctaButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add ripple effect
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);

            // Show alert (in production, this would trigger actual functionality)
            setTimeout(() => {
                alert('این قابلیت به زودی فعال خواهد شد\nThis feature will be activated soon');
            }, 100);
        });
    });

    // Property Card Button Click Handler
    const propertyButtons = document.querySelectorAll('.property-card .btn');
    propertyButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const propertyCard = this.closest('.property-card');
            const propertyTitle = propertyCard.querySelector('.property-title').textContent;

            // In production, this would navigate to property details page
            alert(`مشاهده جزئیات: ${propertyTitle}\nView Details: ${propertyTitle}`);
        });
    });

    // Login/Sign Up Button Click Handlers
    const loginBtn = document.querySelector('.btn-outline-primary');
    const signUpBtn = document.querySelector('.navbar .btn-primary');

    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            alert('صفحه ورود به زودی فعال خواهد شد\nLogin page will be activated soon');
        });
    }

    if (signUpBtn) {
        signUpBtn.addEventListener('click', function() {
            alert('صفحه ثبت نام به زودی فعال خواهد شد\nSign up page will be activated soon');
        });
    }

    // Navbar active state on scroll
    window.addEventListener('scroll', () => {
        let current = '';
        const sections = document.querySelectorAll('section[id]');

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (pageYOffset >= (sectionTop - navbar.offsetHeight - 100)) {
                current = section.getAttribute('id');
            }
        });

        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });

        // Set home as active if at top
        if (window.pageYOffset < 200) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === '#') {
                    link.classList.add('active');
                }
            });
        }
    });

    // Add hover effect to property cards
    const propertyCards = document.querySelectorAll('.property-card');
    propertyCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add parallax effect to hero section
    window.addEventListener('scroll', () => {
        const heroSection = document.querySelector('.hero-section');
        if (heroSection) {
            const scrolled = window.pageYOffset;
            const parallax = scrolled * 0.5;
            heroSection.style.transform = `translateY(${parallax}px)`;
        }
    });

    // Number counter animation (if you want to add statistics)
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);

        const timer = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.ceil(start);
            }
        }, 16);
    }

    // Social media links
    const socialLinks = document.querySelectorAll('.social-icon');
    socialLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const platform = this.querySelector('i').classList[1].replace('bi-', '');
            alert(`باز کردن ${platform}\nOpening ${platform}`);
        });
    });

    // Form validation (if you add contact form later)
    function validateForm(form) {
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        let isValid = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }
        });

        return isValid;
    }

    // Console log for developers
    console.log('%c🏠 Real Estate CRM', 'color: #0d6efd; font-size: 20px; font-weight: bold;');
    console.log('%cWebsite loaded successfully!', 'color: #198754; font-size: 14px;');
    console.log('%cسیستم مدیریت املاک آماده است', 'color: #0d6efd; font-size: 14px;');
});

// Utility function to format numbers (Persian/English)
function formatNumber(num, locale = 'fa-IR') {
    return new Intl.NumberFormat(locale).format(num);
}

// Utility function to handle RTL/LTR content
function detectLanguage(text) {
    const persianRegex = /[\u0600-\u06FF]/;
    return persianRegex.test(text) ? 'rtl' : 'ltr';
}

// Add CSS for ripple effect dynamically
const style = document.createElement('style');
style.textContent = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
