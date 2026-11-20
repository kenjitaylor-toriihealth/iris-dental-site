/* Iris Dental Medical — small site script
   1) Mobile menu open/close
   2) Thin line under the header once the page is scrolled
   3) Booking / phone click tracking — pushes events to the Google Tag Manager
      dataLayer (container GTM-TZVKB3WL). Event names: book_click,
      book_medical_click, phone_click. See README.txt for the GTM setup.
*/
(function () {
  var body = document.body;
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('main-nav');

  function setMenu(open) {
    if (!toggle) return;
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    body.classList.toggle('nav-open', open);
  }

  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      setMenu(toggle.getAttribute('aria-expanded') !== 'true');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setMenu(false);
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) setMenu(false);
    });
  }

  var header = document.querySelector('.site-header');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    var name = null;
    if (/toriihealth\.intakeq\.com/.test(href)) name = 'book_medical_click';
    else if (/intakeq\.com\/booking/.test(href)) name = 'book_click';
    else if (/^tel:/.test(href)) name = 'phone_click';
    if (!name) return;
    var params = {
      link_text: (a.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 80),
      link_location: a.getAttribute('data-cta') || '',
      page_path: location.pathname
    };
    params.event = name;
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(params);
  });
})();
