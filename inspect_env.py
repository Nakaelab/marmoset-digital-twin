import json
import struct

path = 'output (1).glb'
with open(path, 'rb') as f:
    header = f.read(12)
    magic, version, length = struct.unpack('<4sII', header)
    rest = f.read()
    i = 0
    gltf = None
    while i < len(rest):
        chunk_len, chunk_type = struct.unpack('<I4s', rest[i:i+8])
        i += 8
        chunk_data = rest[i:i+chunk_len]
        i += chunk_len
        if chunk_type == b'JSON':
            gltf = json.loads(chunk_data.decode('utf-8'))
            break

for idx, node in enumerate(gltf.get('nodes', [])):
    name = node.get('name', '')
    if 'Cube' in name or 'Cylinder' in name:
        print(idx, name, 'mesh', node.get('mesh'), 'translation', node.get('translation'), 'rotation', node.get('rotation'), 'scale', node.get('scale'))
