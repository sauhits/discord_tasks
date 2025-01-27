import hmac, base64, struct, hashlib, time, os
from dotenv import load_dotenv

load_dotenv()

def get_hotp_token(secret: str, intervals_no: int) -> str:
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return str(h)

def get_totp_token(secret):
    x = get_hotp_token(secret=secret, intervals_no=int(time.time())//30)
    while len(x)!=6:
        x+='0'
    return x