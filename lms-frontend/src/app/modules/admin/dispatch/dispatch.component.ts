import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-dispatch', templateUrl: './dispatch.component.html' })
export class DispatchComponent implements OnInit {
  dispatches: any[] = [];
  parcels: any[] = [];
  agents: any[] = [];
  hubs: any[] = [];
  routes: any[] = [];
  loading = true;
  showModal = false;
  editMode = false;
  success = '';
  error = '';
  form: any = { parcel_id: '', agent_id: '', hub_id: '', route_id: '', dispatch_date: '', expected_delivery: '', notes: '' };

  constructor(private api: ApiService) {}

  ngOnInit() { this.load(); }

  load() {
    this.loading = true;
    this.api.getDispatches().subscribe((data: any) => { this.dispatches = data; this.loading = false; });
    this.api.getParcels().subscribe((data: any) => this.parcels = data);
    this.api.getUsers('agent').subscribe((data: any) => this.agents = data);
    this.api.getHubs().subscribe((data: any) => this.hubs = data);
    this.api.getRoutes().subscribe((data: any) => this.routes = data);
  }

  openCreate() { this.form = { parcel_id: '', agent_id: '', hub_id: '', route_id: '', dispatch_date: '', expected_delivery: '', notes: '' }; this.editMode = false; this.showModal = true; this.error = ''; }

  openEdit(d: any) { this.form = { ...d }; this.editMode = true; this.showModal = true; this.error = ''; }

  save() {
    if (!this.form.parcel_id || !this.form.agent_id || !this.form.hub_id || !this.form.route_id || !this.form.dispatch_date || !this.form.expected_delivery) {
      this.error = 'Please fill all required fields (Parcel, Agent, Hub, Route, and both Dates).';
      return;
    }

    const obs = this.editMode ? this.api.updateDispatch(this.form.id, this.form) : this.api.createDispatch(this.form);
    obs.subscribe(() => { 
      this.success = 'Dispatch saved!'; 
      this.load(); 
      this.showModal = false; 
      setTimeout(() => this.success = '', 3000); 
    }, err => {
      let msg = 'Error saving dispatch';
      if (err.error?.detail) {
        if (Array.isArray(err.error.detail)) {
          msg = err.error.detail.map((e: any) => `${e.loc?.slice(-1)[0]}: ${e.msg}`).join(', ');
        } else {
          msg = err.error.detail;
        }
      }
      this.error = msg;
    });
  }

  delete(id: string) {
    if (confirm('Delete this dispatch?')) {
      this.api.deleteDispatch(id).subscribe(() => { this.success = 'Deleted!'; this.load(); setTimeout(() => this.success = '', 3000); });
    }
  }
}
