import bpy
import re

bl_info = {
    "name": "Duplication Renamer",
    "author": "VAD",
    "version": (1, 0, 27), 
    "blender": (4, 4, 0),
    "location": "3D Viewport > Sidebar > VAD Tools",
    "description": "Custom duplication and rename logic with pattern configuration.",
    "category": "Object",
}

# --- Configuration for Keymap Management ---
UNBIND_OPERATOR_ID = "object.duplicate_move"
UNBIND_KEYMAP_NAMES = ['Object Non-modal', '3D View Generic', 'Window', 'Object Mode', 'Object']

TARGET_OPERATOR_ID = "object.ulitmate_keybind"
BIND_KEY_TYPE = 'D'
BIND_MODIFIER_CTRL = False
BIND_MODIFIER_SHIFT = True
BIND_MODIFIER_ALT = False
BIND_MODIFIER_OSKEY = False

TARGET_KEYMAP_NAME = 'Object Mode'

# Global list to store keymap items added by this addon for clean unregistration
addon_keymap_items = []

# Add-on Preferences
class DuplicationRenamerPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    duplication_pattern: bpy.props.StringProperty(name="Duplication Pattern", default="_COPY_#")
    def draw(self, context):
        layout = self.layout
        layout.label(text="Define suffix pattern for duplicated objects.")
        layout.prop(self, "duplication_pattern")
        pattern = self.duplication_pattern
        preview_name = "OriginalName"
        if '#' in pattern:
            num_hashes = pattern.count('#')
            preview_name += pattern.replace('#' * num_hashes, str(1).zfill(max(1, num_hashes)))
        else:
            preview_name += pattern + "_1"
        layout.label(text=f"Preview: {preview_name}")

# Helper: Get True Base Name
def get_true_base_name(obj_name, pattern_str):
    name_without_blender_suffix = re.sub(r'\.\d{3}$', '', obj_name)
    
    if '#' in pattern_str:
        pattern_regex_for_stripping = re.escape(pattern_str.replace('#', '')) + r'\d+'
        clean_name = re.sub(pattern_regex_for_stripping + r'$', '', name_without_blender_suffix)
    else:
        clean_name = re.sub(re.escape(pattern_str) + r'\d+$', '', name_without_blender_suffix)
        clean_name = re.sub(re.escape(pattern_str) + r'$', '', clean_name)
    
    return clean_name.strip() if clean_name and clean_name != name_without_blender_suffix else name_without_blender_suffix

# Helper: Get Next Available Number
def get_next_available_number(true_base_name, pattern_str):
    max_num = 0
    pattern_regex_search = re.escape(pattern_str)
    if '#' in pattern_regex_search:
        num_hashes = pattern_str.count('#')
        pattern_regex_search = pattern_regex_search.replace(re.escape('#' * num_hashes), r'(\d{' + str(num_hashes) + r'})')
    else:
        pattern_regex_search = re.escape(pattern_str) + r'_(\d+)'
    
    full_regex = r"^" + re.escape(true_base_name) + pattern_regex_search + r"$"
    
    for obj in bpy.context.scene.objects:
        if obj.name.startswith(true_base_name):
            match = re.match(full_regex, obj.name)
            if match:
                try: max_num = max(max_num, int(match.group(1)))
                except (ValueError, IndexError): pass
    return max_num + 1

# Operator: Duplicate and Rename
class OBJECT_OT_ultimateKeybind(bpy.types.Operator):
    bl_idname = "object.ulitmate_keybind"
    bl_label = "Ultimate Duplicate"
    bl_description = "Duplicates and renames objects with custom pattern."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        prefs_data = context.preferences.addons.get(__name__)
        if not prefs_data: return {'CANCELLED'}
        pattern = prefs_data.preferences.duplication_pattern
        
        initial_selection = list(context.selected_objects)
        if not initial_selection: return {'CANCELLED'}

        bpy.ops.object.duplicate('INVOKE_DEFAULT')
        try: bpy.ops.transform.translate('INVOKE_DEFAULT')
        except RuntimeError: pass

        for obj in context.selected_objects:
            if obj not in initial_selection:
                true_base_name_for_new_obj = get_true_base_name(obj.name, pattern)
                next_num = get_next_available_number(true_base_name_for_new_obj, pattern)
                
                new_name = true_base_name_for_new_obj
                if '#' in pattern:
                    num_hashes = pattern.count('#')
                    formatted_num = str(next_num).zfill(max(1, num_hashes))
                    new_name += pattern.replace('#' * num_hashes, formatted_num)
                else:
                    new_name += pattern + "_" + str(next_num)
                
                obj.name = new_name
        
        self.report({'INFO'}, "Ultimate Duplication executed with correct naming.")
        return {'FINISHED'}

