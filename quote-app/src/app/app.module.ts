// app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';  // Import RouterModule
import { AppComponent } from './app.component';
import { QuoteListComponent } from './quote-list/quote-list.component';
import { RandomQuoteComponent } from './random-quote/random-quote.component';
import { routes } from './app.routes';  // Import the routes configuration
import { CommonModule } from '@angular/common';

@NgModule({
  declarations: [
    AppComponent,
    QuoteListComponent,
    RandomQuoteComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
