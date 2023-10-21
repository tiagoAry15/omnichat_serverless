from dotenv import load_dotenv

from authentication.firebase_rules.firebase_rules_manager import get_service_account_access_token, \
    update_firebase_rules, fetch_firebase_rules
from authentication.firebase_rules.pre_made_rules import get_enable_firebase_rule, get_disable_firebase_rule


class FirebaseToggler:
    def __init__(self):
        load_dotenv()
        self.token = get_service_account_access_token()
        self.database_url = "https://pizzadobill-rpin-default-rtdb.firebaseio.com/"

    def enable_firebase(self):
        enable_rule = get_enable_firebase_rule()
        return update_firebase_rules(access_token=self.token, new_rule=enable_rule, database_url=self.database_url)

    def disable_firebase(self):
        disable_rule = get_disable_firebase_rule()
        return update_firebase_rules(access_token=self.token, new_rule=disable_rule, database_url=self.database_url)

    def get_current_firebase_rule(self):
        return fetch_firebase_rules(access_token=self.token, database_url=self.database_url)


def __main():
    ft = FirebaseToggler()
    # current_rule = ft.get_current_firebase_rule()
    # print(current_rule)
    ft.enable_firebase()
    return


if __name__ == '__main__':
    __main()
