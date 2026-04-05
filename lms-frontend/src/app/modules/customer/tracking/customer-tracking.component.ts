import { Component } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-customer-tracking', templateUrl: './customer-tracking.component.html' })
export class CustomerTrackingComponent {
  trackingId = '';
  parcel: any = null;
  billing: any = null;
  loading = false;
  error = '';

  constructor(private api: ApiService) {}

  track() {
    if (!this.trackingId.trim()) { this.error = 'Please enter a tracking ID'; return; }
    this.loading = true; this.error = '';
    this.parcel = null; this.billing = null;
    this.api.trackParcel(this.trackingId.trim().toUpperCase()).subscribe((p: any) => {
      this.parcel = p;
      this.loading = false;
      // Load billing
      this.api.getCustomerBilling(this.trackingId.trim().toUpperCase()).subscribe((b: any) => this.billing = b, () => {});
    }, err => { this.loading = false; this.error = err.error?.detail || 'Parcel not found'; });
  }

  downloadPDF() {
    if (!this.billing) return;
    this.api.downloadInvoiceCustomer(this.billing.id).subscribe(blob => {
      this.api.downloadBlob(blob, `${this.billing.invoice_number}.pdf`);
    });
  }

  getStatusClass(status: string): string {
    const map: any = { 'Delivered': 'success', 'Created': 'blue', 'In Transit': 'warning', 'Out for Delivery': 'warning', 'Picked Up': 'blue', 'At Hub': 'gray' };
    return map[status] || 'gray';
  }
}
