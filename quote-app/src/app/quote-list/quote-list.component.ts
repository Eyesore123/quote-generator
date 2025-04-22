import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { QuoteService } from '../quote.service';
import { FormsModule } from '@angular/forms';

// Define the Quote interface locally to ensure it's available
export interface Quote {
  quote: string;
  author: string;
  category?: string;
}

@Component({
  selector: 'app-quote-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  // Remove providers if QuoteService is already provided at a higher level
  templateUrl: './quote-list.component.html',
  styleUrls: ['./quote-list.component.css'],
})
export class QuoteListComponent implements OnInit {
  allQuotes: Quote[] = [];
  filteredQuotes: Quote[] = [];
  currentPage = 1;
  quotesPerPage = 5;
  selectedCategory: string = 'all';
  
  constructor(private quoteService: QuoteService) {}
  
  ngOnInit(): void {
    this.quoteService.getAllQuotes().subscribe(data => {
      // Make sure this matches the structure of your API response
      this.allQuotes = data;
      this.filteredQuotes = [...this.allQuotes]; // Initialize filtered quotes
    });
  }
  
  get paginatedQuotes(): Quote[] {
    const start = (this.currentPage - 1) * this.quotesPerPage;
    // Use filteredQuotes instead of allQuotes for pagination
    return this.filteredQuotes.slice(start, start + this.quotesPerPage);
  }
  
  nextPage(): void {
    if (this.currentPage * this.quotesPerPage < this.filteredQuotes.length) {
      this.currentPage++;
    }
  }
  
  prevPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }
  
  applyCategoryFilter(): void {
    if (this.selectedCategory === 'all' || this.selectedCategory === '') {
      this.filteredQuotes = [...this.allQuotes];
    } else {
      this.filteredQuotes = this.allQuotes.filter(
        q => q.category === this.selectedCategory
      );
    }
    this.currentPage = 1; // Reset to first page when filtering
  }
}
