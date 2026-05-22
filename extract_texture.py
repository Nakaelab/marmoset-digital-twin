import json
import struct

path = 'output (1).glb'
with open(path, 'rb') as f:
    header = f.read(12)
    magic, version, length = struct.unpack('<4sII', header)
    rest = f.read()
    i = 0
    chunks = []
    while i < len(rest):
        chunk_len, chunk_type = struct.unpack('<I4s', rest[i:i+8])
        i += 8
        chunk_data = rest[i:i+chunk_len]
        i += chunk_len
        chunks.append((chunk_type, chunk_data))

for typ, data in chunks:
    if typ == b'JSON':
        gltf = json.loads(data.decode('utf-8'))
        buffer_views = gltf.get('bufferViews', [])
        # Image 5 is PaletteBaseColor
        img_info = gltf.get('images', [])[5]
        bv_idx = img_info['bufferView']
        bv = buffer_views[bv_idx]
        
        # Now find the binary chunk
        for t2, d2 in chunks:
            if t2 == b'BIN\x00':
                offset = bv.get('byteOffset', 0)
                length = bv['byteLength']
                img_data = d2[offset:offset+length]
                with open('extracted_palette.webp', 'wb') as out_f:
                    out_f.write(img_data)
                print("Saved image to extracted_palette.webp")
