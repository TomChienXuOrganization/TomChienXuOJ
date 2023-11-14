let socket = io();
let editor = ace.edit("editor");
editor.setTheme("ace/theme/monokai");
editor.session.setMode("ace/mode/text");
editor.session.setUseWrapMode(true);

editor.session.on('change', function(delta) {
  let value = editor.getValue();
  socket.emit("render_markdown", value, (data) => {
    document.querySelector("#renderer").innerHTML = data;
    renderMathInElement(document.querySelector("#renderer"), {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
        { left: "~~", right: "~~", display: true },
        { left: "~", right: "~", display: false },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
      ],
      throwOnError: false
    });
    document.querySelectorAll("pre").forEach((element) => {
      if (element.className.includes("uncopyable")) return;

      let div = document.createElement("div");
      div.className = "clipboard-pre unselectable";
      div.innerHTML = `<span class="clipboard-pre-button unselectable" title="Click me to copy">Copy</span>`;
      div.addEventListener("click", () => { copyToClipboard(element.innerText) });
      element.parentElement.insertBefore(div, element);
    })
  });
});