TC_TM_SEQ_SPACKET  = 0x03
ECSS_VER_NUMBER = 0
ECSS_DATA_FIELD_HDR_FLG = 1
TC = 1
TM = 0
ECSS_HEADER_SIZE = 6
ECSS_DATA_HEADER_SIZE = 4
ECSS_CRC_SIZE = 2
ECSS_DATA_OFFSET = ECSS_HEADER_SIZE + ECSS_DATA_HEADER_SIZE
MIN_PKT_SIZE = 5
MAX_PKT_SIZE = 1024
ECSS_PUS_VER = 1
ECSS_SEC_HDR_FIELD_FLG = 0
SATR_PKT_ILLEGAL_APPID     = 0
SATR_PKT_INV_LEN           = 1
SATR_PKT_INC_CRC           = 2
SATR_PKT_ILLEGAL_PKT_TP    = 3
SATR_PKT_ILLEGAL_PKT_STP   = 4
SATR_PKT_ILLEGAL_APP_DATA  = 5
SATR_OK                    = 6
SATR_ERROR                 = 7
SATR_EOT                   = 8
SATR_CRC_ERROR             = 9
SATR_PKT_ILLEGAL_ACK       = 10
SATR_ALREADY_SERVICING     = 11
SATR_MS_MAX_FILES          = 12
SATR_PKT_INIT              = 13
SATR_INV_STORE_ID          = 14
SATR_INV_DATA_LEN          = 15
SATR_LAST                  = 16

OBC_APP_ID      = 1
EPS_APP_ID      = 2
ADCS_APP_ID     = 3
COMMS_APP_ID    = 4
IAC_APP_ID      = 5
GND_APP_ID      = 6
DBG_APP_ID      = 7
LAST_APP_ID     = 8
SERVICES_VERIFICATION_TC_TM = [
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [1, 0], [1, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ], #TC_VERIFICATION_SERVICE
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [0, 0], [1, 0], [0, 0], [0, 0] ], #TC_HOUSEKEEPING_SERVICE
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [1, 0], [0, 0], [0, 0], [1, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ], #TC_EVENT_SERVICE
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ], #TC_FUNCTION_MANAGEMENT_SERVICE
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 0], [0, 1], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ], #TC_SCHEDULING_SERVICE
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [1, 0], [1, 0], [1, 0], [1, 0], [0, 1], [0, 1], [1, 0], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1], [1, 0], [1, 0], [1, 0], [1, 0], [0, 1], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ], #TC_LARGE_DATA_SERVICE
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [1, 0], [1, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 1], [0, 0], [0, 1], [0, 1], [1, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ], #TC_MASS_STORAGE_SERVICE
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [0, 1], [1, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ], #TC_TEST_SERVICE
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ],
    [ [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0] ]
]

TC_ACK_NO        =   0x00
TC_ACK_ACC       =   0x01
TC_ACK_EXE_START =   0x02
TC_ACK_EXE_PROG  =   0x04
TC_ACK_EXE_COMP  =   0x08
TC_ACK_ALL       =   0x0F

FRAME_RECEIVER_IP = '127.0.0.1'
FRAME_RECEIVER_PORT = 16886

#SAT_RETURN_STATE

SATR_PKT_ILLEGAL_APPID     = 0
SATR_PKT_INV_LEN           = 1
SATR_PKT_INC_CRC           = 2
SATR_PKT_ILLEGAL_PKT_TP    = 3
SATR_PKT_ILLEGAL_PKT_STP   = 4
SATR_PKT_ILLEGAL_APP_DATA  = 5
SATR_OK                    = 6
SATR_ERROR                 = 7
SATR_EOT                   = 8
SATR_CRC_ERROR             = 9
SATR_PKT_ILLEGAL_ACK       = 10
SATR_ALREADY_SERVICING     = 11
SATR_MS_MAX_FILES          = 12
SATR_PKT_INIT              = 13
SATR_INV_STORE_ID          = 14
SATR_INV_DATA_LEN          = 15
SATR_SCHEDULE_FULL         = 17 # Schedule array is full */
SATR_SSCH_ID_INVALID       = 18 # Subschedule ID invalid */
SATR_NMR_OF_TC_INVALID     = 19 # Number of telecommands invalid */
SATR_INTRL_ID_INVALID      = 20 # Interlock ID invalid */
SATR_ASS_INTRL_ID_INVALID  = 21 # Assess Interlock ID invalid */
SATR_ASS_TYPE_ID_INVALID   = 22 # Assesment type id invalid*/        
SATR_RLS_TIMET_ID_INVALID  = 23 # Relese time type ID invalid */
SATR_DEST_APID_INVALID     = 24 # Destination APID in embedded TC is invalid */
SATR_TIME_INVALID          = 25 # Release time of TC is invalid */
SATR_TIME_SPEC_INVALID     = 26 #  Release time of TC is specified in a invalid representation*/
SATR_INTRL_LOGIC_ERROR     = 27 # The release time of telecommand is in the execution window of its interlocking telecommand.*/
SATR_SCHEDULE_DISABLED     = 28
SATRF_OK                   = 29 # (0) Succeeded */
SATRF_DISK_ERR             = 30 # (1) A hard error occurred in the low level disk I/O layer */
SATRF_INT_ERR              = 31 # (2) Assertion failed */
SATRF_NOT_READY            = 32 # (3) The physical drive cannot work */
SATRF_NO_FILE              = 33 # (4) Could not find the file */
SATRF_NO_PATH              = 34 # (5) Could not find the path */
SATRF_INVALID_NAME         = 35 # (6) The path name format is invalid */
SATRF_DENIED               = 36 # (7) Access denied due to prohibited access or directory full */
SATRF_EXIST                = 37 # (8) Access denied due to prohibited access */
SATRF_INVALID_OBJECT       = 38 # (9) The file/directory object is invalid */
SATRF_WRITE_PROTECTED      = 39 # (10) The physical drive is write protected */
SATRF_INVALID_DRIVE        = 40 # (11) The logical drive number is invalid */
SATRF_NOT_ENABLED          = 41 # (12) The volume has no work area */
SATRF_NO_FILESYSTEM        = 42 # (13) There is no valid FAT volume */
SATRF_MKFS_ABORTED         = 43 # (14) The f_mkfs() aborted due to any parameter error */
SATRF_TIMEOUT              = 44 # (15) Could not get a grant to access the volume within defined period */
SATRF_LOCKED               = 45 # (16) The operation is rejected according to the file sharing policy */
SATRF_NOT_ENOUGH_CORE      = 46 # (17) LFN working buffer could not be allocated */
SATRF_TOO_MANY_OPEN_FILES  = 47 # (18) Number of open files > _FS_SHARE */
SATRF_INVALID_PARAMETER    = 48 # (19) Given parameter is invalid */    
SATRF_DIR_ERROR            = 49
SATR_LAST                  = 50


