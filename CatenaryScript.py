#-----------------------------------------------
#
# DOCUMENT Blender_catenary_animation.blend
# AUTHOR   Arnau del Rio (arnau@mathinrollercoasters.com)
# DATE     04-11-2022
#
#-----------------------------------------------

import bpy
import math

# SHINE
bpy.context.scene.render.engine = 'BLENDER_EEVEE'
bpy.context.scene.eevee.use_bloom = True

# RESET
bpy.data.objects["Icosphere"].select_set(True)
bpy.ops.object.delete(use_global=False)
bpy.data.objects["Camera"].select_set(True)
bpy.ops.object.delete(use_global=False)
bpy.data.objects["Sun"].select_set(True)
bpy.ops.object.delete(use_global=False)
#bpy.data.objects["BezierCurve"].select_set(True)
#bpy.ops.object.delete(use_global=False)

# CAMERA
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 100, 20), rotation=(math.radians(90), 0, math.radians(180)), scale=(1, 1, 1))
bpy.context.object.data.type = 'ORTHO'
bpy.context.object.data.ortho_scale = 60

# LIGHT
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.context.object.data.energy = 2
bpy.context.object.rotation_euler[0] = 0.383972
bpy.context.object.rotation_euler[1] = 1.0821

# SPHERE
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.5, enter_editmode=False, location=(0, 0, 10))
ico_sphere = bpy.data.objects['Icosphere']

# SPHERE COLOR
mat_name = 'EmiMat'
bpy.ops.material.new()
bpy.data.materials[-1].name = mat_name
bpy.data.materials[mat_name].node_tree.nodes.clear()
bpy.data.materials[mat_name].node_tree.nodes.new("ShaderNodeEmission")
bpy.data.materials[mat_name].node_tree.nodes["Emission"].inputs["Color"].default_value = (0, 0, 1, 1)
bpy.data.materials[mat_name].node_tree.nodes["Emission"].inputs["Strength"].default_value = 50
bpy.data.materials[mat_name].node_tree.nodes.new("ShaderNodeOutputMaterial")
links = bpy.data.materials[mat_name].node_tree.links
links.new(
    bpy.data.materials[mat_name].node_tree.nodes["Emission"].outputs[0], 
    bpy.data.materials[mat_name].node_tree.nodes["Material Output"].inputs[0])
bpy.ops.object.material_slot_add()
mat = bpy.data.materials.get(mat_name)
ob = bpy.context.active_object
ob.data.materials[0] = mat

# TRAIL
bpy.ops.object.particle_system_add()
bpy.data.particles["ParticleSettings"].name = "ParticleSettings"
bpy.data.particles["ParticleSettings"].type = 'EMITTER'
bpy.data.particles["ParticleSettings"].frame_end = 800
bpy.data.particles["ParticleSettings"].effector_weights.gravity = 0
bpy.data.particles["ParticleSettings"].effector_weights.all = 0
bpy.data.particles["ParticleSettings"].effector_weights.vortex = 0
bpy.data.particles["ParticleSettings"].effector_weights.force = 0
bpy.data.particles["ParticleSettings"].effector_weights.vortex = 0
bpy.data.particles["ParticleSettings"].effector_weights.magnetic = 0
bpy.data.particles["ParticleSettings"].effector_weights.harmonic = 0
bpy.data.particles["ParticleSettings"].effector_weights.charge = 0
bpy.data.particles["ParticleSettings"].effector_weights.lennardjones = 0
bpy.data.particles["ParticleSettings"].effector_weights.wind = 0
bpy.data.particles["ParticleSettings"].effector_weights.curve_guide = 0
bpy.data.particles["ParticleSettings"].effector_weights.texture = 0
bpy.data.particles["ParticleSettings"].effector_weights.smokeflow = 0
bpy.data.particles["ParticleSettings"].effector_weights.turbulence = 0
bpy.data.particles["ParticleSettings"].effector_weights.drag = 0
bpy.data.particles["ParticleSettings"].effector_weights.boid = 0
bpy.data.particles["ParticleSettings"].lifetime = 800
bpy.data.particles["ParticleSettings"].normal_factor = 0
bpy.data.particles["ParitcleSettings"].mass = 0

# VARIABLES
fps = 30
g = -9.8
a = 10
x = 20
v0 = 0

x0 = x
y0 = a * math.cosh(x0/a)
vx0 = v0
vy0 = math.sinh(x/a)
x1 = 0
y1 = 0
vx1 = 0
vy1 = 0

ico_sphere.location[0] = x0
ico_sphere.location[2] = y0

# ANIMATION
for i in range (1, 2001):
    for j in range(1, 10):
        t = 1/(fps * 10)
        print(g*math.sinh(x0/a))
        vx1 = vx0 + ((g * math.sinh(x0/a))/(1 + math.sinh(x0/a)**2)) * t
        vy1 = vy0 + ((g * math.sinh(x0/a)**2)/(1 + math.sinh(x0/a)**2)) * t
        print(vx1)
        print(vy1)
        print(math.cosh(x1/a))
        print("-------------------------------------")
        x1 = x0 + vx0 * t
        y1 = y0 + vy0 * t
        x0 = x1
        y0 = y1
        vx0 = vx1
        vy0 = vy1
    
    ico_sphere.location[0] = x1 # X-axis
    ico_sphere.location[2] = a * math.cosh(x1/a) # Y-axis
#    ico_sphere.location[2] = y1 # Y-axis
    ico_sphere.keyframe_insert(data_path = "location", frame = i)

# SHAPE
number_of_points = 5
coords = [(-x, a * x**2, 0), (-x * 4/5, a * (x * 4/5)**2, 0), (-x * 3/5, a * (x * 3/5)**2, 0), (-x * 2/5, a * (x * 2/5)**2, 0), (-x/5, a * (x/5)**2, 0), (0, 0, 0), (x/5, a * (x/5)**2, 0), (x * 2/5, a * (x * 2/5)**2, 0), (x * 3/5, a * (x * 3/5)**2, 0), (-x * 4/5, a * (x * 4/5)**2, 0), (x, a * x**2, 0)]

#curveData = bpy.data.curves.new('myCurve', type='CURVE')
#curveData.dimensions = '3D'
#curveData.resolution_u = 2

#polyline = curveData.splines.new('BEZIER')
#polyline.bezier_points.add(len(coords))
#for i, coord in enumerate(coords):
#    x,y,z = coord
#    polyline.bezier_points[i].co = (x, y, z, 1)

# curveOB = bpy.data.objects.new('myCurve', curveData)

bpy.ops.curve.primitive_bezier_curve_add(enter_editmode=False, align='WORLD', location=(0, -2, 0), rotation=(math.radians(90), 0, 0))

my_curve = bpy.context.active_object

bpy.ops.object.editmode_toggle()
bpy.ops.transform.translate(value=(-1, -0, -0), orient_axis_ortho='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', mirror=False, use_proportional_edit=True, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

#bpy.ops.curve.subdivide(number_cuts=number_of_points)
#my_curve.data.splines[0].bezier_points[3].select_control_point = True

bpy.ops.object.editmode_toggle() 

# RESET OTHER
bpy.context.area.ui_type = "VIEW_3D"
for area in bpy.context.workspace.screens[0].areas:
    for space in area.spaces:
        if space.type == 'VIEW_3D':
            space.shading.type = "RENDERED"
bpy.context.area.ui_type = "PROPERTIES"
bpy.data.scenes['Scene'].render.fps = fps
bpy.context.area.ui_type = "TIMELINE"
bpy.ops.anim.change_frame(frame=0)
bpy.context.area.ui_type = "TEXT_EDITOR"