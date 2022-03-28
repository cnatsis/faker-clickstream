events = [
    "Search",
    "AddToCart",
    "DeleteFromCart",
    "IncreaseQuantity",
    "DecreaseQuantity",
    "AddPromoCode",
    "Checkout",
    "Login",
    "Logout",
    "CheckoutAsGuest"
    "CompleteOrder",
    "CheckOrderStatus"
]

weighted_events = [
    {
        "name": "Search",
        "popularity": 85,
        "dependsOn": [],
        "dependencyFilter": "any"
    },
    {
        "name": "AddToCart",
        "popularity": 70,
        "dependsOn": [],
        "dependencyFilter": "any"
    },
    {
        "name": "DeleteFromCart",
        "popularity": 55,
        "dependsOn": ["AddToCart"],
        "dependencyFilter": "any"
    },
    {
        "name": "IncreaseQuantity",
        "popularity": 40,
        "dependsOn": [],
        "dependencyFilter": "any"
    },
    {
        "name": "DecreaseQuantity",
        "popularity": 40,
        "dependsOn": ["IncreaseQuantity"],
        "dependencyFilter": "any"
    },
    {
        "name": "AddPromoCode",
        "popularity": 25,
        "dependsOn": ["Checkout"],
        "dependencyFilter": "any"
    },
    {
        "name": "Checkout",
        "popularity": 75,
        "dependsOn": ["AddToCart"],
        "dependencyFilter": "any"
    },
    {
        "name": "Login",
        "popularity": 70,
        "dependsOn": [],
        "dependencyFilter": "any"
    },
    {
        "name": "Logout",
        "popularity": 30,
        "dependsOn": ["Login"],
        "dependencyFilter": "any"
    },
    {
        "name": "CheckoutAsGuest",
        "popularity": 40,
        "dependsOn": [],
        "dependencyFilter": "any"
    },
    {
        "name": "CompleteOrder",
        "popularity": 65,
        "dependsOn": ["Checkout", "CheckoutAsGuest"],
        "dependencyFilter": "any"
    },
    {
        "name": "CheckOrderStatus",
        "popularity": 70,
        "dependsOn": ["Login"],
        "dependencyFilter": "any"
    }
]

channel = [
    "Organic search",
    "Direct",
    "Social media",
    "Referral",
    "Other"
]
