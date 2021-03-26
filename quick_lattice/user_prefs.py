import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty

##############################################
#    USER PREFERENCES 
##############################################

class QL_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    popup_dialog : bpy.props.BoolProperty(
        name="Enable Popup Dialog on Creation",
        description="Enable or Disable the Popup Dialog on creation of Quick Lattice", 
        default=True
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
        box.prop(self, "popup_dialog")
        box.separator()
        box.prop(self, "default_resolution", text="Default Resolution (Restart required)")
        box.prop(self, "default_interpolation", text="Default Interpolation (Restart required)")
        box.separator()


####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(QL_Preferences) 
        
def unregister():
    bpy.utils.unregister_class(QL_Preferences)