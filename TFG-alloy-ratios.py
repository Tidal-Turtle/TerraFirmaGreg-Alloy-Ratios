def getAlloyRatio(alloy_type, total_ingots, ore1_mB, ore2_mB, ore_ratio_min, ore_ratio_max):
    ingots_mB = float(144)
    total_mB = round(total_ingots*ingots_mB, 2)
    total_ingots_variation = 1

    print('You want ' + str(total_ingots) + ' ingots of ' + alloy_type + ', which is ' + str(total_mB) + 'mB in total. ' + 'You have ore1 with ' + str(ore1_mB) + 'mB/ore1 and ore2 with ' 
          + str(ore2_mB) + 'mB/ore2. You need a ratio ore1/(ore1+ore2) of ' + str(ore_ratio_min) + '%-' + str(ore_ratio_max) + '%.\n')
    
    max_tries = int(total_ingots) + 255 # arbitrary, there must be a way to calculate it dynamically based on how many mB both ores give. I did put safety measures based on ingots,
                                        # so the program should never really encounter such high iterations.

    n_combinations = []
    n_temporary = []

    ## Step 1: Find all combinations of number of each ore1 and ore2 within range [total_ingots, total_ingots_variation]
    for n_ore1 in range(max_tries):
        for n_ore2 in range(max_tries):
            if (n_ore1*ore1_mB + n_ore2*ore2_mB) > (total_ingots + total_ingots_variation)*ingots_mB:
                break
            elif (n_ore1*ore1_mB + n_ore2*ore2_mB) < total_ingots*ingots_mB:
                continue
            else:
                n_combinations.append([n_ore1, n_ore2]) 
    #print('Step 1: ' + str(n_combinations))

    ## Step 2: Find all combinations of each ore1 and ore2 within ratio ore1/(ore1+ore2) range [ore_ratio_min, ore_ratio_max]
    for row in n_combinations:
        ore_ratio = row[0]*ore1_mB/(row[0]*ore1_mB + row[1]*ore2_mB)
        if ore_ratio > ore_ratio_max/100:
            break
        elif ore_ratio < ore_ratio_min/100:
            continue
        else:
            n_temporary.append(row)
            #print(str(row) + '' + str(ore_ratio))
    n_combinations = n_temporary
    n_temporary = []
    #print('Step 2: ' + str(n_combinations))

    ## Step 3: Find the combination of ore1 and ore2 that wastes the least amount of metal (mB).
    for row in n_combinations:
        #print('Ore1: ' + str(row[0]) + ' | Ore2: ' + str(row[1]))
        delta_mB = (row[0]*ore1_mB + row[1]*ore2_mB) - total_ingots*144
        n_temporary.append(delta_mB)
    #print('Step 3: ' + str(n_temporary))

    return n_temporary, n_combinations, ore1_mB, ore2_mB, alloy_type, total_ingots
    
def printResults(n_temporary, n_combinations, ore1_mB, ore2_mB, alloy_type, total_ingots):
    ## Step 4: Prepare necessary statistics for summary for user to read
    min_delta_mB = min(n_temporary)
    n_ore1 = n_combinations[n_temporary.index(min_delta_mB)][0]
    n_ore2 = n_combinations[n_temporary.index(min_delta_mB)][1]
    final_ratio = round((n_ore1*ore1_mB/(n_ore1*ore1_mB + n_ore2*ore2_mB))*100, 2)
    total_mB_new = n_ore1*ore1_mB + n_ore2*ore2_mB
    total_ingots_new = (total_mB_new)/144

    ## Step 5: Print results
    if min_delta_mB == 0.0:
        print('RESULTS\nPerfect ratio! You won\'t waste any metal while making ' + alloy_type + '. For ' + str(total_ingots_new) + ' ingots, you will need ' + str(n_ore1) + ' of ore1 at ' + str(ore1_mB) 
          + 'mB/ore1 and ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2. The final ratio ore1/(ore1+ore2) is ' + str(final_ratio) + '%.\n')
    else:
        print('RESULTS\nWith given info, I found the most efficient combination for ' + alloy_type + '. At a new total of '+ str(total_ingots_new) +' ingots and ' + str(total_mB_new) + 
              ' mB you will have to waste ' + str(min_delta_mB) + 'mB of metal for every ' + str(total_ingots) + ' ingots. You will need ' + str(n_ore1) + ' of ore1 at ' + str(ore1_mB)
                + 'mB/ore1 and ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2. The final ratio ore1/(ore1+ore2) is ' + str(final_ratio) + '%.\n')
    print('SUMMARY | ' + alloy_type)
    print('==============================================================')
    print('Ore 1 (n): ' + str(n_ore1) + ' (' + str(ore1_mB) + 'mB/ore)')
    print('Ore 2 (n): ' + str(n_ore2) + ' (' + str(ore2_mB) + 'mB/ore)')
    print('Metal loss: ' + str(min_delta_mB) + ' mB per every ' + str(total_ingots) + ' ingots.')
    print('Final ratio (ore1/(ore1+ore2)): ' + str(final_ratio) + '%')

