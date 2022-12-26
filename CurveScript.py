#-----------------------------------------------
#
# DOCUMENT Blender_circle_animation.blend
# AUTHOR   Arnau del Rio (arnau@mathinrollercoasters.com)
# DATE     20-09-2022
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
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0, 0, 35), rotation=(0, 0, 0), scale=(1, 1, 1))

# LIGHT
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.context.object.data.energy = 2
bpy.context.object.rotation_euler[0] = 0.383972
bpy.context.object.rotation_euler[1] = 1.0821

# FLOOR
bpy.ops.mesh.primitive_plane_add(size=25)

# FLOOR COLOR
mat_name = "Base"
bpy.ops.material.new()
bpy.data.materials[-1].name = mat_name
mat = bpy.data.materials.get(mat_name)
mat.use_nodes = False
bpy.data.materials[mat_name].diffuse_color = (0.1, 0.1, 0.1, 1)
bpy.ops.object.material_slot_add()
mat = bpy.data.materials.get(mat_name)
ob = bpy.context.active_object
ob.data.materials[0] = mat

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
bpy.data.particles["ParticleSettings"].frame_end = 200
bpy.data.particles["ParticleSettings"].mass = 0
bpy.data.particles["ParticleSettings"].lifetime = 300
bpy.data.particles["ParticleSettings"].normal_factor = 0
if(bpy.data.particles["ParticleSettings.001"]):
    bpy.ops.object.particle_settings_remove()


# VARIABLES
w = 10
phi0 = 0
R = 5

# ANIMATION
for i in range(251):
    t = i/60
    phi = phi0 + w * t
    
    ico_sphere.location[0] = R * math.cos(phi) # X-axis
    ico_sphere.location[1] = R * math.sin(phi) # Y-axis
    ico_sphere.location[2] = 2
    ico_sphere.keyframe_insert(data_path = "location", frame = i)

# RESET OTHER
bpy.context.area.ui_type = "VIEW_3D"
for area in bpy.context.workspace.screens[0].areas:
    for space in area.spaces:
        if space.type == 'VIEW_3D':
            space.shading.type = "RENDERED"
bpy.context.area.ui_type = "PROPERTIES"
bpy.data.scenes['Scene'].render.fps = 30
bpy.context.area.ui_type = "TIMELINE"
bpy.ops.anim.change_frame(frame=0)
bpy.context.area.ui_type = "TEXT_EDITOR"