from booking.bot import Booking
import time

with Booking() as bot:
    bot.land_first_page()
    
    #bot.change_currency(currency='USD')
    
    bot.select_place_to_go('Rabat')
    bot.select_dates(check_in_date='2025-05-20',check_out_date='2025-05-29')
    bot.select_adults()
    time.sleep(3)



