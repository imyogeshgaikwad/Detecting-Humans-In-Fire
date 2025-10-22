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
    <style>
      .navbar {
        width: 100%;
        background: #111;
        color: #fff;
        padding: 0.75rem 1rem;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 1000;
      }

      .navbar-container {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
      }

      .navbar-title {
        font-size: 1.5rem;
        font-weight: bold;
        letter-spacing: 1px;
      }

      .navbar-links {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
      }

      .nav-link {
        color: #fff;
        text-decoration: none;
        font-size: 1rem;
        transition: color 0.3s;
      }

      .nav-link:hover {
        color: #f33;
      }

      /* Responsive */
      @media (max-width: 600px) {
        .navbar-container {
          flex-direction: column;
          align-items: flex-start;
        }

        .navbar-links {
          margin-top: 0.5rem;
          flex-direction: column;
          width: 100%;
        }

        .nav-link {
          padding: 0.5rem 0;
          width: 100%;
        }
      }
    </style>

    <nav class="navbar">
      <div class="navbar-container">
        <div class="navbar-title"> FIRE</div>
        <div class="navbar-links">
          ${showLinks()}
        </div>
      </div>
    </nav>
  `;

  // auto-inject into <div id="navbar">
  const target = document.getElementById("navbar");
  if (target) target.innerHTML = HTML;
  else console.warn('No element with id="navbar" found');

  return HTML;
}

// Automatically render when imported
navbar();
