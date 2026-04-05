import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-dashboard', templateUrl: './dashboard.component.html' })
export class DashboardComponent implements OnInit {
  stats: any = {};
  statusDist: any[] = [];
  recentParcels: any[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getDashboard().subscribe((data: any) => {
      this.stats = data;
      this.statusDist = data.status_distribution || [];
      this.recentParcels = data.recent_parcels || [];
      this.loading = false;
    }, () => this.loading = false);
  }

  getStatusClass(status: string): string {
    const map: any = { 'Delivered': 'success', 'Created': 'blue', 'In Transit': 'warning', 'Out for Delivery': 'warning', 'Picked Up': 'blue', 'At Hub': 'gray' };
    return map[status] || 'gray';
  }
}
