const links = [
  { title: "Home", link: "/" },
  { title: "Login", link: "/login" },
  { title: "About", link: "/about" },
  { title: "Contact", link: "/contact" }
];

function showLinks() {
  return links
    .map(link => `<a class="nav-link" href="${link.link}">${link.title}</a>`)
    .join("");
}

export function navbar() {
    console.log("TESTING");
    
  const HTML = `
      <header class="site-header">
        <div class="header-content">
            <i class="fas fa-fire-alt"></i>
            <h1>Fire Detection System</h1>
        </div>
    </header>
  `;

  // auto-inject into <div id="navbar">
  const target = document.getElementById("navbar");
  if (target) target.innerHTML = HTML;
  else console.warn('No element with id="navbar" found');

  return HTML;
}

// Automatically render when imported
navbar();
