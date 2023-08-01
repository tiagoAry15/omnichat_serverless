from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_conversation import FirebaseConversation


def get_all_conversations(request=None):
    fc = FirebaseConnection()
    fcm = FirebaseConversation(fc)
    return fcm.getAllConversations()


def __main():
    aux = get_all_conversations()
    print(aux)
    return


if __name__ == '__main__':
    __main()
