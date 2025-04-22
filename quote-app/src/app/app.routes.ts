// app.routes.ts
import { Routes } from '@angular/router';
import { QuoteListComponent } from './quote-list/quote-list.component';
import { RandomQuoteComponent } from './random-quote/random-quote.component';
import { HomeComponent } from './home/home.component';
import { SearchComponent } from './search/search.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'quotes', component: QuoteListComponent },
  { path: 'random-quote', component: RandomQuoteComponent },
  { path: 'search', component: SearchComponent },
  { path: '**', redirectTo: '' },
];
