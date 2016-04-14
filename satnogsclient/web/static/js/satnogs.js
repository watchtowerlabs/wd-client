function AnimateRotate(degrees) {
    var $elem = $('#current-pass-arrow');
    $({deg: degrees}).animate({deg: degrees}, {
        duration: 2000,
        step: function(now) {
            $elem.css({
                transform: 'rotate(' + now + 'deg)'
            });
        }
    });
}

function initMap(lat,lng) {
  var latf = parseFloat(lat);
  var lngf = parseFloat(lng);
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 1,
    center: new google.maps.LatLng(latf, lngf)
  });

  var marker = new google.maps.Marker({
    position: new google.maps.LatLng(latf, lngf),
    map: map,
    title: 'Hello World!'
  });

  map.setZoom(1);
  return map;
}

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
  })
});

function update_status_ui(data, param) {
        var json_data = data;

        if (json_data["azimuth"] === "NA" && json_data["altitude"] === "NA") {
          document.getElementById("azimuth").innerHTML = json_data["azimuth"];
          document.getElementById("elevation").innerHTML = json_data["altitude"];
        }
        else {
          document.getElementById("azimuth").innerHTML = json_data["azimuth"] + " &deg;";
          document.getElementById("elevation").innerHTML = json_data["altitude"] + " &deg;";
          param.setCenter(new google.maps.LatLng(json_data["azimuth"] , json_data["altitude"]));
          AnimateRotate(parseFloat(json_data["azimuth"]));
        }
        if (json_data["frequency"] === "NA") {
          document.getElementById("freq").innerHTML = json_data["frequency"];
        }
        else {
          document.getElementById("freq").innerHTML = json_data["frequency"] + " MHz";
        }

}

function query_status_info(JSONData, localMode, url, param) {
        var localJSONData = JSONData;
        var postMode = localMode;

         $.ajax({
                type: postMode,
                url: url,
                contentType:"application/json; charset=utf-8",
                dataType:"json",
                data:  JSONData,
                success: function(data) {
                    update_status_ui(data , param);
                }
		});
}

$(document).ready(function(){
  document.getElementById("azimuth").innerHTML = "NA";
  document.getElementById("elevation").innerHTML = "NA";
  document.getElementById("freq").innerHTML = "NA";
  map = initMap(49.496675,-102.65625);

  var counter = 45;
  setInterval(function(){
      query_status_info({}, 'GET', '/update_status', map);
  }, 1000);

})
