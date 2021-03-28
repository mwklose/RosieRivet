var analysis = [];
(function() {
  for(i = 0; i < sessionStorage.length; i++){
    if(sessionStorage.key(i).endsWith("_analysis")){
      analysis.push(JSON.parse(sessionStorage.getItem(sessionStorage.key(i))))
    }
  }
})();
// c stands for class
function hide(c){
  $("."+c).addClass("hidden");
}
// c stands for class
function show(c){
  $("."+c).removeClass("hidden");
}


function makeTable(){
  var table = document.createElement('table');
  // ADJUST ONCE CSS OF TABLE
  table.border = "1px solid #000";
  // test if this overflow works later
  table.overflow = scroll;

  document.getElementById("datalist").appendChild(table);
  // Create the Table Header
  var theader = table.createTHead();
  var row = theader.insertRow(-1);
  // Add columns for each Riveter header
  for (key in analysis[0]){
    var headerCell = document.createElement('th');
    headerCell.innerText = key
    row.appendChild(headerCell);
  }
  // Create the Table Body
  var tbody = document.createElement('tbody');
  table.appendChild(tbody);
  // Add the Information for each Riveter in its table body
  for (var i = 0; i < analysis.length; i++) {
    row = tbody.insertRow(-1);
  	for (key in analysis[i]) {
      var cell = row.insertCell(-1);
      cell.id = key;
      var jsondata = analysis[i][key]["detected"];
      cell.innerText = jsondata;

      for (k in jsondata){
        document.write(k + "\n")
      }
      if(Object.keys(jsondata).length === 0){
        document.write("<td>" + "No detected data" + "</td>");
        continue;
      } else {
        document.write("<td>" + "LAURENS DOGS" + "</td>");
      }
    }
  }
}

function sortColumns(jsondata){
  return jsondata;
}

makeTable();
//
// console.log(analysis);
// document.write("<table border==\"1\"><tr>");
// for (key in analysis[0]) {
// 	document.write('<td>' + key + '</td>');
// }
// document.write("</tr>");
// document.write('<tr>');
//
// for (var i = 0; i < analysis.length; i++) {
// 	for (key in analysis[i]) {
//     document.write('<td>');
//     var jsondata = analysis[i][key]["detected"]
//     if(Object.keys(jsondata).length === 0){
//       document.write("No detected data");
//       continue;
//     }
//
//     // var arr = jsondata.split(",");
//   	//document.write('<td>' + JSON.stringify(analysis[i][key]["detected"]) + '</td>');
//     document.write("<table border==\"1\"><tr>");
//     document.write('<td>' + "Row" + '</td>');
//     document.write('<td>' + "Column" + '</td>');
//     document.write('<td>' + "Column Name" + '</td>');
//     document.write('<td>' + "Data" + '</td>');
//     document.write("</tr>");
//
//     // Separate the JSON string by commas?
//     // Iterate over how many items there are with a for loop
//     for (key in jsondata) {
//       column_key = key.split(":")
//       document.write('<tr' + ' id = column_key[1]' + '>');
//       document.write('<td>' + column_key[0] + '</td>');
//       document.write('<td>' + column_key[1] + '</td>');
//       document.write('<td>' + column_key[2] + '</td>');
//
//
//       document.write('<td>' + jsondata[key] + '</td>');
//       document.write('</tr>');
//     }
//
//     document.write("</table>");
//     document.write('</td>');
//
//   }
// }
// document.write('</tr>');
//
// document.write("</table>");
