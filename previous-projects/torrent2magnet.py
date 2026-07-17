import bencode
torrent =open('C:\Users\Nikhil\Downloads\Stanford-CS106a-Programming-Methodology.torrent', 'r').read()
metadata=bencode.bdecode(torrent)
hashcontents=bencode.bencode(metadata['info'])
import hashlib
digest=hashlib.sha1(hashcontents).digest()
import base64
b32hash=base64.b32encode(digest)
b32hash