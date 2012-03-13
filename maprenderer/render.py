# -*- coding: utf-8 -*-
import Image, ImageColor, cairo, sys, math, gtk.gdk
# min_lon, min_lat, perPixelLon, perPixelLat

class renderer:
	# function to get the distance between two coordinate pairs
	# from http://www.johndcook.com/python_longitude_latitude.html
	def getDistance(self, lat1, long1, lat2, long2):
		# Convert latitude and longitude to 
		# spherical coordinates in radians.
		degrees_to_radians = math.pi/180.0
			
		# phi = 90 - latitude
		phi1 = (90.0 - lat1)*degrees_to_radians
		phi2 = (90.0 - lat2)*degrees_to_radians
			
		# theta = longitude
		theta1 = long1*degrees_to_radians
		theta2 = long2*degrees_to_radians
			
		# Compute spherical distance from spherical coordinates.
			
		# For two locations in spherical coordinates 
		# (1, theta, phi) and (1, theta, phi)
		# cosine( arc length ) = 
		#    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
		# distance = rho * arc length

		cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
			   math.cos(phi1)*math.cos(phi2))
		arc = math.acos( cos )

		# Remember to multiply arc by the radius of the earth 
		# in your favorite set of units to get length.
		return arc * 6373 * 1000	# multiplicated by 6373 to get kilometres, multiplicated by 1000 to get meters
		
	def __init__(self, config, style, nodes, xml, zoomLevel):
		alreadyRendered = []

		# set utf-8 as default
		reload(sys)
		sys.setdefaultencoding("utf-8")

		# set the boundary size
		min_lat = float(xml.find("bounds").attrib["minlat"])
		min_lon = float(xml.find("bounds").attrib["minlon"])
		max_lat = float(xml.find("bounds").attrib["maxlat"])
		max_lon = float(xml.find("bounds").attrib["maxlon"])
		
		# calculate the picture size
		## get the 1:1 size of the boundary in meters
		aperture_sizeInMeters = self.getDistance(min_lat, min_lon, max_lat, max_lon)
		side_sizeInMeters = aperture_sizeInMeters / 2 * math.sin(45)
		side_sizeInCm = side_sizeInMeters * 100
		## get the zoom-leveld size of the boundary in centimeters
		side_sizeInCm = side_sizeInCm / zoomLevel
		## get the size in pixel
		side_sizeInPx = side_sizeInCm / 2.54 * 72	# 72 is the dpi-value
		
		
		perPixelLat = side_sizeInPx / (max_lat - min_lat)
		perPixelLon = side_sizeInPx / (max_lon - min_lon)

		# generate a new image
		image = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(side_sizeInPx), int(side_sizeInPx))
		draw = cairo.Context(image)
		draw.set_line_cap(cairo.LINE_CAP_ROUND)
		draw.set_line_join(cairo.LINE_JOIN_ROUND)
		print "Map surface generated"
		
		# get all ways
		for way in xml.findall("way"):
			draw.new_path()
			# check if this way has a style
			for tag in way.findall("tag"):

				# dray the way
				if style.has_section(tag.attrib["k"]):
					if style.has_option(tag.attrib["k"], tag.attrib["v"]):
						# generate a new context on the surface

						# draw the way
						lastlon = -1
						lastlat = -1
						for nd in way.findall("nd"):
							# check if the last lon and lat are setted before drawing the image
							if lastlon == -1:
								if lastlat == -1:
									# only set them; do not draw anything
									lastlon = (nodes[nd.attrib["ref"]]["lon"] - min_lon) * perPixelLon
									lastlat = (nodes[nd.attrib["ref"]]["lat"] - min_lat) * perPixelLat
									draw.move_to(lastlat, lastlon)
							else:
								# draw the line
								draw.line_to((nodes[nd.attrib["ref"]]["lat"] - min_lat) * perPixelLat, (nodes[nd.attrib["ref"]]["lon"] - min_lon) * perPixelLon)
								
								lastlon = (nodes[nd.attrib["ref"]]["lon"] - min_lon) * perPixelLon
								lastlat = (nodes[nd.attrib["ref"]]["lat"] - min_lat) * perPixelLat
						
						# close the path
						#draw.close_path()
						
						# set the color and line-width
						## color hack from http://stackoverflow.com/questions/5197973/can-not-change-color-of-line-using-rgb-value-using-cairo-in-pygtk
						color = gtk.gdk.Color(style.get(tag.attrib["k"], tag.attrib["v"]))
						r = float(color.red) / 65535
						g = float(color.green) / 65535
						b = float(color.blue) / 65535
						draw.set_source_rgb(r, g, b)
						draw.set_line_width(float(style.get(tag.attrib["k"], tag.attrib["v"] + "_s")))
						
						# check if there is filling needed
						if style.has_option(tag.attrib["k"], tag.attrib["v"] + "_fill"):
							# stroke the line
							draw.fill_preserve()
							# set the new color
							color = gtk.gdk.Color(style.get(tag.attrib["k"], tag.attrib["v"]))
							r = float(color.red) / 65535
							g = float(color.green) / 65535
							b = float(color.blue) / 65535
							draw.set_source_rgb(r, g, b)
							draw.stroke()
						else:
							draw.stroke()	
					else:
						#pass
						if tag.attrib["v"] != "steps":
							#print tag.attrib["v"]
							pass

				# # draw the object name
				# if tag.attrib["k"] == "name":
				# 	if tag.attrib["v"] not in alreadyRendered:
				# 		if len(tag.attrib["v"]) < 42:
				# 			labels.text((lastlat, lastlon), tag.attrib["v"], fill=ImageColor.getrgb("#ff0000"), font=ImageFont.truetype(style.get("map", "font"), float(style.get("map", "font_s"))))
				# 		alreadyRendered.append(tag.attrib["v"])

		# save the map
		image.write_to_png(config.get("tiles", "store") + "tile.png")
		
		# generate the tiles
		tiles = Image.open(config.get("tiles", "store") + "tile.png")
		tiles = tiles.rotate(90)
		tileSize = int(config.get("tiles", "size"))
		tileCount = side_sizeInPx / tileSize
		
		c_x = 0
		c_y = 0
		
		while c_y < side_sizeInPx - 1:
			print "<tr>"
			while c_x < side_sizeInPx - 1:
				print "<td>"
				print "<img src=\"{0}\">".format(str(c_x) + "_" + str(c_y) + ".png")
				print "</td>"
				tile = tiles.crop((c_x, c_y, c_x + tileSize, c_y + tileSize))
				tile.save(config.get("tiles", "store") + str(c_x) + "_" + str(c_y) + ".png", "PNG")
				
				c_x += tileSize
			
			print "</tr>"
			c_x = 0
			c_y += tileSize
