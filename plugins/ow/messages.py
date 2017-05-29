from plugins.ow.mappings import (diff_stats, dps_stats, overall_stats,
                                 support_stats, tank_stats)
from plugins.ow.settings import OW_DPS, OW_HEROES_MAPPING, OW_SUPPORT, OW_TANK


class OWMessage:

    def __init__(self, battletag: str, row_data: dict=None):
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


class OWDiffStatsMessage(OWMessage):
    def __init__(self, battletag, prev_data, curr_data):
        super().__init__(battletag)
        self.prev_data = prev_data
        self.current_data = curr_data
        self.comprank_changed, self.level_changed = self.show_stats_diff()

    def show_stats_diff(self):
        comprank_changed = (
            int(self.current_data["comprank"]) - int(self.prev_data[b"comprank"])
        )

        level_changed = (
            int(self.current_data["level"]) - int(self.prev_data[b"level"])
        )

        return comprank_changed, level_changed

    def make_me_pretty(self):
        if self.comprank_changed == 0 and self.level_changed == 0:
            return "`[{}]` *- your stats didn't change*".format(
                self.battletag
            )
        else:
            return diff_stats(
                self.battletag,
                self.comprank_changed,
                self.level_changed,
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
