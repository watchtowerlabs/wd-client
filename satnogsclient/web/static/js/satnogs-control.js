// Initialize status page
$(document).ready(function(){

})

$(function(){
   $("#custom-select").click(function(){
     var elem= document.getElementById('service-param-panel');
     elem.style.display= "block";
   });

   $('#service-param-panel select').on('change', function() {
     // Handle change on service parameter dropdowns
   });

  $('#service-send').on('click', function() {
    var list = $('#service-param-panel').find("select");
    var missing = [];
    var flag = true;
    for (i=0; i<list.length; i++){
      if (isNaN(list[i].value)) {
        missing.push(list[i].value);
        flag = false;
      }
    }
    var app_id = $('#service-param-app_id').val();
    var type = $('#service-param-type').val();
    var ack = $('#service-param-ack').val();
    var service_type = $('#service-param-service_type').val();
    var dest_id = $('#service-param-dest_id').val();


    if (flag){
      encode_service(app_id, service_type,dest_id,ack,type);
    }
    else{
      alert('Please fill ' + missing);
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

   $(':file').change(function(){
      // var file = this.files[0];
      // var name = file.name;
      // var size = file.size;
      // var type = file.type;
      //Your validation
  });

  $(':button').click(function(){
    var formData = new FormData($('form')[0]);
    $.ajax({
        url: '/raw',  //Server script to process data
        type: 'POST',
        xhr: function() {  // Custom XMLHttpRequest
            var myXhr = $.ajaxSettings.xhr();
            if(myXhr.upload){ // Check if upload property exists
                myXhr.upload.addEventListener('progress',progressHandlingFunction, false); // For handling the progress of the upload
            }
            return myXhr;
        },
        //Ajax events
        // beforeSend: beforeSendHandler,
        // success: completeHandler,
        // error: errorHandler,
        // Form data
        data: formData.get('file'),
        //Options to tell jQuery not to process data or worry about content-type.
        cache: false,
        contentType: false,
        processData: false
    });
});

function progressHandlingFunction(e){
    if(e.lengthComputable){
        $('progress').attr({value:e.loaded,max:e.total});
    }
}

  //  $("#fileinput").click(function(){
  //     input = document.getElementById('fileinput');
   //
  //     file = input.files[0];
  //     var reader = new FileReader();
  //     reader.onload = function(){
  //         var binaryString = this.result;
  //         $.ajax({
  //            url: '/raw',
  //            type: 'POST',
  //            contentType: 'application/octet-stream',
  //            data: binaryString,
  //            processData: false
  //         });
  //       };
  //     data = reader.readAsBinaryString(file);
   //
  //  });

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

function encode_service(app_id, service_type,service_subtype,ack,type) {
  var DataFieldHeader = new Object();
  DataFieldHeader.CCSDSSecondaryHeaderFlag = '0';
  DataFieldHeader.TCPacketPUSVersionNumber = '1';
  DataFieldHeader.Ack = ack;
  DataFieldHeader.ServiceType = service_type;
  DataFieldHeader.ServiceSubType = service_subtype;
  DataFieldHeader.SourceID = app_id;
  DataFieldHeader.Spare = '0';

  var PacketID = new Object();
  PacketID.VersionNumber = '0';
  PacketID.Type = type;
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
