from typing import List
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Person_Data:
    name:str
    school_name:str
    phone_number:str
    email:str
    department: List[str] = field(default_factory=list)


