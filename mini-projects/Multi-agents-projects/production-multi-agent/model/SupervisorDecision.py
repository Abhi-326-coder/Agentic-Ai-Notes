from pydantic import BaseModel

class SupervisorDecision(BaseModel):

    needs_research: bool
    needs_coding: bool
    needs_security: bool