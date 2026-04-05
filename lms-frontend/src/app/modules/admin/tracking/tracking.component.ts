import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-tracking', templateUrl: './tracking.component.html' })
export class TrackingComponent implements OnInit {
  trackingId = '';
  parcel: any = null;
  loading = false;
  error = '';
  proofImage: any = null;

  constructor(private api: ApiService) {}

  ngOnInit() {}

  search() {
    if (!this.trackingId) { this.error = 'Enter tracking ID'; return; }
    this.loading = true;
    this.error = '';
    this.parcel = null;
    // Use admin parcels search
    this.api.getParcels().subscribe((parcels: any) => {
      this.parcel = parcels.find((p: any) => p.tracking_id === this.trackingId.toUpperCase());
      if (!this.parcel) this.error = 'Parcel not found';
      this.loading = false;
    });
  }

  updateStatus(status: string) {
    this.api.updateParcelStatus(this.parcel.id, status).subscribe(() => {
      this.parcel.status = status;
    });
  }
}
