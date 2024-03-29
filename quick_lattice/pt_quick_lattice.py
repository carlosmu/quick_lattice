import bpy

class QL_PT_quick_latice(bpy.types.Panel):
    bl_label = "Quick Lattice"
    bl_idname = "QL_PT_QuickLattice"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
 
    def draw(self,context):
        layout = self.layout
        popup_dialog = context.preferences.addons[__package__].preferences.popup_dialog
        if context.selected_objects:
            if context.active_object.type in ['MESH','CURVE','SURFACE','FONT', 'LATTICE']:
                if context.object.mode == 'OBJECT':
                    if not popup_dialog: # If True show popup_dialog        
                        layout.operator_context = "EXEC_DEFAULT"
                    layout.operator("ql.quick_lattice", icon='LATTICE_DATA')
                    layout.operator("ql.lattice_cleaner", icon='SHADERFX')
                else:
                    
                    layout.label(text="Buttons only in Object Mode", icon="INFO")
            else:
                layout.label(text="Object Type not supported")
        else: 
            layout.label(text="No objects selected", icon="INFO")




##############################################
## Register/unregister classes and functions
##############################################
def register():
    bpy.utils.register_class(QL_PT_quick_latice)
        
def unregister():
    bpy.utils.unregister_class(QL_PT_quick_latice)