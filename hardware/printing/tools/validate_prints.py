"""Validate local source hashes, STL/3MF exports and layout; requires NumPy."""
from pathlib import Path
import hashlib
import json
import struct
import zipfile
import xml.etree.ElementTree as ET
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'prepared'
NS = {'m': 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}


def stl(path):
    data = path.read_bytes()
    count = struct.unpack_from('<I', data, 80)[0]
    assert len(data) == 84 + 50 * count, path
    dtype = np.dtype([('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
    return np.frombuffer(data, dtype=dtype, offset=84)['v'].astype(float)


manifest = json.loads((ROOT / 'source-manifest.json').read_text())
assert len(manifest['files']) == 11
for entry in manifest['files']:
    data = (ROOT / entry['file']).read_bytes()
    assert hashlib.sha256(data).hexdigest() == entry['sha256']
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == entry['git_blob_sha']

report = json.loads((OUT / 'validation.json').read_text())
assert len(report['parts']) == 11
for part in report['parts']:
    name = part['name']
    src = stl(ROOT / 'original' / (name + '.stl'))
    prepared = stl(OUT / (name + '-print.stl'))
    assert len(src) == part['source_triangles']
    assert len(prepared) == part['triangles']
    assert len(src) - len(prepared) == part['redundant_facets_removed']
    assert part['boundary_edges'] == part['nonmanifold_edges'] == 0
    rotation = np.array(part['rotation'])
    assert np.allclose(rotation.T @ rotation, np.eye(3))
    assert np.isclose(np.linalg.det(rotation), 1)
    assert np.allclose(prepared.min(axis=(0, 1)), 0, atol=2e-5)
    assert np.allclose(np.ptp(prepared, axis=(0, 1)), part['dimensions_mm'], atol=2e-5)
    # Rigid transforms preserve absolute enclosed volume; zero-volume fins do not contribute.
    def volume(t):
        return abs(np.einsum('ij,ij->i', t[:, 0], np.cross(t[:, 1], t[:, 2])).sum() / 6)
    assert np.isclose(volume(src), volume(prepared), rtol=2e-5, atol=.01), name

for name, count in [('P1S-all-11', 11), ('P1S-base-10', 10), ('P1S-cover-1', 1)]:
    with zipfile.ZipFile(OUT / (name + '.3mf')) as archive:
        assert archive.testzip() is None
        model = ET.fromstring(archive.read('3D/3dmodel.model'))
        assert model.attrib['unit'] == 'millimeter'
        objects = model.findall('m:resources/m:object', NS)
        assert len(objects) == count
        assert len(model.findall('m:build/m:item', NS)) == count
        bounds = []
        triangle_count = 0
        for ob in objects:
            vertices = np.array([[float(v.attrib[a]) for a in ('x', 'y', 'z')]
                                 for v in ob.findall('m:mesh/m:vertices/m:vertex', NS)])
            faces = np.array([[int(t.attrib[a]) for a in ('v1', 'v2', 'v3')]
                              for t in ob.findall('m:mesh/m:triangles/m:triangle', NS)])
            assert faces.min() >= 0 and faces.max() < len(vertices)
            assert np.all(np.isfinite(vertices))
            lo, hi = vertices.min(axis=0), vertices.max(axis=0)
            assert abs(lo[2]) < 1e-6
            assert np.all(lo[:2] >= 10) and np.all(hi[:2] <= 246)
            edges = np.sort(np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]]), axis=1)
            _, edge_counts = np.unique(edges, axis=0, return_counts=True)
            assert np.all(edge_counts == 2), ob.attrib['name']
            triangle_count += len(faces)
            bounds.append((lo, hi))
        assert len(stl(OUT / (name + '.stl'))) == triangle_count
        for i, (alo, ahi) in enumerate(bounds):
            for blo, bhi in bounds[i+1:]:
                delta = np.maximum(np.maximum(alo[:2]-bhi[:2], blo[:2]-ahi[:2]), 0)
                assert np.linalg.norm(delta) >= 8

assert (OUT / 'Sesame-P1S-print-layout.blend').is_file()
print('PASS: 11 source hashes, rigid dimensions/volumes, closed meshes, 3 STL/3MF layouts, bed margins and spacing.')
