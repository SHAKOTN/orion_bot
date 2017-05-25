ROW_MSG = """
    `[{battletag}]`
        *Your rating is - {comprank}*
        *Your level is - {level}*
        *Competitive games count - {games}*
        *Your tier is - {tier}*
        *Your win rate is {win_rate}%*
        *Wins - {wins}*
        *Losses - {losses}*"""


class OWOverwallMessage:

    def __init__(self, battletag: str, row_data: dict):
        self.row_data = row_data
        self._battletag = battletag

    def make_me_pretty(self):
        return (
            ROW_MSG.format(
                battletag=self.battletag,
                comprank=self.row_data["comprank"],
                level=str(
                    int(self.row_data["level"]) + int(self.row_data["prestige"]) * 100
                ),
                games=self.row_data["games"],
                tier=self.row_data["tier"],
                win_rate=self.row_data["win_rate"],
                wins=self.row_data["wins"],
                losses=self.row_data["losses"]
            )
        ).lstrip()

    @property
    def battletag(self):
        return self._battletag