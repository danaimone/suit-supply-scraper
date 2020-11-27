# Welcome to Suit Supply Scraper!
## Introduction
> This program was developed in a few hours and could definitely use some work.
> Since the suit supply outlet was restocking their site constantly
> with items, I thought it'd be useful to be able to know exactly
> when the product you were searching for came back in stock. Thus, the suit 
> supply scraper was created!
## Implementation Details
> Since suit supply wasn't responding properly to POST and GET requests to get
>pass the access code page, I ended up using Selenium to simulate an actual user.
> This requires the use of geckodriver, since this program simulates a headless Firefox browser.

## Installation
```bash
$ pip install -r requirements.txt
```
>You will also need to setup an IFTTT recipe on your personal account.
This recipe will use the Webhook and Notification applets.
> The event name that you setup should be "product_list_updated". This can be customized,
>as the event name is an optional parameter for the program.

## Usage
```bash
$ python suit-supply.py IFTTT_key filter color size event
```
> ***IFTTT_key***: the webhook key of your IFTTT recipe, found under Webhook documentation
>
> ***filter***: the items you want to search for, EX: "Dark Grey Sienna"
>
> ***color***: the color of the item you want to search for, "Ex: Grey". Refer to suit supply website for valid colors.
>
> ***size***: the size of the item you want to search for as an int, Ex: 38
>
> ***--event***: An optional parameter for a custom event name for your recipe.

## TODO
- Add color checking
- Setup global IFTTT recipe
