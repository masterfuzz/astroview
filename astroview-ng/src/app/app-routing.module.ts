import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AlbumDetailComponent } from './album-detail/album-detail.component';
import { AlbumComponent } from './album/album.component';

const routes: Routes = [
  { path: '', redirectTo: '/albums', pathMatch: 'full' },
  { path: 'albums', component: AlbumComponent },
  { path: 'albums/:unique_name', component: AlbumDetailComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
