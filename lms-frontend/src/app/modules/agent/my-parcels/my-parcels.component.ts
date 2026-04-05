import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';
import { AuthService } from '../../../services/auth.service';

@Component({ selector: 'app-my-parcels', templateUrl: './my-parcels.component.html' })
export class MyParcelsComponent implements OnInit {
  parcels: any[] = [];
  loading = true;
  selectedParcel: any = null;
  proofFile: File | null = null;
  success = '';
  error = '';
  uploading = false;
  newStatus = '';
  statuses = ['Picked Up', 'In Transit', 'At Hub', 'Out for Delivery', 'Delivered'];

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit() { this.load(); }

  load() {
    this.loading = true;
    this.api.getAgentParcels().subscribe((data: any) => { this.parcels = data; this.loading = false; });
  }

  openParcel(p: any) { this.selectedParcel = p; this.newStatus = p.status; this.proofFile = null; this.error = ''; }

  updateStatus() {
    this.api.updateAgentStatus(this.selectedParcel.id, this.newStatus).subscribe(() => {
      this.success = `Status updated to: ${this.newStatus}`;
      this.load();
      if (this.newStatus === 'Delivered' && this.proofFile) { this.uploadProof(); } else { this.selectedParcel = null; }
      setTimeout(() => this.success = '', 3000);
    }, err => this.error = err.error?.detail || 'Error updating status');
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (file && file.size <= 5 * 1024 * 1024) { this.proofFile = file; }
    else { this.error = 'File must be JPG/PNG and max 5MB'; }
  }

  uploadProof() {
    if (!this.proofFile) return;
    this.uploading = true;
    const formData = new FormData();
    formData.append('file', this.proofFile);
    this.api.uploadProof(this.selectedParcel.id, formData).subscribe(() => {
      this.uploading = false;
      this.success = 'Proof of delivery uploaded!';
      this.selectedParcel = null;
      this.load();
    }, err => { this.uploading = false; this.error = 'Upload failed'; });
  }

  getStatusClass(status: string): string {
    const map: any = { 'Delivered': 'success', 'Created': 'blue', 'In Transit': 'warning', 'Out for Delivery': 'warning', 'Picked Up': 'blue', 'At Hub': 'gray' };
    return map[status] || 'gray';
  }
}
