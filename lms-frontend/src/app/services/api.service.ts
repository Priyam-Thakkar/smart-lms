import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private base = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  // ─── ADMIN ───
  getDashboard() { return this.http.get(`${this.base}/admin/dashboard`); }
  getParcels() { return this.http.get(`${this.base}/admin/parcels`); }
  createParcel(data: any) { return this.http.post(`${this.base}/admin/parcels`, data); }
  getParcel(id: string) { return this.http.get(`${this.base}/admin/parcels/${id}`); }
  updateParcel(id: string, data: any) { return this.http.put(`${this.base}/admin/parcels/${id}`, data); }
  deleteParcel(id: string) { return this.http.delete(`${this.base}/admin/parcels/${id}`); }
  updateParcelStatus(id: string, status: string) { return this.http.put(`${this.base}/admin/parcels/${id}/status`, { status }); }
  assignAgent(id: string, agent_id: string) { return this.http.put(`${this.base}/admin/parcels/${id}/assign`, { agent_id }); }
  getParcelProof(id: string) { return this.http.get(`${this.base}/admin/parcels/${id}/proof`); }

  getHubs() { return this.http.get(`${this.base}/admin/hubs`); }
  createHub(data: any) { return this.http.post(`${this.base}/admin/hubs`, data); }
  updateHub(id: string, data: any) { return this.http.put(`${this.base}/admin/hubs/${id}`, data); }
  deleteHub(id: string) { return this.http.delete(`${this.base}/admin/hubs/${id}`); }

  getRoutes() { return this.http.get(`${this.base}/admin/routes`); }
  createRoute(data: any) { return this.http.post(`${this.base}/admin/routes`, data); }
  updateRoute(id: string, data: any) { return this.http.put(`${this.base}/admin/routes/${id}`, data); }
  deleteRoute(id: string) { return this.http.delete(`${this.base}/admin/routes/${id}`); }

  getDispatches() { return this.http.get(`${this.base}/admin/dispatch`); }
  createDispatch(data: any) { return this.http.post(`${this.base}/admin/dispatch`, data); }
  updateDispatch(id: string, data: any) { return this.http.put(`${this.base}/admin/dispatch/${id}`, data); }
  deleteDispatch(id: string) { return this.http.delete(`${this.base}/admin/dispatch/${id}`); }

  getAllBilling() { return this.http.get(`${this.base}/admin/billing`); }
  markPaid(id: string) { return this.http.put(`${this.base}/admin/billing/${id}/pay`, {}); }
  downloadInvoiceAdmin(id: string): Observable<Blob> {
    return this.http.get(`${this.base}/admin/billing/${id}/download`, { responseType: 'blob' });
  }

  getReportDeliveries() { return this.http.get(`${this.base}/admin/reports/deliveries`); }
  getReportRevenue() { return this.http.get(`${this.base}/admin/reports/revenue`); }
  getReportAgents() { return this.http.get(`${this.base}/admin/reports/agents`); }
  getReportParcels() { return this.http.get(`${this.base}/admin/reports/parcels`); }

  getAdminTickets() { return this.http.get(`${this.base}/admin/tickets`); }
  updateTicket(id: string, data: any) { return this.http.put(`${this.base}/admin/tickets/${id}`, data); }

  // ─── AGENT ───
  getAgentDashboard() { return this.http.get(`${this.base}/agent/dashboard`); }
  getAgentParcels() { return this.http.get(`${this.base}/agent/parcels`); }
  getAgentParcel(id: string) { return this.http.get(`${this.base}/agent/parcels/${id}`); }
  updateAgentStatus(id: string, status: string) { return this.http.put(`${this.base}/agent/parcels/${id}/status`, { status }); }
  uploadProof(id: string, formData: FormData) { return this.http.post(`${this.base}/agent/parcels/${id}/proof`, formData); }
  getAgentTracking(id: string) { return this.http.get(`${this.base}/agent/tracking/${id}`); }

  // ─── CUSTOMER ───
  trackParcel(trackingId: string) { return this.http.get(`${this.base}/customer/track/${trackingId}`); }
  createTicket(data: any) { return this.http.post(`${this.base}/customer/tickets`, data); }
  getMyTickets() { return this.http.get(`${this.base}/customer/tickets`); }
  getCustomerBilling(trackingId: string) { return this.http.get(`${this.base}/customer/billing/${trackingId}`); }
  downloadInvoiceCustomer(id: string): Observable<Blob> {
    return this.http.get(`${this.base}/customer/billing/${id}/download`, { responseType: 'blob' });
  }

  // ─── COMMON ───
  getProfile() { return this.http.get(`${this.base}/common/profile`); }
  updateProfile(data: any) { return this.http.put(`${this.base}/common/profile`, data); }
  changePassword(data: any) { return this.http.put(`${this.base}/common/profile/password`, data); }
  uploadProfilePic(formData: FormData) { return this.http.post(`${this.base}/common/profile/picture`, formData); }

  getNotifications() { return this.http.get(`${this.base}/common/notifications`); }
  markAllRead() { return this.http.put(`${this.base}/common/notifications/read`, {}); }
  markOneRead(id: string) { return this.http.put(`${this.base}/common/notifications/${id}/read`, {}); }
  deleteNotification(id: string) { return this.http.delete(`${this.base}/common/notifications/${id}`); }

  getSettings() { return this.http.get(`${this.base}/common/settings`); }
  updateSettings(data: any) { return this.http.put(`${this.base}/common/settings`, data); }

  // ─── USERS LIST (for dropdowns) ───
  getUsers(role?: string) {
    const url = role ? `${this.base}/admin/users?role=${role}` : `${this.base}/admin/users`;
    return this.http.get(url);
  }

  downloadBlob(blob: Blob, filename: string) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
  }
}
