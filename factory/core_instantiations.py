from authentication.auth_factory import FirebaseConnectionFactory
from authentication.firebase_rules.firebase_toggler import FirebaseToggler
from firebaseFolder.firebase_conversation import FirebaseConversation
from firebaseFolder.firebase_order import FirebaseOrder

factory = FirebaseConnectionFactory()
fc = factory.create_connection("HTTP")
fcm = FirebaseConversation(fc)
fo = FirebaseOrder(fc)
ft = FirebaseToggler()