(function () {
  // Mobilni izbornik
  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('nav');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'Zatvori izbornik' : 'Otvori izbornik');
      document.body.style.overflow = open ? 'hidden' : '';
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) { btn.click(); btn.focus(); }
    });
  }

  // Godina u podnožju
  document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Kontakt obrazac: statična stranica nema poslužitelj, pa upit otvara e-mail klijent s popunjenim sadržajem
  var form = document.getElementById('upit');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var err = form.querySelector('.form-error');
      if (!form.checkValidity()) {
        err.textContent = 'Ispunite ime, e-mail ili telefon, opis upita i označite privolu.';
        err.classList.add('show');
        form.reportValidity();
        return;
      }
      err.classList.remove('show');
      var d = new FormData(form);
      var subject = 'Upit s web stranice: ' + (d.get('usluga') || 'Opći upit');
      var body = [
        'Ime i prezime: ' + d.get('ime'),
        'E-mail: ' + d.get('email'),
        'Telefon: ' + (d.get('telefon') || '-'),
        'Lokacija objekta: ' + (d.get('lokacija') || '-'),
        'Usluga: ' + (d.get('usluga') || '-'),
        '',
        d.get('poruka')
      ].join('\n');
      window.location.href = 'mailto:' + form.dataset.to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }
})();
