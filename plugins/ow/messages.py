ROW_MSG_OVERALL_STATS = """
    `[{battletag}]`
        *Your rating is - {comprank}*
        *Your level is - {level}*
        *Games count - {games}*
        *Your tier is - {tier}*
        *Your win rate is {win_rate}%*
        *Wins - {wins}*
        *Losses - {losses}*"""

ROW_MSG_HERO_STATS = """
    `[{battletag} {hero}]`
        *Damage done average - {dmg_avg}* 
        *Eliminations average - {elim_avg}* 
        *Objective kills average - {obj_kills_avg}* 
        *Solo kills average - {solo_kills_avg}* 
        *Death average - {death_avg}* 
"""


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

    def make_me_pretty(self):
        return(
            ROW_MSG_HERO_STATS.format(
                battletag=self.battletag,
                hero=self.hero,
                dmg_avg=self.row_data.get("damage_done_average", ""),
                elim_avg=self.row_data.get("eliminations_average", ""),
                obj_kills_avg=self.row_data.get("objective_kills_average", ""),
                solo_kills_avg=self.row_data.get("solo_kills_average", ""),
                death_avg=self.row_data.get("deaths_average", "")
            )
        )