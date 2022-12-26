#-----------------------------------------------
#
# DOCUMENT Blender_helix_animation.blend
# AUTHOR   Arnau del Rio (arnau@mathinrollercoasters.com)
# DATE     02-08-2022
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
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(40, -40, 35), rotation=(1.22, -0, 0.785), scale=(1, 1, 1))

# LIGHT
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.context.object.data.energy = 2
bpy.context.object.rotation_euler[0] = 0.383972
bpy.context.object.rotation_euler[1] = 1.0821


# CILINDER
bpy.ops.mesh.primitive_cube_add(size=1.5, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.ops.object.modifier_add(type='SCREW')
bpy.context.object.modifiers["Screw"].screw_offset = 25
bpy.context.object.modifiers["Screw"].iterations = 1
bpy.context.object.modifiers["Screw"].angle = -12.566371
bpy.context.object.modifiers["Screw"].steps = 32
bpy.context.object.modifiers["Screw"].render_steps = 32
bpy.ops.object.modifier_apply(modifier="Screw")

# CILINDER COLOR
mat_name = "Material"
bpy.ops.material.new()
bpy.data.materials[-1].name = mat_name
mat = bpy.data.materials.get(mat_name)
mat.use_nodes = False
bpy.data.materials[mat_name].diffuse_color = (0.1, 0.1, 0.1, 1)
bpy.ops.object.material_slot_add()
mat = bpy.data.materials.get(mat_name)
ob = bpy.context.active_object
ob.data.materials[0] = mat

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
bpy.data.particles["ParticleSettings"].lifetime = 300
bpy.data.particles["ParticleSettings"].normal_factor = 0


# VARIABLES
g = -9.8
R = 2
p = 0.1
v0 = 0
z0 = 25
theta = (g * p)/(2 * R**2 + 2 * p**2)

# ANIMATION
for i in range(251):
    t = i/15
    ico_sphere.location[0] = R * math.cos(theta * t**2 + v0 * t + z0) # X-axis
    ico_sphere.location[1] = R * math.sin(theta * t**2 + v0 * t + z0) # Y-axis
#    ico_sphere.location[2] = 25 + (-9.8 * ((i/15)/(2 * math.pi))**2 / 2) # Z-axis
#    ico_sphere.location[2] = 25 + (g * math.sqrt(R**2 + k**2) * (i/15)**2)/(k*R*2) # Z-axis
#    ico_sphere.location[2] = 25 - (i/15) / R
    ico_sphere.location[2] = theta * t**2 + v0 * t + z0
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