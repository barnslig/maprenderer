#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import maprenderer, sys
import maprenderer.render as rdr

mr = maprenderer.maprenderer("data/config.ini")
mr.loadMapXML("tmpdata/map.osm")

zoomLevel = 8000

while True:
	cmd = raw_input("> ")

	cmd = cmd.split(" ")

	# style loading
	if cmd[0] == "style":
		try:
			mr.loadStyle(cmd[1])
			print "style {0} loaded.".format(cmd[1])
		except:
			print "loading the stylesheet failed because: {0}".format(sys.exc_info()[1])
			print
			print "please fix your stylesheet and try it again."
	# tile rendering
	elif cmd[0] == "render":
		try:
			rdr.renderer(mr.config, mr.style, mr.nodes, mr.xml, zoomLevel)
		except:
			print "renderer failed with: {0}".format(sys.exc_info()[1])
			print sys.exc_info()
			print
			print "please fix it and reload the renderer."
	# reload renderer
	elif cmd[0] == "reload":
		try:
			reload(rdr)
			print "renderer reloaded."
		except:
			print "reload failed with: {0}".format(sys.exc_info()[1])
			print sys.exc_info()
			print
			print "please fix it and try it again"
	# zoomlevel setter
	elif cmd[0] == "zoom":
		zoomLevel = int(cmd[1])
		print "zoomlevel setted."
	# exit
	elif cmd[0] == "exit":
		sys.exit()
	# nothing matched
	else:
		"unknown command."
