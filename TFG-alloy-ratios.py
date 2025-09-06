import math

def getAlloyRatio(alloy_type, alloy_info_chosen):
    total_ingots = float(alloy_info_chosen.get('Ingots'))
    ore_mB_list = alloy_info_chosen.get('mB/ore')
    ore_ratio_list = alloy_info_chosen.get('ratio_ore')

    #total_ingots, ore1_mB, ore2_mB, ore_ratio_min, ore_ratio_max
    ingots_mB = float(144)
    total_mB = round(total_ingots*ingots_mB, 2)
    total_ingots_variation = 1

    if len(ore_mB_list) == 2:
        try:
            ore1_mB = int(ore_mB_list[0])
            ore2_mB = int(ore_mB_list[1])
        except:
            print('Error: Could not convert alloy info to integer. Please, check the AlloyOreInfo.txt and make sure numbers are where they should be and that there are no accidental'
            'strings next to them, such as 36w, 10O, 4S, etc.')
            quit()
        try:
            ore_ratio_min = int(ore_ratio_list[0][0])
            ore_ratio_max = int(ore_ratio_list[0][1])
        except:
            print('Error: For the chosen ' + alloy_type + ', I require ' + str(len(ore_mB_list)) + ' values of mB/ore and at least ' + str(len(ore_mB_list)-1) + ' ratio range. '
            'Please, edit the AlloyOreInfo.txt file and try again.')
            quit()
        print('You want ' + str(total_ingots) + ' ingots of ' + alloy_type + ', which is ' + str(total_mB) + 'mB in total. ' + 'You have ore1 with ' + str(ore1_mB) + 'mB/ore1 and ore2 with ' 
            + str(ore2_mB) + 'mB/ore2. You need a ratio ore1/(ore1+ore2) of ' + str(ore_ratio_min) + '%-' + str(ore_ratio_max) + '%.\n')
    elif len(ore_mB_list) == 3:
        try:
            ore1_mB = int(ore_mB_list[0])
            ore2_mB = int(ore_mB_list[1])
            ore3_mB = int(ore_mB_list[2])
        except:
            print('Error: Could not convert alloy info to integer. Please, check the AlloyOreInfo.txt file and make sure numbers are where they should be and that there are no ' \
            'accidental strings next to them, such as 36w, 10O, 4S, etc.')
            quit()
        try:
            ore1_ratio_min = int(ore_ratio_list[0][0])
            ore1_ratio_max = int(ore_ratio_list[0][1])
            ore2_ratio_min = int(ore_ratio_list[1][0])
            ore2_ratio_max = int(ore_ratio_list[1][1])
        except:
            print('Error: For the chosen ' + alloy_type + ', I require ' + str(len(ore_mB_list)) + ' values of mB/ore and at least ' + str(len(ore_mB_list)-1) + ' ratio ranges. '
            'Please, edit the AlloyOreInfo.txt file and try again.')
            quit()
    

    if len(ore_mB_list) == 2:
        max_tries = int(total_ingots) + 255 # arbitrary, there must be a way to calculate it dynamically based on how many mB both ores give. I did put safety measures based on ingots,
                                            # so the program should never really encounter such high iterations.
        n_combinations = []
        n_temporary = []
        ore_mB_minmax_list = []

        ## Step 0: Create a list to limit the search area for Step 1. Optimisation!
        print(ore_ratio_list)
        print(ore_mB_list)
        for i in range(len(ore_mB_list)):
            if i < 1:
                ore_mB_min = math.floor((int(ore_ratio_list[i][0])*total_mB)/(int(ore_mB_list[i])*100))
                ore_mB_max = math.ceil((int(ore_ratio_list[i][1])*total_mB)/(int(ore_mB_list[i])*100))
            elif i == 1:
                ore_mB_min = math.floor(((100-int(ore_ratio_list[i-1][1]))*total_mB)/(int(ore_mB_list[i])*100))
                ore_mB_max = math.ceil(((100-int(ore_ratio_list[i-1][0]))*total_mB)/(int(ore_mB_list[i])*100)) 
            ore_mB_minmax_list.append([ore_mB_min, ore_mB_max])
        """ if len(ore_ratio_list) != 2:
            ore_mB_min = math.floor((int((100-ore_ratio_list[0][0]))*total_mB)/(int(ore_mB_list[0])*100))
            ore_mB_max = math.ceil((int((100-ore_ratio_list[0][1]))*total_mB)/(int(ore_mB_list[0])*100))
            ore_mB_minmax_list.append([ore_mB_min, ore_mB_max]) """
        print(ore_mB_minmax_list)


        ## Step 1: Find all combinations of number of each ore1 and ore2 within range [total_ingots, total_ingots_variation]
        for n_ore1 in range(ore_mB_minmax_list[0][0], ore_mB_minmax_list[0][1]):
            for n_ore2 in range(ore_mB_minmax_list[1][0], ore_mB_minmax_list[1][1]):
                if (n_ore1*ore1_mB + n_ore2*ore2_mB) > (total_ingots + total_ingots_variation)*ingots_mB:
                    break
                elif (n_ore1*ore1_mB + n_ore2*ore2_mB) < total_ingots*ingots_mB:
                    continue
                else:
                    n_combinations.append([n_ore1, n_ore2])
        #print('Step 1: ' + str(n_combinations))

        ## Step 2: Find all combinations of each ore1 and ore2 within ratio ore1/(ore1+ore2) range [ore1_ratio_min, ore1_ratio_max]
        for row in n_combinations:
            ore1_ratio = row[0]*ore1_mB/(row[0]*ore1_mB + row[1]*ore2_mB)
            if ore1_ratio > ore_ratio_max/100:
                break
            elif ore1_ratio < ore_ratio_min/100:
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
        return n_temporary, n_combinations, ore_mB_list, alloy_type, total_ingots
    elif len(ore_mB_list) == 3:
        n_combinations = []
        n_temporary = []
        ore_mB_minmax_list = []

        ## Step 0: Create a list to limit the search area for Step 1. Optimisation!
        for i in range(len(ore_ratio_list)):
            ore_mB_min = math.floor((int(ore_ratio_list[i][0])*total_mB)/(int(ore_mB_list[i])*100))
            if ore_mB_min < 0:
                ore_mB_min = 0
            ore_mB_max = math.ceil((int(ore_ratio_list[i][1])*total_mB)/(int(ore_mB_list[i])*100))
            ore_mB_minmax_list.append([ore_mB_min, ore_mB_max])

        print(ore_mB_minmax_list)

        ## Step 1: Find all combinations of number of each ore1, ore2 and ore3 within range [total_ingots, total_ingots_variation]
        for n_ore1 in range(ore_mB_minmax_list[0][0], ore_mB_minmax_list[0][1]):
            for n_ore2 in range(ore_mB_minmax_list[1][0], ore_mB_minmax_list[1][1]):
                for n_ore3 in range(ore_mB_minmax_list[2][0], ore_mB_minmax_list[2][1]):
                    if (n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB) > (total_ingots + total_ingots_variation)*ingots_mB:
                        break
                    elif (n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB) < total_ingots*ingots_mB:
                        continue
                    else:
                        n_combinations.append([n_ore1, n_ore2, n_ore3])
        #print('Step 1: ' + str(n_combinations))

        ## Step 2: Find all combinations of each ore1, ore2 and ore3 within ratio ore1/(ore1+ore2+ore3) range [ore1_ratio_min, ore1_ratio_max] and ore2/(ore1+ore2+ore3) range [ore2_ratio_min, ore2_ratio_max]
        for row in n_combinations:
            ore1_ratio = row[0]*ore1_mB/(row[0]*ore1_mB + row[1]*ore2_mB + row[2]*ore3_mB)
            ore2_ratio = row[1]*ore2_mB/(row[0]*ore1_mB + row[1]*ore2_mB + row[2]*ore3_mB)
            if ore1_ratio > ore1_ratio_max/100 or ore2_ratio > ore2_ratio_max/100:
                break
            elif ore1_ratio < ore1_ratio_min/100 or ore2_ratio < ore2_ratio_min/100:
                continue
            else:
                n_temporary.append(row)
                #print(str(row) + '' + str(ore_ratio))
        n_combinations = n_temporary
        n_temporary = []
        #print('Step 2: ' + str(n_combinations))

        ## Step 3: Find the combination of ore1, ore2 and ore3 that wastes the least amount of metal (mB).
        for row in n_combinations:
            #print('Ore1: ' + str(row[0]) + ' | Ore2: ' + str(row[1]))
            delta_mB = (row[0]*ore1_mB + row[1]*ore2_mB + row[2]*ore3_mB) - total_ingots*144
            n_temporary.append(delta_mB)
        #print('Step 3: ' + str(n_temporary))

        return n_temporary, n_combinations, ore_mB_list, alloy_type, total_ingots
    
