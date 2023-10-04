from typing import List
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Person_Data:
    name:str
    school_name:str
    phone_number:str
    email:str
    department: List[str] = field(default_factory=list)

if __name__=="__main__":
    data = {'name': 'Williamson, Kasja', 'school_name': ['Laketown Elementary', 'Student Support Services'], 'department': 'Student Support Services', 'phone_number': '(952) 442-0690', 'email': 'kwilliamson@isd110.org'}
    p1=Person_Data(data['name'],data['school_name'],data['phone_number'],data['email'],data['department'])
    print(p1)
