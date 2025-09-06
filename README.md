This is version 0.2 of TerraFirmaGreg Alloy Ratios (TFG-AR).

Python version: Python 3.12.2

Other dependencies:
- math (v0.2)

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
As of 0.2, TFG-AR takes at least 5 essential values from the AlloyOreInfo.txt file: 
- Type (name of alloy), 
- Ingots (number of ingots you want)
- mB/ore1 (how many mB a single ore gives, the first one)
- mB/ore2 (how many mB a single ore gives, the second one)
- Ratio_ore1 (the ratio range for the first ore, the second/last one is not needed - it can be calculated)

But at most 8 values:
- Type
- Ingots
- mB/ore1
- mB/ore2
- mB/ore3
- Ratio_ore1
- Ratio_ore2
- Ratio_ore3 (you can still omit the last ratio)

All of these values have to be hand written into the AlloyOreInfo.txt file - it's a small workload for a big time saver. You can find the min/max ratios for every alloy in the 
actual game. The mB/ore depend on the tier of ore you want to use to make the alloy. It is important that you maintain this structure, otherwise something will break. It is also important that the ratios correspond with the their respective ores. The program will still run if they don't match, but you will get the wrong results.

Alright, you have the basic alloy information ready. What now? As of 0.2, I have only tested this program inside of Visual Studio Code. It is optimised to run in this debugger, maybe
even in others, but I'm not sure. The program will communicate with you through the Terminal (should be below the code). 
When you run the code (F5 or Top Left Toolbar > Run > Start debugging), TFG-AR will read the AlloyOreInfo.txt and one of two things will happen. A) If you only have one alloy inside
the file, the program will automatically detect it and calculate it for you - everything you need to know will be written out in the Terminal. B) If you have two or more alloys
inside the file, you will be presented with a choice - choose one of the alloys you're interested in and the results will be written out in the Terminal again (only use numbers, not words, when typing in your answer).

If you want to calculate again or for another alloy, you'll have to stop the debugging session and start it once again.

You might encounter some edge cases and errors that I did not have the time to catch.

# The Algorithm
How TFG-AR determines the best possible combination for your usecase involves 4 steps and some math. For two ores, it is essentially a system of two equations, for three, a system of three equations. This is not a 1:1 description of the code. The symbols and names have been changed but the process is completely identical.
## Step 0 - Optimisation
Before the true search begins, the program has to optimise. Let's say you want to make 14 ingots of Bismuth Bronze. Bismuth Bronze is made from three different ores:
- Copper (50%-65%) - ore1
- Zinc (20%-30%) - ore2
- Bismuth (10%-20%) - ore3

You have raw copper ore that gives you 129mB/ore (millibuckets per ore) each, zinc (31mB/ore) and bismuth (48mB/ore). You want to know how much (n) of every ore you need for 14 ingots of Bismuth Bronze. The program will be solving for n_ore1, n_ore2 and n_ore3.

To determine a small (optimised) range in which the program should look for n_ore, the program takes advantage of the ratio ranges for each ore (they are written just above). The equation is as follows: $n \textunderscore ore1 = \frac{ratio \textunderscore ore1 \times total \textunderscore mB}{mB \textunderscore ore1}$, where $total \textunderscore mB = 14\ ingots \times 144\ mB/ingot$.

This calculation is done for both the minimum and maximum values inside the range of ratios, for *every* ore that is related to this alloy. The result is a list of lists, such as: [[7, 11], [13, 20], [4, 9]]. Every number pair corresponds to one ore:
- [7, 11] - ore1 (Copper)
- [13, 20] - ore2 (Zinc)
- [4, 9] - ore3 (Bismuth)).

These are the ranges in which Step 1 will operate.
## Step 1
The program starts searching through different values of n_ore1, n_ore2 and n_ore3. This is done in two loops when solving for two n_ore values, or in three loops when solving for three n_ore values. Of course, it looks through the ranges we prepared in Step 0. This is faster than starting from zero and searching through infinity or until you hit an arbitrary ceiling (as it was in v0.1). Additionally, the algorithm at this stage is looking at one more thing: the mB sum of the different combinations [n_ore1, n_ore2, n_ore3]:
1) If the sum is smaller than total_mB (defined in Step 0), we ignore the combination.
2) If the sum is in a range [total_mB, total_mB+144mB] (or 14 to 15 ingots worth of mB), we store the combination as a potential candidate.
3) If the sum is bigger than total_mB, we stop the search (stop Step 1).
## Step 2
We have a list of lists of [n_ore1, n_ore2, n_ore3] combinations that sum up to somewhere between 2016mB and 2160mB. But not all of them have the ratio that we need (again, these ratios are defined in AlloyOreInfo.txt). In this example, we have to iterate through every value in the combination and check if it is inside of the ratio range. This narrows down the list of candidate combinations to just a handful.
## Step 3
We have the combinations and the right ratios. The last step is to see which combination wastes the least amount of metal when we make those 14 ingots. This is done by iterating through every [n_ore1, n_ore2, n_ore3] combination left, calculating the mB sum for it and substracting from it 2016mB (again, exactly 14 ingots worth of mB). The algorithm then chooses the combination with the smallest delta (difference). Usually, there is only one result, but there might be a world, where we get 2 results with the same alloy loss. This is not accounted for as of v0.2.
## Output preparation
After the main search is done, the program does some simple calculation and presents the data so you can read it (as of v0.2 in the Debugger's Terminal).

# Room for improvement?
There's lots. I'll list some off the top of my head. Take it as a bucket list that you can add to as well:
- QoL: Given the choice of which alloy to choose, typing in the name of the alloy crashes the program (cause: immediate integer conversion) - find a way to process text input as well.
- QoL: Develop a rudimentary GUI (I am thinking about Tkinter, since I have used it before).
- QoL: Run as .exe (accessibility) - not everyone has Visual Studio Code installed on their system.
- QoL: Save the results to a file. Might be better than copy-pasting them manually.
- Functionality: right now, TFG-AR can only search for best combinations of two and three ores. Find a way to parse multiple (undefined) ores through the algorithm (system of n equations?). This would be especially
useful if you have more than three tiers of the same ore (16mB, 21mB, 36mB, 48mB) and you wanted to use all of them for one batch or one type of alloy. It is the next step of efficiency. For this, I need to
find a pattern, if I ever want to generalise this. Having adapted the program to three variables, I might be closer than ever.
- Functionality: Step 3 does not account for two results with the same alloy loss. Find a way to account for it.
