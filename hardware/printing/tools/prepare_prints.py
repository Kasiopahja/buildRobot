"""Run with Blender 4.3+: blender -b --factory-startup --python prepare_prints.py.
STL coordinates are millimetres. Only rigid, determinant +1 transforms are used.
No remeshing, scaling, mirroring or Boolean operations. Exact duplicate
facets are removed in prepared copies only. Opposite coincident facet pairs
(zero-volume fins) are both removed; original STL files stay untouched.
"""
import bpy
import numpy as np
import struct, json, zipfile, math
from pathlib import Path
from xml.etree import ElementTree as ET
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'prepared'
OUT.mkdir(exist_ok=True)
ROT = {
    '+X': np.array([[0,0,1],[0,-1,0],[1,0,0]], dtype=float),
    '-X': np.array([[0,0,1],[0,1,0],[-1,0,0]], dtype=float),
    '-Y': np.array([[1,0,0],[0,0,1],[0,-1,0]], dtype=float),
    '+Y': np.array([[1,0,0],[0,0,-1],[0,1,0]], dtype=float),
}
PLAN = [
 ('Internal-Frame-v121','-Y',12,12),
 ('Bottom-Cover-v121','+Y',105,12),
 ('Top-Cover-Enclosed-v117','+Y',12,94),
 ('L1-v117','+X',105,94), ('R1-v117','+X',168,94),
 ('L2-v117','+X',105,134), ('R2-v117','+X',168,134),
 ('L3-v117','-X',12,150), ('L4-v117','-X',12,181),
 ('R3-v117','-X',12,212), ('R4-v117','-X',85,212),
]

def read_stl(path):
    data = path.read_bytes()
    count = struct.unpack_from('<I', data, 80)[0]
    assert len(data) == 84 + 50*count, path
    records = np.frombuffer(data, dtype=np.dtype([('normal','<f4',(3,)),('vertices','<f4',(3,3)),('attr','<u2')]),offset=84)
    return records['vertices'].astype(np.float64).copy()

def write_stl(path, parts):
    triangles = np.concatenate([p['triangles'] for p in parts])
    records = np.zeros(len(triangles), dtype=np.dtype([('normal','<f4',(3,)),('vertices','<f4',(3,3)),('attr','<u2')]))
    cross = np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0])
    lengths = np.linalg.norm(cross,axis=1)
    records['normal'] = cross / np.maximum(lengths[:,None],1e-30)
    records['vertices'] = triangles
    path.write_bytes(b'Sesame: rigid print orientation; millimetres'.ljust(80,b'\0')+struct.pack('<I',len(records))+records.tobytes())

def indexed(triangles):
    vertices, inverse = np.unique(triangles.reshape(-1,3),axis=0,return_inverse=True)
    return vertices, inverse.reshape(-1,3)

def write_3mf(path, parts):
    ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
    ET.register_namespace('',ns)
    def sub(parent,tag,attrs=None): return ET.SubElement(parent,'{'+ns+'}'+tag,attrs or {})
    root=ET.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'})
    sub(root,'metadata',{'name':'Title'}).text=path.stem
    sub(root,'metadata',{'name':'Application'}).text='Blender 4.3.2 + prepare_prints.py; geometry only, no slicer profile'
    resources=sub(root,'resources'); build=sub(root,'build')
    for i,part in enumerate(parts,1):
        ob=sub(resources,'object',{'id':str(i),'type':'model','name':part['name']})
        mesh=sub(ob,'mesh'); vertices,faces=indexed(part['triangles'])
        vs=sub(mesh,'vertices')
        for v in vertices: sub(vs,'vertex',dict(zip(['x','y','z'],[format(float(x),'.8f') for x in v])))
        ts=sub(mesh,'triangles')
        for face in faces: sub(ts,'triangle',dict(zip(['v1','v2','v3'],map(str,face))))
        sub(build,'item',{'objectid':str(i)})
    content_types=b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>'
    rels=b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',content_types);z.writestr('_rels/.rels',rels)
        z.writestr('3D/3dmodel.model',ET.tostring(root,encoding='utf-8',xml_declaration=True))

