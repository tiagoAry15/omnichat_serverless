import datetime

from authentication.abstraction.abstract_connection import AbstractFirebaseConnection
from authentication.sdk_auth.firebase_sdk_connection import FirebaseSDKConnection
from firebaseFolder.firebase_core_wrapper import FirebaseWrapper
from utils.patterns import singleton


@singleton
class FirebaseOrder(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: AbstractFirebaseConnection):
        super().__init__()
        self.firebaseConnection = inputFirebaseConnection

    def updateConnection(self):
        self.firebaseConnection.changeDatabaseConnection("orders")

    def getAllOrders(self):
        return self.firebaseConnection.readData()

    def createOrder(self, order_data):
        now = datetime.datetime.now().strftime("%d_%b_%Y_%H_%M_%S_%f")[:-3]
        order_data["timestamp"] = now
        self.firebaseConnection.writeDataWithoutUniqueId(path=f'orders/{now}', data=order_data)
        return now

    def getOrder(self, order_unique_id: str):
        return self.firebaseConnection.getValue(f'orders/{order_unique_id}')

    def updateOrder(self, order_unique_id: str, order_data: dict):
        order = self.getOrder(order_unique_id)
        for key in order_data.keys():
            order[key] = order_data[key]
        return self.firebaseConnection.setValue(f'orders/{order_unique_id}', order)

    def deleteOrder(self, order_unique_id: str):
        return self.firebaseConnection.deleteData(f'orders/{order_unique_id}')


def __main():
    fc = FirebaseSDKConnection()
    fo = FirebaseOrder(fc)
    res = fo.createDummyOrder()
    # res = fo.readAllOrders()
    # res = fo.updateOrder(uniqueOrderId=1, observation="Sem cebola")
    # res = fo.getOrderById(1)
    # all_orders = fo.readAllOrders()
    # res = fo.updateOrder(whatsappNumber="+558597648595", status="finished")
    # res = fo.deleteOrder(whatsappNumber="+558597648595")
    return


if __name__ == "__main__":
    __main()
