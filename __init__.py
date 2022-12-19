# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Parent to nearest bone",
    "author": "Pablo Gentile",
    "version": (0, 8, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Object > Parent > Parent to nearest Bone",
    "description": "Parents object to the nearest bone",
    "warning": "",
    "doc_url": "https://github.com/g3ntile/parentToNearestBone#readme",
    "category": "Object",
}


import bpy
import math 
from mathutils import Vector

C = bpy.context
D = bpy.data

### functions
# Object space Vector to world space Vector
def loc2world(ob, vector):
    '''converts the vector from ob space to world space'''
    return ob.matrix_world @ vector

# returns the closest bone in armature ar to the object ob
def closestBone(ob, ar, use_center):    
    if ar.type != 'ARMATURE':
        print ('select an armature!')
        
    # to edit mode
    bpy.ops.object.mode_set(mode='EDIT')    
    
    # finds the minimum value from a list of tuples that store the distance and the bone itself
    # and stores the resulting bone
    if use_center:
        # use the geometric center vs bone.center method
        closest = min( [ (math.dist(getGeometryCenter(ob), loc2world(ar, bone.center)), bone) for bone in ar.data.edit_bones ])
    else:
        # use the object origin vs bone head method
        closest = min( [ (math.dist(ob.location, loc2world(ar, bone.head)), bone) for bone in ar.data.edit_bones ])
    
    #extract bone name
    bone_name = closest[1].name
    
    # back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    return bone_name
    
def getHeadPosition(ar,bone):
    bpy.ops.object.mode_set(mode='EDIT')  
    head = ar.data.edit_bones[bone].head
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return head 

def getCenterPosition(ar,bone):
    bpy.ops.object.mode_set(mode='EDIT')  
    center = ar.data.edit_bones[bone].center
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return center

def getGeometryCenter(ob):
    # Returns the Geometric center of 
    # the object calculating the average of 
    # the bounding box min and max

    # get matrix world to convert vectors
    mat = ob.matrix_world
    
    # get max and min from bounding box in world space
    max = mat @ Vector(ob.bound_box[6])
    min = mat @ Vector(ob.bound_box[0])
    
    # return average
    return (max+min)/2

# parent to bone via OPS
def parent2BoneKT(ob,arma,parent_bone):
    # The parenting is done using bpy.ops
    # because it's the only way I found for 
    # preserving the transform of the object
    # in the process, all other methods resulted 
    # in weird relocation of the object
    # The drawback is that the process involves
    # deselecting and reselecting each object.
    # This may be slow in case of large selection sets

    # deselects all objects
    bpy.ops.object.select_all(action='DESELECT')

    # select the armature
    arma.select_set(True)
    bpy.context.view_layer.objects.active = arma

    # to edit mode
    bpy.ops.object.mode_set(mode='EDIT')

    # set the bone active
    arma.data.edit_bones.active = arma.data.edit_bones[parent_bone]

    # change to object mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # deselect all again
    bpy.ops.object.select_all(action='DESELECT')  # deselect all objects
    
    # reselect the object and the armature and set it active
    ob.select_set(True)
    arma.select_set(True)
    bpy.context.view_layer.objects.active = arma

    # parent the object to the bone
    # the active object will be the parent of all selected object
    bpy.ops.object.parent_set(type='BONE', keep_transform=True)

# error message  
def oops(self, context):
    self.layout.label(text="Please select an Armature as active object!")

    
#########################

##**##**

def main(context, use_center):
    C = context
    # separate the armature and get only parentable objects
    my_objects = [ob  for ob in C.selected_objects if ob.type != 'ARMATURE']

    # set the armature

    ar = C.active_object

    if ar.type == 'ARMATURE':

        for ob in my_objects:
            print( '–' * 80)
            print (ob.name)
            print( '.' * 80)        
            my_closest = closestBone(ob, ar, use_center)
            parent2BoneKT(ob,ar,my_closest)

    else :
        bpy.context.window_manager.popup_menu(oops, title="Error", icon='ERROR')
        


##**##**

class ParentToNearestBone(bpy.types.Operator):
    """Parents all selected objects to the nearest Bone in Active Armature, comparing the Bone's head to each Object's origin"""
    bl_idname = "object.parent_to_nearest_bone"
    bl_label = "Parent to nearest Bone"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        main(context, False)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ParentToNearestBone.bl_idname, text=ParentToNearestBone.bl_label)

class ParentToNearestBoneCenters(bpy.types.Operator):
    """Parents all selected objects to the nearest Bone in Active Armature, comparing the Bone's center to each Object's geometric center"""
    bl_idname = "object.parent_to_nearest_bone_centers"
    bl_label = "Parent to nearest Bone"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        main(context, True)
        return {'FINISHED'}

def menu_func_center(self, context):
    self.layout.operator(ParentToNearestBoneCenters.bl_idname, text=ParentToNearestBoneCenters.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
# The old version of the operator is commented and not registered, just in case. 
# Will be cleaned  up if everything goes well in 1.0

def register():
    # bpy.utils.register_class(ParentToNearestBone)
    # bpy.types.VIEW3D_MT_object_parent.append(menu_func)
    bpy.utils.register_class(ParentToNearestBoneCenters)
    bpy.types.VIEW3D_MT_object_parent.append(menu_func_center)


def unregister():
    bpy.utils.unregister_class(ParentToNearestBoneCenters)
    bpy.types.VIEW3D_MT_object_parent.remove(menu_func_center)
    # bpy.utils.unregister_class(ParentToNearestBone)
    # bpy.types.VIEW3D_MT_object_parent.remove(menu_func)


if __name__ == "__main__":
    register()

