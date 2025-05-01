import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  imports: [FormsModule, CommonModule]
})
export class HomeComponent {

  timeZone: string = Intl.DateTimeFormat().resolvedOptions().timeZone;

  email: string = '';
  frequency: string = 'daily';
  sendHour: number = 12;
  unsubscribeEmail: string = '';
  statusMessage: { text: string, type: 'success' | 'error' | 'info' } | null = null;
  hours = Array.from({ length: 24 }, (_, i) => i);

  categorySelections = {
    philosophy: false,
    humor: false,
    business: false,
    psychology: false,
    random: false
  };

  constructor(private http: HttpClient) {}

  subscribe() {
    const selectedCategories = Object.entries(this.categorySelections)
      .filter(([_, isSelected]) => isSelected)
      .map(([category]) => category)
      .join(',');

    const body = {
      email: this.email,
      frequency: this.frequency,
      send_hour: this.sendHour,
      time_zone: this.timeZone,
      categories: selectedCategories
    };

    // Url used for testing purposes: http://127.0.0.1:5000/subscribe

    this.http.post<any>('https://quote-app-backend-nk7c.onrender.com/subscribe', body).subscribe({
      next: res => {
        this.statusMessage = { text: res.message, type: 'success' };
        this.resetForm();
      },
      error: err => {
        this.statusMessage = { text: 'Subscription failed. Please try again.', type: 'error' };

      }
    });
  }

  unsubscribe() {
    const body = { email: this.unsubscribeEmail };

    this.http.post<any>('https://quote-app-backend-nk7c.onrender.com/unsubscribe', body).subscribe({
      next: res => {
        this.statusMessage = res.message;
        this.unsubscribeEmail = '';
      },
      error: err => {
        this.statusMessage = { text: 'Unsubscription failed. Please try again.', type: 'error' };
      }
    });
  }

  resetForm() {
    this.email = '';
    this.frequency = 'daily';
    this.sendHour = 12;
    Object.keys(this.categorySelections).forEach(key => {
      this.categorySelections[key as keyof typeof this.categorySelections] = false;
    });
  }
}
