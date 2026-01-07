

export function navbar() {
    
  const HTML = `
      <header class="site-header">
        <div class="header-content">
            <i class="fas fa-fire-alt"></i>
            <h1>Detecting Humans In Fire</h1>
        </div>
    </header>
  `;

  const target = document.getElementById("navbar");
  if (target) target.innerHTML = HTML;
  else console.warn('No element with id="navbar" found');

  return HTML;
}

// Automatically render when imported
navbar();
