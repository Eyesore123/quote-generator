import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Quote {
    id: number;
    author: string;
    text: string;
}

@Injectable({
    providedIn: 'root'
  })
  export class QuoteService {
    private apiUrl = 'http://localhost:5000/'; // Or whatever your backend URL is
  
    constructor(private http: HttpClient) {}
  
    getAllQuotes(): Observable<Quote[]> {
      return this.http.get<Quote[]>(this.apiUrl);
    }
  
    getRandomQuote(): Observable<Quote> {
      return this.http.get<Quote>(`${this.apiUrl}/random`);
    }
  }