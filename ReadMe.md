This is version 0.1 of TerraFirmaGreg Alloy Ratios (TFG-AR).
Python version: Python 3.12.2
Other dependencies: as of 0.1, none

You may improve the code, its functionality and otherwise change it so it fits your needs. Bug reports and suggestions are welcome.

Where does TFG-AR apply?
Right now, it applies to a Minecraft CurseForge modpack called TerraFirmaGreg, but I think you can use it in any type of Minecraft mod, where you need to smelt alloys.

What does TFG-AR do?
TFG-AR is a Python script that takes some basic information about the alloy you want to make in TerraFirmaGreg, a Minecraft Mod, and spits out the most efficient combination of ores
for that alloy. Efficient means that you lose as little as possible from leftover alloy.

Why?
I recently got into TFG and have just encountered my first alloy, Bronze. I felt that much of this modpack is going to be about ratios between different materials. Without those new
materials, there is no progress. I also did not want to do all the math in my head or on my calculator every time I needed to smelt something new (or again). Additionally, there are
many different tiers of ore, all with their own mB (millibucket) values, adding another layer of complexity to this otherwise manual process.

How it works.
As of 0.1, TFG-AR takes 6 essential values from the AlloyOreInfo.txt file: 
- Type (name of alloy), 
- Ingots (number of ingots you want)
- mB/ore1 (how many mB a single ore gives, the first one)
- mB/ore2 (how many mB a single ore gives, the second one)
- Ratio_min ore1/ore2 (the minimum ratio between total mB of ore1 and the total of mB you need for a specified number of ingots)
- Ratio_max ore1/ore2 (the maximum ratio between total mB of ore1 and the total of mB you need for a specified number of ingots)

All of these values have to be hand written into the AlloyOreInfo.txt file - it's a small workload for a big time saver. You can find the min/max ratios for every alloy in the 
actual game. The mB/ore depend on the tier of ore you want to use to make the alloy. The order of mB/ore1 and mB/ore2 inside the file is not important, BUT it is important that the 
two ratios you provide are of the ore1 - you will otherwise get the wrong calculations or none. So, if you swap the two ores, you have to substitute the two ratios with two new ones.

Alright, you have the basic alloy information ready. What now? As of 0.1, I have only tested this program inside of Visual Studio Code. It is optimised to run in this debugger, maybe
even in others, but I'm not sure. The program will communicate with you through the Terminal (should be below the code). 
When you run the code (F5 or Top Left Toolbar > Run > Start debugging), TFG-AR will read the AlloyOreInfo.txt and one of two things will happen. A) If you only have one alloy inside
the file, the program will automatically detect it and calculate it for you - everything you need to know will be written out in the Terminal. B) If you have two or more alloys
inside the file, you will be presented with a choice - choose one of the alloys you're interested in and the results will be written out in the Terminal again.

You might encounter some edge cases that I already accounted for or errors that I did not have the time to catch.

Room for improvement?
There's lots. I'll list some off the top of my head. Take it as a bucket list that you can add to as well:
- QoL: Given the choice of which alloy to choose, typing in the name of the alloy crashes the program (cause: immediate integer conversion) - find a way to process text input as well.
- QoL: Develop a rudimentary GUI (I am thinking about Tkinter, since I have used it before).
- QoL: Run as .exe (accessibility) - not everyone has Visual Studio Code installed on their system.
- QoL: Save the results to a file. Might be better than copy-pasting them manually.
- Functionality: right now, TFG-AR can only search for best combinations of two ores. Find a way to parse three ores through the algorithm.
- Functionality: right now, TFG-AR can only search for best combinations of two ores. Find a way to parse multiple (undefined) ores through the algorithm. This would be especially
useful if you have three tiers of the same ore (16mB, 21mB, 36mB) and you wanted to use all of them for one batch of alloy. It is the next step of efficiency. For this, I need to
find a pattern, if I ever want to generalise this.