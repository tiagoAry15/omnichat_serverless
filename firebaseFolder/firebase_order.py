from typing import Tuple

from authentication.sdk_auth.firebase_sdk_connection import FirebaseSDKConnection
from firebaseFolder.firebase_core_wrapper import FirebaseWrapper
from utils.patterns import singleton
from utils.time_utils import generateTimestamp


@singleton
class FirebaseOrder(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: FirebaseSDKConnection):
        super().__init__()
        self.firebaseConnection: FirebaseSDKConnection = inputFirebaseConnection

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("orders")

    def getNextOrderId(self) -> int:
        """Get the next available order ID."""
        # Get the current max order ID from Firebase
        current_id = self.firebaseConnection.getValue("last_order_id")
        if not current_id:
            return 1  # This is the first order
        return current_id + 1

    def createOrder(self, customerName: str, pizzaName: str, status: str, address: str, platform: str,
                    communication: str, observation: str = "None") -> bool:
        if not customerName:
            raise ValueError("CustomerName cannot be empty when creating an order. CustomerName example: 'João'")
        if not pizzaName:
            raise ValueError("PizzaName cannot be empty when creating an order. PizzaName example: 'Calabresa'")
        if not status:
            raise ValueError("Status cannot be empty when creating an order. Status example: 'Em preparação'")
        if not address:
            raise ValueError("Address cannot be empty when creating an order. Address example: 'Rua da Paz 1428'")
        if not platform:
            raise ValueError("Platform cannot be empty when creating an order. Platform example: 'Instagram'")
        if not communication:
            raise ValueError("Communication cannot be empty when creating an order."
                             " Communication example: joao@example.com'")
        next_order_id = self.getNextOrderId()
        self.firebaseConnection.setValue("last_order_id", next_order_id)
        path = f"orders_pool/{next_order_id}"
        orderData = {"timestamp": generateTimestamp(), "customerName": customerName, "pizzaName": pizzaName,
                     "status": status, "address": address, "platform": platform, "communication": communication,
                     "observation": observation}
        self.firebaseConnection.writeDataWithoutUniqueId(path=path, data=orderData)
        return True

    def readSingleOrder(self, whatsappNumber: str):
        return self._getLastOrderByWhatsappNumber(whatsappNumber)

    def readAllOrders(self):
        return self.firebaseConnection.readData()

    def getOrderById(self, order_id: int):
        all_orders = self.readAllOrders()
        if not all_orders:
            return None
        return all_orders["orders_pool"][order_id]

    def updateOrder(self, orderId: int, **kwargs) -> bool:
        if not orderId:
            raise ValueError("OrderID cannot be empty when updating an order.")
        userOrder = self.getOrderById(orderId)
        if not userOrder:
            return False
        userOrder.update(kwargs)
        path = f"orders_pool/{orderId}"
        self.firebaseConnection.overWriteData(path=path, data=userOrder)
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
        self.createOrder(customerName="João", pizzaName="Calabresa", status="Em preparação", address="Rua da Paz 1428",
                         platform="Instagram", communication="joao@example.com", observation="None")
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
    fc = FirebaseSDKConnection()
    fo = FirebaseOrder(fc)
    # res = fo.createDummyOrder()
    # res = fo.readAllOrders()
    res = fo.updateOrder(orderId=1, observation="Sem cebola")
    # res = fo.getOrderById(1)
    # all_orders = fo.readAllOrders()
    # res = fo.updateOrder(whatsappNumber="+558597648595", status="finished")
    # res = fo.deleteOrder(whatsappNumber="+558597648595")
    return


if __name__ == "__main__":
    __main()
