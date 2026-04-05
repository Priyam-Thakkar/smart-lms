import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-routes', templateUrl: './routes.component.html' })
export class RoutesComponent implements OnInit {
  routes: any[] = [];
  hubs: any[] = [];
  loading = true;
  showModal = false;
  editMode = false;
  success = '';
  error = '';
  form: any = { route_name: '', origin_hub_id: '', destination_hub_id: '', distance_km: 0, estimated_days: 1, waypoint_hubs: [] };

  constructor(private api: ApiService) {}

  ngOnInit() { this.load(); }

  load() {
    this.loading = true;
    this.api.getRoutes().subscribe((data: any) => { this.routes = data; this.loading = false; });
    this.api.getHubs().subscribe((data: any) => this.hubs = data);
  }

  getHubName(id: string): string {
    return this.hubs.find(h => h.id === id)?.hub_name || id;
  }

  openCreate() { this.form = { route_name: '', origin_hub_id: '', destination_hub_id: '', distance_km: 0, estimated_days: 1, waypoint_hubs: [] }; this.editMode = false; this.showModal = true; }

  openEdit(r: any) { this.form = { ...r }; this.editMode = true; this.showModal = true; }

  save() {
    const obs = this.editMode ? this.api.updateRoute(this.form.id, this.form) : this.api.createRoute(this.form);
    obs.subscribe(() => { this.success = 'Route saved!'; this.load(); this.showModal = false; setTimeout(() => this.success = '', 3000); }, err => this.error = err.error?.detail || 'Error');
  }

  delete(id: string) {
    if (confirm('Delete this route?')) {
      this.api.deleteRoute(id).subscribe(() => { this.success = 'Deleted!'; this.load(); setTimeout(() => this.success = '', 3000); });
    }
  }
}
