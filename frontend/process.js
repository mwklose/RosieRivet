var analysis = [];
(function() {
  for(i = 0; i < sessionStorage.length; i++){
    if(sessionStorage.key(i).endsWith("_analysis")){
      analysis.push(JSON.parse(sessionStorage.getItem(sessionStorage.key(i))))
    }
  }
})();

console.log(analysis);
document.write("<table border==\"1\"><tr>");
for (key in analysis[0]) {
	document.write('<td>' + key + '</td>');
}
document.write("</tr>");
for (var i = 0; i < analysis.length; i++) {
	document.write('<tr>');
	for (key in analysis[i]) {
    var jsondata = analysis[i][key]["detected"]
    // var arr = jsondata.split(",");
  	//document.write('<td>' + JSON.stringify(analysis[i][key]["detected"]) + '</td>');
    document.write('<td>');
    document.write("<table border==\"1\"><tr>");
    document.write('<td>' + "column1" + '</td>');
    document.write('<td>' + "column2" + '</td>');
    // Separate the JSON string by commas?
    // Iterate over how many items there are with a for loop
    for (key in jsondata) {
      document.write('<tr>');
      document.write('<td>' + key + '</td> <td>' + jsondata[key] + '</td>');
      document.write('</tr>');
    }

    document.write("</tr>");
    document.write('</td>');
  }
	document.write('</tr>');
}
document.write("</table>");
