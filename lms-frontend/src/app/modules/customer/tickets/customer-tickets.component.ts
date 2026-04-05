import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-customer-tickets', templateUrl: './customer-tickets.component.html' })
export class CustomerTicketsComponent implements OnInit {
  tickets: any[] = [];
  showForm = false;
  form: any = { parcel_id: '', issue_type: '', description: '', priority: 'Medium' };
  success = '';
  error = '';

  constructor(private api: ApiService) {}

  ngOnInit() { this.load(); }

  load() { this.api.getMyTickets().subscribe((d: any) => this.tickets = d || []); }

  submit() {
    if (!this.form.parcel_id || !this.form.issue_type || !this.form.description) { this.error = 'All fields required'; return; }
    this.api.createTicket(this.form).subscribe(() => {
      this.success = 'Ticket submitted! Our team will contact you soon.';
      this.showForm = false;
      this.form = { parcel_id: '', issue_type: '', description: '', priority: 'Medium' };
      this.load();
      setTimeout(() => this.success = '', 5000);
    }, err => this.error = err.error?.detail || 'Failed to create ticket');
  }

  getPriorityClass(p: string): string { return { High: 'danger', Medium: 'warning', Low: 'blue' }[p] || 'gray'; }
  getStatusClass(s: string): string { return { Open: 'danger', 'In Progress': 'warning', Resolved: 'success' }[s] || 'gray'; }
}
