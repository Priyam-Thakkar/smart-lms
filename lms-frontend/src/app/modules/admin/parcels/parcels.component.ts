import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';
import { PARCEL_STATUSES } from '../../../models/parcel.model';

@Component({ selector: 'app-parcels', templateUrl: './parcels.component.html' })
export class ParcelsComponent implements OnInit {
  parcels: any[] = [];
  filtered: any[] = [];
  agents: any[] = [];
  hubs: any[] = [];
  routes: any[] = [];
  loading = true;
  showModal = false;
  showTrackingModal = false;
  editMode = false;
  selectedParcel: any = null;
  searchTerm = '';
  filterStatus = '';
  statuses = PARCEL_STATUSES;
  success = '';
  error = '';
  form: any = { sender_name: '', sender_phone: '', receiver_name: '', receiver_phone: '', receiver_address: '', weight: 0, parcel_type: 'Standard', description: '', price: 0, payment_status: 'Unpaid', assigned_agent_id: '', route_id: '', hub_id: '' };

  constructor(private api: ApiService) {}

  ngOnInit() { this.load(); }

  load() {
    this.loading = true;
    this.api.getParcels().subscribe((data: any) => { this.parcels = data; this.filtered = data; this.loading = false; });
    // Load agents from users (stub - will use users endpoint)
  }

  search() {
    this.filtered = this.parcels.filter(p =>
      (p.tracking_id?.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
       p.receiver_name?.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
       p.sender_name?.toLowerCase().includes(this.searchTerm.toLowerCase())) &&
      (!this.filterStatus || p.status === this.filterStatus)
    );
  }

  openCreate() { this.form = { sender_name: '', sender_phone: '', receiver_name: '', receiver_phone: '', receiver_address: '', weight: 1, parcel_type: 'Standard', description: '', price: 0, payment_status: 'Unpaid', assigned_agent_id: '', route_id: '', hub_id: '' }; this.editMode = false; this.showModal = true; this.error = ''; }

  openEdit(p: any) { this.form = { ...p }; this.editMode = true; this.showModal = true; this.error = ''; }

  viewTracking(p: any) { this.selectedParcel = p; this.showTrackingModal = true; }

  save() {
    if (this.editMode) {
      this.api.updateParcel(this.form.id, this.form).subscribe(() => { this.success = 'Parcel updated!'; this.load(); this.showModal = false; setTimeout(() => this.success = '', 3000); }, err => this.error = err.error?.detail || 'Error');
    } else {
      this.api.createParcel(this.form).subscribe(() => { this.success = 'Parcel created!'; this.load(); this.showModal = false; setTimeout(() => this.success = '', 3000); }, err => this.error = err.error?.detail || 'Error');
    }
  }

  delete(id: string) {
    if (confirm('Delete this parcel?')) {
      this.api.deleteParcel(id).subscribe(() => { this.success = 'Deleted!'; this.load(); setTimeout(() => this.success = '', 3000); });
    }
  }

  updateStatus(p: any, status: string) {
    this.api.updateParcelStatus(p.id, status).subscribe(() => { this.load(); });
  }

  getStatusClass(status: string): string {
    const map: any = { 'Delivered': 'success', 'Created': 'blue', 'In Transit': 'warning', 'Out for Delivery': 'warning', 'Picked Up': 'blue', 'At Hub': 'gray' };
    return map[status] || 'gray';
  }
}
