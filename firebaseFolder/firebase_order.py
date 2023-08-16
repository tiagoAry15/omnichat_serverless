from typing import List, Tuple

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_core_wrapper import FirebaseWrapper
from utils.patterns import singleton
from utils.time_utils import generateTimestamp, getLatestTimestamp


@singleton
class FirebaseOrder(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        super().__init__()
        self.firebaseConnection: FirebaseConnection = inputFirebaseConnection

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("orders")

    def createOrder(self, whatsappNumber: str, status: str, details: str) -> bool:
        if not whatsappNumber:
            raise ValueError("WhatsappNumber cannot be empty when creating an order.")
        if not status:
            raise ValueError("Status cannot be empty when creating an order.")
        if not details:
            raise ValueError("Details cannot be empty when creating an order.")
        orderData = {"whatsappNumber": whatsappNumber, "status": status, "details": details,
                     "timestamp": generateTimestamp()}
        self.firebaseConnection.writeData(data=orderData)
        return True

    def readOrder(self, whatsappNumber: str):
        return self._getLastOrderByWhatsappNumber(whatsappNumber)

    def updateOrder(self, whatsappNumber: str, **kwargs) -> bool:
        if not whatsappNumber:
            raise ValueError("WhatsappNumber cannot be empty when updating an order.")
        userOrder, userOrderUniqueId = self._getLatestOrderAndIdByWhatsappNumber(whatsappNumber)
        if not userOrder:
            return False
        userOrder.update(kwargs)
        self.firebaseConnection.overWriteData(path=userOrderUniqueId, data=userOrder)
        return True

    def deleteOrder(self, whatsappNumber: str):
        if not whatsappNumber:
            raise ValueError("WhatsappNumber cannot be empty when deleting an order.")
        userOrder, userOrderUniqueId = self._getLatestOrderAndIdByWhatsappNumber(whatsappNumber)
        if not userOrderUniqueId:
            return False
        self.firebaseConnection.deleteData(path=userOrderUniqueId)
        return True

    def createDummyOrder(self) -> bool:
        self.createOrder(whatsappNumber="+558597648595", status="pending", details="Sem cebola")
        return True

    def _getLatestOrderAndIdByWhatsappNumber(self, whatsappNumber: str) -> Tuple[dict, str] or Tuple[None, None]:
        rawOrders = self.firebaseConnection.readData()
        if not rawOrders:
            return None, None
        userOrders = [(uniqueId, orderContent) for uniqueId, orderContent in rawOrders.items()
                      if orderContent["whatsappNumber"] == whatsappNumber]
        if not userOrders:
            return None, None
        latestOrder = max(userOrders, key=lambda x: x[1]["timestamp"])
        return latestOrder[1], latestOrder[0]


def __main():
    fc = FirebaseConnection()
    fo = FirebaseOrder(fc)
    # res = fo.updateOrder(whatsappNumber="+558597648595", status="finished")
    res = fo.deleteOrder(whatsappNumber="+558597648595")
    return


if __name__ == "__main__":
    __main()
