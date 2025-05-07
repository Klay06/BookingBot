from booking.booking import Booking
import time

with Booking() as bot:
    bot.land_first_page()
    
    bot.change_currency(currency='AUD')
    bot.select_place_to_go('Rabat')
    time.sleep(10)




