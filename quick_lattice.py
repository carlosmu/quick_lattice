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
    "version" : (0, 1, 0),
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
        dim = bpy.context.active_object.dimensions
        target = bpy.context.active_object
        target_name = bpy.context.active_object.name

        # Create a latticetice with the information previously collected. 
        bpy.ops.object.add(type='LATTICE', enter_editmode=False, align='WORLD', location=target.location, rotation=target.rotation_euler)

        # Save reference and name of lattice (current active object).
        lattice = bpy.context.active_object
        lattice_name = bpy.context.active_object.name

        # Adjust dimensions of lattice and set subdivisions.
        lattice.dimensions = dim
        data = bpy.context.object.data
        data.points_u = 3
        data.points_v = 3
        data.points_w = 3

        # Set the target as active.
        viewlayer = bpy.context.view_layer
        viewlayer.objects.active = bpy.data.objects[target_name]

        # Add lattice modifier to target.
        bpy.ops.object.modifier_add(type='LATTICE')

        # Set lattice object in modifier as deformation cage.
        object = bpy.context.object
        data = bpy.data
        object.modifiers["Lattice"].object = data.objects[lattice_name]

        # Set lattice as active, then set in edit mode.
        viewlayer.objects.active = data.objects[lattice_name]
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