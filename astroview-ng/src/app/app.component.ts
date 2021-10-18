import { Component } from '@angular/core';
import { Album } from './album';
import { AlbumService } from './album.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'astroview';

  albums: Album[];

  constructor(
    private albumService: AlbumService
  ) { this.albums = []; }

  ngOnInit() {
    this.getAlbums();
  }


  getAlbums(): void {
    this.albumService.getAlbums()
      .subscribe(albums => this.albums = albums);
  }
}
