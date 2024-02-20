import datetime

def get_start_end_dates(week_number, year):
    # Bereken de eerste dag van het jaar
    first_day_of_year = datetime.date(year, 1, 1)
    
    # Bereken het aantal dagen dat is verstreken sinds de eerste dag van het jaar tot de eerste maandag
    days_to_first_monday = (7 - first_day_of_year.weekday()) % 7
    
    # Bereken de datum van de eerste maandag van het jaar
    first_monday = first_day_of_year + datetime.timedelta(days=days_to_first_monday)
    
    # Bereken de datum van de eerste maandag van de gevraagde week
    requested_monday = first_monday + datetime.timedelta(weeks=(week_number - 1))
    
    # Bereken de start- en einddatum van de week
    start_date = requested_monday
    end_date = requested_monday + datetime.timedelta(days=7)

    # Formatteer de einddatum in het gewenste formaat
    f_start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
    f_end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
    
    return f_start_date, f_end_date, week_number


