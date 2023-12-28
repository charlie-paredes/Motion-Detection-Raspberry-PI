Raspberry Pi Motion Detection System
Carlos Paredes

The system should work with just a Raspberry Pi and a USB webcam. Any Webcam should work, and I used a
Raspberry Pi 4 but a Pi 3 should work too. Some installs are necessary to use the program successfully.
These being:
Numpy for motion detection logic:
pip install numpy

Fswebcam for video capture:
sudo apt-get install fswebcam

FFMPEG for video capture:
sudo apt-get install ffmpeg

Python:
sudo apt-get install python3

Whoever wants to build this program themselves should also create an app password in their gmail account,
the default password will not work. This project was created with the sender being a gmail account,
and some of the email syntax is gmail-specific.

After the necessary installs are done and the .py file is on a functional Raspberry Pi and a webcam is
plugged in, all you need to do is run the program. The system will begin the ffmpeg subprocess and
capture video frames, and will compare them using Numpy to see if they are different enough to warrant a
motion detection event. If motion is detected, the ffmpeg process will be killed a second video subprocess
will be started which lasts 10 seconds. After the video is captured, it will be sent via email using the 
Gmail server. Then, the first video capture process will resume and continue to detect motion.

Some important notes:
- it is very important the subprocesses are killed before the next subprocess starts. This is because
the system is not able to run the video capture subprocess and image capture subprocess at the same time.
- By restarting the video capture subprocess after an image is captured, we ensure continuous motion
detection. The program continues to run the video capture subprocess after each time it captures an image,
and the Numpy logic continues to analyze video frames and capture and images to the user if motion
is detected.
- The email will be sent regardless if the reciever is on the same network. They can be at work, on vacation,
or wherever, and they will still get appropriate email updates.
