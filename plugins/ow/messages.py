from plugins.ow.mappings import (dps_stats, overall_stats, support_stats,
                                 tank_stats)
from plugins.settings import OW_DPS, OW_HEROES_MAPPING, OW_SUPPORT, OW_TANK


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
        return overall_stats(
            self.battletag,
            self.row_data
        )


class OWHeroStatMessage(OWMessage):

    def __init__(
            self,
            battletag,
            row_data,
            hero
    ):
        super().__init__(battletag, row_data)

        self.hero = hero

    def make_me_pretty(self):
        if OW_HEROES_MAPPING[self.hero] == OW_DPS:
            return dps_stats(
                self.battletag,
                self.hero,
                self.row_data
            )
        elif OW_HEROES_MAPPING[self.hero] == OW_TANK:
            return tank_stats(
                self.battletag,
                self.hero,
                self.row_data
            )
        elif OW_HEROES_MAPPING[self.hero] == OW_SUPPORT:
            return support_stats(
                self.battletag,
                self.hero,
                self.row_data
            )
