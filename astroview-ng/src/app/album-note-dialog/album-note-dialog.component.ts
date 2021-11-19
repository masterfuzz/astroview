import { Component, Inject, OnInit } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-album-note-dialog',
  templateUrl: './album-note-dialog.component.html',
  styleUrls: ['./album-note-dialog.component.css']
})
export class AlbumNoteDialogComponent implements OnInit {

  data: string;

  ngOnInit(): void {
  }

  constructor(
    public dialogRef: MatDialogRef<AlbumNoteDialogComponent>,
    @Inject(MAT_DIALOG_DATA) data: string) {
      this.data = data;
    }

  onNoClick(): void {
    this.dialogRef.close();
  }

}
