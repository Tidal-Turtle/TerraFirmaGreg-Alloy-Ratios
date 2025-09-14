from handleInfoErrors import handleInfo, handleError
from checkAlloyFormatting import checkAlloyFormatting
import sys

global dir_name
global parent_dir
dir_name = 'TFG'
parent_dir = sys.path[0].split('appfiles')[0]
#print(parent_dir)

def getAlloyOreInfo(skipChoice=False):
    info_msg = getAlloyOreInfo.__name__ + '() function called.'
    handleInfo(info_msg, dir_name)

    with open(parent_dir + 'AlloyOreInfo.txt') as file:
        alloy_dict = {}
        empty_line_counter = 0
        ore_counter = 0
        ore_ratio_counter = 0
        alloy_type_list = []
        ore_temp = []
        ratio_buffer = []
        
        for line in file:
            line_words = line.strip('\n').split(' | ')

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
                    err_msg = "Error: The alloy 'Type' in AlloyOreInfo.txt must be a string. You have typed in a variable of type " + str(type(int(line_words[1]))) + " ('" + str(line_words[1]) + "'). Please, check the file and try again."
                    handleError(err_msg, dir_name)
                    break
                except:
                    if len(alloy_type_list) > 1:
                        err_msg = 'Error: You cannot have two succesive alloy types without the basic information about them. Check the AlloyOreInfo.txt file and add the potentially ' \
                        'missing components: Ingots, mB/ore1, mB/ore2, mB/ore3, ..., ratio_ore1, ratio_ore2, ...'
                        handleError(err_msg, dir_name)
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

                for i in range(len(ratio_temp)):
                    percentage = float(ratio_temp[i])
                    ratio_temp[i] = '{:.2f}'.format(percentage)
                ratio_buffer.append(ratio_temp)
                alloy_dict[alloy_type_list[0]].update({'ratio_ore': ratio_buffer})

        alloy_types = list(alloy_dict.keys())   # Converts the view object dict.keys to a list. It doesn't update with the dictionary as the view object would, but I can manipulate
                                                # the list without worrying about the dictionary.
        if skipChoice == False:
            if len(alloy_types) < 1:
                info_msg = 'There are no alloys to choose from. Please, add at least one alloy and its corresponding information '
                '(Ingots, mB/ore1, mB/ore2, mB/ore3, ..., ratio_ore1, ratio_ore2, ...) to the AlloyOreInfo.txt file.'
                handleInfo(info_msg, dir_name)
            elif len(alloy_types) == 1:
                alloy_choice = 0
                info_msg = 'I found only one alloy in the AlloyOreInfo.txt file (' + alloy_types[0] + '). Let\'s see what we can do.'
                handleInfo(info_msg, dir_name)
            else:
                info_msg = 'Alloy types:'
                handleInfo(info_msg, dir_name)
                alloy_index = 0
                
                for alloy in alloy_types:
                    info_msg = str(alloy_index) + ' ' +  str(alloy)
                    handleInfo(info_msg, dir_name)
                    alloy_index += 1
                
                info_msg = 'I noticed there are multiple alloy types in the AlloyOreInfo.txt file. Which alloy type do you want? Type in the number correlated with the alloy above: '
                alloy_choice = int(input(info_msg))
                handleInfo(info_msg + str(alloy_choice), dir_name)
                info_msg = 'You chose ' + str(alloy_types[alloy_choice]) + ' (' + str(alloy_choice) + ')' + '. Let\'s see what we can do.'
                handleInfo(info_msg, dir_name)

            alloy_info_chosen = alloy_dict.get(alloy_types[alloy_choice])

            # Check if there is a ratio range missing (one less than mB/ore entries). If yes, calculate the range. 
            # This is purely cosmetic and is not needed for the functionality of the program.
            if (len(alloy_dict[alloy_types[alloy_choice]].get('mB/ore')) - len(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore'))) == 1:
                info_msg = 'There\'s ' + str(len(alloy_dict[alloy_types[alloy_choice]].get('mB/ore')) - len(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore'))) + ' less ratio range (' + str(len(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore'))) + ') than ores (' + str(len(alloy_dict[alloy_types[alloy_choice]].get('mB/ore'))) + ') in the AlloyOreInfo.txt file for this alloy. Filling in the last ratio range automatically.'
                handleInfo(info_msg, dir_name)
                ore_min_temp = str(100-int(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore')[-1][1]))
                ore_max_temp = str(100-int(alloy_dict[alloy_types[alloy_choice]].get('ratio_ore')[-1][0]))
                ratio_buffer = []
                ratio_buffer = alloy_dict[alloy_types[alloy_choice]].get('ratio_ore')
                ratio_buffer.append([ore_min_temp, ore_max_temp])
                alloy_dict[alloy_types[alloy_choice]].update({'ratio_ore': ratio_buffer})

            info_msg_buffer = [str(alloy_types[alloy_choice]) + ' info: ', '==============================================================', 'Ingots (n): ' + alloy_info_chosen.get("Ingots")]
            for info_msg in info_msg_buffer:
                handleInfo(info_msg, dir_name)
            for i in range(len(alloy_info_chosen.get("mB/ore"))):
                info_msg = 'Ore ' + str(i+1) + ': ' + str(alloy_info_chosen.get("mB/ore")[i]) + 'mB/ore'
                handleInfo(info_msg, dir_name)
            if len(alloy_info_chosen.get("mB/ore")) == 2:
                for i in range(len(alloy_info_chosen.get("ratio_ore"))):
                    info_msg = 'Sought ratio range (ore' + str(i+1) + ')/(ore1+ore2)): ' + str(alloy_info_chosen.get("ratio_ore")[i][0]) + '%-' + str(alloy_info_chosen.get("ratio_ore")[i][1]) + '%'
                    handleInfo(info_msg, dir_name)      
            elif len(alloy_info_chosen.get("mB/ore")) == 3:
                for i in range(len(alloy_info_chosen.get("ratio_ore"))):
                    info_msg = 'Sought ratio range (ore' + str(i+1) + ')/(ore1+ore2+ore3)): ' + str(alloy_info_chosen.get("ratio_ore")[i][0]) + '%-' + str(alloy_info_chosen.get("ratio_ore")[i][1]) + '%'
                    handleInfo(info_msg, dir_name)
            checkAlloyFormatting(alloy_dict)
            return alloy_types[alloy_choice], alloy_info_chosen
        else: 
            for i in range(len(alloy_types)):
                if (len(alloy_dict[alloy_types[i]].get('mB/ore')) - len(alloy_dict[alloy_types[i]].get('ratio_ore'))) == 1:
                    info_msg = 'There\'s ' + str(len(alloy_dict[alloy_types[i]].get('mB/ore')) - len(alloy_dict[alloy_types[i]].get('ratio_ore'))) + ' less ratio range (' + str(len(alloy_dict[alloy_types[i]].get('ratio_ore'))) + ') than ores (' + str(len(alloy_dict[alloy_types[i]].get('mB/ore'))) + ') in the AlloyOreInfo.txt file for ' + alloy_types[i] + '. Filling in the last ratio range automatically.'
                    handleInfo(info_msg, dir_name)
                    ore_min_temp = '{:.2f}'.format(100-float(alloy_dict[alloy_types[i]].get('ratio_ore')[-1][1]))
                    ore_max_temp = '{:.2f}'.format(100-float(alloy_dict[alloy_types[i]].get('ratio_ore')[-1][0]))
                    ratio_buffer = []
                    ratio_buffer = alloy_dict[alloy_types[i]].get('ratio_ore')
                    ratio_buffer.append([ore_min_temp, ore_max_temp])
                    alloy_dict[alloy_types[i]].update({'ratio_ore': ratio_buffer})
            checkAlloyFormatting(alloy_dict)
            return alloy_types, alloy_dict