# Update 0.2
### Date: 06. 09. 2025
TFG-AR version: v0.2

Python version: 3.12.2

Changelog:
- Reading from AlloyOreInfo.txt is now context-dependent and not line-dependent.
- Everything read from AlloyOreInfo.txt is now stored as a dictionary for easier access and flexibility.
- The program now accepts 2 ores and 3 ores, instead of just 2 ores.
- Better parsing enabled me to make the written form of ratio ranges in AlloyOreInfo.txt more compact. Now, ranges have to be written in a new format (ratio_ore1 | 70%-80% or ratio_ore1 | 70-80). You can also be lazy and only place one % sign.
- OPTIMISATION: I've optimised step 1 of the algorithm. Now, it searches inside of a smaller, more confined range. This is determined by the minimum and maximum mB values for every ore that is attributed to the alloy. The program doesn't have to go through tens of thousands of combinations but probably around 100 or less.
- Small exceptions have been caught. There are still many out there.
- Added a dependency: Python (math).

# Update 0.3
### Date: 14. 09. 2025
TFG-AR version: v0.3

Python version: 3.12.2

Changelog:
- Created a GUI with PyQt6.
- Removed headless functionality (no more Terminal compatability).
- Added settings.
- Added dynamic reading and saving from and to AlloyOreInfo.txt and settings.txt. All changes are reflected in the GUI.
- Fragmented certain functions into their own .py files (modules) to avoid cycling referencing and for cleanliness.
- Added an icon for the main window and the settings window.
- Removed some unnecessary code.
- Some bugfixes.
