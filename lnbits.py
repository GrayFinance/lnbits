from cachetools import cached, TTLCache, LRUCache
from requests import request

class Lnbits:

    def __init__(self, admin_key: str, invoice_key: str, url: str = "https://legend.lnbits.com/api"):
        self.url = url
        self.admin_key = admin_key
        self.invoice_key = invoice_key
    
    def call(self, method: str, path: str, data=None, is_admin=False) -> dict:
        if (is_admin == True):
            headers = {"X-Api-Key": self.admin_key}
        else:
            if (self.invoice_key != None):
                headers = {"X-Api-Key": self.invoice_key}
            else:
                headers = {"X-Api-Key": self.admin_key}
        return request(method=method, url=self.url + path, headers=headers, json=data).json()

    @cached(cache=LRUCache(maxsize=10))
    def decode_invoice(self, payment_request: str) -> dict:
        data = {"data": payment_request}
        return self.call("POST", "/v1/payments/decode", data=data)

    @cached(cache=LRUCache(maxsize=25))
    def get_wallet(self):
        return self.call("GET", "/v1/wallet")

    @cached(TTLCache(maxsize=30, ttl=15))
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
