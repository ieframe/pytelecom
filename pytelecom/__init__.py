# External Imports
import requests

# Standard Imports
import datetime

# Configuration
CLIENT_ID = "id-edbb2f23-f526-a8e7-b5da-e41eb7d2dc45"
CLIENT_SECRET = "secret-21d99d78-1028-b37a-75d5-2c23206eb7c7"
SESSION_AGENT = "PYTelecom - https://github.com/ieframe/pytelecom"

# Classes
class User:
    def __init__(self) -> None:
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": SESSION_AGENT})

        self._token_access = ""
        self._token_refresh = ""
        self._token_expires = datetime.datetime.today()

        self.customer = {}
        self.bonuses = []
        self.offers = []
        self.prepaid = {}
        self.gsm_listing = []
        self.commerce_listing = []

    # Methods Responsible For Authentication
    def auth(self, username: str, password: str) -> bool:
        request = {
            "password": password,
            "grant_type": "password",
            "client_secret": CLIENT_SECRET,
            "client_id": CLIENT_ID,
            "username": f"{username}@bhmobile.ba"
        }

        try:
            response = self._session.post("https://moj.bhtelecom.ba/o/oauth2/token", data=request)
            response = response.json()
        except:
            return False

        if "error" in response:
            return False

        self._token_access = response["access_token"]
        self._token_refresh = response["refresh_token"]
        self._token_expires = datetime.datetime.today() + datetime.timedelta(int(response["expires_in"]))

        self._session.headers.update({"Authorization": f"Bearer {self._token_access}"})
        return True

    def reauth(self) -> bool:
        if self._token_refresh == "":
            return False
        if self._token_expires > datetime.datetime.today():
            return True

        request = {
            "refresh_token": self._token_refresh,
            "grant_type": "refresh_token",
            "client_secret": CLIENT_SECRET,
            "client_id": CLIENT_ID
        }

        try:
            response = self._session.post("https://moj.bhtelecom.ba/o/oauth2/token", data=request)
            response = response.json()
        except:
            return False

        if "error" in response:
            return False

        self._token_access = response["access_token"]
        self._token_refresh = response["refresh_token"]
        self._token_expires = datetime.datetime.today() + datetime.timedelta(int(response["expires_in"]))

        self._session.headers.update({"Authorization": f"Bearer {self._token_access}"})
        return True

    # Methods Responsible For Functionality
    def transfer(self, amount: float, msisdn: str) -> str:
        if not self.reauth():
            return ""

        request = {
            "Amount": str(amount),
            "ToMSISDN": msisdn
        }

        try:
            response = self._session.post("https://moj.bhtelecom.ba/o/mobile-app/v1/postMcommerceTopup", json=request)
            response = response.text
        except:
            return ""

        return response

    def activate(self, name: str) -> str:
        if not self.reauth():
            return ""

        request = {
            "Name": name
        }

        try:
            response = self._session.post("https://moj.bhtelecom.ba/o/mobile-app/v1/postSetPackageSubscription", json=request)
            response = response.text
        except:
            return ""

        return response

    # Methods Responsible For Retrieving User Data
    def get_customer(self) -> dict:
        if not self.reauth():
            return {}

        try:
            response = self._session.get("https://moj.bhtelecom.ba/o/mobile-app/v1/getCustomer")
            response = response.json()
        except:
            return {}

        self.customer = response
        return self.customer

    def get_bonuses(self) -> list:
        if not self.reauth():
            return []

        try:
            response = self._session.get("https://moj.bhtelecom.ba/o/mobile-app/v1/getPackageSubscriptionBonus")
            response = response.json()
        except:
            return []

        self.bonuses = response
        return self.bonuses

    def get_offers(self) -> list:
        if not self.reauth():
            return []

        try:
            response = self._session.get("https://moj.bhtelecom.ba/o/mobile-app/v1/getPackageSubscriptionOffers")
            response = response.json()
        except:
            return []

        self.offers = response
        return self.offers

    def get_prepaid(self) -> dict:
        if not self.reauth():
            return {}

        try:
            response = self._session.get("https://moj.bhtelecom.ba/o/mobile-app/v1/getPrepaidAccount")
            response = response.json()
        except:
            return {}

        self.prepaid = response
        return self.prepaid

    def get_gsm_listing(self) -> list:
        if not self.reauth():
            return []

        try:
            listing1 = self._session.get("https://moj.bhtelecom.ba/o/mobile-app/v1/getGsmDetailListing")
            listing1 = listing1.json()
            listing2 = self._session.get("https://moj.bhtelecom.ba/o/mobile-app/v1/getGsmDetailListingLastMonth")
            listing2 = listing2.json()
        except:
            return []

        self.gsm_listing = listing1 + listing2
        return self.gsm_listing

    def get_commerce_listing(self) -> list:
        if not self.reauth():
            return []

        try:
            response = self._session.get("https://moj.bhtelecom.ba/o/mobile-app/v1/getMcommerceListing")
            response = response.json()
        except:
            return []

        self.commerce_listing = response
        return self.commerce_listing