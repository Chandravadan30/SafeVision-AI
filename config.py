CAMERA_INDEX       = 0
FRAME_WIDTH        = 640
FRAME_HEIGHT       = 480
FPS_TARGET         = 30

FALL_ANGLE_THRESH  = 45       # degrees from vertical
FALL_FRAME_WINDOW  = 5       # consecutive frames to confirm
VELOCITY_THRESH    = 0.08     # optional vertical velocity guard
HEADLESS           = True   # set False only if monitor is connected to Jetson
MODEL_PATH         = "yolov8n-pose.pt"
CONF_THRESHOLD     = 0.4
INFERENCE_EVERY_N  = 2

SNAPSHOT_DIR       = "snapshots"
DB_PATH            = "data/events.db"

# Alert settings — fill in your own credentials
ALERT_EMAIL_FROM   = "sobilachandravadan@gmail.com"
ALERT_EMAIL_TO     = "sobilachandravadan@gmail.com"
SENDGRID_API_KEY   = "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"
TWILIO_SID         = "AC6e99572e91f0a125c64bc27d73ad36e9"
TWILIO_TOKEN       = "a752de4f129db807fa78e84496a6d276"
TWILIO_FROM        = "+19867861438"
TWILIO_TO          = "+16674316450"

DASHBOARD_HOST     = "0.0.0.0"
DASHBOARD_PORT     = 5000

