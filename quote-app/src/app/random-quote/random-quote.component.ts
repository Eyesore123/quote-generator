import { Component, OnInit } from '@angular/core';
import { NgIf } from '@angular/common';
import { QuoteService } from '../quote.service';
import { FormsModule } from '@angular/forms';
export interface Quote {
  quote: string;
  author: string;
}

@Component({
  selector: 'app-random-quote',
  imports: [NgIf, FormsModule],
  templateUrl: './random-quote.component.html',
  styleUrls: ['./random-quote.component.css']
})

// RandomQuoteComponent class, which includes:
// - A constructor that takes an instance of QuoteService as a parameter.
// - An ngOnInit method that calls the loadQuote method.
// - A loadQuote method that calls the getRandomQuoteFromAllCategories method of the QuoteService.

export class RandomQuoteComponent implements OnInit {
  quote: Quote | undefined;
  category: string = '';

  constructor(private quoteService: QuoteService) {}

  ngOnInit(): void {
    this.loadQuote();
  }
  loadQuote(): void {
    const fetchQuote = this.category === '' || this.category === 'all'
      ? this.quoteService.getRandomQuoteFromAllCategories()
      : this.quoteService.getQuoteByCategory(this.category);
  
    fetchQuote.subscribe(res => {
      const quoteContainer = document.getElementById('quotecontainer');
      if (quoteContainer) {
        quoteContainer.style.animation = 'none';
        void quoteContainer.offsetWidth; // force reflow
        quoteContainer.style.animation = 'fadeIn 0.5s ease-in';
      }
  
      this.quote = res.quote;
    });
  }
  

  applyFilter(): void {
    if (this.category === '' || this.category === 'all') {
      this.loadQuote();
    } else {
      this.quoteService.getQuoteByCategory(this.category).subscribe(res => {
        this.quote = res.quote;
      });
    }
  }
}
