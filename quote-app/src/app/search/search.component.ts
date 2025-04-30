import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { debounceTime, distinctUntilChanged, Subject } from 'rxjs';

interface Quote {
  id?: number;  // Made optional since your in-memory quotes might not have IDs
  quote: string;
  author: string;
  category?: string;
}

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  searchQuery: string = '';
  searchType: string = 'all';
  searchResults: Quote[] = [];
  isLoading: boolean = false;
  error: string = '';
  resultsCount: number = 0;
  
  // Store all quotes for client-side filtering, remove when moving to server-side search
  allQuotes: Quote[] = [];
  
  private searchTerms = new Subject<string>();
  
  constructor(private http: HttpClient) {
    // Set up debounced search
    this.searchTerms.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(term => {
      this.performClientSideSearch(term);
    });
  }
  
  ngOnInit(): void {
    // Load all quotes when component initializes
    this.loadAllQuotes();
  }
  
  loadAllQuotes(): void {
    this.isLoading = true;
    
    // Fetch all quotes from the endpoint
    // Note: Your Flask endpoint returns a direct array, not an object with a 'quotes' property
    this.http.get<Quote[]>('https://quote-app-backend-nk7c.onrender.com/quotes')
      .subscribe({
        next: (quotes) => {
          // Store the quotes directly since the response is an array
          this.allQuotes = quotes;
          console.log(`Loaded ${this.allQuotes.length} quotes for client-side search`);
          this.isLoading = false;
        },
        error: (error) => {
          this.error = 'Error connecting to server';
          console.error('Failed to load quotes:', error);
          this.isLoading = false;
        }
      });
  }
  
  onSearchInput(): void {
    this.searchTerms.next(this.searchQuery);
  }
  
  onSearchTypeChange(): void {
    if (this.searchQuery.trim()) {
      this.performClientSideSearch(this.searchQuery);
    }
  }
  
  // Client-side search implementation
  performClientSideSearch(term: string): void {
    if (!term.trim()) {
      this.searchResults = [];
      this.resultsCount = 0;
      return;
    }
    
    this.isLoading = true;
    const query = term.toLowerCase();
    
    // Filter based on search type
    if (this.searchType === 'quote') {
      this.searchResults = this.allQuotes.filter(q => 
        q.quote.toLowerCase().includes(query));
    } else if (this.searchType === 'author') {
      this.searchResults = this.allQuotes.filter(q => 
        q.author.toLowerCase().includes(query));
    } else if (this.searchType === 'category') {
      this.searchResults = this.allQuotes.filter(q => 
        q.category && q.category.toLowerCase().includes(query));
    } else { // 'all'
      this.searchResults = this.allQuotes.filter(q => 
        q.quote.toLowerCase().includes(query) || 
        q.author.toLowerCase().includes(query) || 
        (q.category && q.category.toLowerCase().includes(query)));
    }
    
    this.resultsCount = this.searchResults.length;
    this.isLoading = false;
  }
  
  // Keep this method for when you're ready to switch to server-side search
  performServerSideSearch(term: string): void {
    if (!term.trim()) {
      this.searchResults = [];
      this.resultsCount = 0;
      return;
    }
    
    this.isLoading = true;
    
    this.http.get<{success: boolean, quotes: Quote[], count: number, error?: string}>(
      `https://quote-app-backend-nk7c.onrender.com/api/search?q=${encodeURIComponent(term)}&type=${this.searchType}`
    ).subscribe({
      next: (response) => {
        if (response.success) {
          this.searchResults = response.quotes;
          this.resultsCount = response.count;
          this.error = '';
        } else {
          this.error = response.error || 'An error occurred during search';
          this.searchResults = [];
          this.resultsCount = 0;
        }
        this.isLoading = false;
      },
      error: (error) => {
        this.error = error.message || 'Failed to fetch search results';
        this.isLoading = false;
        this.searchResults = [];
        this.resultsCount = 0;
      }
    });
  }
}

  
  // When switching to PostgreSQL backend:
  // 1. Comment out or remove the performClientSideSearch method
  // 2. Change the onSearchInput and onSearchTypeChange methods to call performServerSideSearch
  // 3. Remove the loadAllQuotes method and the allQuotes array

