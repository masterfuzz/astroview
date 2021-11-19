import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlbumSequenceDialogComponent } from './album-sequence-dialog.component';

describe('AlbumSequenceDialogComponent', () => {
  let component: AlbumSequenceDialogComponent;
  let fixture: ComponentFixture<AlbumSequenceDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AlbumSequenceDialogComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AlbumSequenceDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
