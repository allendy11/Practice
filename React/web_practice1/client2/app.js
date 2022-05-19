const title = document.querySelector(".nav_title");
const mobileMenu = document.querySelector(".mobile_menu");
const navMenu = document.querySelector(".nav_menu");

const mobileMenuHandler = () => {
  mobileMenu.classList.toggle("mobileMenu_active");
  navMenu.classList.toggle("navMenu_active");
};
mobileMenu.addEventListener("click", mobileMenuHandler);
