function processFiles() {
  var files = JSON.parse(sessionStorage.getItem("files"))
  console.log(files);
  for(var i = 0, f; f = files[i]; i++){
    console.log(f.name);
  }

}

processFiles();
