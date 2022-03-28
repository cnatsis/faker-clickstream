# Clickstream Faker Provider for Python

- [Clickstream Faker Provider for Python](#clickstream-faker-provider-for-python)
  * [Purpose](#purpose)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Features](#features)
  * [Contributing](#contributing)

## Purpose

This is a custom `Faker` provider for Python that generates clickstream session data. Data generated from this provider
represent user clickstream sessions on an online e-commerce site that sells mobile phones.

## Installation

The Clickstream Faker Provider for Python is available to install from PyPi using `pip`.

```bash
pip install faker_clickstream
```

## Usage

Sample code of Clickstream Provider usage.

```python
from faker import Faker
from faker_clickstream import ClickstreamProvider

fake = Faker()
fake.add_provider(ClickstreamProvider)
fake.session_clickstream()

# or...
fake.session_clickstream(rand_session_max_size=50)  # random number of events from 1 to 50
```

The `session_clickstream()` method returns an array of JSON objects that represents a unique web session. By default, is
configured to return a random number of session events from the range of 1 through 25.

An example response object is the below:

```json
[
  {
    "ip": "85.59.39.221",
    "user_id": 777198,
    "user_agent": "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/11D257 Safari/9537.53",
    "session_id": "d5cba274f7724780d1ed2b60650101892260748df21b0e2fb8b2b2fd88cedf23",
    "event_time": "28/03/2022 23:09:48.360212",
    "event_name": "AddToCart",
    "channel": "Social media",
    "metadata": {
      "product_id": 162012,
      "quantity": 1
    }
  },
  {
    "ip": "85.59.39.221",
    "user_id": 777198,
    "user_agent": "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/11D257 Safari/9537.53",
    "session_id": "d5cba274f7724780d1ed2b60650101892260748df21b0e2fb8b2b2fd88cedf23",
    "event_time": "28/03/2022 23:14:13.360227",
    "event_name": "AddToCart",
    "channel": "Social media",
    "metadata": {
      "product_id": 464710,
      "quantity": 2
    }
  },
  {
    "ip": "85.59.39.221",
    "user_id": 777198,
    "user_agent": "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/11D257 Safari/9537.53",
    "session_id": "d5cba274f7724780d1ed2b60650101892260748df21b0e2fb8b2b2fd88cedf23",
    "event_time": "28/03/2022 23:17:49.360241",
    "event_name": "Checkout",
    "channel": "Social media",
    "metadata": {}
  },
  {
    "ip": "85.59.39.221",
    "user_id": 777198,
    "user_agent": "Mozilla/5.0 (iPad; CPU OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) CriOS/45.0.2454.68 Mobile/11D257 Safari/9537.53",
    "session_id": "d5cba274f7724780d1ed2b60650101892260748df21b0e2fb8b2b2fd88cedf23",
    "event_time": "28/03/2022 23:22:15.360252",
    "event_name": "Search",
    "channel": "Social media",
    "metadata": {
      "query": "Samsung"
    }
  }
]
```

## Features

Each user session includes some static data that are randomly calculated only once, such as the `ip`, `user_agent`, etc.

The events that are available on this clickstream are the following ones, and an event dependency has been configured to
provide a more real representation of a web session flow:

- `Search`
- `AddToCart`
- `DeleteFromCart` (depends on `AddToCart` event)
- `IncreaseQuantity`
- `DecreaseQuantity` (depends on `IncreaseQuantity` event)
- `AddPromoCode` (depends on `Checkout` event)
- `Checkout` (depends on `AddToCart` event)
- `Login`
- `Logout` (depends on `Login` event)
- `CheckoutAsGuest`
- `CompleteOrder` (depends on **any** of `Checkout` or `CheckoutAsGuest` events)
- `CheckOrderStatus` (depends on `Login` event)

Moreover, the `Search`, `AddToCart`, `IncreaseQuantity` `DeleteFromCart` & `CheckOrderStatus` include a metadata field
with additional information about the products and the user queries.

## Contributing

Feel free to support this project and contribute! Support this project by giving a star!