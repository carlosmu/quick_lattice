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
    "version" : (0, 5, 0),
    "category" : "User",
    "location" : "3D View > Object Right Click Context Menu",
    "description" : "Automate the process of modifying an object from a lattice cage.",
    "warning" : "",
    "doc_url" : "https://github.com/carlosmu/quick_lattice",
    "tracker_url" : "https://github.com/carlosmu/quick_lattice/issues",
}

class QL_OT_quick_lattice(bpy.types.Operator):
    """Automates the process of warping an object in a lattice cage"""
    bl_idname = "ql.quick_lattice"
    bl_label = "Quick Lattice"  
    bl_options = {'REGISTER', 'UNDO'}

    ##############################################
    ### PROPERTIES
    ##############################################

    # Resolution Properties
    resolution_u : bpy.props.IntProperty(
        name = "Resolution U (X)",
        description = "Points in U direction (can't changed when there are shape keys)",
        default = 3,
        min = 1, soft_min = 2, soft_max = 16,
    )
    resolution_v : bpy.props.IntProperty(
        name = "V (Y)",
        description = "Points in V direction (can't changed when there are shape keys)",
        default = 3,
        min = 1, soft_min = 2, soft_max = 16,
    )
    resolution_w : bpy.props.IntProperty(
        name = "W (Z)",
        description = "Points in W direction (can't changed when there are shape keys)",
        default = 3,
        min = 1, soft_min = 2, soft_max = 16,
    )

    # Interpolation Types (Tuple)
    interpolation_types = (('KEY_LINEAR', 'Linear', ''),
                            ('KEY_CARDINAL', 'Cardinal', ''),
                            ('KEY_CATMULL_ROM', 'Catmull-Rom', ''),
                            ('KEY_BSPLINE', 'BSpline', ''))
    
    # Interpolation Types Property
    interpolation_types : bpy.props.EnumProperty(
        name = "Interpolation",
        description = "Interpolation Type between dimension points",
        items = interpolation_types,
        default = 'KEY_BSPLINE',
    )

    # Outside Property
    outside : bpy.props.BoolProperty(
        name = "Outside",
        description = "Only draw and use the outher vertices",
        default = False,
    )
 
    # It prevents the operator from appearing in unsupported editors.
    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True
    
    ##############################################
    # Quick Lattice functionality
    ##############################################
    def execute(self, context): 
        # Save target name
        target = bpy.data.objects[context.active_object.name]

        # Save Location on 3d Cursor.
        context.scene.cursor.location = target.location

        # Set origin to geometry (to find the geometry)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        # Then create Lattice object with the information previously collected. 
        bpy.ops.object.add(
                            type='LATTICE', 
                            enter_editmode=False, 
                            align='WORLD', 
                            location=target.location, 
                            rotation=target.rotation_euler
                            )

        # Save reference and name of lattice (current active object).
        lattice = bpy.data.objects[context.active_object.name]
        lattice.name = "Quick_Lattice"

        # Adjust lattice dimensions, points and interpolation
        lattice.dimensions = target.dimensions
        lattice.data.points_u = self.resolution_u
        lattice.data.points_v = self.resolution_v
        lattice.data.points_w = self.resolution_w
        lattice.data.interpolation_type_u = self.interpolation_types
        lattice.data.interpolation_type_v = self.interpolation_types
        lattice.data.interpolation_type_w = self.interpolation_types
        lattice.data.use_outside = self.outside

        # Return Target to Initial Position
        lattice.select_set(False)
        target.select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        target.select_set(False)

        # Add lattice modifier and set the object
        modifier = target.modifiers.new(name="Quick Lattice", type='LATTICE')
        modifier.object = lattice

        # Set lattice as active, then set in edit mode.
        lattice.select_set(True)
        bpy.ops.object.editmode_toggle()    
        return{'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        col = layout.column(align=True)
        col.prop(self, "resolution_u")
        col.prop(self, "resolution_v")
        col.prop(self, "resolution_w")

        col = layout.column(align=False)              
        col.prop(self, "outside")
        col.prop(self, "interpolation_types")

##############################################
### DRAW BUTTONS
##############################################
def draw_quicklattice_menu(self, context):
    layout = self.layout     
    if context.selected_objects: # Menu elements only on selected objects
        layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("ql.quick_lattice", icon='LATTICE_DATA')  # Create Quick Lattice       
        layout.separator() # Separator    

##############################################
### Register/unregister class and functions
##############################################
def register():
    bpy.utils.register_class(QL_OT_quick_lattice)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_quicklattice_menu) 
        
def unregister():
    bpy.utils.unregister_class(QL_OT_quick_lattice)
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_quicklattice_menu) 