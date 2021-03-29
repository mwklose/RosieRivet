var analysis = [];
DEBUG_URL = "http://127.0.0.1:5000";
var editAnalysis = new Set();
(function() {
  for(i = 0; i < sessionStorage.length; i++){
    if(sessionStorage.key(i).endsWith("_analysis")){
      analysis.push(JSON.parse(sessionStorage.getItem(sessionStorage.key(i))))
    }
  }
})();

// c stands for class
function change(c){
	if($(c).is(":checked")){
		for (let x of document.querySelectorAll('.'+c.id)) x.style = "";
      editAnalysis.delete(c.id)
	}else{
		for (let x of document.querySelectorAll('.'+c.id)) x.style = "display:none;";
      editAnalysis.add(c.id)
	}
}





function makeDropDown(name, columns){
  //create a div class to surround lists
	list_div = document.createElement('div');
  //assign id
	list_div.setAttribute("id", name + "_" + "list");
  //use bootstrap dropdown css
	list_div.setAttribute("class", "dropdown btn-group");
	list_div.setAttribute("tabindex", "100");
  //add list div to html
	document.getElementById("dropdown").appendChild(list_div);

  //add an anchor
	anchor = document.createElement('a');
  //represent the button to click and get dropdown
	anchor.setAttribute("class", "btn dropdown-toggle");
	anchor.setAttribute("data-toggle", "dropdown");

  //add name of riveter to button
  anchor.appendChild(document.createTextNode(name));
  list_div.appendChild(anchor);

  //add columns of riveter to list
  items_list = document.createElement('ul');
  items_list.setAttribute("class", "dropdown-menu")
  list_div.appendChild(items_list)
  for (var i = 0; i < columns.length; i++){
  	list_item = document.createElement('li');
  	input = document.createElement("input");
  	input.setAttribute("type","checkbox");
  	list_item.appendChild(input);
  	list_item.appendChild(document.createTextNode(columns[i]));
    //append change function to element
  	input.setAttribute("onchange", "change(this)");
  	input.id =  name + "_" + columns[i];
  	input.checked = true;
  	items_list.appendChild(list_item)
  	}
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
    headerCell.innerText = key;
    row.appendChild(headerCell);
  }
  // Create the Table Body
  var tbody = document.createElement('tbody');
  table.appendChild(tbody);
  // Add the Information for each Riveter in its table body
  row = tbody.insertRow(-1);

  for (var i = 0; i < analysis.length; i++) {
  	for (key in analysis[i]) {
      // represents cell where nested table resides
      var cell = row.insertCell(-1);
      cell.id = key;
      var jsondata = analysis[i][key]["detected"];

      //Add div to make table scrollable
      scroll_div = document.createElement('div');
      scroll_div.style = "height: 400px; overflow-y: scroll;";
      cell.appendChild(scroll_div);
      //make div the parent of nested table
      cell = scroll_div;
      //create nested table
      var analysis_table = document.createElement('table');
      analysis_table.border = "1px solid #000";
      analysis_table.overflow = scroll;
      analysis_table.width = "100%";
      analysis_table.height = "100%";
      //add Row,Column,Column Name, Data header row
      header_row = document.createElement('tr');
      //create column header
      header_row_c = document.createElement('td');
      header_row_c.appendChild(document.createTextNode("Row"));
      header_row.appendChild(header_row_c);
      //create row header
      header_row_r = document.createElement('td');
      header_row_r.appendChild(document.createTextNode("Column"));
      header_row.appendChild(header_row_r);
      //create column name header
      header_row_cn = document.createElement('td');
      header_row_cn.appendChild(document.createTextNode("Column Name"));
      header_row.appendChild(header_row_cn);
      //create data header
      header_row_d = document.createElement('td');
      header_row_d.appendChild(document.createTextNode("Data"));
      header_row.appendChild(header_row_d);
      //Add row to nested analysis table
      analysis_table.appendChild(header_row);
      //add Json Data
      for (i_key in jsondata) {
        column_key = i_key.split(":");
        //create row to represent one line of jsondata
        data_row = document.createElement('tr');
        data_row.setAttribute("class", key+"_"+column_key[1]);
        //create row number 
        row_td = document.createElement('td');
        row_td.appendChild(document.createTextNode(column_key[0]));
        data_row.appendChild(row_td);
        //create column number 
        column_td = document.createElement('td');
        column_td.appendChild(document.createTextNode(column_key[1]));
        data_row.appendChild(column_td);
        //create column name
        column_name_td = document.createElement('td');
        column_name_td.appendChild(document.createTextNode(column_key[2]));
        data_row.appendChild(column_name_td);
        //create data 
        data_td = document.createElement('td');
        data_td.appendChild(document.createTextNode(jsondata[i_key]));
        data_row.appendChild(data_td);
        //add row to nested table
        analysis_table.appendChild(data_row);
      }
      //add nested table to div tag
      cell.appendChild(analysis_table);


    }
  }
}

function sortColumns(jsondata){
  return jsondata;
}

//generate drop downs for all riveters
function generateDropDowns(){
	for (var i = 0; i < analysis.length; i++) {
		for (key in analysis[i]) {
			column_numbers = new Set()
			for (i_key in analysis[i][key]["detected"]){
		        column_key = i_key.split(":");
		        column_numbers.add(column_key[1]);
			}
			makeDropDown(key, Array.from(column_numbers).sort());
		}
	}

}

//send and create protected files
function send(){
  for(var i = 0; i < analysis.length; i++){

      analysis_payload = {}
      for(key in analysis[i]){
        analysis_payload[key] = {}

        for(i_key in analysis[i][key]){
          if(i_key === "detected"){
            analysis_payload[key][i_key] = {}
            for(j_key in analysis[i][key]["detected"]){
              column_key = j_key.split(":");
              if(editAnalysis.has(key+"_"+column_key[1])){
                continue
              }
              else{
                analysis_payload[key][i_key][j_key] =  analysis[i][key]["detected"][j_key]
              }

            }
          } else{
            analysis_payload[key][i_key] =analysis[i][key][i_key]
          }
        }
      }
      var fd = new FormData();
      for(i = 0; i < sessionStorage.length; i++){
        if(sessionStorage.key(i).endsWith("csv")){
          fd.append('file', sessionStorage.getItem(sessionStorage.key(i)));
          break;
        }
      } 
      fd.append('sess_key', sessionStorage.getItem("sess_key"));
      fd.append('analysis', JSON.stringify(analysis_payload))
      var req = jQuery.ajax({
        url: DEBUG_URL+"/v1/process",
        method: 'POST',
        data: fd,
        processData: false,
        contentType: false
      });
      req.then(function(response) {
        const blob = new Blob([response], {type: 'application/pdf'});
        const downloadUrl = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = downloadUrl;
        a.download = "out.csv";
        document.body.appendChild(a);
        a.click();
      }, function(xhr) {
        console.error('failed to fetch xhr', xhr)
      })

  }



}
generateDropDowns();
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
