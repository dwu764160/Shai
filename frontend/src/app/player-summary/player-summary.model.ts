// frontend/src/app/player-summary/player-summary.model.ts

export interface Shot {
  shot_loc_x: number;
  shot_loc_y: number;
  action_type: string;
}

export interface Pass {
  pass_start_loc_x: number;
  pass_start_loc_y: number;
  pass_end_loc_x: number;
  pass_end_loc_y: number;
  action_type: string;
}

export interface Turnover {
  turnover_loc_x: number;
  turnover_loc_y: number;
  action_type: string;
}

export interface ActionStats {
  points: number;
  shots: number;
  passes: number;
  turnovers: number;
  potential_assists: number;
  shooting_fouls: number;
}

export interface Totals {
  total_points: number;
  total_shots: number;
  total_passes: number;
  total_turnovers: number;
  total_potential_assists: number;
  total_shooting_fouls: number;
}

export interface Ranks {
  points: number;
  shots: number;
  passes: number;
  turnovers: number;
  potential_assists: number;
  shooting_fouls: number;
}

export interface PlayerSummary {
  player_id: number;
  player_name: string;
  team_name: string;
  shots: Shot[];
  passes: Pass[];
  turnovers: Turnover[];
  stats_by_action: {
    pickAndRoll: ActionStats;
    isolation: ActionStats;
    postUp: ActionStats;
    offBallScreen: ActionStats;
  };
  totals: Totals;
  ranks: Ranks;
}