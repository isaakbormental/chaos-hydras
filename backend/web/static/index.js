function handleGenerateLink() {
  let xmlHttp = new XMLHttpRequest();
  let url = document.getElementsByClassName("input-field")[0].value;
  xmlHttp.open("GET", "http://127.0.0.1:5000/client-info/" + url, true);
  xmlHttp.onreadystatechange = function () {
    if (xmlHttp.status === 200) {
      var blob = xmlHttp.response;
      document.getElementById('img')
        .setAttribute(
          'src', 'data:image/png;base64,' + blob
      );
    }
    else
      var blob = xmlHttp.response;
      document.getElementById('img')
        .setAttribute(
          'src', 'data:image/png;base64,' + blob
      );
  };
  xmlHttp.send();
}