parts=[]; reports=[]
for name,up,x,y in PLAN:
    src=read_stl(ROOT/'original'/f'{name}.stl'); source_count=len(src)
    _,source_faces=indexed(src)
    _,groups,counts=np.unique(np.sort(source_faces,axis=1),axis=0,return_inverse=True,return_counts=True)
    keep=[]
    for group in range(len(counts)):
        members=np.flatnonzero(groups==group)
        if len(members)==2:
            tri=src[members]
            normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0])
            if np.allclose(normals[0],-normals[1],atol=1e-8):
                continue  # Remove both sides of an exact zero-volume fin.
        keep.append(members[0])
    src=src[np.sort(keep)]
    r=ROT[up]
    assert np.isclose(np.linalg.det(r),1)
    triangles=src@r.T
    shift=-triangles.min(axis=(0,1)); shift[:2] += [x,y]
    triangles += shift
    # Reversible rigid transform and unchanged edge lengths of retained facets.
    assert np.max(np.abs((triangles-shift)@r-src)) < 1e-9
    assert np.allclose(np.linalg.norm(np.diff(src,axis=1),axis=2),np.linalg.norm(np.diff(triangles,axis=1),axis=2),atol=1e-9)
    part=dict(name=name,triangles=triangles)
    parts.append(part)
    lo=triangles.min(axis=(0,1)); hi=triangles.max(axis=(0,1))
    assert abs(lo[2])<1e-8 and np.all(lo[:2]>=10) and np.all(hi[:2]<=246)
    vertices,faces=indexed(triangles)
    edges=np.sort(np.concatenate([faces[:,[0,1]],faces[:,[1,2]],faces[:,[2,0]]]),axis=1)
    _,counts=np.unique(edges,axis=0,return_counts=True)
    normals=np.cross(triangles[:,1]-triangles[:,0],triangles[:,2]-triangles[:,0]);areas=np.linalg.norm(normals,axis=1)/2
    nz=normals[:,2]/np.maximum(2*areas,1e-30)
    contact=areas[triangles[:,:,2].max(axis=1)<.03].sum()
    overhang=areas[(nz<-.7071)&(triangles[:,:,2].min(axis=1)>.2)].sum()
    assert np.all(counts==2), (name,'mesh is not closed/manifold')
    report=dict(name=name,source_up_axis=up,rotation=r.tolist(),translation_mm=shift.tolist(),bounds_mm=[lo.tolist(),hi.tolist()],dimensions_mm=(hi-lo).tolist(),source_triangles=source_count,redundant_facets_removed=source_count-len(src),triangles=len(triangles),contact_area_mm2=float(contact),downward_area_above_45_deg_mm2=float(overhang),boundary_edges=int((counts==1).sum()),nonmanifold_edges=int((counts>2).sum()))
    reports.append(report)
    single={'name':name,'triangles':triangles-np.array([x,y,0])}
    write_stl(OUT/f'{name}-print.stl',[single])

for i,a in enumerate(reports):
    for b in reports[i+1:]:
        alo,ahi=np.array(a['bounds_mm']); blo,bhi=np.array(b['bounds_mm'])
        delta=np.maximum(np.maximum(alo[:2]-bhi[:2],blo[:2]-ahi[:2]),0)
        assert np.linalg.norm(delta)>=8, (a['name'],b['name'],delta)

groups={
 'P1S-all-11':parts,
 'P1S-base-10':[p for p in parts if not p['name'].startswith('Top-Cover')],
 'P1S-cover-1':[{'name':p['name'],'triangles':p['triangles']+np.array([128-(12+79.2262/2),128-(94+37.38/2),0])} for p in parts if p['name'].startswith('Top-Cover')],
}
for name,group in groups.items():
    write_stl(OUT/f'{name}.stl',group)
    write_3mf(OUT/f'{name}.3mf',group)

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for s in list(bpy.data.scenes):
    if s != bpy.context.scene: bpy.data.scenes.remove(s)
colors=[(.10,.42,.75,1),(.12,.64,.49,1),(.95,.48,.12,1),(.46,.25,.74,1)]
for gi,(groupname,group) in enumerate(groups.items()):
    scene=bpy.context.scene if gi==0 else bpy.data.scenes.new(groupname)
    scene.name=groupname
    scene.unit_settings.system='METRIC'; scene.unit_settings.scale_length=.001; scene.unit_settings.length_unit='MILLIMETERS'
    for i,part in enumerate(group):
        vertices,faces=indexed(part['triangles']); mesh=bpy.data.meshes.new(part['name']);mesh.from_pydata(vertices.tolist(),[],faces.tolist());mesh.update()
        ob=bpy.data.objects.new(part['name'],mesh);scene.collection.objects.link(ob)
        ob['quantity']=1;ob['source_file']=part['name']+'.stl';ob['units']='millimeters'
        mat=bpy.data.materials.new(groupname+part['name']);mat.diffuse_color=colors[i%len(colors)];ob.data.materials.append(mat)
    scene.render.engine='BLENDER_WORKBENCH'
    scene.display.shading.light='STUDIO';scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=True
    scene.display.shading.background_type='WORLD'; scene.world=bpy.data.worlds.new(groupname);scene.world.color=(.88,.88,.88)
    scene.render.resolution_x=1400;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
    camera_data=bpy.data.cameras.new('Preview'); camera=bpy.data.objects.new('Preview',camera_data);scene.collection.objects.link(camera);scene.camera=camera
    camera.location=(360,-380,510);target=Vector((128,128,0));camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();camera_data.type='ORTHO';camera_data.ortho_scale=345
    # Reference bed is a render-only wire outline, not part of any exported STL/3MF.
    curve=bpy.data.curves.new('256mm bed outline','CURVE');curve.dimensions='3D';curve.bevel_depth=.25
    spline=curve.splines.new('POLY');spline.points.add(4)
    for point,co in zip(spline.points,[(0,0,-.3,1),(256,0,-.3,1),(256,256,-.3,1),(0,256,-.3,1),(0,0,-.3,1)]):point.co=co
    bed=bpy.data.objects.new('REFERENCE_ONLY_256mm',curve);scene.collection.objects.link(bed)
    scene.render.filepath=str(OUT/(groupname+'-preview.png'))
    bpy.ops.render.render(write_still=True,scene=scene.name)

bpy.context.window.scene=bpy.data.scenes['P1S-all-11']
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'Sesame-P1S-print-layout.blend'),compress=True)
(OUT/'validation.json').write_text(json.dumps({'blender_version':bpy.app.version_string,'bed_mm':[256,256],'margin_mm':10,'minimum_bbox_gap_mm':8,'geometry_changes':'rigid rotation/translation plus removal of coincident/zero-volume facets; no scale or shape changes','parts':reports},indent=2)+'\n')
print('PREPARED',len(parts),'parts;',len(groups),'plate variants',flush=True)
