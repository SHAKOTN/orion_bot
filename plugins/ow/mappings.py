# TODO: Tons of copypasta here. Remove in the nearest future


def overall_stats(battletag, stats):
    return """
    `[{battletag}]`
        *Your rating is - {comprank}*
        *Your level is - {level}*
        *Games count - {games}*
        *Your tier is - {tier}*
        *Your win rate is {win_rate}%*
        *Wins - {wins}*
        *Losses - {losses}*
        *Time played this season - {tm_pld}hrs*
        *Healing done - {hl_done}*
        *Damage done - {dmg_done}*
        """.format(
                battletag=battletag,
                comprank=stats["comprank"],
                level=str(
                    int(stats["level"]) + int(stats["prestige"]) * 100
                ),
                games=stats["games"],
                tier=stats["tier"],
                win_rate=stats["win_rate"],
                wins=stats["wins"],
                losses=stats["losses"],
                tm_pld=stats.get("time_played", 0),
                hl_done=stats.get("healing_done", 0),
                dmg_done=stats.get("damage_done", 0)
    )


def dps_stats(battletag, hero, dps_mapping):
    return """
        `[{battletag} {hero}]`
            *Damage done average - {dmg_avg}* 
            *Eliminations average - {elim_avg}* 
            *Objective kills average - {obj_kills_avg}* 
            *Solo kills average - {solo_kills_avg}* 
            *Death average - {death_avg}* 
            *Win percentage - {win_prcntg}%*
            *Time played - {tm_pld}hrs*
            *Games played - {gms_pld}*
            *Games won - {gms_wn}*
            *Weapon Accuracy - {wpn_acc}* %
        """.format(
        battletag=battletag,
        hero=hero,
        dmg_avg=dps_mapping.get("damage_done_average", ""),
        elim_avg=dps_mapping.get("eliminations_average", ""),
        obj_kills_avg=dps_mapping.get("objective_kills_average", ""),
        solo_kills_avg=dps_mapping.get("solo_kills_average", ""),
        death_avg=dps_mapping.get("deaths_average", ""),
        win_prcntg=round(
            float(
                dps_mapping.get("win_percentage", "0")
            ) * 100
        ),
        tm_pld=dps_mapping.get("time_played", ""),
        gms_pld=dps_mapping.get("games_played", ""),
        gms_wn=dps_mapping.get("games_won", ""),
        wpn_acc=round(
            float(
                dps_mapping.get(
                    "weapon_accuracy",
                    "0"
                ) * 100
            ),
            2)
    )


def support_stats(battletag, hero, support_mapping):
    return """
        `[{battletag} {hero}]`
            *Damage done average - {dmg_avg}* 
            *Eliminations average - {elim_avg}* 
            *Heal avg - {heal_avg}*
            *Death average - {death_avg}* 
            *Win percentage - {win_prcntg}%*
            *Time played - {tm_pld}hrs*
            *Games played - {gms_pld}*
            *Games won - {gms_wn}*
            *Weapon Accuracy - {wpn_acc}* %
        """.format(
        battletag=battletag,
        hero=hero,
        dmg_avg=support_mapping.get("damage_done_average", ""),
        elim_avg=support_mapping.get("eliminations_average", ""),
        heal_avg=support_mapping.get("healing_done_average", ""),
        death_avg=support_mapping.get("deaths_average", ""),
        win_prcntg=round(
            float(
                support_mapping.get("win_percentage", "0")
            ) * 100
        ),
        tm_pld=support_mapping.get("time_played", ""),
        gms_pld=support_mapping.get("games_played", ""),
        gms_wn=support_mapping.get("games_won", ""),
        wpn_acc=round(
            float(
                support_mapping.get(
                    "weapon_accuracy",
                    "0"
                ) * 100
            ),
            2)
    )


def tank_stats(battletag, hero, tank_mapping):
    return """
        `[{battletag} {hero}]`
            *Damage done average - {dmg_avg}* 
            *Eliminations average - {elim_avg}*
            *Damage blocked avg - {dmg_blocked_avg}*
            *Death average - {death_avg}* 
            *Win percentage - {win_prcntg}%*
            *Time played - {tm_pld}hrs*
            *Games played - {gms_pld}*
            *Games won - {gms_wn}*
            *Weapon Accuracy - {wpn_acc}* %
        """.format(
        battletag=battletag,
        hero=hero,
        dmg_avg=tank_mapping.get("damage_done_average", ""),
        elim_avg=tank_mapping.get("eliminations_average", ""),
        dmg_blocked_avg=tank_mapping.get("damage_blocked_average", ""),
        death_avg=tank_mapping.get("deaths_average", ""),
        win_prcntg=round(
            float(
                tank_mapping.get("win_percentage", "0")
            ) * 100
        ),
        tm_pld=tank_mapping.get("time_played", ""),
        gms_pld=tank_mapping.get("games_played", ""),
        gms_wn=tank_mapping.get("games_won", ""),
        wpn_acc=round(
            float(
                tank_mapping.get(
                    "weapon_accuracy",
                    "0"
                ) * 100
            ),
            2)
    )
