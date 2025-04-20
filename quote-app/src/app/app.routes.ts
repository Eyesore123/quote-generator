// app.routes.ts
import { Routes } from '@angular/router';
import { QuoteListComponent } from './quote-list/quote-list.component';
import { RandomQuoteComponent } from './random-quote/random-quote.component';

export const routes: Routes = [
  { path: '', redirectTo: '/quotes', pathMatch: 'full' },
  { path: 'quotes', component: QuoteListComponent },
  { path: 'random-quote', component: RandomQuoteComponent }
];
