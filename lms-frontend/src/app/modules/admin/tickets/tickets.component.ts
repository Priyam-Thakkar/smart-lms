import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-tickets', templateUrl: './tickets.component.html' })
export class TicketsComponent implements OnInit {
  tickets: any[] = [];
  loading = true;
  success = '';
  selectedTicket: any = null;
  adminNotes = '';
  newStatus = '';

  constructor(private api: ApiService) {}

  ngOnInit() { this.load(); }

  load() {
    this.loading = true;
    this.api.getAdminTickets().subscribe((data: any) => { this.tickets = data; this.loading = false; });
  }

  openTicket(t: any) {
    this.selectedTicket = t;
    this.adminNotes = t.admin_notes || '';
    this.newStatus = t.status;
  }

  updateTicket() {
    this.api.updateTicket(this.selectedTicket.id, { status: this.newStatus, admin_notes: this.adminNotes }).subscribe(() => {
      this.success = 'Ticket updated!';
      this.selectedTicket = null;
      this.load();
      setTimeout(() => this.success = '', 3000);
    });
  }

  getPriorityClass(p: string): string {
    return { High: 'danger', Medium: 'warning', Low: 'blue' }[p] || 'gray';
  }

  getStatusClass(s: string): string {
    return { Open: 'danger', 'In Progress': 'warning', Resolved: 'success' }[s] || 'gray';
  }
}
