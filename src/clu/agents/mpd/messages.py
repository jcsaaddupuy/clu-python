"""Module containing MPD control Message """

class MpdControlMessage(obect):
  """ Represent a MPD control message that will be sent throught rabbitmq """
  def __init__(self, command, params={}):
    self.command = command
    self.params = params
