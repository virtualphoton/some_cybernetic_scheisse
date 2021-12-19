# some cybernetic fun

The most important part of this project is
the server, which purposes are to establish communication between the user and some 
device (such as a robot or, in this case, smartwatches) and to stream video of the
operating device; this allows user to comfortably control the device and get feedback.
The user communicates with the server via web interface. The server
communicates with device wrapper via socket; this wrapper then sends commands (or 
receives data) to the device (e.g., using API).

Video can be obtained either from a usb cam, or from the smartphone app called
'IP Webcam' (but only the latter is implemented).

Required packages are in requirements.txt (`pip install -r requirements.txt` to install
them)

To launch the server:
1) download 'IP webcam' on your smartphone
   
2) launch the 'IP webcam' app, scroll down and press 'Start server'
   
3) run `server/app.py` and type url shown by 'IP webcam' (where it streams video)

Device used here is 'LILYGO TTGO T-Watch-2020' with code `machines/watches/watches/watches.ino`

Device wrapper for it is started via running `machines/watches/main.py`, but it wouldn't work without the watches.
[Video](https://www.youtube.com/watch?v=EGJngwPtWNg) of how this works