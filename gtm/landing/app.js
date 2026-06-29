/* Shared waitlist form handler for the control page and every hook-test variant.
   Front-end only: it logs the payload (incl. which hook variant the signup came
   from) and shows a thank-you state. Wire to a real backend — the Apps Script
   webhook (scripts/apps_script/Code.gs), Formspree, or your API — to capture for
   real. The `variant` field is the hook-test attribution: it ties each signup to
   the page/hook that produced it. */
document.getElementById('waitlist-form').addEventListener('submit', function (e) {
  e.preventDefault();
  var payload = {
    email: this.email.value,
    role: this.role.value,
    source: this.source.value,                       // free-text "how did you hear about us?"
    variant: document.body.dataset.variant || 'control'  // which hook this signup came from
  };
  console.log('[waitlist] would submit:', payload);
  this.style.display = 'none';
  document.getElementById('ok').classList.add('show');
});
