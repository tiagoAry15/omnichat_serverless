from firebaseFolder.firebase_connection import FirebaseConnection
from firebaseFolder.firebase_core_wrapper import FirebaseWrapper
from utils.patterns import singleton


@singleton
class FirebaseOrder(FirebaseWrapper):
    def __init__(self, inputFirebaseConnection: FirebaseConnection):
        super().__init__()
        self.firebaseConnection = inputFirebaseConnection


def __main():
    fc = FirebaseConnection()
    fo = FirebaseOrder(fc)


if __name__ == "__main__":
    __main()
