from robot.api import TestSuite

suite = TestSuite()
suite.resource.imports.library('ImageHorizonLibrary', args=['reference_folder=C:/Users/simon_meggle/Documents/images'])
test = suite.tests.create('Image Debugger Test')    
test.body.create_keyword('Debug Image')
result = suite.run(report=None,log=None)