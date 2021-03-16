# Quick Lattice (Blender Addon) 
Tired of setting up lattices?<br>
Looking for a non-destructive way to modify your models?<br>
Quick Lattice is what you are looking for! Do not wait more! (hahaha)<br>

## What its does?
Automating the process of warping an object in a lattice cage.<br>
Setting the size, position, rotation, resolution, interpolation, modifier, etc.<br>
This will save you a lot clicks and other boring settings. But not much more. <br>

## Usage
1. Select the target object
2. Right Click Menú -> Quick Lattice (or W for Right Click Select Users)
<br><br>
<img src="demo/quick_lattice.jpg" width="600" style="border-radius:5px">
<br><br>
<img src="demo/quick_lattice.gif" width="600" style="border-radius:5px">
<br><br>

## Instalation
1. Go to releases page: https://github.com/carlosmu/quick_lattice/releases/
2. Download the python file "quick_lattice.py"
3. Go to Blender > User Preferences > Addons > Install 
4. Select the previously downloaded file.
5. Activate the addon.
7. Enjoy it!

## Changelog
- 0.3.0 First Release!
- 0.3.1 Fix: Crash On Undo, reported by BluePortal77 
- 0.4.0 Add Last Operation Support
<br><img src="demo/last_operation.jpg" width="400" style="border-radius:5px"><br>
- 0.5.0 Add Popup Dialog and User Preferences option
<br><img src="demo/popup_dialog.jpg" width="400" style="border-radius:5px"><br>
<br><img src="demo/popup_user_prefs.jpg" width="400" style="border-radius:5px"><br>
- 0.6.0 Add User Preferences to set the Default Resolution and Interpolation of Lattices
<br><img src="demo/user_preferences_v06.jpg" width="400" style="border-radius:5px"><br>




## Donate
You can support my work by buying this plugin on Gumroad https://gum.co/quicklattice

## Known Issues
When the object's pivot is rotated (but not the whole object), the result may not be what you want. In those cases, try applying the rotation first (Ctrl + A).
<br><br>
<img src="demo/known_issues.jpg" width="600" style="border-radius:5px">
<br><br>

## To-Do List
- Multi Object option.
- Add feature to set bones/empties to all points of lattice.
