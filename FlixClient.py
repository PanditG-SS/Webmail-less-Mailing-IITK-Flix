from socket import *
import pickle
import struct
import cv2
import imutils  # Import imutils for resizing

servername = 'localhost'
serverPort = 12000

# We create a socket for the client using TCP
clientsocket = socket(AF_INET, SOCK_STREAM)

# Now we do a 3 Way Handshake
clientsocket.connect((servername, serverPort))

# Open the receiving window
cv2.namedWindow("Receiving")

while True:
    try:
        # Receive the frame size as a packed struct
        frame_size_data = clientsocket.recv(struct.calcsize("!L"))
        if not frame_size_data:
            break
        frame_size = struct.unpack("!L", frame_size_data)[0]

        # Receive the serialized frame data
        frame_data = b""
        while len(frame_data) < frame_size:
            packet = clientsocket.recv(frame_size - len(frame_data))
            if not packet:
                break
            frame_data += packet

        # Deserialize the frame
        frame = pickle.loads(frame_data)

        # Resize the received frame to a smaller size (e.g., width=500)
        frame = imutils.resize(frame, width=500)

        # Display the received frame
        cv2.imshow("Receiving", frame)

        # Check for the 'q' key press to exit the receiving window
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    except Exception as e:
        print(f"Error: {str(e)}")
        break

# Clean up and close the OpenCV window
cv2.destroyWindow("Receiving")
clientsocket.close()
