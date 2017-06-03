
def overall_stats(battletag, stats):
    return f"""
    `[{battletag}]`
        *Your rating is - {stats['comprank']}*
        *Your level is - {int(stats['level']) + int(stats['prestige']) * 100}*
        *Games count - {stats['games']}*
        *Your tier is - {stats['tier']}*
        *Your win rate is {stats['win_rate']}%*
        *Wins - {stats['wins']}*
        *Losses - {stats['losses']}*
        *Time played this season - {stats.get('time_played', 0)}hrs*
        *Healing done - {stats.get('healing_done', 0)}*
        *Damage done - {stats.get('damage_done', 0)}*
        """


def diff_stats(battletag, comprank, level):
    return f"""
    `[{battletag}]`
        *Your rating has changed on {comprank} points*
        *You increased your level on {level} points*
    """


def dps_stats(battletag, hero, dps_mapping):
    return f"""
        `[{battletag} {hero}]`
            *Damage done average - {dps_mapping.get('damage_done_average', '')}* 
            *Eliminations average - {dps_mapping.get('eliminations_average', '')}* 
            *Objective kills average - {dps_mapping.get('objective_kills_average', '')}* 
            *Solo kills average - {dps_mapping.get('solo_kills_average', '')}* 
            *Death average - {dps_mapping.get('deaths_average', '')}* 
            *Win percentage - {(round(float(dps_mapping.get('win_percentage', '0')) * 100))}%*
            *Time played - {dps_mapping.get('time_played', '')}hrs*
            *Games played - {dps_mapping.get('games_played', '')}*
            *Games won - {dps_mapping.get('games_won', '')}*
            *Weapon Accuracy - {round(float(dps_mapping.get('weapon_accuracy', '0') * 100), 2)}* %
        """


def support_stats(battletag, hero, support_mapping):
    return f"""
        `[{battletag} {hero}]`
            *Damage done average - {support_mapping.get('damage_done_average', '')}* 
            *Eliminations average - {support_mapping.get('eliminations_average', '')}* 
            *Heal avg - {support_mapping.get('healing_done_average', '')}*
            *Death average - {support_mapping.get('deaths_average', '')}* 
            *Win percentage - {round(float(support_mapping.get('win_percentage', '0')) * 100)}%*
            *Time played - {support_mapping.get('time_played', '')}hrs*
            *Games played - {support_mapping.get('games_played', '')}*
            *Games won - {support_mapping.get('games_won', '')}*
            *Weapon Accuracy - {round(float(support_mapping.get('weapon_accuracy', '0') * 100), 2)}* %
        """


def tank_stats(battletag, hero, tank_mapping):
    return f"""
        `[{battletag} {hero}]`
            *Damage done average - {tank_mapping.get('damage_done_average', '')}* 
            *Eliminations average - {tank_mapping.get('eliminations_average', '')}* 
            *Damage blocked avg - {tank_mapping.get('damage_blocked_average', '')}*
            *Death average - {tank_mapping.get('deaths_average', '')}* 
            *Win percentage - {round(float(tank_mapping.get('win_percentage', '0')) * 100)}%*
            *Time played - {tank_mapping.get('time_played', '')}hrs*
            *Games played - {tank_mapping.get('games_played', '')}*
            *Games won - {tank_mapping.get('games_won', '')}*
            *Weapon Accuracy - {round(float(tank_mapping.get('weapon_accuracy', '0') * 100), 2)}* %
        """
