import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  // standalone: true,
  imports: [FormsModule, CommonModule]
})
export class HomeComponent {
  email: string = '';
  frequency: string = 'daily';
  sendHour: number = 12;
  categories: string = '';
  unsubscribeEmail: string = '';
  statusMessage: string = '';
  hours = Array.from({ length: 24 }, (_, i) => i);
  
  // Object to track checkbox selections
  categorySelections = {
    philosophy: false,
    humor: false,
    business: false,
    psychology: false,
    random: false
  };

  selectedCategories: string = '';

  constructor(private http: HttpClient) {}

  subscribe() {
    // Convert checkbox selections to comma-separated string
    const selectedCategories = Object.entries(this.categorySelections)
      .filter(([_, isSelected]) => isSelected)
      .map(([category, _]) => category)
      .join(',');
    
    const body = {
      email: this.email,
      frequency: this.frequency,
      send_hour: this.sendHour,
      categories: selectedCategories
    };

    this.http.post('http://127.0.0.1:5000/subscribe', body).subscribe(response => {
      this.statusMessage = 'Subscribed successfully!';
    }, error => {
      this.statusMessage = 'Subscription failed. Please try again.';
    });
  }

  unsubscribe() {
    const body = { email: this.unsubscribeEmail };
    
    this.http.post('http://127.0.0.1:5000/unsubscribe', body).subscribe(response => {
      this.statusMessage = 'Unsubscribed successfully!';
    }, error => {
      this.statusMessage = 'Unsubscription failed. Please try again.';
    });
  }
}
