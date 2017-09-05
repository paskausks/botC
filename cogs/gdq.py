from discord.ext import commands
import datetime
import math


class Gdq:
    def __init__(self, bot):
        self.bot = bot

    def time_until(self, trg_date, evnt_name='event'):
        """
        Returns time remaining until trg_date.
        :param date: datetime.datetime instance given in UTC. If no tzinfo is provided, UTC is presumed.
        """

        if not isinstance(trg_date, datetime.datetime):
            raise TypeError('trg_date must be an instance of datetime.')

        result = 'Time until %s: ' % evnt_name
        utcnow = datetime.datetime.now(datetime.timezone.utc)

        # Define a table of time units starting from biggest to smallest
        # with the first element being the amount of seconds in the time unit,
        # and the second being the name of the time unit in singular
        time_units = (
            (60 * 60 * 24 * 30, 'month'),
            (60 * 60 * 24, 'day'),
            (60 * 60, 'hour'),
            (60, 'minute'),
            (1, 'second'),
        )

        if not trg_date.tzinfo:
            # Naive date, presume UTC
            trg_date = trg_date.replace(tzinfo=datetime.timezone.utc)

        dt_seconds = (trg_date - utcnow).total_seconds()
        if dt_seconds < 0:
            # Event already happened
            result += 'Already happened!'
            return result

        # Cycle over the time units and build up final result
        for sec_in_unit, unit_name in time_units:
            unit_amnt_in_total = int(math.floor(dt_seconds / sec_in_unit))
            if unit_amnt_in_total:
                # Whole amount/-s of unit in time unprocessed
                # Add plural if needed
                unit_name = unit_name + 's' if unit_amnt_in_total > 1 else unit_name

                # Subtract processed amount
                dt_seconds -= unit_amnt_in_total * sec_in_unit

                # Update result message
                result += '%d %s' % (unit_amnt_in_total, unit_name)

                if dt_seconds < 1:
                    # Nothing more to process
                    break

                # Seconds left for processing
                result += ', '

        return result

    @commands.command(no_pm=True)
    async def countdown(self):
        text = self.time_until(datetime.datetime(2017, 7, 2, 16, 30), 'SGDQ2017')
        await self.bot.say(text)


def setup(bot):
    n = Gdq(bot)
    bot.add_cog(n)
