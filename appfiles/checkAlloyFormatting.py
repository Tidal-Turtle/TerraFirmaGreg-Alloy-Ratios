from handleInfoErrors import handleInfo, handleError

global dir_name
dir_name = 'TFG'

def checkAlloyFormatting(alloy_dict):
    info_msg = checkAlloyFormatting.__name__ + '() function called.'
    handleInfo(info_msg, dir_name)
    alloy_types = list(alloy_dict.keys())
    error_buffer = []

    for i in range(len(alloy_types)):
        alloy_info_current = alloy_dict.get(alloy_types[i])
        alloy_type = alloy_types[i]
        ore_mB_list = alloy_info_current.get('mB/ore')
        ore_ratio_list = alloy_info_current.get('ratio_ore')
        
        if len(ore_mB_list) == 2:
            try:
                ore1_mB = int(ore_mB_list[0])
                ore2_mB = int(ore_mB_list[1])
            except:
                err_msg = 'Error: Could not convert alloy info to integer. Please, check the AlloyOreInfo.txt and make sure numbers are where they should be and that there are no accidental strings next to them, such as 36w, 10O, 4S, etc.'
                error_buffer.append(err_msg)
            try:
                ore_ratio_min = float(ore_ratio_list[0][0])
                ore_ratio_max = float(ore_ratio_list[0][1])
            except:
                err_msg = 'Error: For the chosen ' + alloy_type + ', I require ' + str(len(ore_mB_list)) + ' values of mB/ore and at least ' + str(len(ore_mB_list)-1) + ' ratio range. Please, edit the AlloyOreInfo.txt file and try again.'
                error_buffer.append(err_msg)
        elif len(ore_mB_list) == 3:
            try:
                ore1_mB = int(ore_mB_list[0])
                ore2_mB = int(ore_mB_list[1])
                ore3_mB = int(ore_mB_list[2])
            except:
                err_msg = 'Error: Could not convert alloy info to integer. Please, check the AlloyOreInfo.txt file and make sure numbers are where they should be and that there are no accidental strings next to them, such as 36w, 10O, 4S, etc.'
                error_buffer.append(err_msg)
            try:
                ore1_ratio_min = float(ore_ratio_list[0][0])
                ore1_ratio_max = float(ore_ratio_list[0][1])
                ore2_ratio_min = float(ore_ratio_list[1][0])
                ore2_ratio_max = float(ore_ratio_list[1][1])
            except:
                err_msg = 'Error: For the chosen ' + alloy_type + ', I require ' + str(len(ore_mB_list)) + ' values of mB/ore and at least ' + str(len(ore_mB_list)-1) + ' ratio ranges. Please, edit the AlloyOreInfo.txt file and try again.'
                error_buffer.append(err_msg)
    if len(error_buffer) == 0:
        info_msg = 'AlloyOreInfo.txt check was completed. No errors occured.'
        handleInfo(info_msg, dir_name)
    elif len(error_buffer) == 1:
        info_msg = 'AlloyOreInfo.txt check was completed. One error was caught:'
        handleInfo(info_msg, dir_name)
        for error in error_buffer:
            handleError(error, dir_name)
        quit()
    elif len(error_buffer) > 1:
        info_msg = 'AlloyOreInfo.txt check was completed. Multiple errors were caught:'
        handleInfo(info_msg, dir_name)
        for error in error_buffer:
            handleError(error, dir_name)
        quit()