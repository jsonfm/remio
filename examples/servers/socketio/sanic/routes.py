"""Routes for the socketio communication."""
EXPERIMENT_STREAMS_VIDEO_SERVER = "EXPERIMENT_STREAMS_VIDEO_SERVER"
EXPERIMENT_SENDS_DATA_SERVER = "EXPERIMENT_SEND_DATA_SERVER"
EXPERIMENT_NOTIFIES_DATA_WERE_RECEIVED_SERVER = (
    "EXPERIMENT_NOTIFIES_DATA_WERE_RECEIVED_SERVER"
)
EXPERIMENT_JOINS_ROOM_SERVER = "EXPERIMENT_JOINS_ROOM_SERVER"
EXPERIMENT_EMITS_EVENT_SERVER = "EXPERIMENT_EMITS_EVENT_SERVER"
EXPERIMENT_IS_STREAMING_SERVER = "EXPERIMENT_IS_STREAMING"
EXPERIMENT_STREAMER_SET_PAUSE_SERVER = "EXPERIMENT_STREAMER_SET_PAUSE_SERVER"


SERVER_STREAMS_VIDEO_WEB = "SERVER_STREAMS_VIDEO_WEB"
SERVER_SENDS_DATA_EXPERIMENT = "SERVER_SENDS_DATA_EXPERIMENT"
SERVER_SENDS_DATA_WEB = "SERVER_SENDS_DATA_WEB"
SERVER_REQUESTS_DATA_EXPERIMENT = "SERVER_REQUESTS_DATA_EXPERIMENT"
SERVER_NOTIFIES_DATA_WERE_RECEIVED_WEB = "SERVER_NOTIFIES_DATA_WERE_RECEIVED_WEB"
SERVER_NOTIFIES_DATA_WERE_RECEIVED_EXPERIMENT = (
    "SERVER_NOTIFIES_DATA_WERE_RECEIVED_EXPERIMENT"
)
SERVER_EMITS_EVENT_WEB = "SERVER_EMITS_EVENT_WEB"
SERVER_STREAMER_SET_PAUSE_EXPERIMENT = "SERVER_STREAMER_SET_PAUSE_EXPERIMENT"

WEB_JOINS_ROOM_SERVER = "WEB_JOINS_ROOM_SERVER"
WEB_REQUESTS_ROOM_SERVER = "WEB_REQUESTS_ROOM_SERVER"
WEB_SENDS_DATA_SERVER = "WEB_SENDS_DATA_SERVER"
WEB_NOTIFIES_DATA_WERE_RECEIVED_SERVER = "WEB_NOTIFIES_DATA_WERE_RECEIVED_SERVER"
WEB_EMITS_EVENT_SERVER = "WEB_EMITS_EVENT_SERVER"
