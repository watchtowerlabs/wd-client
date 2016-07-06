$(document).ready(function() {

    init();

    $("#comms-gnu").click(function() {
        mode = "gnuradio";
        request = encode_backend_mode(mode);
        query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);
        $("#comms-gnu").css('background-color', '#5cb85c');
        $("#comms-ser").css('background-color', '#d9534f');
    });

    $("#comms-ser").click(function() {
        mode = "serial";
        request = encode_backend_mode(mode);
        query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);
        $("#comms-gnu").css('background-color', '#d9534f');
        $("#comms-ser").css('background-color', '#5cb85c');
    });


    $('#service-select li').on('click', function() {
        // Handle change on service parameter dropdowns
        selected_service_id = $(this).prop('id');
        $(this).addClass('active');
        display_service(selected_service_id);
    });

    $('#service-param-service_type').on('change', function() {
        // Handle change on service parameter dropdowns
        var subservice = $(this).find("option:selected").text();

        var VR_SERVICE = {
            TM_VR_ACCEPTANCE_SUCCESS: 1,
            TM_VR_ACCEPTANCE_FAILURE: 2
        };

        var HK_SERVICE = {
            TC_HK_REPORT_PARAMETERS: 21,
            TM_HK_PARAMETERS_REPORT: 23
        };

        var EV_SERVICE = {
            TM_EV_NORMAL_REPORT: 1,
            TM_EV_ERROR_REPORT: 4
        };

        var FM_SERVICE = {
            TC_FM_PERFORM_FUNCTION: 1
        };

        var SC_SERVICE = {
            TC_SC_ENABLE_RELEASE: 1,
            TC_SC_DISABLE_RELEASE: 2,
            TC_SC_RESET_SCHEDULE: 3,
            TC_SC_INSERT_TC: 4,
            TC_SC_DELETE_TC: 5,
            TC_SC_TIME_SHIFT_SPECIFIC: 7,
            TC_SC_TIME_SHIFT_SELECTED_OTP: 8,
            TC_SC_TIME_SHIFT_ALL: 15
        };

        var LD_SERVICE = {
            TM_LD_FIRST_DOWNLINK: 1,
            TC_LD_FIRST_UPLINK: 9,
            TM_LD_INT_DOWNLINK: 2,
            TC_LD_INT_UPLINK: 10,
            TM_LD_LAST_DOWNLINK: 3,
            TC_LD_LAST_UPLINK: 11,
            TC_LD_ACK_DOWNLINK: 5,
            TM_LD_ACK_UPLINK: 14,
            TC_LD_REPEAT_DOWNLINK: 6,
            TM_LD_REPEAT_UPLINK: 15,
            TM_LD_REPEATED_DOWNLINK: 7,
            TC_LD_REPEATED_UPLINK: 12,
            TM_LD_ABORT_SE_DOWNLINK: 4,
            TC_LD_ABORT_SE_UPLINK: 13,
            TC_LD_ABORT_RE_DOWNLINK: 8,
            TM_LD_ABORT_RE_UPLINK: 16
        };

        var MS_SERVICE = {
            TC_MS_ENABLE: 1,
            TC_MS_DISABLE: 2,
            TC_MS_CONTENT: 8,
            TC_MS_DOWNLINK: 9,
            TC_MS_DELETE: 11,
            TC_MS_REPORT: 12,
            TM_MS_CATALOGUE_REPORT: 13,
            TC_MS_UPLINK: 14,
            TC_MS_FORMAT: 15
        };

        var CT_SERVICE = {
            TC_CT_PERFORM_TEST: 1,
            TM_CT_REPORT_TEST: 2
        };

        var $select = $('#service-param-service_subtype');
        $select.find('option').remove();
        $select.append('<option selected="true" style="display:none;">Service sub Type</option>');

        var key;
        if (subservice == "TC_VERIFICATION_SERVICE") {
            for (key in VR_SERVICE) {
                $select.append('<option value=' + VR_SERVICE[key] + '>' + key + '</option>');
            }
        } else if (subservice == "TC_HOUSEKEEPING_SERVICE") {
            for (key in HK_SERVICE) {
                $select.append('<option value=' + HK_SERVICE[key] + '>' + key + '</option>');
            }
        } else if (subservice == "TC_EVENT_SERVICE") {
            for (key in EV_SERVICE) {
                $select.append('<option value=' + EV_SERVICE[key] + '>' + key + '</option>');
            }
        } else if (subservice == "TC_FUNCTION_MANAGEMENT_SERVICE") {
            for (key in FM_SERVICE) {
                $select.append('<option value=' + FM_SERVICE[key] + '>' + key + '</option>');
            }
        } else if (subservice == "TC_TIME_MANAGEMENT_SERVICE") {
            for (key in VR_SERVICE) {
                $select.append('<option value=' + VR_SERVICE[key] + '>' + key + '</option>');
            }
        } else if (subservice == "TC_SCHEDULING_SERVICE") {
            for (key in SC_SERVICE) {
                $select.append('<option value=' + SC_SERVICE[key] + '>' + key + '</option>');
            }
        } else if (subservice == "TC_LARGE_DATA_SERVICE") {
            for (key in LD_SERVICE) {
                $select.append('<option value=' + LD_SERVICE[key] + '>' + key + '</option>');
            }
        } else if (subservice == "TC_MASS_STORAGE_SERVICE") {
            for (key in MS_SERVICE) {
                $select.append('<option value=' + MS_SERVICE[key] + '>' + key + '</option>');
            }
        } else if (subservice == "TC_TEST_SERVICE") {
            for (key in CT_SERVICE) {
                $select.append('<option value=' + CT_SERVICE[key] + '>' + key + '</option>');
            }
        } else if (subservice == "TC_SU_MNLP_SERVICE") {
            for (key in VR_SERVICE) {
                $select.append('<option value=' + VR_SERVICE[key] + '>' + key + '</option>');
            }
        }
    });

    $('#service-param-ms-function').on('change', function() {
        fun = $('#service-param-ms-function').find("option:selected").val();
        alert(fun);
        if (fun == "File_system") {
    
        } else if (fun == "Format") {

        } else if (fun == "Enable") {

        }
    });

    $('#service-param-time-report').on('change', function() {
        elem = document.getElementById('datetimepicker1');
        if ($('#service-param-time-report').find("option:selected").val() == "manual") {
            elem.style.display = "table";
        } else {
            elem.style.display = "none";
        }
    });

    $('#service-param-panel :button').on('click', function() {

        var list = $('this').parent().siblings().find('select');
        var selected_value = $('#service-select li.active').attr("data-value");
        //TODO: Check whether all required fields are selected
        var missing = [];
        for (i = 0; i < list.length; i++) {
            if (isNaN(list[i].value)) {
                missing.push(list[i].value);
                flag = false;
            }
        }

        var app_id = 0;
        var type = 0;
        var ack = 0;
        var service_type = 0;
        var service_subtype = 0;
        var dest_id = 0;
        var data = [];

        if (selected_value == "custom") {
            app_id = $('#service-param-app_id').val();
            type = $('#service-param-type').val();
            ack = $('#service-param-ack').val();
            service_type = $('#service-param-service_type').val();
            service_subtype = $('#service-param-service_subtype').val();
            dest_id = $('#service-param-dest_id').val();
            data = $('#service-param-service-data').val().split(",");
            seq_count = 0;

            request = encode_service(type, app_id, service_type, service_subtype, dest_id, ack, data);
            query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);

        } else if (selected_value == "house") {
            app_id = $('#service-param-hk-app_id').val();
            type = 1;
            ack = 0;
            service_type = 3;
            service_subtype = 21;
            dest_id = $('#service-param-hk-dest-id').val();

            data = $('#service-param-hk-sid').val();
            request = encode_service(type, app_id, service_type, service_subtype, dest_id, ack, data);
            query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);


        } else if (selected_value == "mass") {

            app_id = 1;
            type = 1;
            ack = $('#service-param-ms-ack').val();
            dest_id = $('#service-param-ms-dest-id').val();
            service_type = 15;
            data = [];

            var store_id = $('#service-param-ms-sid').val();

            var fun = $('#service-param-ms-function').val();

            if(fun == "Format") {
                if (confirm('Are you sure you want to format the sd?')) {
                    service_subtype = 15;
                } else {
                    return 0;
                }
            } else if(fun == "File_system") {

                var action = $('#service-param-ms-action').val();

                if(action == "Report") {

                    service_subtype = 12;

                } else if(action == "List") {

                    var fn = $('#service-param-service-ms-num').val();
                    service_subtype = 16;

                    data.splice(0, 0, store_id);
                    data.splice(1, 0, ((fn >> 8) & 0x00FF)); // next file
                    data.splice(2, 0, ((fn >> 0) & 0x00FF));

                } else if(action == "Downlink") {

                    var fn = $('#service-param-service-ms-num').val();                                   
                    service_subtype = 9;

                    data.splice(0, 0, store_id);
                    data.splice(1, 0, ((fn >> 8) & 0x00FF)); // file from
                    data.splice(2, 0, ((fn >> 0) & 0x00FF));
                    data.splice(3, 0, 1); // num of files
                
                } else if(action == "Uplink") {

                    service_subtype = 14;

                    file_encode_and_query_backend(type, app_id, service_type, service_subtype, dest_id, ack, store_id);
                    return 0;
                } else if(action == "Delete") {

                    var fnum = $('#service-param-service-ms-num').val();
                    service_subtype = 11;
                    data.splice(0, 0, store_id);
                    data.splice(1, 0, 0); //mode != 6
                    data.splice(2, 0, ((fnum >> 8) & 0x00FF)); // num of files
                    data.splice(3, 0, ((fnum >> 0) & 0x00FF));

                } else if(action == "Hard") {

                    service_subtype = 11;
                    data.splice(0, 0, store_id);
                    data.splice(1, 0, 6);  // 6 is hard delete mode

                } else if(action == "All") {

                    service_subtype = 11;
                    data.splice(0, 0, store_id);
                    data.splice(1, 0, 7);  // 7 is delete all mode
                    data.splice(2, 0, 0); // pads for keeping same format as delete
                    data.splice(3, 0, 0);
                }
             } 
        //      else if(fun == "Enable") {
        //       continue;
        //     }

            request = encode_service(type, app_id, service_type, service_subtype, dest_id, ack, data);
            query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);

        } else if (selected_value == "power") {
            
            dev_id = $('#service-param-dev-id').val();
            type = 1;
            ack = $('#service-param-power-ack').val();

            service_type = 8;
            service_subtype = 1;
            dest_id = $('#service-param-power-dest_id').val();

            if (dev_id == 1) {
                app_id = 2;
            } else if (dev_id == 2) {
                app_id = 2;
            } else if (dev_id == 3) {
                app_id = 2;
            } else if (dev_id == 4) {
                app_id = 2;
            } else if (dev_id == 5) {
                app_id = 1;
            } else if (dev_id == 6) {
                app_id = 2;
            } else if (dev_id == 7) {
                app_id = 3;
            } else if (dev_id == 8) {
                app_id = 1;
            } else if (dev_id == 9) {
                app_id = 3;
            } else if (dev_id == 10) {
                app_id = 3;
            } else if (dev_id == 11) {
                app_id = 3;
            } else if (dev_id == 12) {
                app_id = 3;
            } else if (dev_id == 13) {
                app_id = 3;
            } else if (dev_id == 14) {
                app_id = 3;
            } else if (dev_id == 15) {
                app_id = 3;
            }

            var fun_id = $('#service-param-function').val();
            data = [fun_id, dev_id];

            request = encode_service(type, app_id, service_type, service_subtype, dest_id, ack, data);
            query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);

        } else if (selected_value == "test") {
            app_id = $('#service-param-test-app_id').val();
            type = 1;
            ack = 0;

            service_type = 17;
            service_subtype = 1;
            dest_id = $('#service-param-test-dest_id').val();
            data = [];

            request = encode_service(type, app_id, service_type, service_subtype, dest_id, ack, data);
            query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);

        } else if (selected_value == "time") {
            // TODO: Is app_id needed in time service?
            //app_id = $('#service-param-time-app_id').val();
            app_id = 1;
            type = 1;
            ack = 0;

            service_type = 17;
            service_subtype = 1;
            dest_id = $('#service-param-time-dest_id').val();

            selected_action = $('#service-param-time-report').find("option:selected").val();

            if (selected_action == 'manual') {
                var datetime = datepicker.data("DateTimePicker").date();
                data = [datetime.utc().format().toString()];
            } else if (selected_action == 'auto') {
                data = [moment().utc().format().toString()];
            } else {
                data = [];
            }

            request = encode_service(type, app_id, service_type, service_subtype, dest_id, ack, data);
            query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);

        } else if (selected_value == "adcs") {
            // TODO: Is app_id needed in time service?
            //app_id = $('#service-param-time-app_id').val();
            app_id = 7;
            type = 0;
            ack = 0;

            service_type = 3;
            service_subtype = 23;
            dest_id = 3;

            data = [];
            ascii_to_dec($('#service-param-service-tle').val().split(''), data);
            data.unshift(6);
            //number of TLE chanacters
            if (data.length != 137) {
                alert("TLE shouldnt be: " + data.length);
                return 0;
            }

            request = encode_service(type, app_id, service_type, service_subtype, dest_id, ack, data);
            query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);

        } else if (selected_value == "comms") {
            if ($(this).attr("id") == "comms-tx-on") {
                request = encode_comms_tx_rf(1);
                query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);
            } else if ($(this).attr("id") == "comms-tx-off") {
                request = encode_comms_tx_rf(0);
                query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);
            }
        }
    });

    $("#time-radio").change(function() {
        // If checkbox not checked already
        if ($('input[name=power-radio]').prop('checked') === true) {
            var elem = document.getElementById('subservice-params-time');
            var elem2 = document.getElementById('subservice-params-power');
            elem.style.display = "block";
            elem2.style.display = "none";
            $('input[name=power-radio]').prop('checked', false);
            // TODO: Uncheck every other radio
        }
    });

    $('#filter-section input').on('change', function() {
        var itemsToFilter = $('#response-panel-body ul li');
        for (var i = 0; i < itemsToFilter.length; i++) {
            var currentItem = itemsToFilter[i];
            if (currentItem.getAttribute("data-type") == $(this).val()) {
                if ($(this).is(':checked')) {
                    currentItem.classList.remove('hide-log');
                    currentItem.classList.add('show-log');
                } else {
                    currentItem.classList.remove('show-log');
                    currentItem.classList.add('hide-log');
                }
            }
        }
    });

    $('#clear-log').on('click', function() {
      var itemsToFilter = $('#response-panel-body ul li');
      for (var i = 0; i < itemsToFilter.length; i++) {
        var currentItem = itemsToFilter[i];
        currentItem.remove();
      }
    });

    $("#mode-switch li").click(function() {
        var mode = $(this).attr("data-value");
        display_control_view(mode);
    });

});

