import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-agent-dashboard', templateUrl: './agent-dashboard.component.html' })
export class AgentDashboardComponent implements OnInit {
  stats: any = {};
  recentParcels: any[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getAgentDashboard().subscribe((data: any) => { this.stats = data; this.loading = false; });
    this.api.getAgentParcels().subscribe((data: any) => { this.recentParcels = (data || []).slice(0, 5); });
  }

  getStatusClass(status: string): string {
    const map: any = { 'Delivered': 'success', 'Created': 'blue', 'In Transit': 'warning', 'Out for Delivery': 'warning', 'Picked Up': 'blue', 'At Hub': 'gray' };
    return map[status] || 'gray';
  }
}
