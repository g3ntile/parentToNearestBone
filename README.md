# parentToNearestBone
**Blender addon to parent objects to the nearest bone** 

**Version**: 1.0

## Installation Instructions
1. **Download** the addon using the green button and then download the `.zip` file or go to the release section.
2. **Install and activate** the addon inside Blender 3+.
3. **Select** one or more objects, and an Armature, with the Armature as the active object.
4. Go to `Object -> Parent -> Parent to nearest Bone`.
5. **Enjoy!**

## Features
- Parents objects based on the bone's center and the geometric center of each object to avoid errors.
- Ensures no issues with "Y" joints. Please report if you find any.
- Each object is parented to one (and only one) bone.

## Usage Notes
- **Symmetrical Objects**: For symmetrical parts like robot arms, ensure each arm is a different object. You can't parent one object for both arms if it has a mirror modifier; the addon will throw an error.
- **Mirror Modifiers**: If you have objects with mirror modifiers, apply them (and separate objects) manually, or use Walter Palladino's "Apply Mirror and Separate" addon: [Apply Mirror and Separate](https://github.com/walterpalladino/applyMirrorAndSeparate).

## Disclaimer
While I am familiar in Python, I am not familiar with Blenders coding. This add-on is a revised edit of the original, which did not work in Blender 4 anymore.

## Call for Help
If you encounter any issues or have improvements, please let me know!
