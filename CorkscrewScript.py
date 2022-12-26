#-----------------------------------------------
#
# DOCUMENT Blender_corkscrew_animation.blend
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
bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(0.43, 0.68, 0.2), rotation=(math.radians(75), 0, math.radians(150)), scale=(1, 1, 1))
bpy.context.object.data.type = 'PERSP'
mainCamera = bpy.context.object
mainCamera.data.lens = 50.0
mainCamera.data.clip_start = 0.00005
mainCamera.data.clip_end = 200

# LIGHT
bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
bpy.context.object.data.energy = 2
bpy.context.object.rotation_euler[0] = 0.383972
bpy.context.object.rotation_euler[1] = 1.0821

# CILINDER
#bpy.ops.mesh.primitive_cylinder_add(radius=2, depth=120, enter_editmode=False, align='WORLD', location=(0, 60, 0), rotation=(1.5708, 0, 0), scale=(3, 3, 1))

# CILINDER COLOR
#bpy.ops.material.new()
#bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.1, 0.1, 0.1, 1)

# SPHERE
#bpy.ops.mesh.primitive_ico_sphere_add(radius=0.5, enter_editmode=False, location=(0, 0, 10), scale=(2, 2, 2))
bpy.ops.mesh.primitive_ico_sphere_add(radius=0.5, enter_editmode=False, location=(0, 0, 10), scale=(0.01, 0.01, 0.01))
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
    bpy.data.particles["ParticleSettings"].count = 2000
    bpy.data.particles["ParticleSettings"].frame_end = 500
    bpy.data.particles["ParticleSettings"].effector_weights.gravity = 0
    bpy.data.particles["ParticleSettings"].lifetime = 1000
    bpy.data.particles["ParticleSettings"].normal_factor = 0
    bpy.data.particles["ParticleSettings"].mass = 0

# VARIABLES
fps = 30 # frames per second
g = - 9.8 # gravity
R = 10 # radius
k = 0.05
ddtheta = 0
f = 0 # frame
h = 300 # frames in in-line twist
w = 0 # number of half-rotations in in-line twist
t = 1/(fps * 50000)
clothoidConstant = 0.5

theta0 = 0
dtheta0 = 5
vx0 = 0
vy0 = 0
vz0 = 0
x0 = 0
y0 = 0
z0 = 0

xPosSwitch = 0
yPosSwitch = 0
zPosSwitch = 0

x1 = 0
y1 = 0
z1 = 0
vx1 = 0
vy1 = 0
vz1 = 0
theta1 = 0
dtheta1 = 0

ico_sphere.location[0] = x0
ico_sphere.location[1] = y0
ico_sphere.location[2] = z0
ico_sphere.keyframe_insert(data_path = "location", frame = 0)

# ANIMATION - Loop
while (2 * theta0 * math.cos(theta0**2) >= 0):
    f = f + 1
    for j in range(1, 100):
        ddtheta = g * math.sin(theta0**2)
        dtheta1 = dtheta0 + ddtheta * t
        theta1 = theta0 + dtheta0 * t
        
        vx1 = math.cos(theta0**2)
        x1 = vx0 * t + x0
        y1 = k * theta0
        vz1 = math.sin(theta0**2) * 1.2
        z1 = vz0 * t + z0
        
        x0 = x1
        z0 = z1
        vx0 = vx1
        vz0 = vz1
        theta0 = theta1
        dtheta0 = dtheta1
    
    ico_sphere.location[0] = x1 # X-axis
    ico_sphere.location[1] = y1 # Y-axis
    ico_sphere.location[2] = z1 # Z-axis
    ico_sphere.keyframe_insert(data_path = "location", frame = f)

#R = (clothoidConstant**2)/theta0
R = 0.08

lastTheta = theta0
lastdTheta = dtheta0

xPosSwitch = x1 - R
yPosSwitch = y1
zPosSwitch = z1

print("--------------------------------------------------------------")
print(str(f) + " | " + str(2 * theta0 * math.cos(theta0**2)) + " | " + str(dtheta0))
print(str(R) + " | " + str(theta0) + " ||| "+ str(xPosSwitch) + " | " + str(yPosSwitch) + " | " + str(zPosSwitch))

theta0 = 0
dtheta0 = 20

