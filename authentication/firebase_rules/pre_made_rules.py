def get_enable_firebase_rule() -> dict:
    return {"rules": {
        ".read": "auth != null && auth.uid === 'geoztGJEq7NRdKPbxyfziXXfKNn2'",
        ".write": "auth != null && auth.uid === 'geoztGJEq7NRdKPbxyfziXXfKNn2'",
    }}


def get_disable_firebase_rule() -> dict:
    return {"rules": {
        ".read": False,
        ".write": False,
    }}
