(() => {
    const track = document.querySelector('.carousel-track');
    const cards = document.querySelectorAll('.carousel-card');
    const prevBtn = document.querySelector('.carousel-prev');
    const nextBtn = document.querySelector('.carousel-next');
    const dotsContainer = document.querySelector('.carousel-dots');

    if (!track || cards.length === 0) return;

    const visibleCount = () => {
        if (window.innerWidth <= 600) return 1;
        if (window.innerWidth <= 900) return 2;
        return 3;
    };

    let current = 0;
    let autoInterval;

    const totalPages = () => Math.ceil(cards.length / visibleCount());

    function buildDots() {
        dotsContainer.innerHTML = '';
        const pages = totalPages();
        for (let i = 0; i < pages; i++) {
            const dot = document.createElement('span');
            dot.classList.add('dot');
            if (i === current) dot.classList.add('active');
            dot.addEventListener('click', () => goTo(i));
            dotsContainer.appendChild(dot);
        }
    }

    function updateDots() {
        const dots = dotsContainer.querySelectorAll('.dot');
        dots.forEach((d, i) => d.classList.toggle('active', i === current));
    }

    function goTo(page) {
        const pages = totalPages();
        current = ((page % pages) + pages) % pages;
        const cardWidth = cards[0].offsetWidth + 20;
        const offset = current * visibleCount() * cardWidth;
        track.style.transform = `translateX(-${offset}px)`;
        updateDots();
    }

    function next() {
        goTo(current + 1);
    }

    function prev() {
        goTo(current - 1);
    }

    function startAuto() {
        stopAuto();
        autoInterval = setInterval(next, 6000);
    }

    function stopAuto() {
        clearInterval(autoInterval);
    }

    nextBtn.addEventListener('click', () => { next(); startAuto(); });
    prevBtn.addEventListener('click', () => { prev(); startAuto(); });

    track.addEventListener('mouseenter', stopAuto);
    track.addEventListener('mouseleave', startAuto);

    window.addEventListener('resize', () => {
        buildDots();
        goTo(0);
    });

    buildDots();
    startAuto();
})();
