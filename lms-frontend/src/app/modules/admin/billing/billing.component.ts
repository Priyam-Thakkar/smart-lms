import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-billing', templateUrl: './billing.component.html' })
export class BillingComponent implements OnInit {
  billings: any[] = [];
  loading = true;
  success = '';
  error = '';

  constructor(private api: ApiService) {}

  ngOnInit() { this.load(); }

  load() {
    this.loading = true;
    this.api.getAllBilling().subscribe((data: any) => { this.billings = data; this.loading = false; });
  }

  markPaid(id: string) {
    this.api.markPaid(id).subscribe(() => { this.success = 'Marked as paid!'; this.load(); setTimeout(() => this.success = '', 3000); });
  }

  downloadPDF(id: string, invoiceNo: string) {
    this.api.downloadInvoiceAdmin(id).subscribe(blob => {
      this.api.downloadBlob(blob, `${invoiceNo}.pdf`);
    });
  }

  getPaymentClass(status: string): string {
    return status === 'Paid' ? 'success' : 'danger';
  }
}
