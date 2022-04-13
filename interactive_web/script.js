(function () {
  const stageElem = document.querySelector(".stage");
  const houseElem = document.querySelector(".house");
  const barElem = document.querySelector(".progress-bar");
  let maxScrollValue;
  const mousePos = { x: 0, y: 0 };
  function resizeHandler() {
    maxScrollValue = document.body.offsetHeight - window.innerHeight;
  }
  window.addEventListener("scroll", function () {
    const zMove = pageYOffset / maxScrollValue;
    houseElem.style.transform = `translateZ(${zMove * 980 - 490}vw)`;
    barElem.style.width = `${zMove * 100}%`;
  });
  window.addEventListener("mousemove", (e) => {
    mousePos.x = (e.clientX / window.innerWidth) * 2 - 1;
    mousePos.y = ((e.clientY / window.innerHeight) * 2 - 1) * -1;
    stageElem.style.transform = `rotateX(${mousePos.y * 10}deg) rotateY(${
      mousePos.x * 10
    }deg)`;
  });
  window.addEventListener("resize", resizeHandler);
  window.onload = resizeHandler();
})();
