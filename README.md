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
> To install the gecko driver for the first time, pass the --install flag.
### Setting up an IFTTT Recipe
1. Navigate to https://ifttt.com/create/ and click Add on If This. 
2. Search for the Webhooks services
3. Click on "Receive a web request"
4. In the event name field, type "product_list_updated"
5. You should now see the create page again. Click on Add on the Then That button.
6. Search for the action you'd like. For this setup, we will use Notifications.
7. Click on Send a rich notification from the IFTTT app.
8. Set the title to whatever you'd like. 
9. For the message field, type in ``` {{Value1}} was added to Suit Supply sale. ```
10. Click on save.
11. Navigate to https://ifttt.com/maker_webhooks and click on Documentation in the upper right corner.
12. In here, you will find your IFTTT key at the top. Keep this key a secret! This is what you will pass 
as the first arg to the program.


## Usage
```bash
$ python suit_supply.py IFTTT_key filter color size event
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
