from requests import request

class Lnbits:

    def __init__(
                self, 
                admin_key: str = None, 
                invoice_key: str = None, 
                wallet_id: str = None, 
                wallet_user: str = None,
                url: str = "https://legend.lnbits.com/api"
        ):
        self.url = url
        self.wallet_id = wallet_id
        self.admin_key = admin_key
        self.invoice_key = invoice_key
        self.wallet_user = wallet_user

    def load_wallet(self, admin_key: str = None, invoice_key: str = None, wallet_id: str = None, wallet_user: str = None):
        self.wallet_id = wallet_id
        self.admin_key = admin_key
        self.invoice_key = invoice_key
        self.wallet_user = wallet_user

    def call(self, method: str, path: str, data=None, is_admin=False) -> dict:
        if (is_admin == True):
            headers = {"X-Api-Key": self.admin_key}
        else:
            if (self.invoice_key != None):
                headers = {"X-Api-Key": self.invoice_key}
            else:
                headers = {"X-Api-Key": self.admin_key}
        return request(method=method, url=self.url + path, headers=headers, json=data).json()
    
    def create_account(self, name: str = "wallet") -> dict:
        return request("POST", url=self.url.replace("/api", "") \
                       + "/api/v1/account", json={"name": name}).json()

    def enable_extensions(self, extension: str):
        r = request("GET", url=self.url.replace("/api", "") \
                       + f"/extensions?usr={self.wallet_user}&enable={extension}")
        return r.status_code == 200

    def decode_invoice(self, payment_request: str) -> dict:
        data = {"data": payment_request}
        return self.call("POST", "/v1/payments/decode", data=data)

    def get_wallet(self):
        return self.call("GET", "/v1/wallet")

    def list_payments(self, offset: int = 0, limit: int = 10):
        return self.call("GET", "/v1/payments")

    def create_invoice(self, amount: float, memo=None, unit="sat", expiry=(60 * 60) * 2, webhook=None) -> dict:
        data = {"out": False, "amount": amount, "memo": memo, "expiry": expiry, "unit": unit, "webhook": webhook}
        return self.call("POST", "/v1/payments", data=data)

    def check_invoice_status(self, payment_hash: str) -> dict:
        return self.call("GET", f"/v1/payments/{payment_hash}")

    def pay_invoice(self, invoice: str) -> dict:
        data = {"out": True, "bolt11": invoice}
        return self.call("POST", "/v1/payments", data=data, is_admin=True)
