import hashlib
import random
import string
from datetime import datetime, timedelta
from random import choice, randint

from faker.providers import BaseProvider

from faker_clickstream.event_constants import weighted_events, events, channel
from faker_clickstream.ip import ip_list
from faker_clickstream.mobile_phones import mobile_phones
from faker_clickstream.user_agents import user_agents


class ClickstreamProvider(BaseProvider):
    """
        A Provider for clickstream related test data.

        >>> from faker import Faker
        >>> from faker_clickstream import ClickstreamProvider
        >>> fake = Faker()
        >>> fake.add_provider(ClickstreamProvider)
        >>> fake.session_clickstream()
    """

    def user_agent(self):
        """
        Generate random user agent.

        :return: User agent string
        """
        return choice(user_agents)

    def event(self):
        """
        Generate random event type name for e-commerce site.

        :return: Event type string
        """
        return choice(events)

    def weighted_event(self):
        """
        Generate a random event object according to popularity weight. Higher popularity increases the
        chances of occurrence.

        :return: Event object (JSON)
        """
        return random.choices(weighted_events, weights=[e['popularity'] for e in weighted_events], k=1)[0]

    def session_clickstream(self, rand_session_max_size: int = 25):
        """
        Generate session clickstream events.

        :param rand_session_max_size: Max number of possible events in session. Defaults to 25.
        :return: List of session events
        """

        # Initialize static session values
        session_events = []
        user_id = _get_user_id()
        user_agent = self.user_agent()
        session_id = _get_session_id()
        ip = _get_ip()
        channel_type = _get_channel()
        random_session_size = randint(1, rand_session_max_size)
        incremental_delta_delay = randint(1, 60)

        # Keep track of unique values in a session
        unique_session_events = set()
        product_codes = set()

        for s in range(random_session_size):
            # Mock time delay between events
            incremental_delta_delay = incremental_delta_delay + (s * randint(1, 60))
            event_time = _format_time(_get_event_time(delta=incremental_delta_delay))

            # Fetch weighted event
            event = self.weighted_event()

            if (event['name'] == 'Login' and event['name'] in unique_session_events) \
                    or (event['name'] == 'CheckoutAsGuest' and user_id != 0):
                # If user ID is not 0, discard CheckoutAsGuest event
                # or Login exists in session, discard Login event
                # Add a mock Search event
                event['name'] = 'Search'

            if event['name'] == 'Login' and user_id == 0:
                # If user id is -1 and Login event, regenerate user ID.
                user_id = _get_user_id(start=1)

            if (event['name'] == 'Login' and user_id != 0) or (event['name'] == 'Logout' and user_id == 0):
                # Add a mock Search event
                event['name'] = 'Search'

            # Keep track of unique events in session
            unique_session_events.add(event['name'])

            # Handle event dependencies
            if len(event['dependsOn']):
                list_check = [d in unique_session_events for d in event['dependsOn']]
                if event['dependencyFilter'] == 'all':
                    f = all(list_check)
                else:
                    f = any(list_check)
                if not f:
                    # Add a mock Search event
                    event['name'] = 'Search'

            # If CompleteOrder, remove some events from the unique list to reoccur.
            if event['name'] == 'CompleteOrder':
                if 'Checkout' in unique_session_events:
                    unique_session_events.remove('Checkout')
                if 'CheckoutAsGuest' in unique_session_events:
                    unique_session_events.remove('CheckoutAsGuest')
                if 'DecreaseQuantity' in unique_session_events:
                    unique_session_events.remove('DecreaseQuantity')

            # Fill metadata object conditionally
            metadata = {}
            if event['name'] == 'Search':
                sample_product = _get_weighted_mobile_phone()
                metadata['query'] = choice(
                    (sample_product['model_name'], sample_product['brand_name'], sample_product['os'])
                )

            if event['name'] in ('AddToCart', 'IncreaseQuantity'):
                metadata['product_id'] = _get_product_code()
                metadata['quantity'] = _get_quantity()
                product_codes.add(metadata['product_id'])

            if event['name'] == 'DeleteFromCart':
                if len(product_codes):
                    random_delete = choice(list(product_codes))
                    product_codes.remove(random_delete)
                    metadata['product_id'] = random_delete

            if event['name'] == 'CheckOrderStatus':
                metadata['order_id'] = _get_order_id()

            # Construct final event object
            r = {
                "ip": ip,
                "user_id": user_id,
                "user_agent": user_agent,
                "session_id": session_id,
                "event_time": event_time,
                "event_name": event['name'],
                "channel": channel_type,
                "metadata": metadata
            }
            session_events.append(r)
        return session_events


def _get_session_id():
    """
    Generate session ID

    :return: Session ID string
    """
    return hashlib.sha256(
        ('%s%s%s' % (
            datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"),
            (''.join(random.choice(string.ascii_lowercase)) for _ in range(10)),
            'faker_clickstream'
        )).encode('utf-8')
    ).hexdigest()


def _get_product_code():
    """
    Generate random product code from range 1 to 999999.

    :return: Random integer number
    """
    return randint(1, 999999)


def _get_order_id():
    """
    Generate random order id from range 1 to 999999.

    :return: Random integer number
    """
    return randint(1, 999999)


def _get_user_id(start: int = 0, end: int = 999999):
    """
    Generate random user id from range 0 to 999999. Zero value may identify null user.

    :param start: Index start (Default: 0)
    :param end: Index end (Default: 999999)
    :return:
    """
    return randint(start, end)


def _get_event_time(delta):
    """
    Generate current event time, added by some delta value.

    :param delta: Delta time value in seconds
    :return: Event time
    """
    return datetime.now() + timedelta(seconds=delta)


def _format_time(t):
    """
    Format time to string.

    :param t: Time object
    :return: Time string in format like 28/03/2022 23:22:15.360252
    """
    return t.strftime("%d/%m/%Y %H:%M:%S.%f")


def _get_quantity():
    """
    Get random product order quantity from 1 to 5. Values are given a weight, decreasing as the quantity number
    increases.

    :return: Product quantity number
    """
    return random.choices([1, 2, 3, 4, 5], weights=[50, 20, 20, 5, 5], k=1)[0]


def _get_weighted_mobile_phone():
    """
    Get mobile phone object according to popularity

    :return: Mobile phone object
    """
    return random.choices(mobile_phones, weights=[e['popularity'] for e in mobile_phones], k=1)[0]


def _get_ip():
    """
    Get random IP address from list.

    :return: IP address string
    """
    return choice(ip_list)


def _get_channel():
    """
    Get user origin channel (e.g. "Organic search", "Direct", "Social media", "Referral", "Other")

    :return: Origin channel string
    """
    return choice(channel)
