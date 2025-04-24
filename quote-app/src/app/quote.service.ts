import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Quote {
  quote: string;
  author: string;
  category?: string;
}

@Injectable({
  providedIn: 'root'
})
export class QuoteService {
  private apiUrl = 'http://127.0.0.1:5000'; // Flask backend URL
  
  constructor(private http: HttpClient) {}

  // Get a random quote from a specific category
  getQuoteByCategory(category: string): Observable<{ quote: Quote }> {
    return this.http.get<{ quote: Quote }>(`${this.apiUrl}/quote/${category}`);
  }

  // Get a random quote from all categories
  getRandomQuoteFromAllCategories(): Observable<{ quote: Quote }> {
    return this.http.get<{ quote: Quote }>(`${this.apiUrl}/quote/all`);
  }

  // Get all quotes from all categories
  getAllQuotes(): Observable<Quote[]> {
    return this.http.get<Quote[]>(`${this.apiUrl}/quotes`);
  }

  // Subscribe to daily quotes
  subscribe(email: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/subscribe`, { email });
  }

  // Unsubscribe from daily quotes
  unsubscribe(email: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/unsubscribe`, { email });
  }
}
