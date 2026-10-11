/* EduPulse AI - GitHub Pages Interactive Canvas Particle Network & Animation Script */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Navbar Scroll Backdrop & Shadow Shift
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 40) {
            navbar.style.background = 'rgba(7, 19, 15, 0.95)';
            navbar.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.6)';
        } else {
            navbar.style.background = 'rgba(7, 19, 15, 0.85)';
            navbar.style.boxShadow = 'none';
        }
    });

    // 2. Interactive Canvas Particle Background
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        const canvas = document.createElement('canvas');
        canvas.id = 'particle-canvas';
        canvas.style.position = 'absolute';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '0';
        heroSection.insertBefore(canvas, heroSection.firstChild);

        const ctx = canvas.getContext('2d');
        let width = (canvas.width = heroSection.offsetWidth);
        let height = (canvas.height = heroSection.offsetHeight);

        window.addEventListener('resize', () => {
            width = canvas.width = heroSection.offsetWidth;
            height = canvas.height = heroSection.offsetHeight;
        });

        const particles = [];
        const particleCount = Math.min(width > 768 ? 55 : 25, 60);

        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * width,
                y: Math.random() * height,
                vx: (Math.random() - 0.5) * 0.6,
                vy: (Math.random() - 0.5) * 0.6,
                radius: Math.random() * 2 + 1,
                alpha: Math.random() * 0.5 + 0.2
            });
        }

        function drawParticles() {
            ctx.clearRect(0, 0, width, height);

            // Connect nearby particles with glowing green lines
            for (let i = 0; i < particles.length; i++) {
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = particles[i].x - particles[j].x;
                    const dy = particles[i].y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 120) {
                        ctx.beginPath();
                        ctx.strokeStyle = `rgba(95, 242, 165, ${0.25 * (1 - dist / 120)})`;
                        ctx.lineWidth = 0.8;
                        ctx.moveTo(particles[i].x, particles[i].y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.stroke();
                    }
                }
            }

            // Draw individual particles
            particles.forEach(p => {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(95, 242, 165, ${p.alpha})`;
                ctx.shadowBlur = 8;
                ctx.shadowColor = '#5FF2A5';
                ctx.fill();

                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > width) p.vx *= -1;
                if (p.y < 0 || p.y > height) p.vy *= -1;
            });

            requestAnimationFrame(drawParticles);
        }

        drawParticles();
    }

    // 3. Scroll Reveal Animation for Section Elements
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.feature-card, .workflow-step, .section-header, .disclaimer-box').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(24px)';
        el.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        revealObserver.observe(el);
    });

    // Helper class for revealed state
    const style = document.createElement('style');
    style.textContent = `.revealed { opacity: 1 !important; transform: translateY(0) !important; }`;
    document.head.appendChild(style);
});
