import { Component, OnInit } from '@angular/core';
import { NgIf } from '@angular/common';
import { QuoteService } from '../quote.service';
export interface Quote {
  quote: string;
  author: string;
}

@Component({
  selector: 'app-random-quote',
  standalone: true,
  imports: [NgIf],
  template: `
    <div *ngIf="quote" class="quote-container">
      <blockquote>{{ quote.quote }}</blockquote>
      <p>— {{ quote.author }}</p>
      <p>
        <button (click)="loadQuote()">New Quote</button>
      </p>
    </div>
  `,
  styleUrls: ['./random-quote.component.css']
})
export class RandomQuoteComponent implements OnInit {
  quote: Quote | undefined;

  constructor(private quoteService: QuoteService) {}

  ngOnInit(): void {
    this.loadQuote();
  }

  loadQuote(): void {
    this.quoteService.getQuoteByCategory('random').subscribe(res => {
      this.quote = res.quote;
    });
  }
}
