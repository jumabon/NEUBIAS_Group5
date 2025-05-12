# Presentation notes

## Caching the cellpose results
- cache the segmentation in a napari layer
- check if this exists

## Saving to CSV
oops we forgot
- where does the save go ?

## Checking a properties triggers the recomputing

## Tabs communication structure
- tabs as wdiget
    - split into different files so that we can work each on it
    - figure out the connection
        - tab1 constructor takes the tab2 and tab3 as input ot be able to orchestrate the calls ?

### Structure
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


# optional
highlight selected cell from table


