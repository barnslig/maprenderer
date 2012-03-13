# -*- coding: utf-8 -*-
import ConfigParser
from xml.etree.ElementTree import ElementTree

class maprenderer:
	def __init__(self, config):
		# load the configuration
		self.config = ConfigParser.ConfigParser()
		self.config.read(config)

	def loadStyle(self, style):
		# load the style
		self.style = ConfigParser.ConfigParser()
		self.style.read(style)
	
	# function to load the map xml-file
	def loadMapXML(self, pathToXml):
		# load the xml-file
		self.xml = ElementTree()
		self.xml.parse(pathToXml)
		print "XML-File loaded"
		
		# load all node positions
		self.nodes = {}
		for node in self.xml.findall("node"):
			self.nodes[node.attrib["id"]] = {"lat": float(node.attrib["lat"]), "lon": float(node.attrib["lon"])}
		print "Nodes loaded"