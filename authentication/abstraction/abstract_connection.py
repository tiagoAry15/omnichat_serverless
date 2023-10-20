from abc import ABC, abstractmethod
from typing import Any


class AbstractFirebaseConnection(ABC):
    @abstractmethod
    def changeDatabaseConnection(self, path: str):
        pass

    @abstractmethod
    def readData(self, path: str = None):
        pass

    @abstractmethod
    def getValue(self, path: str) -> Any:
        pass

    @abstractmethod
    def setValue(self, path: str, value: Any) -> bool:
        pass

    @abstractmethod
    def writeData(self, path: str = None, data: dict = None) -> bool:
        pass

    @abstractmethod
    def writeDataWithoutUniqueId(self, path: str = None, data: dict = None) -> bool:
        pass

    @abstractmethod
    def overWriteData(self, path: str = None, data=None) -> bool:
        pass

    @abstractmethod
    def deleteData(self, path: str, data=None) -> bool:
        pass

    @abstractmethod
    def deleteAllData(self) -> bool:
        pass

    @abstractmethod
    def getUniqueIdByData(self, path: str = None, data=None) -> str:
        pass
