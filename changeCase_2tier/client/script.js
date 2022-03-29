class App {
  init() {
    document
      .querySelector("#btn_upper")
      .addEventListener("click", this.toUpperCase.bind(this));
    document
      .querySelector("#btn_lower")
      .addEventListener("click", this.toLowerCase.bind(this));
  }
  post(path, body) {
    const url = `http://localhost:4000/${path}`;
    fetch(url, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => this.render(data));
  }
  toUpperCase() {
    const text = document.querySelector(".text_input").value;
    this.post("upper", text);
  }
  toLowerCase() {
    const text = document.querySelector(".text_input").value;
    this.post("lower", text);
  }
  render(text) {
    document.querySelector(".text_output").value = text;
  }
}
const app = new App();
app.init();
