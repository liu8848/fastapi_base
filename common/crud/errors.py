
class SQLAlchemyCRUDException(Exception):
    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


class ModelColumnError(SQLAlchemyCRUDException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class SelectOperatorError(SQLAlchemyCRUDException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class ColumnSortError(SQLAlchemyCRUDException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class MultipleResultsError(SQLAlchemyCRUDException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class CompositePrimaryKeysError(SQLAlchemyCRUDException):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)