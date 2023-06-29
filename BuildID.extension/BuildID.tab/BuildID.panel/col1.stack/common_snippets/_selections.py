# -*- coding: utf-8 -*-
# Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import Transaction, FilteredElementCollector  
from Autodesk.Revit.DB.Mechanical import *
from Autodesk.Revit.DB.Plumbing import *

# pyRevit
# from pyrevit import revit, forms

# app = __revit__.Application
# uidoc = __revit__.ActiveUIDocument
# doc = __revit__.ActiveUIDocument.Document

def get_selected_elements(doc):
    """
    parameter: uidoc,
    return list of selected elements
    """
    # selected_elements = []
    # for element_id in uidoc.Selection.GetElementsIds():
    #     element = uidoc.Document.GetElement(element_id)
    #     selected_elements.append(element)
    
    # selected_elements= [uidoc.Document.GetElement(element_id) for element_id in uidoc.Selection.GetElementsIds()]
    selected_elements= [doc.GetElement(elId) for elId in __revit__.ActiveUIDocument.Selection.GetElementIds()]
    
    return selected_elements