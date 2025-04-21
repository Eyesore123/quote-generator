import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { QuoteService } from '../quote.service';
import { Quote } from '../quote.service';

@Component({
  selector: 'app-quote-list',
  standalone: true,
  imports: [CommonModule],
  providers: [QuoteService],
  templateUrl: './quote-list.component.html',
  styleUrls: ['./quote-list.component.css'],
})
export class QuoteListComponent implements OnInit {
  quotes: Quote[] = [];
  currentPage = 1;
  quotesPerPage = 5;

  constructor(private quoteService: QuoteService) {}

  ngOnInit(): void {
    this.quoteService.getAllQuotes().subscribe(data => {
      this.quotes = data;
    });
  }

  get paginatedQuotes(): Quote[] {
    const start = (this.currentPage - 1) * this.quotesPerPage;
    return this.quotes.slice(start, start + this.quotesPerPage);
  }

  nextPage(): void {
    if (this.currentPage * this.quotesPerPage < this.quotes.length) {
      this.currentPage++;
    }
  }

  prevPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }
}
