from handleInfoErrors import handleInfo, handleError
import sys

global dir_name
global parent_dir
dir_name = 'TFG'
parent_dir = sys.path[0].split('appfiles')[0]

def saveAlloyInfo(filename, alloy_dict):
    alloy_types = list(alloy_dict.keys())

    with open(parent_dir + filename) as file:
        data = file.readlines()
        new_data = []

        for i, line in enumerate(data):
            data[i] = line.rstrip()
            data[i] = line.replace(',', '.')
            data[i] = line.rstrip(',00')

    for i, line in enumerate(data):
        for alloy_type in alloy_types:
            if 'Type' + ' | ' + alloy_type == line:
                if len(new_data) == 0:
                    new_data.append('Type' + ' | ' + alloy_type)
                else:
                    new_data.append('\n\nType' + ' | ' + alloy_type)
                new_data.append('\nIngots' + ' | ' + alloy_dict[alloy_type].get('Ingots'))
                for j in range(1, len(alloy_dict[alloy_type].get('mB/ore'))+1):
                    new_data.append('mB/ore' + str(j) + ' | ' + alloy_dict[alloy_type].get('mB/ore')[j-1])
                for j in range(1, len(alloy_dict[alloy_type].get('ratio_ore'))+1):
                    new_data.append('ratio_ore' + str(j) + ' | ' + alloy_dict[alloy_type].get('ratio_ore')[j-1][0] + '%-' + alloy_dict[alloy_type].get('ratio_ore')[j-1][1] + '%')
                del alloy_types[alloy_types.index(alloy_type)]
                break

    for alloy_type_leftover in alloy_types:
        new_data.append('\n\nType' + ' | ' + alloy_type_leftover)
        new_data.append('\nIngots' + ' | ' + alloy_dict[alloy_type_leftover].get('Ingots'))
        for j in range(1, len(alloy_dict[alloy_type_leftover].get('mB/ore'))+1):
            new_data.append('\nmB/ore' + str(j) + ' | ' + alloy_dict[alloy_type_leftover].get('mB/ore')[j-1])
        for j in range(1, len(alloy_dict[alloy_type_leftover].get('ratio_ore'))+1):
            new_data.append('\nratio_ore' + str(j) + ' | ' + alloy_dict[alloy_type_leftover].get('ratio_ore')[j-1][0] + '%-' + alloy_dict[alloy_type_leftover].get('ratio_ore')[j-1][1] + '%')
    for i, line in enumerate(new_data):
            new_data[i] = line.replace(',', '.')    # SaveAlloyInfo.txt will always save decimals with a dot - the GUI comma is only visual.

    if new_data != []:
        open(parent_dir + filename, 'w').close()
        with open(parent_dir + filename, 'w') as file:
            file.write(''.join(new_data))
        info_msg = 'Saved data: (of type ' + str(type(new_data)) + '): ' + ''.join(new_data)
        handleInfo(info_msg, 'app')

def getSettingsInfo(filename):
    handleInfo('Settings info - reading', 'app')
    settings_dict_read = {}

    try:
        with open(parent_dir + filename) as file:
            for line in file:
                if line != '' or line != '\n':
                    line = line.strip('\n')
                    line_elements = line.split(' | ')
                    settings_dict_read[line_elements[0]] = line_elements[1]
        handleInfo('Settings info - read', 'app')
        return settings_dict_read
    except:
        return {}

def saveSettingsInfo(filename, settings_dict):
    handleInfo('Settings info - saving', 'app')
    settings_dict_read = {}
    write_buffer = []

    for i, key in enumerate(list(settings_dict.keys())):
        key = key.strip('\n')
        line = key + ' | ' + settings_dict.get(key)
        write_buffer.append(line)

    if write_buffer != []:
        open(parent_dir + filename, 'w').close()
        with open(parent_dir + filename, 'w') as file:
            file.write(''.join(write_buffer))
        info_msg = 'Saved data (of type ' + str(type(write_buffer)) + '): ' + ''.join(write_buffer)
        handleInfo(info_msg, 'app')
    return  