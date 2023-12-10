import subprocess
import numpy as np
import time
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders

#Email configuration
sender_email = 'charlie.paredes619@gmail.com'
sender_password = 'asca vdxs vsgr txcj'
receiver_email = 'cparedes2696@sdsu.edu'
subject = 'Motion Detected!'
body = 'Motion has been detected in the surveillance area.'

#Initialize reference frame as None
reference_frame = None

#function to capture output video to send to email
def capture_video(output_file):
    subprocess.run(['ffmpeg', '-y', '-t', '10', '-s', '640x480', '-i', '/dev/video1', output_file])


# Motion detection and time parameters
threshold = 150
start_time = time.time()
cooldown_time = 10  # seconds
last_email_time = 0
motion_detected = False
output_file1 = None

if not motion_detected:
    # Start capturing video using 'ffmpeg'
    video_capture_process = subprocess.Popen([
        "ffmpeg",
        "-f", "v4l2",
        "-framerate", "30",
        "-video_size", "640x480",
        "-i", "/dev/video1",
        "-f", "rawvideo",
        "-"
    ], stdout=subprocess.PIPE)

# Continuous motion detection loop
while True:
    # Read a frame from the video capture process
    frame_bytes = video_capture_process.stdout.read(640 * 480 * 3)
    if not frame_bytes:
        break

    # Convert the frame bytes to a NumPy array
    frame = np.frombuffer(frame_bytes, dtype=np.uint8).reshape(480, 640, 3)

    # Convert the frame to grayscale for motion detection
    current_frame = Image.fromarray(frame)
    current_frame = current_frame.convert("L")

    if reference_frame is not None:
		
        # Calculate the absolute difference between the current frame and the reference frame
        frame_diff = np.abs(np.array(current_frame) - np.array(reference_frame))

        # Calculate the mean of the difference frame
        mean_diff = np.mean(frame_diff)

        if mean_diff > threshold and time.time() > (start_time + 5):
            motion_detected = True
            # Motion detected, take action (e.g., save the frame, send a notification)
            print('**************************************************************')
            print("Motion detected!")
            print('**************************************************************')

            # Create an output file if motion is detected
            if output_file1 is None:
                # Send email notification after creating the output file
                if (time.time() is not None) or last_email_time == 0:
                    video_capture_process.kill()
                    
                    video_file = "captured_video.mp4"

                    # Capture video using the function
                    capture_video(video_file)
                    
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587

					#Create Mime object with necessary Info
                    message = MIMEMultipart()
                    message['From'] = sender_email
                    message['To'] = receiver_email
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
					
					#attach captured video to the email generated
                    attachment = open(video_file, "rb")
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload((attachment).read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename= {video_file}")
                    message.attach(part)
                    
                    #Connect to gmail server
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, receiver_email, message.as_string())
                    video_capture_process = subprocess.Popen([
					"ffmpeg",
					"-f", "v4l2",
					"-framerate", "30",
					"-video_size", "640x480",
					"-i", "/dev/video1",
					"-f", "rawvideo",
					"-"
				    ], stdout=subprocess.PIPE)
                    print('*****************************************************')
                    print('Email sent successfully!')
                    print('**************************************************************')
				    
			#capture current time and update last email time
            motion_time = time.time()
            last_email_time = motion_time
            #restart video capture process to keep 
				    

    # Set the current frame as the reference frame for the next iteration
    reference_frame = current_frame.copy()

#Stop capturing video using 'ffmpeg'
video_capture_process.terminate()
print('Video Process Terminated')
