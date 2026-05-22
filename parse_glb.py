import json
import struct

path = 'output (1).glb'
with open(path, 'rb') as f:
    header = f.read(12)
    magic, version, length = struct.unpack('<4sII', header)
    print('magic', magic, 'version', version, 'length', length)
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
    print('chunk', typ, len(data))
    if typ == b'JSON':
        gltf = json.loads(data.decode('utf-8'))
        print('scenes', len(gltf.get('scenes', [])), 'nodes', len(gltf.get('nodes', [])), 'meshes', len(gltf.get('meshes', [])), 'materials', len(gltf.get('materials', [])))
        for idx, mat in enumerate(gltf.get('materials', [])):
            print('--- material', idx, mat.get('name'))
            for key, value in mat.items():
                if key == 'pbrMetallicRoughness':
                    pbr = value
                    print('   pbrMetallicRoughness keys:', list(pbr.keys()))
                    print('    baseColorFactor:', pbr.get('baseColorFactor'))
                    print('    baseColorTexture:', pbr.get('baseColorTexture'))
                elif key in ('name', 'alphaMode', 'doubleSided', 'extensions', 'extras'):
                    print('   {}: {}'.format(key, value))
                else:
                    print('   {}: {}'.format(key, type(value)))
        for idx, mesh in enumerate(gltf.get('meshes', [])):
            print('mesh', idx, mesh.get('name'))
            for prim_idx, prim in enumerate(mesh.get('primitives', [])):
                print('  prim', prim_idx, 'material', prim.get('material'), 'mode', prim.get('mode'), 'attributes', list(prim.get('attributes', {}).keys()))
        for idx, node in enumerate(gltf.get('nodes', [])):
            print('node', idx, node.get('name'), 'mesh', node.get('mesh'), 'children', node.get('children'))
        print('textures', len(gltf.get('textures', [])))
        for idx, tex in enumerate(gltf.get('textures', [])):
            print('texture', idx, tex)
        print('images', len(gltf.get('images', [])))
        for idx, img in enumerate(gltf.get('images', [])):
            print('image', idx, img)