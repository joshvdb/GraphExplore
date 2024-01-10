class Account:
    """
    Define the class used to store user account details.
    """
    def __init__(self, account_name, account_description, follower_accounts, following_accounts):
        self.account_name = account_name
        self.account_description = account_description
        self.follower_accounts = follower_accounts
        self.following_accounts = following_accounts