from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation
from utils.createDummyConversations import createDummyConversations


class ConversationCrud:
    def __init__(self):
        self.fc = FirebaseConnection()
        self.fcm = FirebaseConversation(self.fc)

    def getAllConversations(self) -> dict:
        return self.fcm.getAllConversations()

    @staticmethod
    def insertDummyConversations(parameters: tuple):
        createDummyConversations(parameters)


def __main():
    cc = ConversationCrud()
    aux = cc.getAllConversations()
    return


if __name__ == '__main__':
    __main()
