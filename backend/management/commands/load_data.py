import json
from django.core.management.base import BaseCommand
from app.dbmodels.models import Team, Game, Player, Event
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Loads data from raw_data JSON files into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting data loading process...'))

        # Construct paths to the data files
        base_dir = os.path.join(settings.BASE_DIR, 'raw_data')
        teams_file = os.path.join(base_dir, 'teams.json')
        games_file = os.path.join(base_dir, 'games.json')
        players_file = os.path.join(base_dir, 'players.json')

        # Load Teams
        self.stdout.write('Loading teams...')
        with open(teams_file, 'r') as f:
            teams_data = json.load(f)
            for team_data in teams_data:
                Team.objects.update_or_create(
                    id=team_data['team_id'],
                    defaults={'name': team_data['name']}
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(teams_data)} teams.'))

        # Load Games
        self.stdout.write('Loading games...')
        with open(games_file, 'r') as f:
            games_data = json.load(f)
            for game_data in games_data:
                Game.objects.update_or_create(
                    id=game_data['id'],
                    defaults={'date': game_data['date']}
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(games_data)} games.'))

        # Load Players and Events
        self.stdout.write('Loading players and their events...')
        with open(players_file, 'r') as f:
            players_data = json.load(f)
            for player_data in players_data:
                team_obj = Team.objects.get(id=player_data['team_id'])

                # Create or update the player
                player_obj, created = Player.objects.update_or_create(
                    id=player_data['player_id'],
                    defaults={
                        'name': player_data['name'],
                        'team': team_obj
                    }
                )

                # Load shots as events
                for shot in player_data.get('shots', []):
                    game_obj = Game.objects.get(id=shot['game_id'])
                    Event.objects.update_or_create(
                        player=player_obj,
                        game=game_obj,
                        event_type='shot',
                        action_type=shot['action_type'],
                        id=shot.get('id'),
                        defaults={
                            'points': shot['points'],
                            'is_shooting_foul': shot['shooting_foul_drawn'],
                            'shot_loc_x': shot['shot_loc_x'],
                            'shot_loc_y': shot['shot_loc_y'],
                        }
                    )

                # Load passes as events
                for pass_event in player_data.get('passes', []):
                    game_obj = Game.objects.get(id=pass_event['game_id'])
                    Event.objects.update_or_create(
                        player=player_obj,
                        game=game_obj,
                        event_type='pass',
                        action_type=pass_event['action_type'],
                        id=pass_event.get('id'),
                        defaults={
                            'is_pass_completed': pass_event['completed_pass'],
                            'is_potential_assist': pass_event['potential_assist'],
                            'pass_start_loc_x': pass_event['ball_start_loc_x'],
                            'pass_start_loc_y': pass_event['ball_start_loc_y'],
                            'pass_end_loc_x': pass_event['ball_end_loc_x'],
                            'pass_end_loc_y': pass_event['ball_end_loc_y'],
                        }
                    )
                
                # Load turnovers as events
                for turnover in player_data.get('turnovers', []):
                    game_obj = Game.objects.get(id=turnover['game_id'])
                    Event.objects.update_or_create(
                        player=player_obj,
                        game=game_obj,
                        event_type='turnover',
                        action_type=turnover['action_type'],
                        id=turnover.get('id'),
                        defaults={
                            'turnover_loc_x': turnover['tov_loc_x'],
                            'turnover_loc_y': turnover['tov_loc_y'],
                        }
                    )

        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(players_data)} players and their associated events.'))
        self.stdout.write(self.style.SUCCESS('Data loading complete!'))