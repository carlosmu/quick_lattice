# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy

bl_info = {
    "name" : "Quick Lattice",
    "author" : "carlosmu <carlos.damian.munoz@gmail.com>",    
    "blender" : (2, 83, 0),
    "version" : (0, 2, 0),
    "category" : "User",
    "location" : "3D View > Object Right Click Context Menu",
    "description" : "Automate the process of modifying an object from a lattice cage.",
    "warning" : "",
    "doc_url" : "https://github.com/carlosmu/quick_lattice",
    "tracker_url" : "",
}

# Operator class
class QL_OT_quick_lattice(bpy.types.Operator):
    """Quick lattice"""
    bl_idname = "ops.quick_lattice"
    bl_label = "Quick Lattice"  
    
    # It prevents the operator from appearing in unsupported editors.
    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True
    
    # Quick Lattice functionality
    def execute(self, context):
        # Save dimension of active object
        dim = bpy.context.active_object.dimensions

        # Save target object
        target = bpy.context.active_object

        # Save target name
        target_name = bpy.context.active_object.name

        # Save origin location of active object
        origin_loc = bpy.context.active_object.location

        # Save rotation of active on cursor
        cursor_rot = bpy.context.active_object.rotation_euler
        bpy.context.scene.cursor.rotation_euler = cursor_rot

        # Apply rotation for better bounding box
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

        # Set 3d cursor location to origin of active object
        bpy.context.scene.cursor.location = origin_loc

        # Set origin to geometry
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')

        # Create a latticetice with the information previously collected. 
        bpy.ops.object.add(type='LATTICE', enter_editmode=False, align='WORLD', location=bpy.context.active_object.location, rotation=target.rotation_euler)

        # Save reference and name of lattice (current active object).
        lattice = bpy.context.active_object
        lattice_name = bpy.context.active_object.name

        # Adjust dimensions of lattice and set subdivisions.
        lattice.dimensions = dim
        data = bpy.context.object.data
        data.points_u = 3
        data.points_v = 3
        data.points_w = 3

        ## Set origin to cursor
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = bpy.data.objects[target_name]
        bpy.context.view_layer.objects.active.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN') 

        # Inverted Rotation
        rotation_inverted = bpy.context.scene.cursor.rotation_euler.to_quaternion().inverted()
        bpy.context.active_object.rotation_euler = rotation_inverted.to_euler()
        # Apply rotation
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        # Rotation from cursor
        bpy.context.active_object.rotation_euler = bpy.context.scene.cursor.rotation_euler

        # Deselect the monkey
        bpy.ops.object.select_all(action='DESELECT')

        # Add lattice modifier to target.
        bpy.context.view_layer.objects.active = bpy.data.objects[target_name]
        bpy.ops.object.modifier_add(type='LATTICE')

        # Set lattice object in modifier as deformation cage.
        object = bpy.context.object
        data = bpy.data
        object.modifiers["Lattice"].object = data.objects[lattice_name]
        object.modifiers["Lattice"].name = "Quick Lattice"

        # Set lattice as active, then set in edit mode.
        bpy.context.view_layer.objects.active = data.objects[lattice_name]
        bpy.ops.object.editmode_toggle()
        
        return{'FINISHED'}

# Draw buttons
def draw_ql_menu(self, context):
    layout = self.layout 
    # Menu elements only on selected objects
    if context.selected_objects:
        layout.operator("ops.quick_lattice", icon='LATTICE_DATA')  # Create Quick Lattice       
        layout.separator() # Separator
    

# Register/unregister the operator class and draw function
def register():
    bpy.utils.register_class(QL_OT_quick_lattice)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_ql_menu) 
        
def unregister():
    bpy.utils.unregister_class(QL_OT_quick_lattice)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_ql_menu) 