import { Component, OnInit } from '@angular/core';
import { NgIf } from '@angular/common';
import { QuoteService } from '../quote.service';

@Component({
  selector: 'app-random-quote',
  standalone: true,
  imports: [NgIf],
  template: `
    <div *ngIf="quote" class="quote-container">
      <blockquote>{{ quote }}</blockquote>
      <p>
        <button (click)="loadQuote()">New Quote</button>
      </p>
    </div>
  `,
  styleUrls: ['./random-quote.component.css']
})
export class RandomQuoteComponent implements OnInit {
  quote: string | undefined;

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
