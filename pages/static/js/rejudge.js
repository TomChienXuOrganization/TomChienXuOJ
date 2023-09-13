function rejudge(id) {
  fetch(`/s/${id}/rejudge`, {
    method: "POST"
  }).then(res => {
    switch (res.status) {
      case 200:
        alert(`The submission whose ID is ${id} has been rejudged! Click OK to continue going to the submission view!`);
        window.location.href = `/s/${id}`;
        break;
      case 403:
        alert(`You don't have permission to perform this action!`);
        break;
      case 404:
        alert(`Can't find any submission whose ID is ${id}!`);
        break;
      default:
        alert(`Unexpected/Unidentified error. Can't execute this action!`)
    }
  });
}