function display_service(selection) {
    var services = {
        'custom-select': 'service-param-custom',
        'power-select': 'service-param-power',
        'test-select': 'service-param-test',
        'time-select': 'service-param-time',
        'tle-select': 'service-param-tle',
        'ms-select': 'service-param-mass-storage',
        'comms-select': 'service-param-comms',
        'hk-select': 'service-param-housekeeping'
    };
    var keys = [];
    for (var key in services) {
        var elem = document.getElementById(services[key]);
        var service_param_panel = document.getElementById('service-param-panel');
        var service_select = document.getElementById(key);
        if (key == selection) {
            elem.style.display = "block";
            service_param_panel.style.backgroundColor = '#f8f8f8';
        } else {
            elem.style.display = "none";
            service_select.classList.remove('active');
        }
    }
}

function ascii_to_dec(inc, out) {
    for (var i = 0; i < inc.length; i++) {
        out[i] = inc[i].charCodeAt(0);
    }
}

function encode_service(type, app_id, service_type, service_subtype, dest_id, ack, data, seq_count) {
    var DataFieldHeader = {};
    DataFieldHeader.CCSDSSecondaryHeaderFlag = '0';
    DataFieldHeader.TCPacketPUSVersionNumber = '1';
    DataFieldHeader.Ack = ack;
    DataFieldHeader.ServiceType = service_type;
    DataFieldHeader.ServiceSubType = service_subtype;
    DataFieldHeader.SourceID = dest_id;
    DataFieldHeader.Spare = '0';

    var PacketID = {};
    PacketID.VersionNumber = '0';
    PacketID.Type = type;
    PacketID.DataFieldHeaderFlag = '1';
    PacketID.ApplicationProcessID = app_id;

    var PacketSequenceControl = {};
    PacketSequenceControl.SequenceFlags = '3';


    if (typeof seq_count != "undefined") {
        PacketSequenceControl.SequenceCount = seq_count;
    }

    var PacketDataField = {};
    PacketDataField.DataFieldHeader = DataFieldHeader;
    if (data) {
        PacketDataField.ApplicationData = data;
    } else {
        PacketDataField.ApplicationData = '';
    }
    PacketDataField.Spare = '0';
    PacketDataField.PacketErrorControl = '5';

    var PacketHeader = {};
    PacketHeader.PacketID = PacketID;
    PacketHeader.PacketSequenceControl = PacketSequenceControl;
    PacketHeader.PacketLength = '66';

    var TestServicePacket = {};
    TestServicePacket.PacketHeader = PacketHeader;
    TestServicePacket.PacketDataField = PacketDataField;

    var ecss_cmd = {};
    ecss_cmd.ecss_cmd = TestServicePacket;
    ecss_cmd.backend = backend;

    console.log(JSON.stringify(ecss_cmd));
    var json_packet = JSON.stringify(ecss_cmd);
    return json_packet;
}

