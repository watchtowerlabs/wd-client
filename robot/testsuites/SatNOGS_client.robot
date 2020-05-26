*** Settings ***
Test Setup        Initialize Server And Client
Test Teardown     Terminate Client And Server
Test Timeout      30
Library           OperatingSystem
Library           Process
Library           DateTime
Library           String
Library           HttpCtrl.Server
Library           ${LIBRARY_PATH}Orbital.py

*** Variables ***
${LIBRARY_PATH}    libraries/
${SATNOGS_API_TOKEN}    1234567890
${SATNOGS_NETWORK_API_URL}    http://127.0.0.1:52342/
${SATNOGS_STATION_ID}    123
${SATNOGS_STATION_LAT}    10.0
${SATNOGS_STATION_LON}    20.0
${SATNOGS_STATION_ELEV}    123
${SATNOGS_SOAPY_RX_DEVICE}    driver=rtlsdr
${SATNOGS_RX_SAMP_RATE}    2.048e6
${SATNOGS_ANTENNA}    RX
${SATNOGS_LOG_LEVEL}    DEBUG
${SATNOGS_NETWORK_API_QUERY_INTERVAL}    10
${SATNOGS_NETWORK_API_POST_INTERVAL}    10

*** Test Cases ***
No Crash At Startup
    ${Result} =    Wait For Process    handle=satnogsclient    timeout=10 seconds    on_timeout=terminate
    Wait Until Keyword Succeeds    10 seconds    1 second    Process Should Be Stopped
    Should Be Equal As Integers    ${Result.rc}    -15

Request For Jobs Returning No Scheduled Jobs
    Request For Jobs
    Reply By    200    []

Post Observation Data
    Request For Jobs
    ${start} =    Get Current Date    time_zone=UTC    increment=5 seconds    result_format=%Y-%m-%dT%H:%M:%SZ
    ${end} =    Get Current Date    time_zone=UTC    increment=15 seconds    result_format=%Y-%m-%dT%H:%M:%SZ
    ${tle_date} =    Get Current Date    time_zone=UTC    increment=10 seconds    result_format=datetime
    @{tle} =    Generate Fake Tle    ${SATNOGS_STATION_LAT}    ${SATNOGS_STATION_LON}    ${SATNOGS_STATION_ELEV}    ${tle_date}
    ${transmitter} =    Generate Random String    length=22
    ${response} =    Catenate
    ...    \[
    ...    {
    ...    "id" : 1,
    ...    "ground_station": ${SATNOGS_STATION_ID},
    ...    "start" : "${start}",
    ...    "end" : "${end}",
    ...    "transmitter" : "${transmitter}",
    ...    "frequency" : 435791000,
    ...    "tle0" : "${tle}[0]",
    ...    "tle1" : "${tle}[1]",
    ...    "tle2" : "${tle}[2]",
    ...    "mode" : "CW",
    ...    "baud" : 15
    ...    }
    ...    \]
    Reply By    200    ${response}
    Wait For Post Data

*** Keywords ***
Start SatNOGS Client
    Set Environment Variable    SATNOGS_API_TOKEN    ${SATNOGS_API_TOKEN}
    Set Environment Variable    SATNOGS_NETWORK_API_URL    ${SATNOGS_NETWORK_API_URL}
    Set Environment Variable    SATNOGS_STATION_ID    ${SATNOGS_STATION_ID}
    Set Environment Variable    SATNOGS_STATION_LAT    ${SATNOGS_STATION_LAT}
    Set Environment Variable    SATNOGS_STATION_LON    ${SATNOGS_STATION_LON}
    Set Environment Variable    SATNOGS_STATION_ELEV    ${SATNOGS_STATION_ELEV}
    Set Environment Variable    SATNOGS_SOAPY_RX_DEVICE    ${SATNOGS_SOAPY_RX_DEVICE}
    Set Environment Variable    SATNOGS_RX_SAMP_RATE    ${SATNOGS_RX_SAMP_RATE}
    Set Environment Variable    SATNOGS_ANTENNA    ${SATNOGS_ANTENNA}
    Set Environment Variable    SATNOGS_LOG_LEVEL    ${SATNOGS_LOG_LEVEL}
    Set Environment Variable    SATNOGS_NETWORK_API_QUERY_INTERVAL    ${SATNOGS_NETWORK_API_QUERY_INTERVAL}
    Start Process    satnogs-client    shell=True    alias=satnogsclient

Initialize Server And Client
    Start Server    127.0.0.1    52342
    Start SatNOGS Client

Terminate Client And Server
    ${result} =    Terminate Process    handle=satnogsclient
    Log Many    stdout: ${result.stdout}    stderr: ${result.stderr}
    Stop Server

Request For Jobs
    [Arguments]    ${timeout}=60
    Wait For Request    timeout=${timeout}
    ${method} =    Get Request Method
    ${url} =    Get Request Url
    ${body} =    Get Request Body
    Run Keyword If    '${method}' == 'PUT'    Reply By    200
    Should Be Equal    ${method}    GET
    Should Be Equal    ${url}    /jobs/?ground_station=${SATNOGS_STATION_ID}&lat=${SATNOGS_STATION_LAT}&lon=${SATNOGS_STATION_LON}&alt=${SATNOGS_STATION_ELEV}
    Should Be Equal    ${body}    ${None}

Post Data
    [Arguments]    ${timeout}=60
    Wait For Request    timeout=${timeout}
    ${method} =    Get Request Method
    ${url} =    Get Request Url
    ${body} =    Get Request Body
    Run Keyword If    '${method}' == 'GET'    Reply By    200    []
    Should Be Equal    ${method}    PUT

Wait For Post Data
    Wait Until Keyword Succeeds    60 seconds    1 second    Post Data
