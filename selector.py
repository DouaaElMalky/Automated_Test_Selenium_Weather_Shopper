landing_page = {
    'temperature': 'temperature',
    'moisturizer_button': '/html/body/div[1]/div[3]/div[1]/a/button',
    'sunscreen_button': '/html/body/div[1]/div[3]/div[2]/a/button'
}

product_card = {
    'all_products': "//button[contains(text(), 'Add')]/ancestor::div[@class='text-center col-4']",
    'name': ".//p[contains(@class, 'font-weight-bold')]",
    'price': ".//p[contains(@class, 'font-weight-bold')]/following-sibling::p",
    'add_button': './button',
    'cart_button': '//*[@id="cart"]'
}

cart = {
    'base': '/html/body/div[1]/div[2]/table',
    'pay_button': 'stripe-button-el',
    'stripe_iframe': '//iframe'
}

payment = {
    'email': '//*[@id="email"]',
    'card_number': '//*[@id="card_number"]',
    'expiry_date': '//*[@id="cc-exp"]',
    'cvc_code': '//*[@id="cc-csc"]',
    'zip_code': '//*[@id="billing-zip"]',
    'submit_button': 'submitButton'
}

confirmation = {
    'header': 'h2'
}