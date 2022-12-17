bl_info = {
    "name": "Parent to nearest bone",
    "author": "Pablo Gentile",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Object > Parent > Parent to nearest Bone",
    "description": "Parents object to the nearest bone",
    "warning": "",
    "doc_url": "https://github.com/g3ntile/parentToNearestBone#readme",
    "category": "Object",
}


import bpy
import math 

C = bpy.context
D = bpy.data

### functions
# Object space Vector to world space Vector
def loc2world(ob, vector):
    '''converts the vector from ob space to world space'''
    return ob.matrix_world @ vector

# returns the closest bone in armature ar to the object ob
def closestBone(ob, ar):    
    if ar.type != 'ARMATURE':
        print ('select an armature!')
        
    # to edit mode
    bpy.ops.object.mode_set(mode='EDIT')    
    print(ar)
    print('bones:' , [bone.name for bone in ar.data.edit_bones])
    # finds the minimum value from a list of tuples that store the distance and the bone itself
    # and stores the resulting bone
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

# parent to bone via OPS
def parent2BoneKT(ob,arma,parent_bone):
    bpy.ops.object.select_all(action='DESELECT')

    arma.select_set(True)
    bpy.context.view_layer.objects.active = arma

    bpy.ops.object.mode_set(mode='EDIT')

    arma.data.edit_bones.active = arma.data.edit_bones[parent_bone]

    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')  # deselect all objects
    ob.select_set(True)
    arma.select_set(True)
    bpy.context.view_layer.objects.active = arma
    # the active object will be the parent of all selected object

    bpy.ops.object.parent_set(type='BONE', keep_transform=True)

# error message  
def oops(self, context):
    self.layout.label(text="Please select an Armature as active object!")

    
#########################

##**##**

def main(context):
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
            my_closest = closestBone(ob, ar)
            parent2BoneKT(ob,ar,my_closest)

    else :
        bpy.context.window_manager.popup_menu(oops, title="Error", icon='ERROR')
        


##**##**

class ParentToNearestBone(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.parent_to_nearest_bone"
    bl_label = "Parent to nearest Bone"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE'

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(ParentToNearestBone.bl_idname, text=ParentToNearestBone.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(ParentToNearestBone)
    bpy.types.VIEW3D_MT_object_parent.append(menu_func)


def unregister():
    bpy.utils.unregister_class(ParentToNearestBone)
    bpy.types.VIEW3D_MT_object_parent.remove(menu_func)


if __name__ == "__main__":
    register()

