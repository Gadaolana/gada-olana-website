import socket, cv2, pickle, struct, threading
import pyaudio

def video_stream(client_socket):
    vid = cv2.VideoCapture(0)
    while vid.isOpened():
        ret, frame = vid.read()
        data = pickle.dumps(frame)
        message = struct.pack("Q", len(data)) + data
        client_socket.sendall(message)
        cv2.imshow('Video from Server', frame)
        if cv2.waitKey(10) == 13:
            break
    client_socket.close()

def audio_stream(client_socket):
    chunk = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=chunk)
    while True:
        data = stream.read(chunk)
        client_socket.sendall(data)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = socket.gethostbyname(socket.gethostname())
    server_socket.bind((host_ip, 9999))
    server_socket.listen(5)
    print("Listening at:", (host_ip, 9999))

    while True:
        client_socket, addr = server_socket.accept()
        print('Connected to:', addr)
        threading.Thread(target=video_stream, args=(client_socket,)).start()
        threading.Thread(target=audio_stream, args=(client_socket,)).start()

start_server()