function encode_comms_tx_rf(status) {
    var response = {};
    var custom_cmd = {};
    var comms_tx_rf = {};
    if (status) {
        custom_cmd.comms_tx_rf = 'comms_on';
    } else {
        custom_cmd.comms_tx_rf = 'comms_off';
    }
    response.custom_cmd = custom_cmd;
    console.log(JSON.stringify(response));
    var json_packet = JSON.stringify(response);
    return json_packet;
}

function encode_backend_mode(mode) {
    var response = {};
    var custom_cmd = {};
    var backend = {};
    if (mode == "gnuradio") {
        custom_cmd.backend = 'gnuradio';
    } else if (mode == "serial") {
        custom_cmd.backend = 'serial';
    }
    response.custom_cmd = custom_cmd;
    console.log(JSON.stringify(response));
    var json_packet = JSON.stringify(response);
    return json_packet;
}

function print_command_response(data) {
    var response_panel = $('#response-panel-body ul');
    var data_type;
    console.log(JSON.stringify(data));

    for(var key in data) {
        var resp = data[key];

        if (resp.id == 1) {
            data_type = 'cmd';
            log_data = resp.log_message;
        } else if (resp.id == 2) {
            data_type = 'ecss';
            log_data = resp.log_message;
        } else {
            data_type = 'other';
            log_data = resp.log_message;
        }
        response_panel.append('<li class="' + apply_log_filter(data_type) + '"' + ' data-type="' + data_type + '">[' + moment().format('DD-MM-YYYY HH:mm:ss').toString() + '] ' + log_data + '</li>');
    }
    response_panel.scrollTop = response_panel.scrollHeight;
}

