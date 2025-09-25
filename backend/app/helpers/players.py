from django.db.models import Sum, Count, Q, Window
from django.db.models.functions import Rank
from app import models

def get_player_summary_stats(player_id: int):
    """
    Aggregates and calculates the summary statistics for a given player.
    """
    # Get the specific player
    player = models.Player.objects.get(id=player_id)

    # Base query for all events related to this player
    player_events = models.Event.objects.filter(player=player)

    # --- Aggregate totals for the entire season ---
    total_stats = player_events.aggregate(
        total_points=Sum('points', default=0),
        total_shots=Count('id', filter=Q(event_type='shot')),
        total_passes=Count('id', filter=Q(event_type='pass')),
        total_turnovers=Count('id', filter=Q(event_type='turnover')),
        total_potential_assists=Count('id', filter=Q(is_potential_assist=True)),
        total_shooting_fouls=Count('id', filter=Q(is_shooting_foul=True))
    )

    # --- Aggregate stats for each action type ---
    action_types = ["pickAndRoll", "isolation", "postUp", "offBallScreen"]
    action_stats = {}

    for action in action_types:
        stats = player_events.filter(action_type=action).aggregate(
            points=Sum('points', default=0),
            shots=Count('id', filter=Q(event_type='shot')),
            passes=Count('id', filter=Q(event_type='pass')),
            turnovers=Count('id', filter=Q(event_type='turnover')),
            potential_assists=Count('id', filter=Q(is_potential_assist=True)),
            shooting_fouls=Count('id', filter=Q(is_shooting_foul=True))
        )
        action_stats[action] = stats

    # --- Get individual event locations ---
    shots = list(player_events.filter(event_type='shot').values('shot_loc_x', 'shot_loc_y', 'action_type'))
    passes = list(player_events.filter(event_type='pass').values('pass_start_loc_x', 'pass_start_loc_y', 'pass_end_loc_x', 'pass_end_loc_y', 'action_type'))
    turnovers = list(player_events.filter(event_type='turnover').values('turnover_loc_x', 'turnover_loc_y', 'action_type'))

    # --- Structure the final summary ---
    summary = {
        "player_id": player.id,
        "player_name": player.name,
        "team_name": player.team.name,
        "shots": shots,
        "passes": passes,
        "turnovers": turnovers,
        "stats_by_action": action_stats,
        "totals": total_stats
    }

    return summary

def get_ranks(player_summary_stats: dict):
    """
    Calculates the rank of the player's total stats against all other players.
    """
    # --- Calculate total stats ---
    all_player_stats = models.Player.objects.annotate(
        total_points=Sum('events__points', default=0),
        total_shots=Count('events', filter=Q(events__event_type='shot')),
        total_passes=Count('events', filter=Q(events__event_type='pass')),
        total_turnovers=Count('events', filter=Q(events__event_type='turnover')),
        total_potential_assists=Count('events', filter=Q(events__is_potential_assist=True)),
        total_shooting_fouls=Count('events', filter=Q(events__is_shooting_foul=True))
    ).values('id', 'total_points', 'total_shots', 'total_passes', 'total_turnovers', 'total_potential_assists', 'total_shooting_fouls')

    # --- Use Window functions to rank each stat ---
    ranked_stats = all_player_stats.annotate(
        points_rank=Window(expression=Rank(), order_by=Sum('events__points', default=0).desc()),
        shots_rank=Window(expression=Rank(), order_by=Count('events', filter=Q(events__event_type='shot')).desc()),
        passes_rank=Window(expression=Rank(), order_by=Count('events', filter=Q(events__event_type='pass')).desc()),
        turnovers_rank=Window(expression=Rank(), order_by=Count('events', filter=Q(events__event_type='turnover')).desc()),
        potential_assists_rank=Window(expression=Rank(), order_by=Count('events', filter=Q(events__is_potential_assist=True)).desc()),
        shooting_fouls_rank=Window(expression=Rank(), order_by=Count('events', filter=Q(events__is_shooting_foul=True)).desc()),
    )

    # Find the ranks
    player_id = player_summary_stats["player_id"]
    player_ranks = ranked_stats.get(id=player_id)

    # Format the ranks
    ranks = {
        "points": player_ranks["points_rank"],
        "shots": player_ranks["shots_rank"],
        "passes": player_ranks["passes_rank"],
        "turnovers": player_ranks["turnovers_rank"],
        "potential_assists": player_ranks["potential_assists_rank"],
        "shooting_fouls": player_ranks["shooting_fouls_rank"],
    }
    
    player_summary_stats["ranks"] = ranks
    return player_summary_stats