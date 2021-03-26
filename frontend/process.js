(function() {
  for(i = 0; i < sessionStorage.length; i++){
    if(sessionStorage.key(i).endsWith("_analysis")){
      console.log(sessionStorage.getItem(sessionStorage.key(i)))
    }
  }
})();
