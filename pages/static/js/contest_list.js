function checkAndShowStatusToast() {
  let toastID = sessionStorage.getItem("onReadyToast");
  if (!toastID) return;

  let toast = new bootstrap.Toast(document.getElementById(toastID));
  toast.show();
  sessionStorage.removeItem("onReadyToast");
}

function replaceDeltaTimeString(originalString, deltaTime) {
  return originalString.replace("%day%", deltaTime.day.toString())
    .replace("%hour%", deltaTime.hour.toString().padStart(2, "0"))
    .replace("%minute%", deltaTime.minute.toString().padStart(2, "0"))
    .replace("%second%", deltaTime.second.toString().padStart(2, "0"));
}

function calculateDateTimeDifferential(begin, end) {
  let deltaTime = new Date(end) - new Date(begin);
  return {
    day: Math.floor(deltaTime / (1000 * 60 * 60 * 24)),
    hour: Math.floor((deltaTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
    minute: Math.floor((deltaTime % (1000 * 60 * 60)) / (1000 * 60)),
    second: Math.floor((deltaTime % (1000 * 60)) / 1000)
  }
}

checkAndShowStatusToast();

document.querySelectorAll("span.dynamic-window-time").forEach((element) => {
  let [beginTime, endTime] = [element.getAttribute("begin"), element.getAttribute("end")];
  element.innerHTML = replaceDeltaTimeString(
    document.querySelector("span.dynamic-window-time-span").innerHTML,
    calculateDateTimeDifferential(beginTime, endTime)
  );
})

document.querySelectorAll("span.dynamic-contest-time").forEach((element) => {
  let [beginTime, endTime] = [element.getAttribute("begin"), element.getAttribute("end")];
  userTime = new Date();
  beginTime = new Date(beginTime + "+00:00");
  endTime = new Date(endTime + "+00:00");

  if (userTime < beginTime) {
    setInterval(() => {
      let currentTime = new Date();
      let deltaTime = calculateDateTimeDifferential(currentTime, beginTime);

      if (currentTime > beginTime) {
        clearAllIntervals();
        sessionStorage.setItem("onReadyToast", "reload-contest-page-warning-toast");
        window.location.reload();
      } else {
        element.innerHTML = replaceDeltaTimeString(
          document.querySelector("span.dynamic-beginning-time-span").innerHTML,
          deltaTime
        );
      }
    }, 1000)
  } else if (beginTime <= userTime && userTime < endTime) {
    setInterval(() => {
      let currentTime = new Date();
      let deltaTime = calculateDateTimeDifferential(currentTime, endTime);

      if (currentTime > endTime) {
        clearAllIntervals();
        sessionStorage.setItem("onReadyToast", "reload-contest-page-warning-toast");
        window.location.reload();
      } else {
        element.innerHTML = replaceDeltaTimeString(
          document.querySelector("span.dynamic-remaining-time-span").innerHTML,
          deltaTime
        );
      }
    }, 1000)
  } else if (userTime >= endTime) {
    element.innerHTML = document.querySelector("span.dynamic-ended-time-span").innerHTML;
  }
})