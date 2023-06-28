# -*- coding: utf-8 -*-
__title__ = 'Release EPC no.'
__doc__ = 'Assign an EPC number and book it at BuldID database'
__authors__ = ['Pooya.Jalilian@gmail.com']

import os
import requests
__fullframeengine__=True

# pyRevit
from pyrevit import revit, forms, script

#custom imports
from common_snippets import console
from Parameter_actions._actions import set_buildid_values
from Parameter_actions._checks import check_buildid_parmeters_exist
from common_snippets._selections import get_selected_elements
from Buildid_CRUD.auth_check import config_file_check
from Buildid_CRUD.response_to_file import response_file_check
from Buildid_CRUD.buildid_data_from_file import get_item_by_epc_number
from Buildid_CRUD.api_calls import get_item_by_EPC_no,booking_request,make_item_availabe


# start of code
uidoc = __revit__.ActiveUIDocument
app = __revit__.Application
doc = __revit__.ActiveUIDocument.Document

output = script.get_output()
output.set_height(700)
logger = script.get_logger()

selection = get_selected_elements(doc)

# if no element is selected we ask the user to select one
if len(selection)==0:
    forms.alert('Select an object.', exitscript=False)
    element = revit.pick_element()

if len(selection)>0:
    element = selection[0]

# we check whether the buildID parameters exists in the project or assigned to the element
check_buildid_parmeters_exist(element)

# checking if config.json file exists
grandparent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = config_file_check(grandparent_directory)
API_BASE_URI = config.get('API_BASE_URI') 
PASSWORD = config.get('PASSWORD')
USERNAME = config.get('USERNAME') 
USERNAME_itemlistexport = config.get('USERNAME_itemlistexport')
PASSWORD_itemlistexport = config.get('PASSWORD_itemlistexport')
projectId = config.get('projectId')

