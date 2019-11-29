import temperature_sensor

def get_user_info():
    name = input("What is your name?")
    return name

def get_current_temp():
    try:
        current_temp = temperature_sensor.read_temperature()
        if (current_temp > 70) and (current_temp<80):
            return ("Good temp, {}".format(current_temp))
        if current_temp < 0:
            raise OverflowError
        return "Tough weather,{}".format(current_temp)
    except KeyError:
        return 'KeyError'