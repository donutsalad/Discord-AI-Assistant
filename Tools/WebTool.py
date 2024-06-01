class WebTool:
  def __init__(self, tool_id: str, description: str, paramone: str, paramtwo: str):
    self.tool_id = tool_id
    self.description = description
    
    self.paramone = paramone
    self.paramtwo = paramtwo
    
  def as_dict(self):
    return {
      "tool_id": self.tool_id,
      "description": self.description,
      "ParameterOne": self.paramone,
      "ParameterTwo": self.paramtwo,
    }