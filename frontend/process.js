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
document.write('<tr>');

for (var i = 0; i < analysis.length; i++) {
	for (key in analysis[i]) {
    document.write('<td>');
    var jsondata = analysis[i][key]["detected"]
    if(Object.keys(jsondata).length === 0){
      document.write("No detected data");
      continue;
    }

    // var arr = jsondata.split(",");
  	//document.write('<td>' + JSON.stringify(analysis[i][key]["detected"]) + '</td>');
    document.write("<table border==\"1\"><tr>");
    document.write('<td>' + "Row" + '</td>');
    document.write('<td>' + "Column" + '</td>');
    document.write('<td>' + "Column Name" + '</td>');
    document.write('<td>' + "Data" + '</td>');
    document.write("</tr>");

    // Separate the JSON string by commas?
    // Iterate over how many items there are with a for loop
    for (key in jsondata) {
      document.write('<tr>');
      column_key = key.split(":")
      document.write('<td>' + column_key[0] + '</td>');
      document.write('<td>' + column_key[1] + '</td>');
      document.write('<td>' + column_key[2] + '</td>');


      document.write('<td>' + jsondata[key] + '</td>');
      document.write('</tr>');
    }

    document.write("</table>");
    document.write('</td>');

  }
}
document.write('</tr>');

document.write("</table>");
