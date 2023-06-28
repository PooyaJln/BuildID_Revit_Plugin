# pyRevit
from pyrevit import revit, forms

def check_buildid_parmeters_exist(element):
    parameters_list = list(element.Parameters)
    parameters_name_list = []
    for parameter in parameters_list:
        parameters_name_list.append(parameter.Definition.Name)
    
    buildID_parameters_list = ['EPC_number','BuildID_link']
    
    buildID_empty_parameters_list = []
    for parameter in buildID_parameters_list:
        if not parameter in parameters_name_list:
            buildID_empty_parameters_list.append(parameter)
    
    if len(buildID_empty_parameters_list) == 1:
        forms.alert("\"{}\" is missing among this object's parameters.\nAdd \"{}\" to shared parameters or\ncheck if it is assigned for this object type.\n".format(parameter, parameter), exitscript=True)
    elif len(buildID_empty_parameters_list) == 2:
        forms.alert("\"{}\" and \"{}\" are missing among this object's parameters.\nAdd them to shared parameters or\ncheck if it is assigned for this object type.\n".format(buildID_empty_parameters_list[0], buildID_empty_parameters_list[1]), exitscript=True)
    else:
        return True