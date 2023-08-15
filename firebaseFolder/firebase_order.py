from typing import List

from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_core_wrapper import FirebaseWrapper
from utils.patterns import singleton


@singleton
class FirebaseOrder(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        super().__init__()
        self.firebaseConnection: FirebaseConnection = inputFirebaseConnection

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("orders")

    def createOrder(self, whatsappNumber: str, status: str, details: str):
        if not whatsappNumber:
            raise ValueError("WhatsappNumber cannot be empty when creating an order.")
        if not status:
            raise ValueError("Status cannot be empty when creating an order.")
        if not details:
            raise ValueError("Details cannot be empty when creating an order.")
        orderData = {"whatsappNumber": whatsappNumber, "status": status, "details": details}
        self.firebaseConnection.writeData(data=orderData)

    def createDummyOrder(self):
        self.createOrder(whatsappNumber="+558597648595", status="pending", details="Sem cebola")

    def getAllOrders(self) -> List:
        rawOrders = self.firebaseConnection.readData()
        return list(rawOrders.values()) if rawOrders is not None else ["None"]

    def getOrderByWhatsappId(self, whatsappNumber: str):
        allOrders = self.getAllOrders()
        return [item for item in allOrders if item["whatsappNumber"] == whatsappNumber]


def __main():
    fc = FirebaseConnection()
    fo = FirebaseOrder(fc)
    res = fo.getOrderByWhatsappId("+558597648595")
    return


if __name__ == "__main__":
    __main()
