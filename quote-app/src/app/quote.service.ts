import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class QuoteService {
  private apiUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {}

  getQuoteByCategory(category: string): Observable<{ quote: string }> {
    return this.http.get<{ quote: string }>(`${this.apiUrl}/quote/${category}`);
  }
}
