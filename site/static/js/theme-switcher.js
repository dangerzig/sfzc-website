// SFZC Design Direction Switcher
// Allows stakeholders to toggle between 5 design themes

(function() {
  const themes = [
    { id: 'classic', name: 'Classic', color: '#77180C', desc: 'Zen Center Red + Serif' },
    { id: 'modern', name: 'Modern Minimal', color: '#475569', desc: 'Clean sans-serif + slate' },
    { id: 'dark', name: 'Dark Contemplative', color: '#1a1a2e', desc: 'Dark bg + gold accents' },
    { id: 'earth', name: 'Earth & Nature', color: '#2d5016', desc: 'Forest green + organic' },
    { id: 'bold', name: 'Bold Contemporary', color: '#312e81', desc: 'Indigo + amber accents' },
  ];

  // Restore saved theme
  const saved = localStorage.getItem('sfzc-theme') || 'classic';
  if (saved !== 'classic') {
    document.documentElement.setAttribute('data-theme', saved);
  }

  function setTheme(id) {
    if (id === 'classic') {
      document.documentElement.removeAttribute('data-theme');
    } else {
      document.documentElement.setAttribute('data-theme', id);
    }
    localStorage.setItem('sfzc-theme', id);
    updateButtons(id);
  }

  function updateButtons(activeId) {
    document.querySelectorAll('.theme-switcher button').forEach(function(btn) {
      btn.classList.toggle('active', btn.dataset.theme === activeId);
    });
  }

  // Build the switcher panel
  function createSwitcher() {
    var panel = document.createElement('div');
    panel.className = 'theme-switcher';
    panel.id = 'theme-panel';
    panel.style.display = 'none';

    var header = document.createElement('div');
    header.className = 'theme-switcher-header';
    header.textContent = 'Design Direction';
    panel.appendChild(header);

    themes.forEach(function(t) {
      var btn = document.createElement('button');
      btn.dataset.theme = t.id;
      if (t.id === saved) btn.className = 'active';

      var dot = document.createElement('span');
      dot.className = 'theme-dot';
      dot.style.backgroundColor = t.color;

      var label = document.createElement('span');
      label.innerHTML = '<strong>' + t.name + '</strong><br><span style="font-size:11px;opacity:0.7">' + t.desc + '</span>';

      btn.appendChild(dot);
      btn.appendChild(label);
      btn.addEventListener('click', function() { setTheme(t.id); });
      panel.appendChild(btn);
    });

    // Toggle button
    var toggle = document.createElement('button');
    toggle.className = 'theme-switcher-toggle';
    toggle.id = 'theme-toggle';
    toggle.innerHTML = '&#x1f3a8;';
    toggle.title = 'Switch design direction';
    toggle.addEventListener('click', function() {
      var p = document.getElementById('theme-panel');
      if (p.style.display === 'none') {
        p.style.display = 'block';
        toggle.style.display = 'none';
      }
    });

    // Close on click outside
    document.addEventListener('click', function(e) {
      var p = document.getElementById('theme-panel');
      var tgl = document.getElementById('theme-toggle');
      if (p && p.style.display === 'block' && !p.contains(e.target) && e.target !== tgl) {
        p.style.display = 'none';
        tgl.style.display = 'flex';
      }
    });

    document.body.appendChild(panel);
    document.body.appendChild(toggle);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createSwitcher);
  } else {
    createSwitcher();
  }
})();
