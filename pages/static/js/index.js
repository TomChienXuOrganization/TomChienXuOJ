if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
};

function convertToDataTable(table) {
  table.DataTable({
    info: true,
    search: false,
    "iDisplayLength": 50,
    order: [],
    columnDefs: [
      { bSort: false, targets: "no-sort", orderable: false }
    ]
  })
}

function copyToClipboard(text) {
  const listener = function (event) {
    event.preventDefault();
    event.clipboardData.setData("text/plain", text);
  };
  document.addEventListener("copy", listener);
  document.execCommand("copy");
  document.removeEventListener("copy", listener);
}

document.addEventListener("DOMContentLoaded", function () {
  renderMathInElement(document.body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false },
      { left: "\\(", right: "\\)", display: false },
      { left: "\\[", right: "\\]", display: true }
    ],
    throwOnError: false
  });

  document.querySelectorAll("table.table-utility.preload").forEach((element) => {
    convertToDataTable(element);
  });
});

"MM/DD/YYYY, HH:mm:ss"

document.querySelectorAll(".time-from-now").forEach((element) => {
  console.log(element.getAttribute("since"));
  element.innerHTML = moment(element.getAttribute("since"), "YYYY-MM-DD HH:mm:ss").fromNow();
});

document.querySelectorAll("textarea").forEach((element) => {
  if (element.value) {
    element.height = element.scrollHeight;
  };
})

document.querySelectorAll("pre").forEach((element) => {
  if (element.className.includes("uncopyable")) return;

  let div = document.createElement("div");
  div.className = "clipboard-pre unselectable";
  div.innerHTML = `<span class="clipboard-pre-button unselectable" title="Click me to copy">Copy</span>`;
  div.addEventListener("click", () => { copyToClipboard(element.innerText) })
  element.parentElement.insertBefore(div, element);
})

$(document).ready(() => {
  // $("select.form-select").each((index) => {
  //   $(this).select2({
  //     theme: "bootstrap-5"
  //   })
  // });

  $("select.form-select").select2({
    theme: "bootstrap-5"
  })
});