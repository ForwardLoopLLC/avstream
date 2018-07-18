docker run \
    --privileged \
    -i -t --rm \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /dev/video0:/dev/video0 \
    -v /home/nick/src/floop/drivers/avstream:/vlc/ \
    -e DISPLAY=$DISPLAY \
    live-camera_vlc \
    /vlc/run.sh