//A function that returns the appropriate class based on the applied filters
function apply_log_filter(log_data_type) {
    var status = $('#filter-section :input[value=' + log_data_type + ']').is(':checked');
    if (status) {
        return 'show-log';
    } else {
        return 'hide-log';
    }
}

function query_control_backend(data, post_mode, url, content_type, data_type, process_data) {
    $.ajax({
        type: post_mode,
        url: url,
        contentType: content_type,
        dataType: data_type,
        data: data,
        processData: process_data,
        success: function(data) {
            print_command_response(data);
        },
        error: function(data) {}
    });
}

function display_control_view(mode) {
    if (mode == 'Network') {
        // Disable Upsat Command and Control
        $('#cnc_mode').css('display', 'none');
        $('#network_mode').css('display', 'block');
    } else if (mode == 'Stand-Alone') {
        // Enable Upsat Command and Control
        $('#cnc_mode').css('display', 'block');
        $('#network_mode').css('display', 'none');
    }
}

//Retrieve file encode command and post the request
function file_encode_and_query_backend(type, app_id, service_type, service_subtype, dest_id, ack, store_id) {
  input = document.getElementById('file');
  file = input.files[0];
  reader = new FileReader();
  reader.readAsBinaryString(file.slice());
  reader.onloadend = function(evt) {
    if (evt.target.readyState == FileReader.DONE) {
      data = [];
      result = evt.target.result;
      ascii_to_dec(result,data);

      data.unshift(store_id);
      console.log(data);
      request = encode_service(type, app_id, service_type, service_subtype, dest_id, ack, data);
      query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);
    }
  };
}

function init() {
    // Various variable definition
    var app_id, type, ack, service_type, service_subtype, dest_id, data, seq_count;

    //mode = $("#mode-switch li").attr("data-value");
    mode = Cookies.get('mode');
    display_control_view(mode);

    // Set initial back-end mode
    backend = 'serial';
    request = encode_backend_mode(backend);
    query_control_backend(request, 'POST', '/command', "application/json; charset=utf-8", "json", true);

    // Setup the periodic packet polling
    setInterval(function() {
        query_control_backend({}, 'POST', '/control_rx', "application/json; charset=utf-8", "json", true);
    }, 10000);

    // Setup the datetimepicker
    datepicker = $('#datetimepicker1').datetimepicker({
        format: 'DD-MM-YYYY HH:mm:ss',
    });
}
