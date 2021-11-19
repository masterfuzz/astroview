import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { AlbumDetail } from '../album-detail';
import { AlbumNoteDialogComponent } from '../album-note-dialog/album-note-dialog.component';
import { AlbumSequenceDialogComponent } from '../album-sequence-dialog/album-sequence-dialog.component';
import { AlbumStats } from '../album-stats';
import { AlbumService } from '../album.service';
import { ImageDetail } from '../image-detail';
import { YesNoDialogComponent } from '../yes-no-dialog/yes-no-dialog.component';

@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrls: ['./album-detail.component.css']
})
export class AlbumDetailComponent implements OnInit {

  constructor(
    private route: ActivatedRoute,
    private albumService: AlbumService,
    public dialogService: MatDialog
  ) { }

  ngOnInit(): void {
    this.getAlbumDetail();
  }

  album = new AlbumDetail();
  stats = new AlbumStats();
  images: ImageDetail[] = [];
  displayedColumns: string[] = ['ordinal', 'thumbnail', 'name', 'iso', 'exposure', 'sequence', 'notes'];

  filter_exposure?: string | number;
  filter_iso?: number;

  getAlbumDetail(): void {
    const unique_name = this.route.snapshot.paramMap.get('unique_name')!;
    this.albumService.getAlbumDetail(unique_name)
      .subscribe(album => this.album = album);
    
    this.albumService.getAlbumStats(unique_name)
      .subscribe(stats => this.stats = stats);

    this.getImages(unique_name);

  }

  getImages(unique_name: string): void {
    this.albumService.getImages(unique_name)
      .subscribe(images => this.images = images.filter(img => 
        ((this.filter_iso ?? img.iso) == img.iso) && ((this.filter_exposure ?? img.exposure) == img.exposure)
      ));

  }

  setFilter(iso?: string, exposure?: string): void {
    if (iso) {
      this.filter_iso = parseInt(iso);
    } else {
      this.filter_iso = undefined;
    }
    this.filter_exposure = exposure;

    this.getImages(this.album.unique_name);
  }

  openAddNoteDialog(): void {
    const dialogRef = this.dialogService.open(AlbumNoteDialogComponent, {
      width: '250px',
      data: ""
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.album.notes.push(result)
    });
  }

  openEditNoteDialog(index: any): void {
    const dialogRef = this.dialogService.open(AlbumNoteDialogComponent, {
      width: '250px',
      data: this.album.notes[index]
    });

    dialogRef.afterClosed().subscribe(result => {
      this.album.notes[index] = result
    });
  }

  openAddSequenceDialog(): void {
    const dialogRef = this.dialogService.open(AlbumSequenceDialogComponent, {
      width: '250px',
      data: ""
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }
  
  openDelSequenceDialog(): void {
    const dialogRef = this.dialogService.open(YesNoDialogComponent, {
      width: '250px',
      data: ""
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
    });
  }


}
