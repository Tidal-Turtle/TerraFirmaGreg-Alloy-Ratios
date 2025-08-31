This is version 0.1 of TerraFirmaGreg Alloy Ratios (TFG-AR).

Python version: Python 3.12.2

Other dependencies: as of 0.1, none

You may improve the code, its functionality and otherwise change it so it fits your needs. Bug reports and suggestions are welcome. This stays open-source.

# Where does TFG-AR apply?
Right now, it applies to a Minecraft CurseForge modpack called TerraFirmaGreg, but I think you can use it in any type of Minecraft mod, where you need to smelt alloys.

# What does TFG-AR do?
TFG-AR is a Python script that takes some basic information about the alloy you want to make in TerraFirmaGreg, a Minecraft Mod, and spits out the most efficient combination of ores
for that alloy. Efficient means that you lose as little as possible from leftover alloy.

# Why?
I recently got into TFG and have just encountered my first alloy, Bronze. I felt that much of this modpack is going to be about ratios between different materials. Without those new
materials, there is no progress. I also did not want to do all the math in my head or on my calculator every time I needed to smelt something new (or again). Additionally, there are
many different tiers of ore, all with their own mB (millibucket) values, adding another layer of complexity to this otherwise manual process.

# How it works.
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

If you want to calculate again or for another alloy, you'll have to stop the debugging session and start it once again.

You might encounter some edge cases that I already accounted for or errors that I did not have the time to catch.

# The Algorithm
How TFG-AR determines the best possible combination for your usecase involves 3 steps and some math. For two ores, it is essentially a system of two equations. This is not a 1:1 description of the code. The symbols and names have been changed but the process is completely identical.
## Step 1
After you choose the alloy to solve for, the program starts searching through different values a and b. Value a is the amount of 'Ore 1', connected to it is c, the amount of mB (millibuckets) a single 'Ore 1' provides. Value b is similar to value a and value d is similar to value c, but they are connected to 'Ore2'. Every ingot is 144mB. 14 ingots equate to 2016mB, 15 ingots equate to 2160mB. The sum of a\*c and b\*d must be above 2016mB, but below 2160mB. The program looks through different combinations of a and b, adhering to these two rules and creates a list of lists. As of 0.1, the algorithm starts searching in a range [0 to number of ingots+255], which is arbitrary, but the program should never reach this high number of iterations. This search algorithm is not efficient and can be improved - more on this under the "Room for improvement?" section.
## Step 2
We have a list of lists of [a,b] combinations that sum up to somewhere between 2016mB and 2160mB (if we want 14 ingots of alloy, max 15). But not all of them have the a/(a+b) ratio that we need (again, this ratio is in the AlloyOreInfo.txt). Since we have a range of ratios (conditions) again, the algorithm has to iterate through all the [a,b] combinations from Step 1. It then stores only those that fall between the ratio range (e.g. 70%-80%) into a list of lists.
## Step 3
We have the combinations and the right ratios. The last step is to see which combination wastes the least amount of metal when we make those 14 ingots. This is done by iterating through every [a,b] combination, calculating the mB sum for it and substracting from it 2016mB (again, exactly 14 ingots worth of mB). The algorithm then chooses the [a,b] combination with the smallest delta (difference). Usually, there is only one result, but there might be a world, where we get 2 results with the same alloy loss. This is not accounted for as of 0.1.
## Output preparation
After the main search is done, the program does some simple calculation and presents the data so you can read it.

# Room for improvement?
There's lots. I'll list some off the top of my head. Take it as a bucket list that you can add to as well:
- QoL: Given the choice of which alloy to choose, typing in the name of the alloy crashes the program (cause: immediate integer conversion) - find a way to process text input as well.
- QoL: Develop a rudimentary GUI (I am thinking about Tkinter, since I have used it before).
- QoL: Run as .exe (accessibility) - not everyone has Visual Studio Code installed on their system.
- QoL: Save the results to a file. Might be better than copy-pasting them manually.
- Functionality: right now, TFG-AR can only search for best combinations of two ores. Find a way to parse three ores through the algorithm (system of three equations?).
- Functionality: right now, TFG-AR can only search for best combinations of two ores. Find a way to parse multiple (undefined) ores through the algorithm (system of n equations?). This would be especially
useful if you have three tiers of the same ore (16mB, 21mB, 36mB) and you wanted to use all of them for one batch of alloy. It is the next step of efficiency. For this, I need to
find a pattern, if I ever want to generalise this.
- Functionality: Step 3 does not account for two results with the same alloy loss. Find a way to account for it.
- Efficiency: make the Step 1 algorithm more effecient. As of 0.1, the program in theory iterates from 0 to 255+whatever the number of ingots the AlloyOreInfo.txt has written down. In practice it always starts at 0 but should never reach 255, because of other limitations (if statements). But this is hardcoded, non-dynamic and less efficient than I know it can be. I propose an algorithm where you search in halves and check the algorithm conditions. If they're not met, take the next half and so on. Not sure how this sort is called but I have an idea for it. How do you adapt this for systems of more than two equations? 
