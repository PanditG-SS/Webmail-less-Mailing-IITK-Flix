from socket import *
import cv2
import pickle
import struct
import imutils  # Import imutils for resizing

serverPort = 12000

# Use TCP
serversocket = socket(AF_INET, SOCK_STREAM)
serversocket.bind(('localhost', serverPort))
# The welcoming socket should be open to receive requests from any client.
serversocket.listen(1)
print("The server is ready to receive")

# Open the streaming window
cv2.namedWindow("Streaming")

while True:
    connectionsocket, clientaddress = serversocket.accept()
    print('GOT CONNECTION FROM:', clientaddress)

    video = cv2.VideoCapture(0)

    while True:
        ret, frame = video.read()

        if not ret:
            break

        # Resize the frame to a smaller size (e.g., width=500)
        frame = imutils.resize(frame, width=500)

        # Display the streaming video
        cv2.imshow("Streaming", frame)

        # Serialize the frame using pickle
        serialdata = pickle.dumps(frame)

        # Send the frame size as a struct.pack to help the client know when the frame ends
        frame_size = struct.pack("!L", len(serialdata))
        connectionsocket.sendall(frame_size)

        # Send the serialized frame data
        connectionsocket.sendall(serialdata)

        # Check for the 'q' key press to exit the streaming window
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    video.release()
    connectionsocket.close()

# Close the streaming window when the server exits
cv2.destroyWindow("Streaming")
