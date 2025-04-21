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
  private apiUrl = 'http://127.0.0.1:5000';
  
  constructor(private http: HttpClient) {}
  
  getQuoteByCategory(category: string): Observable<{ quote: Quote }> {
    return this.http.get<{ quote: Quote }>(`${this.apiUrl}/quote/${category}`);
  }
  
  getRandomQuoteFromAllCategories(): Observable<{ quote: Quote }> {
    return this.http.get<{ quote: Quote }>(`${this.apiUrl}/quote/all`);
  }
  
  getAllQuotes(): Observable<Quote[]> {
    return this.http.get<Quote[]>(`${this.apiUrl}/quotes`);
  }
}
