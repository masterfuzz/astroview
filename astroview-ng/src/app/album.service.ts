import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { Album } from './album';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AlbumList } from './album-list';
import { AlbumDetail } from './album-detail';

@Injectable({
  providedIn: 'root'
})
export class AlbumService {

  constructor(
    private http: HttpClient
  ) { }

  private albumUrl = "http://localhost:4200/api/albums";
  httpOptions = {
    headers: new HttpHeaders({ 'ContentType': 'application/json' })
  };

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {
      console.error(error);

      // this.log(`${operation} failed: ${error.message}`, "error");

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  getAlbums(): Observable<Album[]> {
    console.log("getAlbums");
    return this.http.get<AlbumList>(this.albumUrl)
      .pipe(
        catchError(this.handleError<AlbumList>('getAlbums', {albums: []})),
        map(a => a.albums)
      );
  }

  getAlbumDetail(unique_name: string): Observable<AlbumDetail> {
    console.log("getAlbumDetail");
    return this.http.get<AlbumDetail>(`${this.albumUrl}/${unique_name}`)
      .pipe(
        catchError(this.handleError<AlbumDetail>('getAlbumDetail', undefined))
      )

  }
}
