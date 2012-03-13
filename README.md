maprenderer
===========

About
-----
This is just a silly renderer for the <a href="http://www.openstreetmap.org/">OpenStreetMap</a>-XML-Mapfiles based on <a href="http://python.org">Python 2</a> and <a 
href="http://cairographics.org/">Cairo</a>.

How-To set up
-------------
1.  Please create a directory called „data“ or so and create a <i>config.ini</i> and a <i>style.ini</i> in it.
2.  Now you have to configure the style of the map and some other things. 
  *  Use for each way-element from the XML-Mapfile a new section in your style-configuration. Use something like that:  
     > [key]  
     > value = #ff0000  
     > value_s = 2  
     > value_fill = #00ff00  
  *  Create a section named <i>[tiles]</i> in your <i>config.ini</i> and set the both values store and size. Size defines the size of the tiles (usually 256), store the place where 
the renderer should store the tiles. (data/tiles/ or something like that)
3.  Set the place of your XML-Mapfile in the <i>start.py</i> — it's hardcoded there because I'm so lazy :P 
4.  Start the start.py with a Python 2.7-Interpreter from your console, the ugly improvised console will show to you after a few seconds where the XML-File is loading.

The improvised renderer-console
-------------------------------
*  style — set the place of the style-configuration. Example: > style data/style.ini
*  zoom — set the map-scale. Example: zoom 8000. OSM-Tile-Zoomlevels are here: <a href="https://wiki.openstreetmap.org/wiki/DE:Zoom_levels">OpenStreetMap-Wiki</a>.
*  reload — reloads the renderer to apply code-changes
*  render — renders your tiles
*  exit — exits
