function checkSingleOrPluralCases() {
  const number = document.querySelector("#number-of-cases").value;
  let status = (number == 1) ? true : false;
  var buttons = document.querySelectorAll(".delete-button");
  for (var i = 0; i < buttons.length; i++) {
    buttons.item(i).disabled = status;
  }
}

function setValues(item, value, resetValue = false) {
  item.setAttribute("index", value);
  item.querySelector(".delete-button").innerHTML = `<b>DELETE THIS SAMPLE (${value})</b>`;
  if (resetValue) {
    item.querySelector(".input").value = "";
    item.querySelector(".output").value = "";
    item.querySelector(".explanation").value = "";
  }
  item.querySelector(".input").name = "input-" + value;
  item.querySelector(".output").name = "output-" + value;
  item.querySelector(".explanation").name = "explanation-" + value;
  item.querySelector(".input").id = "input-" + value;
  item.querySelector(".output").id = "output-" + value;
  item.querySelector(".explanation").id = "explanation-" + value;
}

function addSample() {
  document.querySelector("#number-of-cases").value++;
  let number = document.querySelector("#number-of-cases").value;
  const node = document.querySelector(".sample-case-child");
  const clone = node.cloneNode(true);
  setValues(clone, number, true);
  document.querySelector("#sample-cases").appendChild(clone);
  checkSingleOrPluralCases();
}

function removeSample() {
  const elementParent = event.target.closest("button").parentElement.parentElement;
  const testIndex = elementParent.getAttribute("index");
  elementParent.remove();
  document.getElementById("number-of-cases").value--;
  const samples = document.querySelectorAll("[index]");
  for (var i = testIndex; i <= samples.length; i++) {
    setValues(samples.item(i - 1), parseInt(samples.item(i - 1).getAttribute("index")) - 1);
  }
  checkSingleOrPluralCases();
}

function generate() {
  let resultString = "";
  let inputFile = document.querySelector("#input-file").value ? `: Data taken from <code>${document.querySelector("#input-file").value}</code>` : "";
  let outputFile = document.querySelector("#output-file").value ? `: Data written in <code>${document.querySelector("#output-file").value}</code>` : "";
  let constrains = document.querySelector("#limitations").value ? `
<h4 class="section-title"><b>Limitations</b></h4>
<hr class="close">

${document.querySelector("#limitations").value}
` : "";

  resultString = `${document.querySelector("#legend").value}
<h4 class="section-title"><b>Input Specification${inputFile}</b></h4>
<hr class="close">

${document.querySelector("#input-specification").value}

<h4 class="section-title"><b>Output Specification${outputFile}</b></h4>
<hr class="close">

${document.querySelector("#output-specification").value}
${constrains}
<h4 class="section-title"><b>Sample Case(s)</b></h4>
<hr class="close">
`;
  console.log(resultString)
  let number = document.querySelector("#number-of-cases").value;
  for (let i = 1; i <= number; i++) {
    resultString += `<div class="row">
  <div class="col">
    <p class="h5">Input #${i}:</p>
    <div markdown="1">
${document.querySelector(`#input-${i}`).value}
    </div>
  </div>
  <div class="col">
    <p class="h5">Output #${i}:</p>
    <div markdown="1">
${document.querySelector(`#output-${i}`).value}
    </div>
  </div>
</div>
`;

    if (document.querySelector(`#explanation-${i}`).value) {
      resultString += `<p class="h5">Explanation:</p>
${document.querySelector(`#explanation-${i}`).value}

`;
    }

    if (number != 1 && i != number) {
      resultString += '<hr class="close" style="width: 75%" size="2">\n';
    }
  }

  socket.emit("render_markdown", resultString, (data) => {
    document.querySelector("#renderer").innerHTML = data;
    renderMathInElement(document.querySelector("#renderer"), {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$", right: "$", display: false },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true }
      ],
      throwOnError: false
    });
    socket.emit("render_markdown", "```html\n" + data + "\n```", (data) => {
      let preElement = document.createElement("pre");
      preElement.innerText = resultString;
      document.querySelector("#result").innerHTML = "";
      document.querySelector("#result").append(preElement);
      document.querySelectorAll("pre").forEach((element) => {
        if (element.className.includes("uncopyable")) return;
  
        let div = document.createElement("div");
        div.className = "clipboard-pre unselectable";
        div.innerHTML = `<span class="clipboard-pre-button unselectable" title="Click me to copy">Copy</span>`;
        div.addEventListener("click", () => { copyToClipboard(element.innerText) });
        element.parentElement.insertBefore(div, element);
      })
    })
  })
}

checkSingleOrPluralCases();
var socket = io();