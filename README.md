# parentToNearestBone
Blender addon to parent objects to the nearest bone
0.8

1. download the addon using the green button and then download .zip or go to the release section
2. Install and activate the addon inside Blender 3+
3. select one or more objects, and an Armature, with the Armature as active object
4. Goto to Object->Parent->Parent to nearest Bone
5. enjoy

Notes:
* Now it will parent the object based on the bone's center, and the geometric center of each object. It's done this way to avoid some errors triggered by the former method (bone's head vs object origin)
* Now there should be no problem with "Y" joints. Please report if you find one.

I'm not a developer, just a Blender user with some limited python skills, please be kind, this may indeed have errors.

CALL FOR HELP:
I couldn't register this operator into the "Ctl+P" operator, I couldn't find that menu bl_idname. If you know how to append this op there, please tell me! :-)

