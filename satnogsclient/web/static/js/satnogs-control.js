// Initialize status page
$(document).ready(function(){

})

$(function(){
  $("#command-dropdown li a").click(function(){
    if($(this).index() == 0) {
      $("#command-btn:first-child").text($(this).text());
      $("#command-btn:first-child").append('<span class="caret" id="caret-custom"></span>');
        if ($("#command-btn:first-child").text() == 'Test Service') {
          var elem= document.getElementById('service-params');
          elem.style.display= "block";
        }
    } else if($(this).index() == 1) {
      $("#command-btn:nth-child(2)").text($(this).text());
      $("#command-btn:nth-child(2)").append('<span class="caret" id="caret-custom"></span>');
        if ($("#command-btn:nth-child(2)").text() == 'Custom Packet') {
          var elem= document.getElementById('service-params-custom');
          elem.style.display= "block";
        }
    }
   });

   $("#power-radio").change(function(){
     // If checkbox not checked already
     if ($('input[name=power-radio]').prop('checked') == true) {
       var elem= document.getElementById('subservice-params-power');
       var elem2= document.getElementById('subservice-params-time');
       elem.style.display= "block";
       elem2.style.display= "none";
       $('input[name=time-radio]').prop('checked',false);
       // TODO: Uncheck every other radio
     }
   });

   $("#comms-tx-on").click(function(){
     request = encode_comms_tx_rf(1);
     query_control_backend(request, 'POST', '/command', true);
   });

   $("#comms-tx-off").click(function(){
     request = encode_comms_tx_rf(0);
     query_control_backend(request, 'POST', '/command', true);
   });

   $("#time-radio").change(function(){
     // If checkbox not checked already
     if ($('input[name=power-radio]').prop('checked') == true) {
       var elem= document.getElementById('subservice-params-time');
       var elem2= document.getElementById('subservice-params-power');
       elem.style.display= "block";
       elem2.style.display= "none";
       $('input[name=power-radio]').prop('checked',false);
       // TODO: Uncheck every other radio
     }
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

  var PacketID = new Object();
  PacketID.VersionNumber = '0';
  PacketID.Type = '1';
  PacketID.DataFieldHeaderFlag = '1';
  PacketID.ApplicationProcessID = '1';

  var PacketSequenceControl = new Object();
  PacketSequenceControl.SequenceFlags = '3';
  PacketSequenceControl.SequenceCount = '59';

  var PacketDataField = new Object();
  PacketDataField.DataFieldHeader = DataFieldHeader;
  PacketDataField.ApplicationData = '';
  PacketDataField.Spare = '0';
  PacketDataField.PacketErrorControl = '5';

  var PacketHeader = new Object();
  PacketHeader.PacketID = PacketID;
  PacketHeader.PacketSequenceControl = PacketSequenceControl;
  PacketHeader.PacketLength = '66';

  var TestServicePacket = new Object();
  TestServicePacket.PacketHeader = PacketHeader;
  TestServicePacket.PacketDataField = PacketDataField;

  console.log(JSON.stringify(TestServicePacket));
  var json_packet = JSON.stringify(TestServicePacket);
  return json_packet;
}

function encode_comms_tx_rf(status) {
  var response = new Object();
  var custom_cmd = new Object();
  var comms_tx_rf = new Object();
  if (status) {
    custom_cmd.comms_tx_rf = 'comms_on';
  }
  else {
    custom_cmd.comms_tx_rf = 'comms_off';
  }
  response.custom_cmd = custom_cmd;
  console.log(JSON.stringify(response));
  var json_packet = JSON.stringify(response);
  return json_packet;
}

function print_command_response(data) {
  var response_panel= document.getElementById('response-panel-body');
  response_panel.innerHTML += data['Response'];
  response_panel.innerHTML += '<br>';
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
