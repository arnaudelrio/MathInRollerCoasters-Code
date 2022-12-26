#-----------------------------------------------
#
# DOCUMENT Blender_in-line_twist_animation.blend
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
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# CAMERA
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(160, 350, 200), rotation=(math.radians(60), 0, math.radians(150)), scale=(1, 1, 1))
bpy.context.object.data.type = 'ORTHO'
bpy.context.object.data.ortho_scale = 150

# LIGHT
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.context.object.data.energy = 2
bpy.context.object.rotation_euler[0] = 0.383972
bpy.context.object.rotation_euler[1] = 1.0821

# CILINDER
bpy.ops.mesh.primitive_cylinder_add(radius=2, depth=120, enter_editmode=False, align='WORLD', location=(0, 60, 0), rotation=(1.5708, 0, 0), scale=(3, 1, 3))

# CILINDER COLOR
bpy.ops.material.new()
bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.1, 0.1, 0.1, 1)

# SPHERE
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.5, enter_editmode=False, location=(0, 0, 10), scale=(2, 2, 2))
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
#C = bpy.data.objects['Icosphere']
#ps = C.particle_systems['ParticleSystem'].settings
bpy.ops.object.particle_system_add()
bpy.ops.object.ParticleSettings = "ParticleSettings"
#if not 'ParticleSettings':
if True:
    bpy.data.particles["ParticleSettings"].name = "ParticleSettings"
    bpy.data.particles["ParticleSettings"].type = 'EMITTER'
    bpy.data.particles["ParticleSettings"].frame_end = 1000
    bpy.data.particles["ParticleSettings"].effector_weights.gravity = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.all = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.vortex = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.force = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.vortex = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.magnetic = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.harmonic = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.charge = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.lennardjones = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.wind = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.curve_guide = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.texture = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.smokeflow = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.turbulence = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.drag = 0
    #bpy.data.particles["ParticleSettings"].effector_weights.boid = 0
    bpy.data.particles["ParticleSettings"].lifetime = 1000
    bpy.data.particles["ParticleSettings"].normal_factor = 0
    bpy.data.particles["ParticleSettings"].mass = 0

# VARIABLES
fps = 30
g = 9.8
R = 10
k = 2
ddtheta = 0

theta0 = math.radians(90)
dtheta0 = 1
x0 = R * math.cos(theta0)
y0 = k * theta0
z0 = R * math.sin(theta0)

x1 = 0
y1 = 0
z1 = 0
theta1 = 0
dtheta1 = 0

ico_sphere.location[0] = x0
ico_sphere.location[1] = y0
ico_sphere.location[2] = z0
ico_sphere.keyframe_insert(data_path = "location", frame = 0)

# ANIMATION
for i in range(1, 1000):
    for j in range(1, 100):
        t = 1/(fps * 100)
        costheta0 = math.cos(theta0)
        sintheta0 = math.sin(theta0)
        
        ddtheta = - (g * R * costheta0)/(R**2 + k**2)
        dtheta1 = ddtheta * t + dtheta0
        theta1 = dtheta0 * t + theta0

        x1 = R * costheta0
        y1 = k * theta0
        z1 = R * sintheta0
        
        x0 = x1
        y0 = y1
        z0 = z1
        theta0 = theta1
        dtheta0 = dtheta1
    
    ico_sphere.location[0] = x1 # X-axis
    ico_sphere.location[1] = y1 # Y-axis
    ico_sphere.location[2] = z1 # Z-axis
    ico_sphere.keyframe_insert(data_path = "location", frame = i)

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