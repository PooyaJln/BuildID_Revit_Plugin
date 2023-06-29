# -*- coding: utf-8 -*-
__title__ = 'Book EPC no.'
__doc__ = 'Assign an EPC number and book it at BuldID database'
__authors__ = ['Pooya.Jalilian@gmail.com']

import os
import requests
__fullframeengine__=True
# .NET Imports
# import clr
# clr.AddReferenceByPartialName('PresentationCore')
# clr.AddReferenceByPartialName('AdWindows')
# clr.AddReferenceByPartialName("PresentationFramework")
# clr.AddReferenceByPartialName('System')
# clr.AddReferenceByPartialName('System.Windows.Forms')
# from System.Collections.Generic import List

# Autodesk
# from Autodesk.Revit.DB import *
# from Autodesk.Revit.DB import Transaction, FilteredElementCollector  
# from Autodesk.Revit.DB.Mechanical import *
# from Autodesk.Revit.DB.Plumbing import *

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
output.set_height(400)
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

# loading the data from buildid
# items = response_file_check(grandparent_directory,API_BASE_URI,USERNAME_itemlistexport,PASSWORD_itemlistexport)

def set_and_book():
    '''
    this function opens a window for user input and returns a string as EPC number.
    if the entered EPC number is already booked, it asks the user if they want to
    enter a new one or cancel the process.
    '''
# TODO: error handling when the user cancels the input
# 
    while True:
        epc_number = forms.ask_for_string(
            default='',
            prompt='Enter new EPC name:',
            title='EPC number input dialog'
        )
        new_item = get_item_by_EPC_no(API_BASE_URI,USERNAME_itemlistexport,PASSWORD_itemlistexport,epc_number)
        print('new EPC number: ',epc_number)
        if new_item[0].get('registrationStatus').lower() == 'bokad' :           
            user_input = forms.alert('This EPC number is already booked. Do you want to enter a new Epc number?',ok=False, yes=True, no=True, exitscript=False)
            if not user_input:
                break
        else:
            epc_number_list=[]
            epc_number_list.append(epc_number)
            # print('epc_number_list:', epc_number_list)
            set_buildid_values(epc_number,element, doc,__title__,API_BASE_URI)
            booking_request(epc_number_list,API_BASE_URI,USERNAME,PASSWORD,projectId)
            break




if (not element.LookupParameter('EPC_number').HasValue) or (element.LookupParameter('EPC_number').HasValue and element.LookupParameter('EPC_number').AsString() == ""):
    # print('hasValue: False')
    set_and_book()


elif element.LookupParameter('EPC_number').HasValue and element.LookupParameter('EPC_number').AsString() != "": # To do: it should also check if the value is not empty.
    # print('has some Value')
    existing_epc_no = element.LookupParameter('EPC_number').AsString()
    print('existing_epc_no: ',existing_epc_no)
    existing_item = get_item_by_EPC_no(API_BASE_URI,USERNAME_itemlistexport,PASSWORD_itemlistexport,existing_epc_no)
    # print('existing_item: ',existing_item)
    
    if len(existing_item) == 0: #if the existing EPc number doesn't return any object from the buildID database, then it doesn't exist.
        # print('not a valid EPC number')
        set_and_book()

    elif len(existing_item) == 1:        # if this length is 1 then this EPC number exists in the database and is booked. if user wants to change it, its status should be updated in the database.
        # print('a valid EPC number')
        epc_number_list_to_make_available=[]
        epc_number_list_to_make_available.append(existing_epc_no)
        user_input = forms.alert('this element already has a EPC_number, Do you want to change it?',ok=False, yes=True, no=True, exitscript=False)
        if user_input:
            set_and_book()
            make_item_availabe(epc_number_list_to_make_available,API_BASE_URI,USERNAME,PASSWORD,projectId)
