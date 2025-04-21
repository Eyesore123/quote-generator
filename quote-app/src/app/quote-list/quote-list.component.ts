import { Component, OnInit } from '@angular/core';
import { QuoteService } from '../quote.service';
import { Quote } from '../random-quote/random-quote.component';

@Component({
  selector: 'app-quote-list',
  imports: [],
  templateUrl: './quote-list.component.html',
  styleUrl: './quote-list.component.css',
  standalone: true,
})
export class QuoteListComponent implements OnInit {
  quotes: Quote[] = [];
  currentPage = 1;
  quotesPerPage = 10;

  constructor(private quoteService: QuoteService) {}

  ngOnInit(): void {
    this.quoteService.getAllQuotes().subscribe(data => {
      this.quotes = data;
    });
  }

  get paginatedQuotes(): Quote[] {
    const startIndex = (this.currentPage - 1) * this.quotesPerPage;
    return this.quotes.slice(startIndex, startIndex + this.quotesPerPage);
  }

  nextPage(): void {
    if (this.currentPage * this.quotesPerPage < this.quotes.length) {
      this.currentPage++;
    }
  }

  previousPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }
}
