$(function(){
  $('#config-save-button').on('click', function(e){
    var table = document.getElementById("config-table");
    var array = {};
	array.configuration = {};
	for (var i = 1, row; row = table.rows[i]; i++) {
	    array.configuration[row.cells[0].innerText] = row.cells[1].innerText;	    
	}
	var json = JSON.stringify(array);
	postJSONData(json, "POST", "/config_update");
	console.log(json);
  })
});

function postJSONData(JSONData, localMode, url) {
        var localJSONData = JSONData;
        var postMode = localMode;

         $.ajax({
                type: postMode,
                url: url,
                contentType:"application/json; charset=utf-8",
                dataType:"json"
                data:  JSONData
                success: function(data){
					console.log("POST success");
                }   // Success Function
		}); // AJAX Call

}