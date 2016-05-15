// Initialize status page
$(document).ready(function(){

})

$(function(){
    $("#command-dropdown li a").click(function(){
      $("#command-btn:first-child").text($(this).text());
      // if ($("#command-btn:first-child").text() == 'Test Service') {
      //   $("#command-btn:first-child").append('<span class="caret"></span>');
      //   var elem= document.getElementById('test-service-params');
      //   elem.style.display= "block";
      // }
   });

   $("#send-cmd").click(function(){
     if ($("#command-btn:first-child").text() == 'Test Service') {
       request = encode_test_service();
     }
     else {
       alert('Invalid command');
       request = false;
     }
     query_control_backend(request, 'POST', '/command', true);
  });
});

function encode_test_service() {
  var DataFieldHeader = new Object();
  DataFieldHeader.CCSDSSecondaryHeaderFlag = '0';
  DataFieldHeader.TCPacketPUSVersionNumber = '1';
  DataFieldHeader.Ack = '0';
  DataFieldHeader.ServiceType = '17';
  DataFieldHeader.ServiceSubType = '1';
  DataFieldHeader.SourceID = '3';
  DataFieldHeader.Spare = '0';

  var PacketDataField = new Object();
  PacketDataField.DataFieldHeader = DataFieldHeader;
  PacketDataField.ApplicationData = '';
  PacketDataField.Spare = '0';
  PacketDataField.PacketErrorControl = '5';

  //var PacketData = new Object();
  //PacketData.PacketDataField = PacketDataField;

  //var PacketDataFieldJsonArray = new Array();
  //PacketDataFieldJsonArray.push(PacketDataField);
  //console.log(JSON.stringify(PacketDataField));
  //console.log(JSON.stringify(PacketDataField['DataFieldHeader']['ServiceType']));
  var json_packet = JSON.parse(JSON.stringify(PacketDataField));
  return json_packet
}

function print_command_response(data) {
  var response_panel= document.getElementById('response-panel');
  response_panel.innerHTML = data['Response'];
}

function query_control_backend(JSONData, localMode, url, param) {
  var localJSONData = JSONData;
  var postMode = localMode;

   $.ajax({
          type: postMode,
          url: url,
          contentType:"application/json; charset=utf-8",
          dataType:"json",
          data:  JSONData,
          success: function(data) {
              print_command_response(data);
          },
          error: function(data) {
              alert('Something went wrong!')
          }
  });
}
