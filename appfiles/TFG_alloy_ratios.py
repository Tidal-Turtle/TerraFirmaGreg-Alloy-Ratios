import math
from handleInfoErrors import handleInfo, handleError, initLogFile

global dir_name
dir_name = 'TFG'

def getAlloyRatio(alloy_type, alloy_info_chosen):
    info_msg = getAlloyRatio.__name__ + '() function called.'
    handleInfo(info_msg, dir_name)

    total_ingots = float(alloy_info_chosen.get('Ingots'))
    ore_mB_list = alloy_info_chosen.get('mB/ore')
    ore_ratio_list = alloy_info_chosen.get('ratio_ore')

    ingots_mB = float(144)
    total_mB = round(total_ingots*ingots_mB, 2)
    total_ingots_variation = 1

    print(ore_ratio_list)

    for i, ore in enumerate(ore_ratio_list):
        for j, string in enumerate(ore_ratio_list[i]):
            if ',' in string:
                ore_ratio_list[i][j] = string.replace(',', '.')

    if len(ore_mB_list) == 2:
            ore1_mB = int(ore_mB_list[0])
            ore2_mB = int(ore_mB_list[1])
            ore_ratio_min = float(ore_ratio_list[0][0])
            ore_ratio_max = float(ore_ratio_list[0][1])
    elif len(ore_mB_list) == 3:
            ore1_mB = int(ore_mB_list[0])
            ore2_mB = int(ore_mB_list[1])
            ore3_mB = int(ore_mB_list[2])
            ore1_ratio_min = float(ore_ratio_list[0][0])
            ore1_ratio_max = float(ore_ratio_list[0][1])
            ore2_ratio_min = float(ore_ratio_list[1][0])
            ore2_ratio_max = float(ore_ratio_list[1][1])

    if len(ore_mB_list) == 2:
        n_combinations = []
        n_temporary = []
        ore_mB_minmax_list = []

        ## Step 0: Create a list to limit the search area for Step 1. Optimisation!
        print(ore_ratio_list)
        print(ore_mB_list)
        for i in range(len(ore_mB_list)):
            if i < 1:
                ore_mB_min = math.floor((float(ore_ratio_list[i][0])*total_mB)/(int(ore_mB_list[i])*100))
                ore_mB_max = math.ceil((float(ore_ratio_list[i][1])*total_mB)/(int(ore_mB_list[i])*100))
            elif i == 1:
                ore_mB_min = math.floor(((100-float(ore_ratio_list[i-1][1]))*total_mB)/(int(ore_mB_list[i])*100))
                ore_mB_max = math.ceil(((100-float(ore_ratio_list[i-1][0]))*total_mB)/(int(ore_mB_list[i])*100)) 
            ore_mB_minmax_list.append([ore_mB_min, ore_mB_max])
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
        info_msg = 'End of ' + getAlloyRatio.__name__ + '() function.'
        handleInfo(info_msg, dir_name)
        return printResults(n_temporary, n_combinations, ore_mB_list, alloy_type, total_ingots)
    elif len(ore_mB_list) == 3:
        n_combinations = []
        n_temporary = []
        ore_mB_minmax_list = []

        ## Step 0: Create a list to limit the search area for Step 1. Optimisation!
        for i in range(len(ore_ratio_list)):
            ore_mB_min = math.floor((float(ore_ratio_list[i][0])*total_mB)/(int(ore_mB_list[i])*100))
            if ore_mB_min < 0:
                ore_mB_min = 0
            ore_mB_max = math.ceil((float(ore_ratio_list[i][1])*total_mB)/(int(ore_mB_list[i])*100))
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

        info_msg = 'End of ' + getAlloyRatio.__name__ + '() function.'
        handleInfo(info_msg, dir_name)
        return printResults(n_temporary, n_combinations, ore_mB_list, alloy_type, total_ingots)
    
