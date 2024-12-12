"""
Protocol:
CLIENT: 
- pause
- start <seconds> : Starts lights at time X with the light data previously uploaded. Seconds has max 3 decimal places. 
Uploading is done in 2 parts. A 'upload' message to give time for the server the delete the previous light data, which is responded by ok when ready, and then the file. 
- upload num_lines: Uploads a file of light data. This should be used for all f. To save space, the previous light data may be deleted. 

SERVER:
Responds with 'ok' or 'er'
"""

"""
Light Data File format

SYNTAX
This is using Extended Backus Naur Form. All plain text is quoted with single quotes. A space does not mean theres actually a space unless its quoted!

<FILE>      = <line>*
<line>      = \\d+ '.' \\d{0,3} ' ' <rgb> ' ' <rgb> ' ' <rgb>
<rgb>       = 0..255

BODY DESCRIPTION:
Each line of the body contains a timestamp in seconds, rounded to maximum 3 decimal places, and 3 values from 0-255 representing RGB values.
"""

# Communication constants to be used by client and server
PAUSE = "pause"
START = "start"
UPLOAD = "upload"
DONE = "done"
OK = "ok"
ERR = "er"

MIN_DIFF = 0.05 # Min difference between color time steps
SIG_FIGS = 100 # How much to multiply by to make above 1
DECIMAL_PLACES = 2

class InvalidFormatError(RuntimeError):
    ...

def decode_file(p: str):
    from pprint import pprint
    t: dict[float, tuple[int, int, int]] = {}
    with open(p, "rb") as f:
        b: bytes = f.read()
        r = 0
        while r < len(b):
            timestamp = int.from_bytes([b[r], b[r+1]], "big") / SIG_FIGS
            t[timestamp] = (b[r+2], b[r+3], b[r+4])
            r+=5
    pprint(t)

if __name__ == '__main__':
    decode_file("./client/songs/DISCO LINES - BABY GIRL [Lxu_9m23qHg].mp3.color")