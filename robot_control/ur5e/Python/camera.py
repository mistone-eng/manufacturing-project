import cv2
import threading


def find_available_camera(max_devices=5):
    """Scan for available camera index."""
    for i in range(1, max_devices):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            cap.release()
            print(f"Camera found at index {i}")
            return i
        cap.release()
    print("No available camera found.")
    return None


def camera_feed(video_source=None):
    """
    Start a live feed from the Insta360 camera in a non-blocking thread.
    If video_source is None, auto-detect the available camera.
    """
    def stream(index):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        if not cap.isOpened():
            print("Cannot open camera at index", index)
            return

        print(f"Streaming from camera index {index}")
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            cv2.imshow("Insta360 USB Live Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    if video_source is None:
        video_source = find_available_camera()
        if video_source is None:
            return  # No camera found; exit safely

    thread = threading.Thread(target=stream, args=(video_source,))
    thread.daemon = True
    thread.start()
