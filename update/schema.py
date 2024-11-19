import polars as pl


# statcast data types: https://baseballsavant.mlb.com/csv-docs
__all__ = ["STATCAST_SCHEMA"]

DATE_FEATURES = {"game_date": pl.Datetime}

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
        "game_type",
        "inning_topbot",
        "pitch_name",
    ]
}


FLOAT_FEATURES = {
    col: pl.Float64
    for col in [
        "hc_x",
        "hc_y",
        "bat_speed",
        "swing_length",
        "release_speed",
        "release_pos_x",
        "release_pos_y",
        "release_pos_z",
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
        "launch_speed",
        "launch_angle",
        "launch_speed_angle",
        "effective_speed",
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
        # new with arm angle update
        "arm_angle",
        "api_break_x_batter_in",
        "api_break_x_arm",
        "api_break_z_with_gravity",
        "bat_win_exp",
        "home_win_exp",
        "hyper_speed",
        "delta_pitcher_run_exp",
        "estimated_slg_using_speedangle",
    ]
}


INT_FEATURES = {
    col: pl.Int64
    for col in [
        "hit_distance_sc",
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
        "fld_score",
        "fielder_2.1",
        "pitcher.1",
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
        "release_spin_rate",
        "spin_dir",
        "umpire",
        # new with arm angle update
        "batter_days_until_next_game",
        "pitcher_days_until_next_game",
        "batter_days_since_prev_game",
        "pitcher_days_since_prev_game",
        "n_priorpa_thisgame_player_at_bat",
        "n_thruorder_pitcher",
        "age_bat",
        "age_pit",
        "age_bat_legacy",
        "age_pit_legacy",
        "bat_score_diff",
        "home_score_diff",
        # deprecated, all nulls
        "spin_rate_deprecated",
        "break_length_deprecated",
        "break_angle_deprecated",
        "tfs_deprecated",
        "tfs_zulu_deprecated",
    ]
}

STATCAST_SCHEMA = FLOAT_FEATURES | INT_FEATURES | DATE_FEATURES | STRING_FEATURES
