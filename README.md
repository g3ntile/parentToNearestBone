# parentToNearestBone
Blender addon to parent objects to the nearest bone
1. download the addon using the green button and then download .zip
2. Install and activate the addon inside Blender 3+
3. select one or more objects, and an Armature, with the Armature as active object
4. Goto to Object->Parent->Parent to nearest Bone
5. enjoy

Keep in mind:
* it will parent the object based on its origin. It will guess better if the origin is on one extreme, the "head" from the bone's point of view. 
* If the object happens to be on a joint with 2 bones that share it's origin (head) like in a "Y" shape, for example, it may get parented to the wrong bone. The only criteria the addon takes is bone (head) proximity to the object origin. You may need to tweak and reparent those.

I'm not a developer, just a Blender user with some limited python skills, please be kind, this may indeed have errors.

CALL FOR HELP:
I couldn't register this operator into the "Ctl+P" operator, I couldn't find that menu bl_idname. If you know how to append this op there, please tell me! :-)

