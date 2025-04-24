import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';  // Import RouterModule
import { AppComponent } from './app.component';
import { QuoteListComponent } from './quote-list/quote-list.component';
import { RandomQuoteComponent } from './random-quote/random-quote.component';
import { HomeComponent } from './home/home.component';
import { routes } from './app.routes';  // Import the routes configuration
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HomeModule } from './home/home.module';

@NgModule({
  declarations: [
    AppComponent,
    QuoteListComponent,
    RandomQuoteComponent,
    HomeComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    RouterModule.forRoot(routes),
    FormsModule,
    HomeModule
  ],
  // providers: [QuoteService],
  bootstrap: [AppComponent]
})
export class AppModule { }