def printResults(n_temporary, n_combinations, ore_mB_list, alloy_type, total_ingots):
    ## Step 4: Prepare necessary statistics for summary for user to read
    try:
        min_delta_mB = min(n_temporary)
    except:
        if total_ingots == 1:
            print('Error (empty list): Somehow, I wasn\'t able to find any efficient combination for ' + str(total_ingots) + ' ingot of ' + str(alloy_type) + '.')
            quit()
        else:
            print('Error (empty list): Somehow, I wasn\'t able to find any efficient combination for ' + str(total_ingots) + ' ingots of ' + str(alloy_type) + '.')
            quit()

    if len(ore_mB_list) == 2:
        n_ore1 = n_combinations[n_temporary.index(min_delta_mB)][0]
        n_ore2 = n_combinations[n_temporary.index(min_delta_mB)][1]
        ore1_mB = int(ore_mB_list[0])
        ore2_mB = int(ore_mB_list[1])
        final_ratio = round((n_ore1*ore1_mB/(n_ore1*ore1_mB + n_ore2*ore2_mB))*100, 2)
        total_mB_new = n_ore1*ore1_mB + n_ore2*ore2_mB
    elif len(ore_mB_list) == 3:
        n_ore1 = n_combinations[n_temporary.index(min_delta_mB)][0]
        n_ore2 = n_combinations[n_temporary.index(min_delta_mB)][1]
        n_ore3 = n_combinations[n_temporary.index(min_delta_mB)][2]
        ore1_mB = int(ore_mB_list[0])
        ore2_mB = int(ore_mB_list[1])
        ore3_mB = int(ore_mB_list[2])
        final_ratio1 = round((n_ore1*ore1_mB/(n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB))*100, 2)
        final_ratio2 = round((n_ore2*ore2_mB/(n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB))*100, 2)
        final_ratio3 = round((n_ore3*ore3_mB/(n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB))*100, 2)
        total_mB_new = n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB
    total_ingots_new = (total_mB_new)/144

    ## Step 5: Print results
    if len(ore_mB_list) == 2:
        if min_delta_mB == 0.0:
            print('\nRESULTS\nPerfect ratio! You won\'t waste any metal while making ' + alloy_type + '. For ' + str(total_ingots_new) + ' ingots, you will need ' + str(n_ore1) + 
                  ' of ore1 at ' + str(ore1_mB) + 'mB/ore1 and ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2.')
        else:
            print('\nRESULTS\nWith given info, I found the most efficient combination for ' + alloy_type + '. At a new total of '+ str(total_ingots_new) +' ingots and ' 
                  + str(total_mB_new) + ' mB you will have to waste ' + str(min_delta_mB) + 'mB of metal for every ' + str(total_ingots) + ' ingots. You will need ' + 
                  str(n_ore1) + ' of ore1 at ' + str(ore1_mB) + 'mB/ore1 and ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2.')
        print('\nSUMMARY | ' + alloy_type)
        print('==============================================================')
        if min_delta_mB == 0.0:
            print('Ingots (n): ' + str(total_ingots))
        else:
            print('Ingots (n, rounded down): ' + str(round(total_ingots_new, 0)))
        print('Ore 1 (n): ' + str(n_ore1) + ' (' + str(ore1_mB) + 'mB/ore)')
        print('Ore 2 (n): ' + str(n_ore2) + ' (' + str(ore2_mB) + 'mB/ore)')
        print('Metal loss: ' + str(min_delta_mB) + ' mB per every ' + str(total_ingots) + ' ingots.')
        print('Final ratio (ore1)/(ore1+ore2)): ' + str(final_ratio) + '%')
        print('Final ratio (ore2)/(ore1+ore2)): ' + str(round(100-final_ratio, 2)) + '%')
    elif len(ore_mB_list) == 3:
        if min_delta_mB == 0.0:
            print('\nRESULTS\nPerfect ratio! You won\'t waste any metal while making ' + alloy_type + '. For ' + str(total_ingots_new) + ' ingots, you will need ' + str(n_ore1) +
                  ' of ore1 at ' + str(ore1_mB) + 'mB/ore1, ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2 and ' + str(n_ore3) + ' of ore3 at ' + str(ore3_mB) + 'mB/ore3.')
        else:
            print('\nRESULTS\nWith given info, I found the most efficient combination for ' + alloy_type + '. At a new total of '+ str(total_ingots_new) +' ingots and ' + 
                  str(total_mB_new) + ' mB you will have to waste ' + str(min_delta_mB) + 'mB of metal for every ' + str(round(total_ingots_new, 0)) + ' ingots. You will need ' + 
                  str(n_ore1) + ' of ore1 at ' + str(ore1_mB) + 'mB/ore1, ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2 and ' + str(n_ore3) + ' of ore3 at ' + 
                  str(ore3_mB) + 'mB/ore3. ')
        print('\nSUMMARY | ' + alloy_type)
        print('==============================================================')
        if min_delta_mB == 0.0:
            print('Ingots (n): ' + str(total_ingots))
        else:
            print('Ingots (n, rounded down): ' + str(round(total_ingots_new, 0)))
        print('Ore 1 (n): ' + str(n_ore1) + ' (' + str(ore1_mB) + 'mB/ore)')
        print('Ore 2 (n): ' + str(n_ore2) + ' (' + str(ore2_mB) + 'mB/ore)')
        print('Ore 3 (n): ' + str(n_ore3) + ' (' + str(ore3_mB) + 'mB/ore)')
        print('Metal loss: ' + str(min_delta_mB) + ' mB per every ' + str(total_ingots) + ' ingots.')
        print('Final ratio (ore1)/(ore1+ore2+ore3)): ' + str(final_ratio1) + '%')
        print('Final ratio (ore2)/(ore1+ore2+ore3)): ' + str(final_ratio2) + '%')
        print('Final ratio (ore3)/(ore1+ore2+ore3)): ' + str(final_ratio3) + '%')

