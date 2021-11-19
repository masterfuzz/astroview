import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlbumNoteDialogComponent } from './album-note-dialog.component';

describe('AlbumNoteDialogComponent', () => {
  let component: AlbumNoteDialogComponent;
  let fixture: ComponentFixture<AlbumNoteDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AlbumNoteDialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AlbumNoteDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
