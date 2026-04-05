import { Component } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-agent-tracking', template: `
  <div class="page-header"><div><h1>📍 Parcel Tracking</h1><p>Track any assigned parcel</p></div></div>
  <div class="card" style="margin-bottom: 24px;">
    <div style="display: flex; gap: 12px; align-items: flex-end;">
      <div class="form-group" style="flex: 1; margin: 0;"><label>Parcel ID</label><input [(ngModel)]="parcelId" placeholder="Enter parcel ID" /></div>
      <button class="btn btn-primary" (click)="search()">🔍 Search</button>
    </div>
    <div *ngIf="error" class="alert alert-danger" style="margin-top: 12px; margin-bottom: 0;">{{ error }}</div>
  </div>
  <div *ngIf="result" class="card">
    <h3 style="font-size: 14px; font-weight: 700; color: #1B2A4A; margin-bottom: 16px;">📦 {{ result.tracking_id }} — Current: {{ result.status }}</h3>
    <div class="timeline">
      <div *ngFor="let h of result.history?.slice().reverse()" class="timeline-item">
        <div class="timeline-status">{{ h.status }}</div>
        <div class="timeline-time">{{ h.timestamp | date:'dd MMM yyyy, h:mm a' }}</div>
        <div class="timeline-by">by {{ h.updated_by }}</div>
      </div>
    </div>
  </div>
`})
export class AgentTrackingComponent {
  parcelId = '';
  result: any = null;
  error = '';
  constructor(private api: ApiService) {}
  search() {
    if (!this.parcelId) return;
    this.api.getAgentTracking(this.parcelId).subscribe((d: any) => { this.result = d; this.error = ''; }, () => this.error = 'Parcel not found');
  }
}
