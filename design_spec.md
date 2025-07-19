The user will step through the following interfaces:

1) Select story type
2) Select story sub-type
3) Select key theme
4) Select core arc
5) Select genre
6) Select sub-genre

The UI has a left and right panel

The left panel displays the choices that the user has made so far
- choices are stored in the story class

The right panel shows the options that the user can choose from a panels

At the top of the left panel is a load and save button.  
- the save button is pressed the story object is save to disk in json format
- when the load button is pressed 
    - the the json is loaded and converted in to the story object.  
    - The UI is updated to show the current state of the story
    - If the story is incomplete, user taken to selection page for step with next missing information