# Panel in 3D Viewport Sidebar
class DUPLICATION_RENAME_PT_panel(bpy.types.Panel):
    bl_label = "Duplication"
    bl_idname = "DUPLICATION_RENAME_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tools"
    def draw(self, context):
        layout = self.layout
        prefs_data = context.preferences.addons.get(__name__)
        if not prefs_data: return
        prefs = prefs_data.preferences
        layout.prop(prefs, "duplication_pattern")

# Registration
def register():
    for cls in (DuplicationRenamerPreferences, OBJECT_OT_ultimateKeybind, DUPLICATION_RENAME_PT_panel):
        bpy.utils.register_class(cls)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.user # Use 'user' for persistent changes

    if kc:
        # Unbind original duplicate
        for key_map in kc.keymaps:
            if key_map.name in UNBIND_KEYMAP_NAMES:
                for km_item in key_map.keymap_items:
                    if km_item.idname == UNBIND_OPERATOR_ID and km_item.active:
                        km_item.active = False
                        addon_keymap_items.append({'keymap': key_map, 'item': km_item, 'original_active': True})
        
        # Bind our ultimate duplicate
        target_keymap = None
        for km in kc.keymaps:
            if km.name == TARGET_KEYMAP_NAME:
                target_keymap = km
                break

        if not target_keymap: # Fallback if specific keymap not found
             for km in kc.keymaps:
                if km.name == 'Window':
                    target_keymap = km
                    break
        
        if target_keymap:
            existing_binding_found = False
            for km_item in target_keymap.keymap_items:
                if (km_item.idname == TARGET_OPERATOR_ID and
                    km_item.type == BIND_KEY_TYPE and
                    km_item.shift == BIND_MODIFIER_SHIFT and
                    km_item.ctrl == BIND_MODIFIER_CTRL and
                    km_item.alt == BIND_MODIFIER_ALT and
                    km_item.oskey == BIND_MODIFIER_OSKEY):
                    
                    if not km_item.active:
                        km_item.active = True
                    existing_binding_found = True
                    addon_keymap_items.append({'keymap': target_keymap, 'item': km_item, 'original_active': False})
                    break
            
            if not existing_binding_found:
                new_km_item = target_keymap.keymap_items.new(
                    TARGET_OPERATOR_ID, 
                    type=BIND_KEY_TYPE, 
                    value='PRESS', 
                    shift=BIND_MODIFIER_SHIFT, 
                    ctrl=BIND_MODIFIER_CTRL, 
                    alt=BIND_MODIFIER_ALT,
                    oskey=BIND_MODIFIER_OSKEY
                )
                addon_keymap_items.append({'keymap': target_keymap, 'item': new_km_item, 'original_active': False})
        
        # NOTE: Removed bpy.ops.wm.save_userpref() to prevent _RestrictContext error.
        # User must manually save preferences after enabling/disabling the add-on for changes to persist.
        
# Unregistration
def unregister():
    # Restore original keymap states
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.user # Use 'user' for persistent changes (if keymaps were touched)

    if kc: # Ensure keyconfig is available during unregister
        for entry in addon_keymap_items:
            km_item = entry['item']
            # Re-fetch keymap item if it might have become invalid (e.g., if reloaded Blender)
            # This makes the unregister more robust, as direct `km_item` references might break.
            # A simple way to do this is to iterate over the keymap_items and find it again.
            # However, for simplicity and typical usage, the direct reference often suffices if Blender isn't restarted.
            
            if entry['original_active']: # If we deactivated it, reactivate it
                if km_item.rna_type and hasattr(km_item.rna_type, 'name'): # Check if item is still valid
                    km_item.active = True
            else: # If we added or activated it, remove it
                try:
                    if entry['keymap'].keymap_items: # Check if keymap_items collection exists
                        entry['keymap'].keymap_items.remove(km_item)
                except RuntimeError:
                    # Item might have been removed manually or already unlinked.
                    # Print for debugging, but don't crash.
                    # print(f"Warning: Could not remove keymap item during unregistration: {km_item.idname}")
                    pass
    addon_keymap_items.clear()
    
    # NOTE: Removed bpy.ops.wm.save_userpref() to prevent _RestrictContext error.
    # User must manually save preferences after enabling/disabling the add-on for changes to persist.

    # Unregister classes
    for cls in reversed((DuplicationRenamerPreferences, OBJECT_OT_ultimateKeybind, DUPLICATION_RENAME_PT_panel)):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    try:
        unregister()
    except RuntimeError:
        pass
    register()