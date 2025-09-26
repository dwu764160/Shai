import { Component, OnInit } from '@angular/core';
import { PlayersService } from '../_services/players.service';
import { UntilDestroy, untilDestroyed } from '@ngneat/until-destroy';
import { PlayerSummary } from './player-summary.model'; // <-- Import our new interface

@UntilDestroy()
@Component({
  selector: 'app-player-summary',
  templateUrl: './player-summary.component.html',
  styleUrls: ['./player-summary.component.scss']
})
export class PlayerSummaryComponent implements OnInit {

  public playerData: PlayerSummary | null = null; // <-- Add property to hold data

  constructor(
    private playersService: PlayersService
  ) { }

  ngOnInit(): void {
    // This currently fetches data for player_id = 0.
    // We can make this dynamic later if needed.
    this.playersService.getPlayerSummary(0).pipe(
      untilDestroyed(this)
    ).subscribe(response => {
      this.playerData = response; // <-- Store the response in our property
      console.log('Player Data Loaded:', this.playerData); // For debugging
    })
  }

}