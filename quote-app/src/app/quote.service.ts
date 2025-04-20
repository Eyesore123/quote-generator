import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class QuoteService {
    constructor(private http: HttpClient) {}

    getQuote(): Observable<any> {
        return this.http.get('http://localhost:5000/api/quote');
    }
}