#for i in range(int(f), int(f + h) + 1):
# ANIMATION - Twist
while (w < 5):
    if w % 2 == 0:
        if (- math.sin(theta0) >= 0):
            w = w + 1
            print("PATH 1: " + str(f))
    else:
        if (- math.sin(theta0) <= 0):
            w = w + 1
            print("PATH 2: " + str(f))
    f = f + 1
#for i in range(41, 341):
    for j in range(1, 100):
        costheta0 = math.cos(theta0)
        sintheta0 = math.sin(theta0)
        
        ddtheta = (g * R * costheta0)/(R**2 + k**2)
        dtheta1 = ddtheta * t + dtheta0
        theta1 = dtheta0 * t + theta0

        x1 = R * costheta0
        y1 = k * theta0/2
        z1 = R * sintheta0
        
        x0 = x1
        y0 = y1
        z0 = z1
        theta0 = theta1
        dtheta0 = dtheta1
    
    ico_sphere.location[0] = x1 + xPosSwitch # X-axis
    ico_sphere.location[1] = y1 + yPosSwitch # Y-axis
    ico_sphere.location[2] = z1 + zPosSwitch # Z-axis
    ico_sphere.keyframe_insert(data_path = "location", frame = f)
    #print("> " + str(x1) + " | " + str(y1) + " | "+ str(z1) + " | " + str(xPosSwitch) + " | " + str(yPosSwitch) + " | " + str(zPosSwitch))

theta0 = lastTheta
xPosSwitch = xPosSwitch - R
dtheta0 = lastdTheta

x0 = 0
y0 = 0
z0 = 0

print(str(f) + " | " + str(2 * theta0 * math.cos(theta0**2)) + " | " + str(dtheta0))
print(str(R) + " | " + str(theta0) + " ||| "+ str(xPosSwitch) + " | " + str(yPosSwitch) + " | " + str(zPosSwitch))

f1 = f

# ANIMATION - Loop
#while (z0 + zPosSwitch >= 0):
while(x1 <= xPosSwitch + 2*R):
    f = f + 1
    for j in range(1, 100):
        ddtheta = (g * math.sin(theta0**2))
        dtheta1 = dtheta0 - ddtheta * t
        theta1 = theta0 - dtheta0 * t
        
        vx1 = math.cos(theta0**2)
        x1 = vx0 * t + x0
        vz1 = math.sin(theta0**2) * 1.2
        z1 = -vz0 * t + z0
        
        x0 = x1
        z0 = z1
        vx0 = vx1
        vz0 = vz1
        theta0 = theta1
        dtheta0 = dtheta1
    
    ico_sphere.location[0] = x1 + xPosSwitch # X-axis
    ico_sphere.location[2] = z1 + zPosSwitch # Z-axis
    ico_sphere.keyframe_insert(data_path = "location", frame = f)
    
print(str(f) + " | " + str(2 * theta0 * math.cos(theta0**2)) + " | " + str(dtheta0))

theta0 = 0

yPosSwitch = y1 + 2*yPosSwitch
f1 = f

while (theta0 <= lastTheta):
    for j in range(1, 100):
        ddtheta = g * math.sin(theta0**2)
        dtheta1 = dtheta0 + ddtheta * t
        theta1 = theta0 + dtheta0 * t
        
        vx1 = math.cos(theta0**2)
        x1 = vx0 * t + x0
        y1 = - k * theta0
        vz1 = math.sin(theta0**2) * 1.2
        z1 = vz0 * t + z0
        
        x0 = x1
        z0 = z1
        vx0 = vx1
        vz0 = vz1
        theta0 = theta1
        dtheta0 = dtheta1

    ico_sphere.location[1] = y1  + yPosSwitch # Y-axis
    ico_sphere.keyframe_insert(data_path = "location", index = 1, frame = f1)
    f1 = f1 - 1

# RESET OTHER
bpy.context.area.ui_type = "VIEW_3D"
for area in bpy.context.workspace.screens[0].areas:
    for space in area.spaces:
        if space.type == 'VIEW_3D':
            space.shading.type = "RENDERED"
bpy.context.area.ui_type = "PROPERTIES"
bpy.data.scenes['Scene'].render.fps = fps
bpy.data.scenes['Scene'].frame_end = f
bpy.context.area.ui_type = "TIMELINE"
bpy.ops.anim.change_frame(frame=0)
bpy.context.area.ui_type = "TEXT_EDITOR"