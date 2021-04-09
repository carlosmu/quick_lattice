import bpy

from .user_prefs import QL_Preferences

### Register preferences for use in properties
bpy.utils.register_class(QL_Preferences)


##############################################
#   MAIN OPERATOR
##############################################

class QL_OT_quick_lattice(bpy.types.Operator):
    """Automating the process of warping an object in a lattice cage."""
    bl_idname = "ql.quick_lattice"
    bl_label = "Quick Lattice"  
    bl_options = {'REGISTER', 'UNDO'}

    ql_props = bpy.context.preferences.addons[__package__].preferences

    # Resolution Properties
    resolution_u : bpy.props.IntProperty(
        name = "Resolution U (X)",
        description = "Points in U direction (can't changed when there are shape keys)",
        default = ql_props.default_resolution,
        min = 1, soft_min = 2, soft_max = 32, max =256, 
    )
    resolution_v : bpy.props.IntProperty(
        name = "V (Y)",
        description = "Points in V direction (can't changed when there are shape keys)",
        default = ql_props.default_resolution,
        min = 1, soft_min = 2, soft_max = 32, max =256, 
    )
    resolution_w : bpy.props.IntProperty(
        name = "W (Z)",
        description = "Points in W direction (can't changed when there are shape keys)",
        default = ql_props.default_resolution,
        min = 1, soft_min = 2, soft_max = 32, max =256, 
    )

    # Interpolation Types Property
    interpolation_types : bpy.props.EnumProperty(
        name = "Interpolation",
        description = "Interpolation Type between dimension points",
        items = [('KEY_LINEAR', 'Linear', ''),
                ('KEY_CARDINAL', 'Cardinal', ''),
                ('KEY_CATMULL_ROM', 'Catmull-Rom', ''),
                ('KEY_BSPLINE', 'BSpline', '')],
        default = bpy.context.preferences.addons[__package__].preferences.default_interpolation
    )

    # Outside Property
    outside : bpy.props.BoolProperty(
        name = "Outside",
        description = "Only draw and use the outher vertices",
        default = False,
    )
 
    # Prevents operator appearing in unsupported editors
    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True
    

    ##############################################
    #   Quick Lattice functionality
    ##############################################
    def execute(self, context): 
        ql_props = bpy.context.preferences.addons[__package__].preferences

        # Save target name
        target = bpy.data.objects[context.active_object.name]

        # Save Location on 3d Cursor
        context.scene.cursor.location = target.location

        # Set origin to geometry (to find the geometry)
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        # Create Lattice object 
        bpy.ops.object.add(
                            type='LATTICE', 
                            enter_editmode=False, 
                            align='WORLD', 
                            location=target.location, 
                            rotation=target.rotation_euler
                            )

        # Save references of lattice (current active object)
        lattice = bpy.data.objects[context.active_object.name]
        # Custom Names
        if ql_props.custom_names:
            if ql_props.name_prefix:
                lattice.name = target.name + ql_props.name_separator + ql_props.lattice_object_name
            else:
                lattice.name = ql_props.lattice_object_name  

        # Adjust lattice properties
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
        modifier = target.modifiers.new(name="Lattice", type='LATTICE') #name="Quick Lattice"
        if ql_props.custom_names:
            modifier.name = ql_props.lattice_modifier_name
        modifier.object = lattice

        # Set lattice in edit mode.
        lattice.select_set(True)
        if ql_props.enter_editmode:
            bpy.ops.object.editmode_toggle()  

        return{'FINISHED'}

    # Popup
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    # Custom draw
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

### Unregister Preferences for use in main functionality
bpy.utils.unregister_class(QL_Preferences)

##############################################
## Register/unregister classes and functions
##############################################
def register():
    bpy.utils.register_class(QL_OT_quick_lattice)
        
def unregister():
    bpy.utils.unregister_class(QL_OT_quick_lattice)