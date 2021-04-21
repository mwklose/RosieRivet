/*
filedrag.js - HTML5 File Drag & Drop demonstration
Featured on SitePoint.com
Developed by Craig Buckler (@craigbuckler) of OptimalWorks.net
*/

(function() {
	DEBUG_URL = "http://127.0.0.1:5000/v1/analyze";
	sessionStorage.clear()
	// getElementById
	function $id(id) {
		return document.getElementById(id);
	}


	// output information
	function Output(msg) {
		var m = $id("messages");
		m.innerHTML = msg + m.innerHTML;
	}


	// file drag hover
	function FileDragHover(e) {
		e.stopPropagation();
		e.preventDefault();
		e.target.className = (e.type == "dragover" ? "hover" : "");
	}


	// file selection
	function FileSelectHandler(e) {

		//Set or Get session key for current user
		if(sessionStorage.getItem("sess_key") === null){
			sessionStorage.setItem("sess_key",Math.random() * 1000);
		}

		// cancel event and hover styling
		FileDragHover(e);

		// fetch FileList object
		var files = e.target.files || e.dataTransfer.files;

		// process all File objects
		for (var i = 0, f; f = files[i]; i++) {
			
			sessionStorage.setItem(f.name,f);
			ParseFile(f);
		}

		document.getElementById("button_load").setAttribute("class", "fa fa-spinner fa-spin");


	}


	// output file information
	function ParseFile(file) {
		Output(
			"<p>File information: <strong>" + file.name +
			"</strong> type: <strong>" + file.type +
			"</strong> size: <strong>" + file.size +
			"</strong> bytes</p>"
		);


		var fd = new FormData();
		fd.append('file', file);
		fd.append('sess_key', sessionStorage.getItem("sess_key"));
		var req = jQuery.ajax({
			url: DEBUG_URL,
			method: 'POST',
			data: fd,
			processData: false,
 			contentType: false
		});
		req.then(function(response) {
			sessionStorage.setItem(file.name + "_analysis", JSON.stringify(response["data_analysis"]));
			for (var key in response["meta_analysis"]){
				if( response["meta_analysis"][key]["detected"]){
				Output(
				"<p>" + key + "- <strong>" + response["meta_analysis"][key]["detected"]["data"] + "</strong>"
					);
				}

			}
			if(response["data_analysis"]){
				Output(
					"<div class=\"tooltip\"> Confidence <span class=\"tooltiptext\">Rivet has detected "+
					"possible misinterpretations in your file, configure the confidence value Rivet should use in remedying these issues</span></div>" + "<input id=confidence_value type=\"text\"" + " value = 80>"
				);
			}
			document.getElementById("button_load").setAttribute("class", "");
			document.getElementById("process_page").removeAttribute("disabled");


		}, function(xhr) {
		  console.error('failed to fetch xhr', xhr)
			document.getElementById("button_load").setAttribute("class", "");

		})




	}




	// initialize
	function Init() {

		var fileselect = $id("fileselect"),
			filedrag = $id("filedrag"),
			submitbutton = $id("submitbutton");

		// file select
		fileselect.addEventListener("change", FileSelectHandler, false);

		// is XHR2 available?
		var xhr = new XMLHttpRequest();
		if (xhr.upload) {

			// file drop
			filedrag.addEventListener("dragover", FileDragHover, false);
			filedrag.addEventListener("dragleave", FileDragHover, false);
			filedrag.addEventListener("drop", FileSelectHandler, false);
			filedrag.style.display = "block";

			// remove submit button
			submitbutton.style.display = "none";
		}

	}

	// call initialization file
	if (window.File && window.FileList && window.FileReader) {
		Init();
	}

})();
function submit(){
	parent.location='process.html';
	sessionStorage.setItem("confidence", document.getElementById("confidence_value").value);
}
document.getElementById("process_page").addEventListener ("click", submit, false);

