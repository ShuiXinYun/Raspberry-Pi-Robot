
+ Stream Video from the Raspberry Pi Camera to Web Browsers(MJPEG)
  [https://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android]

+ Capture an image in jpeg format:
  `raspistill -o image.jpg`

+ Capture a 5s video in h264 format:
`raspivid -o video.h264`

+ Capture a 10s video:
`raspivid -o video.h264 -t 10000`

+ Capture a 10s video in demo mode:
`raspivid -o video.h264 -t 10000 -d`

+ To see a list of possible options for running raspivid or raspistill, you can run:
`raspivid | less`
`raspistill | less`

