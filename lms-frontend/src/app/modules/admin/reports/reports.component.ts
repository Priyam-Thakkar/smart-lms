import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-reports', templateUrl: './reports.component.html' })
export class ReportsComponent implements OnInit {
  deliveries: any[] = [];
  revenue: any[] = [];
  parcelStats: any = {};
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getReportDeliveries().subscribe((d: any) => this.deliveries = d);
    this.api.getReportRevenue().subscribe((d: any) => this.revenue = d);
    this.api.getReportParcels().subscribe((d: any) => { this.parcelStats = d; this.loading = false; });
  }

  getTotalRevenue(): number {
    return this.revenue.filter(r => r.payment_status === 'Paid').reduce((s, r) => s + r.total, 0);
  }

  getPendingRevenue(): number {
    return this.revenue.filter(r => r.payment_status === 'Unpaid').reduce((s, r) => s + r.total, 0);
  }
}
