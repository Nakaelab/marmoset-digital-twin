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
        
        print("=" * 60)
        print("MATERIALS LIST")
        print("=" * 60)
        for idx, mat in enumerate(gltf.get('materials', [])):
            pbr = mat.get('pbrMetallicRoughness', {})
            base_color = pbr.get('baseColorFactor', 'N/A')
            base_tex = pbr.get('baseColorTexture', 'N/A')
            alpha = mat.get('alphaMode', 'OPAQUE')
            print(f"  material[{idx}] name={mat.get('name')!r}  alphaMode={alpha}  baseColorFactor={base_color}  baseColorTexture={base_tex}")
        
        print()
        print("=" * 60)
        print("MESH -> MATERIAL MAPPING")
        print("=" * 60)
        materials = gltf.get('materials', [])
        for idx, mesh in enumerate(gltf.get('meshes', [])):
            print(f"  mesh[{idx}] name={mesh.get('name')!r}")
            for prim_idx, prim in enumerate(mesh.get('primitives', [])):
                mat_idx = prim.get('material')
                mat_name = materials[mat_idx].get('name') if mat_idx is not None and mat_idx < len(materials) else '???'
                print(f"    prim[{prim_idx}] -> material[{mat_idx}] = {mat_name!r}")
        
        print()
        print("=" * 60)
        print("NODE -> MESH MAPPING (only nodes with mesh)")
        print("=" * 60)
        meshes = gltf.get('meshes', [])
        for idx, node in enumerate(gltf.get('nodes', [])):
            mesh_idx = node.get('mesh')
            if mesh_idx is not None:
                mesh_name = meshes[mesh_idx].get('name') if mesh_idx < len(meshes) else '???'
                # Find which materials this mesh uses
                mesh_data = meshes[mesh_idx] if mesh_idx < len(meshes) else {}
                mat_names = []
                for prim in mesh_data.get('primitives', []):
                    mi = prim.get('material')
                    if mi is not None and mi < len(materials):
                        mat_names.append(f"{materials[mi].get('name')}[{mi}]")
                print(f"  node[{idx}] name={node.get('name')!r}  -> mesh[{mesh_idx}] name={mesh_name!r}  materials=[{', '.join(mat_names)}]")
        
        print()
        print("=" * 60)
        print("WHICH NODES USE PaletteMaterial001?")
        print("=" * 60)
        for idx, node in enumerate(gltf.get('nodes', [])):
            mesh_idx = node.get('mesh')
            if mesh_idx is not None and mesh_idx < len(meshes):
                mesh_data = meshes[mesh_idx]
                for prim in mesh_data.get('primitives', []):
                    mi = prim.get('material')
                    if mi is not None and mi < len(materials):
                        if materials[mi].get('name') == 'PaletteMaterial001':
                            print(f"  node[{idx}] name={node.get('name')!r}  mesh[{mesh_idx}] name={mesh_data.get('name')!r}")
                            break

        # Also check: what color does PaletteMaterial001 have?
        print()
        print("=" * 60)
        print("PaletteMaterial001 DETAIL")
        print("=" * 60)
        for idx, mat in enumerate(gltf.get('materials', [])):
            if mat.get('name') == 'PaletteMaterial001':
                print(json.dumps(mat, indent=2))
