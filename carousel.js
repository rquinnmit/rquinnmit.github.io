/**
 * Reading-list carousel.
 *
 * Every card lives in one .carousel-track and this script pages through them
 * by translating the track. How many cards make a page is the stylesheet's
 * decision, read from the track's --per-page custom property, so the
 * breakpoints live in one place. A resize re-measures the page width and
 * rebuilds the dots only when the count changes, so a phone's address bar
 * appearing does not snap the list back to its first page. Autoplay advances
 * every six seconds, pauses while the pointer or keyboard focus is on the
 * track or the tab is hidden, and never runs under prefers-reduced-motion.
 */
(() => {
    'use strict';

    const track = document.querySelector('.carousel-track');
    const cards = track ? [...track.querySelectorAll('.carousel-card')] : [];
    const dots = document.querySelector('.carousel-dots');
    if (!track || !dots || cards.length < 2) return;

    const AUTO_MS = 6000;
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
    let perPage = 0;
    let current = 0;
    let timer = null;

    const cardsPerPage = () => parseInt(getComputedStyle(track).getPropertyValue('--per-page'), 10) || 1;
    const pageCount = () => Math.ceil(cards.length / perPage);

    function goTo(page) {
        const pages = pageCount();
        current = ((page % pages) + pages) % pages;
        const pitch = cards[1].offsetLeft - cards[0].offsetLeft;
        track.style.transform = `translateX(-${current * perPage * pitch}px)`;
        [...dots.children].forEach((dot, i) => {
            dot.classList.toggle('active', i === current);
            dot.setAttribute('aria-current', i === current ? 'true' : 'false');
        });
    }

    function buildDots() {
        dots.replaceChildren();
        for (let i = 0; i < pageCount(); i++) {
            const dot = document.createElement('button');
            dot.type = 'button';
            dot.className = 'dot';
            dot.setAttribute('aria-label', `Page ${i + 1}`);
            dot.addEventListener('click', () => { goTo(i); start(); });
            dots.append(dot);
        }
    }

    function stop() {
        clearInterval(timer);
        timer = null;
    }

    function start() {
        stop();
        if (reduced.matches || document.hidden) return;
        timer = setInterval(() => goTo(current + 1), AUTO_MS);
    }

    function layout() {
        const count = cardsPerPage();
        if (count === perPage) {
            goTo(current);
            return;
        }
        perPage = count;
        buildDots();
        goTo(0);
    }

    document.querySelector('.carousel-prev').addEventListener('click', () => { goTo(current - 1); start(); });
    document.querySelector('.carousel-next').addEventListener('click', () => { goTo(current + 1); start(); });

    track.addEventListener('mouseenter', stop);
    track.addEventListener('mouseleave', start);
    track.addEventListener('focusin', stop);
    track.addEventListener('focusout', (event) => {
        if (!track.contains(event.relatedTarget)) start();
    });
    document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
    reduced.addEventListener('change', start);
    window.addEventListener('resize', layout);

    layout();
    start();
})();
