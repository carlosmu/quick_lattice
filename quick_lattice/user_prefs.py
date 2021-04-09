import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty

##############################################
#    USER PREFERENCES 
##############################################

class QL_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    popup_dialog : bpy.props.BoolProperty(
        name="Popup Dialog on lattice creation",
        description="Enable or Disable the Popup Dialog on creation of Quick Lattice", 
        default=True
    )
    enable_on_context : bpy.props.BoolProperty(
        name="Button on Context Menu",
        description="Enable or Disable Quick Lattice Button on Context Menu. For example, if you prefer a shortcut or pie menu", 
        default=True
    )
    custom_names : bpy.props.BoolProperty(
        name="Custom Names",
        description="Set custom names for lattice object and modifier", 
        default=True
    )
    name_prefix : bpy.props.BoolProperty(
        name="Object Name Prefix",
        description="For use the name of main object as lattice name prefix. Only used when you create the lattice", 
        default=False
    )
    name_separator : bpy.props.StringProperty(
        name="Separator",
        description="Separator character between prefix and name", 
        default= ".",
        maxlen= 10,
    )
    lattice_object_name : bpy.props.StringProperty(
        name="Lattice Object Name",
        description="Separator character between prefix and name", 
        default= "Quick_Lattice",
        maxlen= 32,
    )
    lattice_modifier_name : bpy.props.StringProperty(
        name="Lattice Modifier Name",
        description="Separator character between prefix and name", 
        default= "Quick_Lattice",
        maxlen= 32,
    )
     

    default_resolution : bpy.props.IntProperty(
        name="Default Lattice Resolution",
        description="Default subdivisions of the Lattice Object", 
        default= 3,
        min = 1, soft_min = 2, soft_max = 32, max =256,
    )

    default_interpolation : bpy.props.EnumProperty(
        name = "Default Lattice Interpolation",
        description = "Interpolation Type between dimension points",
        items = [
            ('KEY_LINEAR', 'Linear', ''),
            ('KEY_CARDINAL', 'Cardinal', ''),
            ('KEY_CATMULL_ROM', 'Catmull-Rom', ''),
            ('KEY_BSPLINE', 'BSpline', '')],
        default = 'KEY_BSPLINE'
    )
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = True
        box = layout.box()
        box.separator()
        box.prop(self, "enable_on_context")
        box.prop(self, "popup_dialog")
        # box.separator()
        box.prop(self, "default_resolution", text="Default Resolution (Restart required)")
        box.prop(self, "default_interpolation", text="Default Interpolation (Restart required)")
        box.separator()

        layout.use_property_split = False
        custom_names = context.preferences.addons[__package__].preferences.custom_names 
        name_prefix = context.preferences.addons[__package__].preferences.name_prefix 

        layout.prop(self, "custom_names")

        if custom_names:
            row = layout.row()            
            row.prop(self, "name_prefix")
            if name_prefix:
                row.prop(self, "name_separator")
            layout.prop(self, "lattice_object_name")
            layout.prop(self, "lattice_modifier_name")


####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(QL_Preferences) 
        
def unregister():
    bpy.utils.unregister_class(QL_Preferences)