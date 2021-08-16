import bpy

##############################################
#   LATTICE CLEANER OPERATOR
##############################################

class QL_OT_lattice_cleaner(bpy.types.Operator):
    """Apply lattice modifiers, and remove unused. Then delete lattice objects"""
    bl_idname = "ql.lattice_cleaner"
    bl_label = "Lattice Cleaner"  
    bl_options = {'REGISTER', 'UNDO'}

    apply_mod : bpy.props.BoolProperty(
        name = "Apply Lattice Modifiers",
        description = "Apply all Lattice Modifiers in use",
        default = True
    )
    remove_mod : bpy.props.BoolProperty(
        name = "Remove Unused Lattice Modifiers",
        description = "If a lattice modifier does not have an lattice object, it will be removed",
        default = True
    )
    delete_lattices : bpy.props.BoolProperty(
        name = "Delete Lattice Type Objects",
        description = "Delete all selected Lattice objects after apply the modifiers",
        default = True
    )

    # Prevents operator appearing in unsupported editors, and unsupported objects
    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D') and context.selected_objects:
            return True 

    ##############################################
    #   Main functionality
    ##############################################
    def execute(self, context): 

        # Apply used and remove unused lattice modifiers
        objects = context.selected_objects

        for ob in objects:
            # Set each object as active
            context.view_layer.objects.active = ob
            for mod in ob.modifiers:
                if mod.type == 'LATTICE':            
                    if mod.object:
                        if self.apply_mod:
                            bpy.ops.object.modifier_apply(modifier = mod.name)  
                    else:
                        if self.remove_mod:
                            ob.modifiers.remove(mod)

        # Remove Lattice selected objects
        if self.delete_lattices:
            objs = [ob for ob in context.selected_objects if ob.type == 'LATTICE']
            bpy.ops.object.delete({"selected_objects": objs})

        return{'FINISHED'}

    # Popup
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    # Custom draw
    def draw(self, context):
        layout = self.layout
        layout.label(text="Only affects selected objects", icon='INFO')

        box = layout.box()            
        box.prop(self, "apply_mod")
        box.prop(self, "remove_mod")
        box.prop(self, "delete_lattices")

##############################################
## REGISTER/UNREGISTER
##############################################
def register():
    bpy.utils.register_class(QL_OT_lattice_cleaner)

def unregister():
    bpy.utils.unregister_class(QL_OT_lattice_cleaner)