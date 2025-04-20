import { Component } from '@angular/core';

@Component({
  selector: 'app-random-quote',
  imports: [],
  templateUrl: './random-quote.component.html',
  styleUrl: './random-quote.component.css'
})
export class RandomQuoteComponent {
  randomQuote: string = 'This is a random quote!!!';
}
