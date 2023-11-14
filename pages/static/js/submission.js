let socket = io();

socket.on("connect", function () {
  socket.emit("join_room_submission", document.querySelector("input#submission-authentication").value);
});

const banner_color = {
  "AC": "success",
  "WA": "danger",
  "TLE": "secondary",
  "RTE": "warning",
  "IR": "warning",
  "MLE": "warning",
  "OLE": "danger",
  "IE": "danger"
};
const status_code = {
  "AC": "Accepted",
  "WA": "Wrong Answer",
  "TLE": "Time Limit Exceeded",
  "RTE": "Runtime Error/Exception",
  "IR": "Invalid Return",
  "MLE": "Memory Limit Exceeded",
  "OLE": "Output Limit Exceeded",
  "IE": "Internal Error"
}

socket.on("receiving_judge_feedback_from_server", (data) => {
  var grandParentDiv = document.createElement("div");

  for (let i = 0; i < data.length; i++) {
    if (data.length != 1) {
      let batchNumber = document.createElement("b");
      batchNumber.innerHTML = `Batch #${i + 1}:`;
      grandParentDiv.appendChild(batchNumber);
    
      var parentDiv = document.createElement("div");
      parentDiv.className = "ps-3 mb-1";
    }

    for (let j = 0; j < data[i].length; j++) {
      var listItem = document.createElement("li");
      var standardErrorMessage = data[i][j].standard_error_result ? `
        <li><b>Standard error:</b>
          <pre><code>${data[i][j].standard_error_result}</code></pre>
        </li>
      ` : ``;
      listItem.innerHTML = `
        <a data-bs-toggle="collapse" href="#batch_${i + 1}_${j + 1}"><b>[Feedback]</b></a>
        <b>Case #${j + 1}:</b>
        <b><span class="text-${banner_color[data[i][j].status_code]}">${status_code[data[i][j].status_code]} (${data[i][j].status_code})</span></b> [${(data[i][j].time).toFixed(2)}s; ${(data[i][j].memory).toFixed(2)} MB]
        <div class="collapse" id="batch_${i + 1}_${j + 1}">
          <div class="callout callout-${banner_color[data[i][j]["status_code"]]} mb-2">
            <ul class="no-bullets">
              <li><b>Judge's feedback:</b> ${data[i][j]["feedback"]}</li>
              <li><b>Points received:</b> ${data[i][j]["point"]}</li>
              ${standardErrorMessage}
            </ul>
          </div>
        </div>
      `
      if (data.length != 1) {
        parentDiv.appendChild(listItem);
        grandParentDiv.appendChild(parentDiv);
      } else {
        grandParentDiv.appendChild(listItem);
      }
    }
  }
  let resultList = document.querySelector("ul#result-section");
  resultList.innerHTML = "";
  resultList.appendChild(grandParentDiv);
});