def printResults(n_temporary, n_combinations, ore_mB_list, alloy_type, total_ingots):
    info_msg = printResults.__name__ + '() function called.'
    handleInfo(info_msg, dir_name)
    alloy_results_dict = {}
    ## Step 4: Prepare necessary statistics for summary for user to read
    try:
        min_delta_mB = min(n_temporary)
    except:
        if total_ingots == 1:
            err_msg = 'Error (empty list): Somehow, I wasn\'t able to find any efficient combination for ' + str(total_ingots) + ' ingot of ' + str(alloy_type) + '.'
            print(err_msg, dir_name)
            handleError(err_msg, dir_name)
        else:
            err_msg = 'Error (empty list): Somehow, I wasn\'t able to find any efficient combination for ' + str(total_ingots) + ' ingots of ' + str(alloy_type) + '.'
            handleError(err_msg, dir_name)
        return err_msg, dir_name

    if len(ore_mB_list) == 2:
        n_ore1 = n_combinations[n_temporary.index(min_delta_mB)][0]
        n_ore2 = n_combinations[n_temporary.index(min_delta_mB)][1]
        n_ore_list = [str(n_ore1), str(n_ore2)]
        ore1_mB = int(ore_mB_list[0])
        ore2_mB = int(ore_mB_list[1])
        final_ratio1 = round((n_ore1*ore1_mB/(n_ore1*ore1_mB + n_ore2*ore2_mB))*100, 2)
        final_ratio2 = round(100-final_ratio1, 2)
        print(final_ratio1, final_ratio2)
        final_ratio_list = ['{:.2f}'.format(final_ratio1), '{:.2f}'.format(final_ratio2)]
        total_mB_new = n_ore1*ore1_mB + n_ore2*ore2_mB
    elif len(ore_mB_list) == 3:
        n_ore1 = n_combinations[n_temporary.index(min_delta_mB)][0]
        n_ore2 = n_combinations[n_temporary.index(min_delta_mB)][1]
        n_ore3 = n_combinations[n_temporary.index(min_delta_mB)][2]
        n_ore_list = [str(n_ore1), str(n_ore2), str(n_ore3)]
        ore1_mB = int(ore_mB_list[0])
        ore2_mB = int(ore_mB_list[1])
        ore3_mB = int(ore_mB_list[2])
        final_ratio1 = round((n_ore1*ore1_mB/(n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB))*100, 2)
        final_ratio2 = round((n_ore2*ore2_mB/(n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB))*100, 2)
        final_ratio3 = round((n_ore3*ore3_mB/(n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB))*100, 2)
        final_ratio_list = ['{:.2f}'.format(final_ratio1), '{:.2f}'.format(final_ratio2), '{:.2f}'.format(final_ratio3)]
        total_mB_new = n_ore1*ore1_mB + n_ore2*ore2_mB + n_ore3*ore3_mB
    total_ingots_new = (total_mB_new)/144

    ## Step 5: Print results
    if len(ore_mB_list) == 2:
        if min_delta_mB == 0.0:
            info_msg_buffer = ['RESULTS','Perfect ratio! You won\'t waste any metal while making ' + alloy_type + '. For ' + str(total_ingots_new) + ' ingots, you will need ' + str(n_ore1) + ' of ore1 at ' + str(ore1_mB) + 'mB/ore1 and ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2.']
        else:
            info_msg_buffer = ['RESULTS','With given info, I found the most efficient combination for ' + alloy_type + '. At a new total of '+ str(total_ingots_new) +' ingots and ' + str(total_mB_new) + ' mB you will have to waste ' + str(min_delta_mB) + 'mB of metal for every ' + str(total_ingots) + ' ingots. You will need ' + str(n_ore1) + ' of ore1 at ' + str(ore1_mB) + 'mB/ore1 and ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2.']
        info_msg_buffer.append('\nSUMMARY | ' + alloy_type) 
        info_msg_buffer.append('==============================================================')
        if min_delta_mB == 0.0:
            info_msg_buffer.append('Ingots (n): ' + str(total_ingots))
        else:
            info_msg_buffer.append('Ingots (n, rounded down): ' + str(round(total_ingots_new, 0)))
        info_msg_buffer.extend(['Ore 1 (n): ' + str(n_ore1) + ' (' + str(ore1_mB) + 'mB/ore)', 
                               'Ore 2 (n): ' + str(n_ore2) + ' (' + str(ore2_mB) + 'mB/ore)', 
                               'Metal loss: ' + str(min_delta_mB) + ' mB per every ' + str(total_ingots) + ' ingots.',
                               'Final ratio (ore1)/(ore1+ore2)): ' + '{:.2f}'.format(final_ratio1) + '%',
                               'Final ratio (ore2)/(ore1+ore2)): ' + '{:.2f}'.format(final_ratio2) + '%'])
        for info_msg in info_msg_buffer:
            handleInfo(info_msg, dir_name)
    elif len(ore_mB_list) == 3:
        if min_delta_mB == 0.0:
            info_msg_buffer = ['RESULTS','Perfect ratio! You won\'t waste any metal while making ' + alloy_type + '. For ' + str(total_ingots_new) + ' ingots, you will need ' + str(n_ore1) + ' of ore1 at ' + str(ore1_mB) + 'mB/ore1, ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2 and ' + str(n_ore3) + ' of ore3 at ' + str(ore3_mB) + 'mB/ore3.']
        else:
            info_msg_buffer = ['RESULTS','With given info, I found the most efficient combination for ' + alloy_type + '. At a new total of '+ str(total_ingots_new) +' ingots and ' + str(total_mB_new) + ' mB you will have to waste ' + str(min_delta_mB) + 'mB of metal for every ' + str(round(total_ingots_new, 0)) + ' ingots. You will need ' + str(n_ore1) + ' of ore1 at ' + str(ore1_mB) + 'mB/ore1, ' + str(n_ore2) + ' of ore2 at ' + str(ore2_mB) + 'mB/ore2 and ' + str(n_ore3) + ' of ore3 at ' + str(ore3_mB) + 'mB/ore3. ']
        info_msg_buffer.append('\nSUMMARY | ' + alloy_type) 
        info_msg_buffer.append('==============================================================')
        if min_delta_mB == 0.0:
            info_msg_buffer.append('Ingots (n): ' + str(total_ingots))
        else:
            info_msg_buffer.append('Ingots (n, rounded down): ' + str(round(total_ingots_new, 0)))
        info_msg_buffer.extend(['Ore 1 (n): ' + str(n_ore1) + ' (' + str(ore1_mB) + 'mB/ore)', 
                               'Ore 2 (n): ' + str(n_ore2) + ' (' + str(ore2_mB) + 'mB/ore)', 
                               'Ore 3 (n): ' + str(n_ore3) + ' (' + str(ore3_mB) + 'mB/ore)', 
                               'Metal loss: ' + str(min_delta_mB) + ' mB per every ' + str(total_ingots) + ' ingots.',
                               'Final ratio (ore1)/(ore1+ore2+ore3)): ' + '{:.2f}'.format(final_ratio1) + '%',
                               'Final ratio (ore2)/(ore1+ore2+ore3)): ' + '{:.2f}'.format(final_ratio2) + '%',
                               'Final ratio (ore3)/(ore1+ore2+ore3)): ' + '{:.2f}'.format(final_ratio3) + '%'])
        for info_msg in info_msg_buffer:
            handleInfo(info_msg, dir_name)
       
    alloy_results_dict[alloy_type] = {}
    alloy_results_dict[alloy_type].update({'Final ingots': str(round(total_ingots_new, 0))})
    ore_results_temp = []
    for i in range(len(ore_mB_list)):
        ore_results_temp.append(ore_mB_list[i])
    alloy_results_dict[alloy_type].update({'n': n_ore_list})
    alloy_results_dict[alloy_type].update({'mB/ore': ore_results_temp})
    alloy_results_dict[alloy_type].update({'final_ratio_ore': final_ratio_list})
    return alloy_results_dict, info_msg_buffer


info_msg = 'TFG_alloy_ratios.py initialized.'
handleInfo(info_msg, dir_name)