class CustomTool:
  def __init__(self, tool_id: str, description: str, 
               paramone: str, paramtwo: str, paramthree: str, paramfour: str):
    self.tool_id = tool_id
    self.description = description
    
    self.paramone = paramone
    self.paramtwo = paramtwo
    self.paramthree = paramthree
    self.paramfour = paramfour
    
  def as_dict(self):
    return {
      "tool_id": self.tool_id,
      "description": self.description,
      "ParameterOne": self.paramone,
      "ParameterTwo": self.paramtwo,
      "ParameterThree": self.paramthree,
      "ParameterFour": self.paramfour
    }