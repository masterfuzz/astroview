import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { Album } from './album';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AlbumList } from './album-list';
import { AlbumDetail } from './album-detail';
import { ImageDetailList } from './image-detail-list';
import { ImageDetail } from './image-detail';
import { AlbumStats } from './album-stats';

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

  getImages(unique_name: string): Observable<ImageDetail[]> {
    return this.http.get<ImageDetailList>(`${this.albumUrl}/${unique_name}/images`)
      .pipe(
        catchError(this.handleError<ImageDetailList>('getImages', undefined)),
        map(il => il.images)
      );
  }

  getAlbumStats(unique_name: string): Observable<AlbumStats> {
    return this.http.get<AlbumStats>(`${this.albumUrl}/${unique_name}/stats`)
      .pipe(
        catchError(this.handleError<AlbumStats>('getAlbumStats', undefined))
      )
  }
}
