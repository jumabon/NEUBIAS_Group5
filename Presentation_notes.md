- cache the segmentation in a napari layer
- tabs as wdiget
    - split into different files so that we can work each on it
    - figure out the connection
        - tab1 constructor takes the tab2 and tab3 as input ot be able to orchestrate the calls ?


- where does the save go ?

# Structure
The Segment image has the properties and table tabs as contructor parameters

class Properties
    - check boxes
    - function get_properties that gives back list of checked properties as a whaetever skimage requires

class Table
    - _update_table input: the skimage output
    - region_props_dict properties

class SegmentImage
    - save_as_csv: pull 
    - call measurement

New structure:
- the container is passed as a argument of the init, the tabs call each other to pass commands

# issues
- too many lines
- checking the box should redo measures

# optional
highlight selected cell from table


