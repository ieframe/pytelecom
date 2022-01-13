## PYTelecom
A [python](https://www.python.org/) implementation of the [BH Telecom](https://www.bhtelecom.ba/) android [application](https://play.google.com/store/apps/details?id=ba.bhtelecom.mojbhtelecom).

## Prerequisites
- A sim card registered with the carrier
- A Moj BH Telecom account

The account can be obtained by texting `061-1103` with `PRIJAVA`. A new password can be requested with `RESET`.

```
Example username: 38761234567
Example password: a12Bc3

Note: The username must include a country code.
```

- Python 3
- Python requests module

Python can be obtained [here](https://www.python.org/downloads/). Installation instructions for requests are available [here](https://docs.python-requests.org/en/latest/user/install/).

## Configuration
The android application uses [OAuth 2.0](https://oauth.net/2/) for authentication. Changes to the client_id and client_secret can be performed as such.

```python
import pytelecom

pytelecom.CLIENT_ID = "id-new-example"
pytelecom.CLIENT_SECRET = "secret-new-example"
```

The default request configuration denotes that it was made in an automated fashion. Changes to the user agent string can be performed as such.

```python
import pytelecom

pytelecom.SESSION_AGENT = "okhttp/3.14.9"
```

## Examples
Let's transfer some credit from our account and activate a package.

```python
import pytelecom

user = pytelecom.User()
user.auth("38761234567", "a12Bc3")

user.transfer(10.00, "38761765432")
user.activate("Travel")
```

Now let's get some info about the customer.

```python
import pytelecom

user = pytelecom.User()
user.auth("38761234567", "a12Bc3")

customer = user.get_customer()
print(customer["customer_name"])

# User now also holds a reference of the customer data.
print(user.customer["customer_name"])
```

All values are examples. Error checking omitted.