def getAlloyOreInfo():
    with open('AlloyOreInfo.txt') as file:
        alloy_dict = {}
        empty_line_counter = 0
        ore_counter = 0
        ore_ratio_counter = 0
        alloy_type_list = []
        ore_temp = []
        ratio_buffer = []
        
        for line in file:
            line_words = line.rstrip().split(' | ')

            if line_words == ['']:
                empty_line_counter = 0
                ore_counter = 0
                ore_ratio_counter = 0
                alloy_type_list = []
                ore_temp = []
                ratio_buffer = []
                continue
            elif line_words[0] == 'Type':
                empty_line_counter += 1
                try:
                    int(line_words[1])
                    print("Error: The alloy 'Type' in AlloyOreInfo.txt must be a string. You have typed in a variable of type " + str(type(int(line_words[1]))) + " ('" + 
                          str(line_words[1]) + "'). Please, check the file and try again.")
                    break
                except:
                    if len(alloy_type_list) > 1:
                        print('Error: You cannot have two succesive alloy types without the basic information about them. Check the AlloyOreInfo.txt file and add the potentially ' \
                        'missing components: Ingots, mB/ore1, mB/ore2, mB/ore3, ..., ratio_ore1, ratio_ore2, ...')
                        break
                    else:
                        alloy_dict[line_words[1]] = {}
                        alloy_type_list.append(line_words[1])
            elif line_words[0] == 'Ingots':
                alloy_dict[alloy_type_list[0]].update({line_words[0]: line_words[1]})
            elif line_words[0] == ('mB/ore' + str(ore_counter+1)) and empty_line_counter != 0:
                ore_counter += 1
                ore_temp.append(line_words[1])
                alloy_dict[alloy_type_list[0]].update({'mB/ore': ore_temp})
            elif line_words[0] == ('ratio_ore' + str(ore_ratio_counter+1)) and empty_line_counter != 0:
                ore_ratio_counter += 1
                ratio_temp = line_words[1].split('-')

                if '%' in ratio_temp[0] or ratio_temp[1]:
                    for i in range(len(ratio_temp)):
                        ratio_temp[i] = ratio_temp[i].removesuffix('%')

                ratio_buffer.append(ratio_temp)
                alloy_dict[alloy_type_list[0]].update({'ratio_ore': ratio_buffer})

        alloy_types = list(alloy_dict.keys())   # Converts the view object dict.keys to a list. It doesn't update with the dictionary as the view object would, but I can manipulate
                                                # the list more than the dictionary.
        if len(alloy_types) < 1:
            print('There are no alloys to choose from. Please, add at least one alloy and its corresponding information '
            '(Ingots, mB/ore1, mB/ore2, mB/ore3, ..., ratio_ore1, ratio_ore2, ...) to the AlloyOreInfo.txt file.')
        elif len(alloy_types) == 1:
            alloy_choice = 0
            print('I found only one alloy in the AlloyOreInfo.txt file (' + alloy_types[0] + '). Let\'s see what we can do.\n')
        else:
            print('\nAlloy types:')
            alloy_index = 0
            
            for alloy in alloy_types:
                print(str(alloy_index) + ' ' +  str(alloy))
                alloy_index += 1
            
            alloy_choice = int(input('\nI noticed there are multiple alloy types in the AlloyOreInfo.txt file. Which alloy type do you want? Type in the number correlated with the alloy above: '))
            print('You chose ' + str(alloy_types[alloy_choice]) + ' (' + str(alloy_choice) + ')' + '. Let\'s see what we can do.\n')

        alloy_info_chosen = alloy_dict.get(alloy_types[alloy_choice])

        # Check if there is a ratio range missing (one less than mB/ore entries). If yes, calculate the range. 
        # This is purely cosmetic and is not needed for the functionality of the program.
        if (len(alloy_dict[alloy_types[alloy_choice]].get('mB/ore')) - len(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore'))) == 1:
            print('There\'s ' + str(len(alloy_dict[alloy_types[alloy_choice]].get('mB/ore')) - len(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore'))) + 
                  ' less ratio range (' + str(len(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore'))) + ') than ores (' +
                  str(len(alloy_dict[alloy_types[alloy_choice]].get('mB/ore'))) + ') in the AlloyOreInfo.txt file for this alloy. Filling in the last ratio range automatically.')
            ore_min_temp = str(100-int(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore')[-1][1]))
            ore_max_temp = str(100-int(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore')[-1][0]))
            ratio_buffer = []
            ratio_buffer = alloy_dict[alloy_types[alloy_choice]].get('ratio_ore')
            ratio_buffer.append([ore_min_temp, ore_max_temp])
            alloy_dict[alloy_types[alloy_choice]].update({'ratio_ore': ratio_buffer})

        print('\n' + str(alloy_types[alloy_choice]) + ' info: ')
        print('==============================================================')
        print('Ingots (n): ' + alloy_info_chosen.get("Ingots"))
        for i in range(len(alloy_info_chosen.get("mB/ore"))):
            print('Ore ' + str(i+1) + ': ' + str(alloy_info_chosen.get("mB/ore")[i]) + 'mB/ore')
        if len(alloy_info_chosen.get("mB/ore")) == 2:
            for i in range(len(alloy_info_chosen.get("ratio_ore"))):
                print('Sought ratio range (ore' + str(i+1) + ')/(ore1+ore2)): ' + str(alloy_info_chosen.get("ratio_ore")[i][0]) + '%-' + str(alloy_info_chosen.get("ratio_ore")[i][1]) + '%')         
        elif len(alloy_info_chosen.get("mB/ore")) == 3:
            for i in range(len(alloy_info_chosen.get("ratio_ore"))):
                print('Sought ratio range (ore' + str(i+1) + ')/(ore1+ore2+ore3)): ' + str(alloy_info_chosen.get("ratio_ore")[i][0]) + '%-' + str(alloy_info_chosen.get("ratio_ore")[i][1]) + '%')

        return alloy_types[alloy_choice], alloy_info_chosen

alloy_type, alloy_info_chosen = getAlloyOreInfo()
n_temporary, n_combinations, ore_mB_list, alloy_type, total_ingots = getAlloyRatio(alloy_type, alloy_info_chosen)
printResults(n_temporary, n_combinations, ore_mB_list, alloy_type, total_ingots)