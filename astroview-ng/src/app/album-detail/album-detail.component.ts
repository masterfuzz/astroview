import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AlbumDetail } from '../album-detail';
import { AlbumService } from '../album.service';

@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrls: ['./album-detail.component.css']
})
export class AlbumDetailComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private albumService: AlbumService
  ) { }

  ngOnInit(): void {
    this.getAlbumDetail();
  }

  album = new AlbumDetail();

  getAlbumDetail(): void {
    const unique_name = this.route.snapshot.paramMap.get('unique_name')!;
    this.albumService.getAlbumDetail(unique_name)
      .subscribe(album => this.album = album);
  }

}
