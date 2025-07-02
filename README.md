
# Custom Duplicate for Blender: Enhanced Prefix Management

## Streamline Object Naming for Improved Efficiency.

Blender's default `.001` suffixes can lead to cluttered scenes and less intuitive object management. This add-on addresses the need for a more organized and intuitive workflow by reassigning the `Shift+D` keybind to a custom function. This function allows users to define their own prefixes for duplicated objects, thereby enhancing scene organization.

This add-on aims to transform object naming from a source of clutter into a streamlined, organized process, providing a core utility that optimizes your creative workflow.

---

### Features

* **Customizable Prefixes:** Eliminate default `.001` suffixes. Define custom prefixes (e.g., `_copy`, `-instance`, `_clone_`) for duplicated objects.

* **Seamless Integration:** Replaces the default `Shift+D` keybind, ensuring a natural and familiar workflow.

* **Clean Scene Management:** Facilitates a tidy Outliner and improves object identification.

* **Lightweight & Efficient:** Designed with a minimal footprint for optimal performance.

---

### Installation

1.  **Download:** Obtain the `custom_duplicate.py` file from this repository.

2.  **Blender Preferences:** In Blender, navigate to `Edit > Preferences > Add-ons`.

3.  **Install:** Click `Install...` and select the downloaded `custom_duplicate.py` file.

4.  **Enable:** Activate the add-on by checking the box next to "Object: Custom Duplicate Prefix."

---

### Usage

Upon successful installation and activation, the add-on is fully operational.

1.  **Set Your Prefix:**

    * In Blender's 3D Viewport, press `N` to open the N-Panel (Sidebar).

    * Navigate to the **"Tools"** tab.

    * Locate the **"Custom Duplicate"** panel.

    * Enter your preferred prefix in the "Duplicate Prefix" text field (e.g., `_variant_`).

2.  **Duplicate with `Shift+D`:**

    * Select the object(s) intended for duplication.

    * Press `Shift+D`. The newly duplicated object will now incorporate the custom prefix (e.g., `Cube_variant_001`, `Sphere_variant_002`).

**Note:** If the prefix field remains empty, the add-on will default to a simple incrementing number without any specific prefix, maintaining a similar behavior to Blender's default but under the management of this add-on.

---

### How It Works (Core Functionality)

This add-on functions by intercepting the standard `object.duplicate_move` operator. It first unregisters Blender's default `Shift+D` keymap entry for duplication. Subsequently, it registers its own custom operator, `object.custom_duplicate`, and assigns it to `Shift+D`.

When `Shift+D` is activated, the custom operator performs the following steps:

1.  Retrieves the user-defined prefix from the add-on's properties.

2.  Iterates through all selected objects.

3.  For each object, it executes a standard duplication.

4.  Critically, it then renames the newly duplicated object, integrating your custom prefix and ensuring a unique numerical suffix to prevent naming conflicts.

This methodology ensures compatibility and a familiar user experience while providing enhanced customization capabilities.

---

### Why This Add-on?

In the complex environment of 3D modeling, effective organization is paramount. The default `.001` naming convention, while functional, can often contribute to visual clutter and hinder efficient object identification. This add-on provides a solution to enhance efficiency. It empowers users to establish custom naming standards, transforming a minor inconvenience into a significant quality-of-life improvement. This initiative is about gaining control over the naming process, moving beyond default settings, and cultivating a workflow that precisely aligns with your creative vision.

---

### Contributing

Contributions are welcomed. Should you have suggestions for improvements, bug reports, or wish to add new features, please submit an issue or a pull request.

---

### License

This project is licensed under the MIT License - refer to the [LICENSE](https://www.google.com/search?q=LICENSE) file for comprehensive details.

---
