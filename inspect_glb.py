import json, struct

with open('output (1).glb', 'rb') as f:
    f.read(12)
    json_len = struct.unpack('<I', f.read(4))[0]
    f.read(4)
    json_data = f.read(json_len)
    data = json.loads(json_data.decode('utf-8'))

meshes = data.get('meshes', [])
materials = data.get('materials', [])

# Print material for meshes 0, 1, 2, 4
for i in [0, 1, 2, 4]:
    if i < len(meshes):
        mat_idx = meshes[i].get('primitives', [{}])[0].get('material')
        if mat_idx is not None:
            mat_name = materials[mat_idx].get('name')
            print(f"mesh {i} uses material index {mat_idx} ({mat_name})")
        else:
            print(f"mesh {i} has no material")
