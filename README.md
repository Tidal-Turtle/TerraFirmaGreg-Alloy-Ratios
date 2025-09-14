This is version 0.3 of TerraFirmaGreg Alloy Ratios (TFG-AR).

Python version: Python 3.12.2

Other dependencies:
- Python libraries: math, sys, os, logging, datetime
- PyQt6 (for the GUI)

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

# How do I use it?
As of v0.3, TFG-AR is a GUI-only program (like any other good program). Hurray! There are two ways you can go about using it: 
- Simply launch the TFG-AR.exe provided in the appfiles\exe folder or 
- Use it in a debugger like Visual Studio code (still a GUI)
## TFG-AR.exe
You can find the executable file in the TerraFirmaGreg-Alloy-Ratios\appfiles\exe folder. Ignore all other files.
1) Download and unzip .zip or clone the github repository (the green button somewhere on this page)
2) Go to TerraFirmaGreg-Alloy-Ratios\appfiles\exe and click the TFG-AR.exe

If you are suspicious of .exe files (as you should be), you can build the .exe yourself. I provided a .bat (batch) file in the TerraFirmaGreg-Alloy-Ratios\appfiles folder. Before you run the batch file, make sure you have pyinstaller installed and that you add the absolute path for the icon files (they are in the images folder). For example, my path looked like this:
> C:\Programing\TerraFirmaGreg-Alloy-Ratios\images\window.ico

while yours might look like this:

> C:\Users\TidalTurtle\Downloads\TerraFirmaGreg-Alloy-Ratios\images\window.ico

So, you would have to replace the first with the second.
## Code debugger
You can also use a code debugger like Visual Studio Code (others probably work too). Simply navigate to app.py, open it in your debugger and start debugging it (in VSC this is F5 or Run > Start debugging). As long as you have Python 3.12.2 or newer and PyQt6 installed, everything should work.
## Recipe mode
As of v0.3, TFG-AR has implemented the 'Recipe mode'. Recipe mode gives you the number of ores you need to create an alloy. It takes into account the ratio ranges every ore in order for the smelted metal to turn into an alloy, the amount of mB every ore gives and the number of ingots that you want.

![Recipe mode before calculation](/images/TFG-AR_recipeMode1.png)
![Recipe mode after calculation](/images/TFG-AR_recipeMode2.png)
## Ratio mode
As of v0.3, TFG-AR has not implemented the 'Ratio mode' yet. It will work similarly to Recipe mode, but it will give you the numbers of each ore for the minimum number of alloy ingots you can make. It will take into account ratio ranges, mB/ore and the alloy name (but no number of ingots).
# How it works
As of v0.3, TFG-AR takes at least 5 essential values from the AlloyOreInfo.txt file: 
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

As of v0.3, all of these values can be added through the GUI *or* hand written into the AlloyOreInfo.txt file. You can find the min/max ratios for every alloy in the 
actual game. The mB/ore depend on the tier of ore you want to use to make the alloy. If you decide to manually edit the file, it is important that you maintain the structure, otherwise something will break. It is also important that the ratios correspond with the their respective ores. The program will still run if they don't match, but you will get the wrong results or no results at all.

Alright, you have the basic alloy information ready. What now? As of v0.3, the program can be run with a provided .exe file or through a debugger like Visual Studio Code. It cannot be run through the Terminal anymore, as the underlying code architecture has been adapted for a GUI. You can still run it in a debugger, but it cannot run headless. In the GUI, you can choose an alloy from a list on the left, change some numbers if you want and click Calculate. Calculate will dump results in the bottom for you to read. You might not get results for every combination (more on that in the 'Step 1' section).

You might encounter some edge cases and errors that I did not have the time to catch.

# The Algorithm
How TFG-AR determines the best possible combination for your usecase involves 4 steps and some math. This is not a 1:1 description of the code. The symbols and names have been changed but the process is completely identical.
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
- [4, 9] - ore3 (Bismuth).

These are the ranges in which Step 1 will operate.
## Step 1
The program starts searching through different values of n_ore1, n_ore2 and n_ore3. This is done in two loops when solving for two n_ore values, or in three loops when solving for three n_ore values. Of course, it looks through the ranges we prepared in Step 0. This is faster than starting from zero and searching through infinity or until you hit an arbitrary ceiling (as it was in v0.1). Additionally, the algorithm at this stage is looking at one more thing: the mB sum of the different combinations [n_ore1, n_ore2, n_ore3]:
1) If the sum is smaller than total_mB (defined in Step 0), we ignore the combination.
2) If the sum is in a range [total_mB, total_mB+144mB] (or 14 to 15 ingots worth of mB), we store the combination as a potential candidate.
3) If the sum is bigger than total_mB, we stop the search (stop Step 1).

Note: Sometimes, the results are not possible within the [14, 15] ingots range (or [n, n+1]). The '+1' here, I call it the 'ingots headroom'. It is currently hardcoded, but I will make this editable in the future, so that in the search for the most efficient ore combination (with the ores you have), you can extend the search. The only downside would be that you'd be making more than 14 (or more than n) ingots. The GUI will notify you if you encounter such a case.
## Step 2
We have a list of lists of [n_ore1, n_ore2, n_ore3] combinations that sum up to somewhere between 2016mB and 2160mB. But not all of them have the ratio that we need (these ratios are defined in AlloyOreInfo.txt). In this example, we have to iterate through every value in the combination and check if it is inside of the ratio range. This narrows down the list of candidate combinations to just a handful - or none :(.
## Step 3
We have the combinations and the right ratios. The last step is to see which combination wastes the least amount of metal when we make those 14 ingots. This is done by iterating through every [n_ore1, n_ore2, n_ore3] combination left, calculating the mB sum for it and substracting from it 2016mB (again, exactly 14 ingots worth of mB). The algorithm then chooses the combination with the smallest delta (difference). Usually, there is only one result, but there might be a world, where we get 2 results with the same alloy loss. This is not accounted for as of v0.3.
## Output preparation
After the main search is done, the program does some simple calculation and presents the data so you can read it (as of v0.3 in the GUI).

# Room for improvement?
There's lots. I'll list some off the top of my head. Take it as a bucket list that you can add to as well:
- QoL: Save the results to a file. Might be better than copy-pasting them manually. As of v0.3, they are presented to you in the GUI.
- QoL: Choose a save folder for AlloyOreInfo.txt, settings.txt and the to-be results.txt.
- QoL: Sort the alloy list in the GUI alphabetically (A-Z and Z-A).
- QoL: Add a remove button that removes the currently selected alloy.
- Functionality: right now, TFG-AR can only search for best combinations of two and three ores. Find a way to parse multiple (undefined) ores through the algorithm (system of n equations?). This would be especially
useful if you have more than three tiers of the same ore (16mB, 21mB, 36mB, 48mB) and you wanted to use all of them for one batch or one type of alloy. It is the next step of efficiency. For this, I need to
find a pattern, if I ever want to generalise this. Having adapted the program to three variables, I might be closer than ever.
- Functionality: Step 3 does not account for two results with the same alloy loss. Find a way to account for it.
- Functionality: Add a way for the user to edit the ingots headroom.
- Functionality: A new mode: 'Ratio mode' that will show you the minimum ratios between ores and how many ingots you get, based on the ores you have. This mode wouldn't use the number of ingots as a parameter, but as a result, along with n_ore1, n_ore2, n_ore3, etc.
