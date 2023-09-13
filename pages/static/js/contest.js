function initializeContestData(begin, end, url) {
  [contestBeginTime, contestEndTime, contestPage] = [begin, end, url];
}

function setNavbarActivePage(page) {
  document.querySelector(`ul.contest-navbar > div.navigation-bar > li.nav-item > a#${page}`).classList.add("active");
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

function replaceDeltaTimeString(originalString, deltaTime) {
  return originalString.replace("%day%", deltaTime.day.toString())
    .replace("%hour%", deltaTime.hour.toString().padStart(2, "0"))
    .replace("%minute%", deltaTime.minute.toString().padStart(2, "0"))
    .replace("%second%", deltaTime.second.toString().padStart(2, "0"));
}

function checkAndShowStatusToast() {
  let toastID = sessionStorage.getItem("onReadyToast");
  if (!toastID) return;

  let toast = new bootstrap.Toast(document.getElementById(toastID));
  toast.show();
  sessionStorage.removeItem("onReadyToast");
}

document.addEventListener("DOMContentLoaded", () => {
  contestBeginTime = new Date(contestBeginTime + "+00:00");
  contestEndTime = new Date(contestEndTime + "+00:00");

  let windowDeltaTime = calculateDateTimeDifferential(contestBeginTime, contestEndTime);
  let userTime = new Date();
  document.querySelector("span.window-time").innerHTML = replaceDeltaTimeString(
    document.querySelector("span.window-time-span").innerHTML,
    windowDeltaTime
  );

  document.querySelector("#time-bar").style.width = "0%";
  checkAndShowStatusToast();

  if (userTime < contestBeginTime) {
    let interval = setInterval(() => {
      let currentTime = new Date();
      // currentTime.setSeconds(currentTime.getSeconds() + 1);
      let userSideDeltaTime = calculateDateTimeDifferential(currentTime, contestBeginTime);
      document.querySelector("span.contest-timer").innerHTML = replaceDeltaTimeString(
        document.querySelector("span.will-begin-remaining-span").innerHTML,
        userSideDeltaTime
      );

      if (currentTime >= contestBeginTime) {
        clearInterval(interval);
        document.querySelector("span.contest-timer").innerHTML = document.querySelector("span.begun-span").innerHTML;
        sessionStorage.setItem("onReadyToast", "starting-toast");
        setTimeout(() => {
          window.location.href = contestPage;
        }, 1000);
      }
    }, 1000);
  } else if (contestBeginTime <= userTime && userTime < contestEndTime) {
    let timeBarInterval = setInterval(() => {
      let currentTime = new Date();
      let timeBarPercentage = (currentTime - contestBeginTime) * 100 / (contestEndTime - contestBeginTime);
      timeBarPercentage = timeBarPercentage > 100 || timeBarPercentage < 0 ? 100 : timeBarPercentage;
      document.querySelector("#time-bar").style.width = `${timeBarPercentage}%`;
    }, 1)

    let interval = setInterval(() => {
      let currentTime = new Date();
      let userSideDeltaTime = calculateDateTimeDifferential(currentTime, contestEndTime);
      document.querySelector("span.contest-timer").innerHTML = replaceDeltaTimeString(
        document.querySelector("span.will-end-remaining-span").innerHTML,
        userSideDeltaTime
      );

      if (currentTime >= contestEndTime) {
        clearInterval(interval);
        clearInterval(timeBarInterval);
        document.querySelector("span.contest-timer").innerHTML = document.querySelector("span.ended-span").innerHTML;
        sessionStorage.setItem("onReadyToast", "ending-toast");
        setTimeout(() => {
          window.location.href = contestPage;
        }, 1000);
      }
    }, 1000);
  } else if (userTime >= contestEndTime) {
    document.querySelector("span.contest-timer").innerHTML = document.querySelector("span.ended-span").innerHTML;
    setTimeout(() => {
      document.querySelector("#time-bar").style.width = "100%";
    }, 200)
  }
})