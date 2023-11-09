from authentication.auth_factory import FirebaseConnectionFactory
from authentication.firebase_rules.firebase_toggler import FirebaseToggler
from factory.global_object import GlobalObject
from firebaseFolder.firebase_conversation import FirebaseConversation
from firebaseFolder.firebase_order import FirebaseOrder
from firebaseFolder.firebase_user import FirebaseUser

factory = FirebaseConnectionFactory()
fc = factory.create_connection("HTTP")
fcm = FirebaseConversation(fc)
fu = FirebaseUser(fc)
fo = FirebaseOrder(fc)
ft = FirebaseToggler()
g = GlobalObject()
