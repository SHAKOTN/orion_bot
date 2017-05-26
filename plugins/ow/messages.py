from plugins.ow.mappings import dps_stats, support_stats, tank_stats
from settings import OW_DPS, OW_HEROES_MAPPING, OW_SUPPORT, OW_TANK


ROW_MSG_OVERALL_STATS = """
    `[{battletag}]`
        *Your rating is - {comprank}*
        *Your level is - {level}*
        *Games count - {games}*
        *Your tier is - {tier}*
        *Your win rate is {win_rate}%*
        *Wins - {wins}*
        *Losses - {losses}*"""


class OWMessage:

    def __init__(self, battletag: str, row_data: dict):
        self.row_data = row_data
        self._battletag = battletag

    def make_me_pretty(self):
        pass

    @property
    def battletag(self):
        return self._battletag


class OWOverwallMessage(OWMessage):

    def make_me_pretty(self):
        return (
            ROW_MSG_OVERALL_STATS.format(
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


class OWHeroStatMessage(OWMessage):

    def __init__(
            self,
            battletag,
            row_data,
            hero
    ):
        super().__init__(battletag, row_data)

        self.hero = hero

        if OW_HEROES_MAPPING[self.hero] == OW_DPS:
            self.stat_message = dps_stats(
                self.battletag,
                self.hero,
                self.row_data
            )
        elif OW_HEROES_MAPPING[self.hero] == OW_TANK:
            self.stat_message = tank_stats(
                self.battletag,
                self.hero,
                self.row_data
            )
        elif OW_HEROES_MAPPING[self.hero] == OW_SUPPORT:
            self.stat_message = support_stats(
                self.battletag,
                self.hero,
                self.row_data
            )
