import bpy

##############################################
## DRAW MENU BUTTON
##############################################
def draw_quicklattice_menu(self, context):
    # Popup user preference
    popup_dialog = context.preferences.addons[__package__].preferences.popup_dialog    
    enable_on_context = context.preferences.addons[__package__].preferences.enable_on_context 

    layout = self.layout     
    # if context.selected_objects: # Menu elements only on selected objects
    if enable_on_context:
        if popup_dialog: # If True show popup_dialog        
            layout.operator_context = "INVOKE_DEFAULT"
        layout.operator("ql.quick_lattice", icon='LATTICE_DATA')  # Create Quick Lattice       
        layout.separator()   


##############################################
## Register/unregister classes and functions
##############################################
def register():
    bpy.types.VIEW3D_MT_object_context_menu.prepend(draw_quicklattice_menu) 
        
def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_quicklattice_menu) 