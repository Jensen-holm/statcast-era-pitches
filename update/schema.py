import polars as pl


# statcast data types: https://baseballsavant.mlb.com/csv-docs
__all__ = ["STATCAST_SCHEMA"]

DATE_FEATURES = {"game_date": pl.Date}

STRING_FEATURES = {
    col: pl.String
    for col in [
        "player_name",
        "bb_type",
        "pitch_type",
        "p_throws",
        "stand",
        "home_team",
        "away_team",
        "description",
        "des",
        "events",
        "type",
        "if_fielding_alignment",
        "of_fielding_alignment",
        "sv_id",
    ]
}


FLOAT_FEATURES = {
    col: pl.Float64
    for col in [
        "bat_speed",
        "break_length_deprecated",
        "break_angle_deprecated",
        "swing_length",
        "release_speed",
        "release_pos_x",
        "release_pos_y",
        "release_pos_z",
        "release_spin",
        "break_angle",
        "hit_location",
        "pfx_x",
        "pfx_z",
        "plate_x",
        "plate_z",
        "inning",
        "vx0",
        "vy0",
        "vz0",
        "ax",
        "ay",
        "az",
        "sz_top",
        "sz_bot",
        "hit_distance",
        "launch_speed",
        "launch_angle",
        "launch_speed_angle",
        "effective_speed",
        "release_spin",
        "release_extension",
        "release_pos_y",
        "estimated_ba_using_speedangle",
        "estimated_woba_using_speedangle",
        "woba_value",
        "woba_denom",
        "babip_value",
        "iso_value",
        "delta_home_win_exp",
        "delta_run_exp",
        "tfs_deprecated",
        "tfs_zulu_deprecated",
    ]
}


INT_FEATURES = {
    col: pl.Int64
    for col in [
        "balls",
        "strikes",
        "outs_when_up",
        "batter",
        "pitcher",
        "game_year",
        "on_3b",
        "on_2b",
        "on_1b",
        "game_pk",
        "fielder_2",
        "fielder_3",
        "fielder_4",
        "fielder_5",
        "fielder_6",
        "fielder_7",
        "fielder_8",
        "fielder_9",
        "at_bat_number",
        "pitch_number",
        "home_score",
        "away_score",
        "bat_score",
        "post_home_score",
        "post_away_score",
        "post_bat_score",
        "zone",
        "spin_axis",
        "post_bat_score",
        "post_fld_score",
        "post_away_score",
        "post_home_score",
    ]
}

STATCAST_SCHEMA = FLOAT_FEATURES | INT_FEATURES | DATE_FEATURES | STRING_FEATURES
