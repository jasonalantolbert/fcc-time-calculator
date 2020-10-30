def add_time(start, duration, current_day=None) -> str:
    """
    Adds an amount of hours and minutes to a given time and returns the result.
    @param start: The initial time in the format HH:MM AM/PM.
    @param duration: The amount of time to add in the format HH:MM.
    @param current_day: A day of the week. Defaults to None.
    @return: A nicely-formatted string containing information about the new time.
    """

    def split_and_convert_time(time) -> list:
        """
        Converts a given time to 24-hour format and splits it into its hour and minute parts.
        @param time: The time to convert and split.
        @return: A list in the form [int(hour), int(minute)].
        """
        hour, minute = time.split(sep=":")
        if "M" in minute:
            minute, meridiem = minute.split(sep=" ")
            if meridiem == "PM":
                hour = int(hour) + 12
            elif int(hour) == 12:
                hour = int(hour) * 0
        return [int(hour), int(minute)]

    def calculate_new_time(start_list, duration_list) -> tuple:
        """
        Calculates the new time.
        @param start_list: A list containing the components of the initial time.
        @param duration_list: A list containing the components of the duration that is to be added to the initial time.
        @return: A tuple containing a dictionary with the components of the calculated new time, the number of days
        that have passed between the initial time and the calculated new time, and the new day of the week (if one
        was provided).
        """
        days_passed = 0

        new_hour = start_list[0] + duration_list[0]

        new_minute = start_list[1] + duration_list[1]
        if new_minute > 59:
            new_minute -= 60
            new_hour += 1

        if new_hour > 23:
            while new_hour > 23:
                new_hour -= 24
                days_passed += 1

        meridiem = "AM" if new_hour < 12 else "PM"

        if new_hour > 12:
            new_hour -= 12
        elif new_hour == 0:
            new_hour = 12

        if len(str(new_minute)) == 1:  # appends a leading zero to single-digit minutes
            new_minute = "0" + str(new_minute)

        new_time_dict = {"hour": new_hour, "minute": new_minute, "meridiem": meridiem}

        if current_day:  # calculates new day of the week
            day_codes = {1: "sunday",
                         2: "monday",
                         3: "tuesday",
                         4: "wednesday",
                         5: "thursday",
                         6: "friday",
                         7: "saturday"}

            current_day_code = list(day_codes.keys())[list(day_codes.values()).index(current_day.lower())]
            new_day_code = current_day_code + days_passed
            if new_day_code > 7:
                new_day_code -= 7 * (new_day_code // 7)
            new_day = day_codes[new_day_code]
            return new_time_dict, days_passed, new_day
        else:
            return new_time_dict, days_passed, None

    def create_time_string(new_time_dict, days_passed, new_day) -> str:
        """
        Creates a nicely-formatted string containing information about the new time.
        @param new_time_dict: A dictionary containing the components of the new time.
        @param days_passed: The number of days that have passed between the initial time and calculated new time.
        @param new_day: The new day of the week, or None, depending on the result of calculate_new_time().
        @return: A nicely-formatted string containing the new time, the number of days that have passed (if applicable),
        and the new day of the week.
        """
        string = ""
        string += f"{new_time_dict['hour']}:{new_time_dict['minute']} {new_time_dict['meridiem']}"
        if new_day:
            string += f", {new_day.capitalize()}"
        if days_passed:
            string += f" ({f'next day' if days_passed == 1 else f'{days_passed} days later'})"
        return string

    def main() -> str:
        """
        Controls all other inner functions of add_time().
        @return: The string recieved from create_time_string().
        """
        start_dict = split_and_convert_time(start)
        duration_list = split_and_convert_time(duration)
        new_time_dict, days_passed, new_day = calculate_new_time(start_dict, duration_list)
        new_time_string = create_time_string(new_time_dict, days_passed, new_day)
        return new_time_string

    return main()
