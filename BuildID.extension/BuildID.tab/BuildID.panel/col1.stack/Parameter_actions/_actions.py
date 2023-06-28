# Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Transaction

# pyRevit
from pyrevit import revit, forms


def set_buildid_values(epc_number, element, doc,title,API_BASE_URI ):
    # epc_number_input = forms.ask_for_string(
    #     default='Enter an EPC number',
    #     prompt='Enter new EPC name:',
    #     title='EPC number input dialog'
    # )
    print('setting epc number')
    t = Transaction(doc,title)
    t.Start()
    epc_number_parameter = element.LookupParameter('EPC_number')
    epc_number_parameter.Set(epc_number)
    buildid_link = element.LookupParameter('BuildID_link')
    buildid_link.Set('{}Items/publicdetails/{}'.format(API_BASE_URI,epc_number))
    # buildid_link_parameter = element.LookupParameter('BuildID_link')
    # To do: return the product id and create a string
    # buildid_link_string = f'' 
    # buildid_link_parameter.Set(epc_number_input)
    t.Commit()