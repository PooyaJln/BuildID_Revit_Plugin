A revit plugin to automate data syncing between Cirkulära BuildID database and a Revit model.
Cirkulära BuildID database offers an API for booking EPC number, which means a designer assigns
an item from the warehouse to an element in the Revit model to be used in construction.

The first time a user runs the plugin it checks got credentials.
if a credential file exists it checks whether it's populated with correct data or not.
If it's empty or some of the data is missing it asks the user to fill in the data and
it creates the file and returns the required data as a dictionary.

In the next step, it checks if the required shared parmeters exist in the project.
If not it warns the user.

Then it checks whether any Revit model is selected or not. If no element is selected it
prompts the user to select one.

Then it asks the user to enter an EPC number from BuildID database.
This function later checks if the entered EPC number is already booked and if it is, it
warns the user and asks for a new number.

With an available number it goes ahead and adds the number to the element's parameters
and adds a link to the public database.

The function also checks if the element already has a valid EPC number and if it has, it asks
the user if they want to update it or not. In case the user wants to add a new EPC number
it will make the old one available.

Some images of different functions in action:
https://lnkd.in/d5-enjvE

and a short video of a function for changing the EPC number:
https://www.linkedin.com/feed/update/urn:li:activity:7077038568870674433/

To use this plugin follow the steps below:
1. install pyrevit.
2. create a clone of pyrevit using ironpython engine 2.7.10
3. attach the clone to Revit.
4. save the zip file on a desired directory and unzip it.
5. add the parent directory of BuildID.extension to pyrevit setting so it can recognize the plugin.
6. save and reload pyrevit.
7. If everything goes smoothly, you will see a BuildID tab ready to use.