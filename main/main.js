const menuBtn = document.getElementById("menu-btn");
const navLinks = document.getElementById("nav-links");
const menuBtnIcon = menuBtn.querySelector("i");

menuBtn.addEventListener("click", (e) => {
  navLinks.classList.toggle("open");

  const isOpen = navLinks.classList.contains("open");
  menuBtnIcon.setAttribute("class", isOpen ? "ri-close-line" : "ri-menu-line");
});

navLinks.addEventListener("click", (e) => {
  navLinks.classList.remove("open");
  menuBtnIcon.setAttribute("class", "ri-menu-line");
});

const scrollRevealOption = {
  origin: "bottom",
  distance: "50px",
  duration: 1000,
};

ScrollReveal().reveal(".header__image img", {
  ...scrollRevealOption,
  origin: "right",
});
ScrollReveal().reveal(".header__content p", {
  ...scrollRevealOption,
  delay: 500,
});
ScrollReveal().reveal(".header__content h1", {
  ...scrollRevealOption,
  delay: 1000,
});
ScrollReveal().reveal(".header__btns", {
  ...scrollRevealOption,
  delay: 1500,
});

ScrollReveal().reveal(".destination__card", {
  ...scrollRevealOption,
  interval: 500,
});

ScrollReveal().reveal(".showcase__image img", {
  ...scrollRevealOption,
  origin: "left",
});
ScrollReveal().reveal(".showcase__content h4", {
  ...scrollRevealOption,
  delay: 500,
});
ScrollReveal().reveal(".showcase__content p", {
  ...scrollRevealOption,
  delay: 1000,
});
ScrollReveal().reveal(".showcase__btn", {
  ...scrollRevealOption,
  delay: 1500,
});

ScrollReveal().reveal(".banner__card", {
  ...scrollRevealOption,
  interval: 500,
});

ScrollReveal().reveal(".discover__card", {
  ...scrollRevealOption,
  interval: 500,
});

const swiper = new Swiper(".swiper", {
  slidesPerView: 3,
  spaceBetween: 20,
  loop: true,
});
document.addEventListener("DOMContentLoaded", () => {
  const username = localStorage.getItem("loggedInUser");

  if (username) {
    const navBtns = document.querySelector(".nav__btns");
    if (navBtns) {
      navBtns.innerHTML = `
        <span style="color: white; margin-right: 10px;">Hi, ${username}</span>
        <button class="btn" onclick="logout()">Logout</button>
      `;
    }

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("login") === "success") {
      alert(`Login successful! Welcome, ${username}`);
      window.history.replaceState({}, document.title, "index.html");
    }
  }
});
function switchForm(type) {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const title = document.getElementById('form-title');

  if (type === 'signup') {
    loginForm.classList.add('hidden');
    signupForm.classList.remove('hidden');
    title.innerText = 'Sign Up';
  } else {
    signupForm.classList.add('hidden');
    loginForm.classList.remove('hidden');
    title.innerText = 'Login';
  }
}

async function submitLogin(e) {
  e.preventDefault();
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  const res = await fetch('http://127.0.0.1:5000/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  if (data.status === "success") {
    localStorage.setItem("loggedInUser", username);
    window.location.href = `index.html?login=success`;
  } else {
    alert(data.message);
  }
}

async function submitSignup(e) {
  e.preventDefault();
  const name = document.getElementById('signup-name').value;
  const username = document.getElementById('signup-username').value;
  const password = document.getElementById('signup-password').value;

  const res = await fetch('http://127.0.0.1:5000/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, username, password })
  });

  const data = await res.json();
  alert(data.message);
  if (data.status === "success") switchForm('login');
}

// For header login state
document.addEventListener("DOMContentLoaded", () => {
  const username = localStorage.getItem("loggedInUser");

  if (username) {
    const navBtns = document.querySelector(".nav__btns");
    if (navBtns) {
      navBtns.innerHTML = `
        <span style="color: white; margin-right: 10px;">Hi, ${username}</span>
        <button class="btn" onclick="logout()">Logout</button>
      `;
    }

    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get("login") === "success") {
      alert(`Login successful! Welcome, ${username}`);
      window.history.replaceState({}, document.title, "index.html");
    }
  }
});

function logout() {
  localStorage.removeItem("loggedInUser");
  window.location.href = "login.html";
}
