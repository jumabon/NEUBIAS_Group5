- cache the segmentation in a napari layer
- tabs as wdiget
    - split into different files so that we can work each on it
    - figure out the connection
        - tab1 constructor takes the tab2 and tab3 as input ot be able to orchestrate the calls ?


- where does the save go ?

# Structure
class properties
    - check boxes
    - function get_properties that gives back list of checked properties as a whaetever skimage requires

class Table
    - _update_table input: the skimage output
    - region_props_dict properties

class SegmentImage
    - save_as_csv: pull 
    - call measurement

