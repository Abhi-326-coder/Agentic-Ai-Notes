from pydantic import BaseModel,Field

class ToolParameter(BaseModel):
    name:str
    type:str
    description:str
    required: bool = True

class ToolSchema(BaseModel):
    name:str
    description:str
    parameters:list[ToolParameter] = []
    
class CalculatorArguments(BaseModel):
    expression: str = Field(
        description="Mathematical expression such as '25 * 4'."
    )

class ToolDefinition(BaseModel):
    name: str
    description: str
    argument_schema: dict

class TimeArguments(BaseModel):
    pass

class RandomNumberArguments(BaseModel):
    minimum: int = Field(
        description="Minimum possible random number."
    )

    maximum: int = Field(
        description="Maximum possible random number."
    )
    
