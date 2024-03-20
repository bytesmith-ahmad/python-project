from enum import Enum

class SQL:
    
    class Operation(Enum):
        SELECT = "SELECT"
        INSERT = "INSERT"
        UPDATE = "UPDATE"
        DELETE = "DELETE"
        
    def __init___(self,
        operation: str, # required regardless of op
        table: str,     # required regardless of op
        columns: list = [],
        # TODO if len = 0, then replace by '*' IFF SELECT, by '' IFF INSERT, error if UPDATE, irrelevant for DELETE
        # TODO required for UPDATE
        # TODO special case for INSERT and DELETE        
        values: list[tuple] = [],
        # TODO required for UPDATE as a list of singular tuple of size 1
        # TODO required for INSERT
        conditions: list[str] = None,  # WHERE, optional
        order: str = None     # ORDER BY, optional
        ):
            self.operation = operation,
            self.table = table,
            self.columns = columns,
            self.values = values,
            self.conditions = conditions,
            self.order = order
            
            self.__query = None
    
    def build_sql(self) -> int:
        #TODO USE DATA ABOVE TO CONSTRUCT QUERY BASED ON OPERATION TYPE
        pseudo = """
        if self.operation.upper() any of the Operatio enum, op = self.operation, 
        return 0 if successful,
        return 1 if not
        """
    
    def __str__(self):
        if self.__query is None:
            self.query = self.build_sql()
        return self.__query
