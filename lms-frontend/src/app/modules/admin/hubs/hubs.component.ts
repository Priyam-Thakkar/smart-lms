import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-hubs', templateUrl: './hubs.component.html' })
export class HubsComponent implements OnInit {
  hubs: any[] = [];
  loading = true;
  showModal = false;
  editMode = false;
  success = '';
  error = '';
  form: any = { hub_name: '', hub_code: '', city: '', address: '', contact_person: '', phone: '', capacity: 100 };

  constructor(private api: ApiService) {}

  ngOnInit() { this.load(); }

  load() {
    this.loading = true;
    this.api.getHubs().subscribe((data: any) => { this.hubs = data; this.loading = false; });
  }

  openCreate() { this.form = { hub_name: '', hub_code: '', city: '', address: '', contact_person: '', phone: '', capacity: 100 }; this.editMode = false; this.showModal = true; }

  openEdit(h: any) { this.form = { ...h }; this.editMode = true; this.showModal = true; }

  save() {
    const obs = this.editMode ? this.api.updateHub(this.form.id, this.form) : this.api.createHub(this.form);
    obs.subscribe(() => { this.success = this.editMode ? 'Hub updated!' : 'Hub created!'; this.load(); this.showModal = false; setTimeout(() => this.success = '', 3000); }, err => this.error = err.error?.detail || 'Error');
  }

  delete(id: string) {
    if (confirm('Delete this hub?')) {
      this.api.deleteHub(id).subscribe(() => { this.success = 'Hub deleted!'; this.load(); setTimeout(() => this.success = '', 3000); });
    }
  }
}
