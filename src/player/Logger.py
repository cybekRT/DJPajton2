_logger = None

class Logger():
	@staticmethod
	def instance():
		global _logger
		if _logger is None:
			_logger = Logger()

		return _logger
	
	def __init__(self):
		global _logger
		if _logger is not None:
			raise "Logger was initialized!"
		
		self.messages = []
		
	def Latest(self):
		if len(self.messages) == 0:
			return -1
		
		return len(self.messages) - 1
	
	def GetSince(self, index):
		if index < 0:
			return self.messages
		
		return self.messages[index+1:]
	
	def Log(self, msg):
		print "Logged: {}".format(msg)
		self.messages.append(msg)