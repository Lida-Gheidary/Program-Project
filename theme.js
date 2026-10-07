(() => {
  'use strict';

  const storageKey = 'attribution-study-theme';
  const root = document.documentElement;
  const themeMeta = document.querySelector('meta[name="theme-color"]');

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    if (themeMeta) themeMeta.setAttribute('content', theme === 'light' ? '#f8faf9' : '#000000');
  }

  // Apply a saved choice before the stylesheet loads. First visits are dark.
  let initialTheme = 'dark';
  try {
    if (localStorage.getItem(storageKey) === 'light') initialTheme = 'light';
  } catch {
    // The toggle still works when browser storage is unavailable.
  }
  applyTheme(initialTheme);

  function initialiseToggle() {
    const toggle = document.getElementById('theme-toggle');
    if (!toggle) return;
    const label = toggle.querySelector('.theme-label');

    function updateLabel() {
      const nextMode = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      if (label) label.textContent = nextMode === 'light' ? 'Light mode' : 'Dark mode';
      toggle.setAttribute('aria-label', `Switch to ${nextMode} mode`);
      toggle.setAttribute('title', `Switch to ${nextMode} mode`);
    }

    toggle.addEventListener('click', () => {
      const nextTheme = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      applyTheme(nextTheme);
      updateLabel();
      try {
        localStorage.setItem(storageKey, nextTheme);
      } catch {
        // A blocked storage write must not prevent changing the theme.
      }
    });

    updateLabel();
    toggle.hidden = false;
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialiseToggle, {once: true});
  } else {
    initialiseToggle();
  }
})();