def getAlloyOreInfo():
    with open('AlloyOreInfo.txt') as file:
        alloy_types = [] # Keeps a list of all alloy types the user has entered into AlloyOreInfo.txt
        alloy_info = [] # Keeps a list of information about the alloy and the ores the user has entered into AlloyOreInfo.txt (everything except the alloy type)
        counter = 1
        place_of_alloy_type = 1 # This is the line number in AlloyOreInfo.txt, where "Type" appears at. 
                                # It is crucial that you update this whenever you add a line and break the pattern of the txt file
                                # The data organisation might have to change, because I feel like it isn't conducive to changes very much (it is very much line-dependent and not
                                # context-dependent). Right now, you can separate data sets by line. The code will ignore empty lines (they don't break the code).
        
        for line in file:
            #print(counter)
            line_words = line.rstrip().split(' | ')

            if line_words == ['']:
                continue
            elif (counter - place_of_alloy_type) % 5 == 0:
                #print('\n' + str(line_words))
                alloy_types.append(line_words[1])
                counter += 1
                continue
            if (counter - (place_of_alloy_type+1)) % 5 == 0 and float(line_words[1])*144 % 144 != 0:
                print("Warning! In the AlloyOreInfo.txt file, you entered a non-integer number of ingots (" + line_words[1] + 
                    "). In TFG, you can only craft full ingots, which are multiples of 144mB. Edit the file and try again.")
                break
            else:
                for i in range(len(line_words)):
                    try:
                        x = float(line_words[i])
                        alloy_info.append(x)
                    except:
                        continue
            if counter == 5:
                counter = 0
            else:
                counter += 1

    if len(alloy_types) > 1:
        print('\nAlloy types:')
        alloy_index = 0
        for alloy in alloy_types:
            print(str(alloy_index) + ' ' +  str(alloy))
            alloy_index += 1
        alloy_choice = int(input('\nI noticed there are multiple alloy types in the AlloyOreInfo.txt file. Which alloy type do you want? Type in the number correlated with the alloy above: '))
        print('You chose ' + str(alloy_types[alloy_choice]) + ' (' + str(alloy_choice) + ')' + '. Let\'s see what we can do.\n')

    if alloy_info != []:
        temp_list = []
        print(str(alloy_types[alloy_choice]) + ' info: ')
        print('==============================================================')
        alloy_type_index = alloy_types.index(alloy_types[alloy_choice])

        for i in range(alloy_type_index*5, 5 + 5*alloy_type_index):
            temp_list.append(i)
            if i % 5 == 0:
                print('Ingots (n): ' + str(alloy_info[i]))
            if i % 5 == 1:
                print('Ore 1: ' + str(alloy_info[i]) + 'mB/ore)')
            if i % 5 == 2:
                print('Ore 2: ' + str(alloy_info[i]) + 'mB/ore)')
            if i % 5 == 3:
                print('Sought ratio range (ore1/(ore1+ore2)): ' + str(alloy_info[i]) + '%-' + str(alloy_info[i+1]) + '%')

        alloy_info_index = min(temp_list)

        return alloy_types, alloy_choice, alloy_info, alloy_info_index

alloy_types, alloy_choice, alloy_info, alloy_info_index = getAlloyOreInfo()
n_temporary, n_combinations, ore1_mB, ore2_mB, alloy_type, total_ingots = getAlloyRatio(str(alloy_types[alloy_choice]), alloy_info[alloy_info_index], alloy_info[alloy_info_index+1], alloy_info[alloy_info_index+2], alloy_info[alloy_info_index+3], alloy_info[alloy_info_index+4])
printResults(n_temporary, n_combinations, ore1_mB, ore2_mB, alloy_type, total_ingots)
