import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

import { BaseService } from './base.service';

@Injectable({
  providedIn: 'root'
})
export class PlayersService extends BaseService {
  constructor(protected http: HttpClient) {
    super(http);
  }

  getPlayerSummary(playerID: number): Observable<any> {
    // This is the corrected line. It creates a relative URL.
    const endpoint = `/api/v1/playerSummary/${playerID}`;

    return this.get(endpoint).pipe(map(
      (data: Object) => {
        // We also need to return the raw data directly, not a modified object.
        return data;
      },
      error => {
        return error;
      }
    ));
  }
}