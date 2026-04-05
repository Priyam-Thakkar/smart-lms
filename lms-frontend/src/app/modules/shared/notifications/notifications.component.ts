import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-notifications', templateUrl: './notifications.component.html' })
export class NotificationsComponent implements OnInit {
  notifications: any[] = [];
  loading = true;

  constructor(private api: ApiService) {}

  ngOnInit() { this.load(); }

  load() {
    this.loading = true;
    this.api.getNotifications().subscribe((d: any) => { this.notifications = d || []; this.loading = false; });
  }

  markAllRead() {
    this.api.markAllRead().subscribe(() => { this.notifications.forEach(n => n.is_read = true); });
  }

  markRead(n: any) {
    if (!n.is_read) { this.api.markOneRead(n.id).subscribe(() => n.is_read = true); }
  }

  delete(id: string) {
    this.api.deleteNotification(id).subscribe(() => { this.notifications = this.notifications.filter(n => n.id !== id); });
  }

  getIcon(type: string): string {
    return { parcel: '📦', ticket: '🎫', billing: '💳', dispatch: '🚀', system: '🔔' }[type] || '🔔';
  }

  getTimeAgo(dateStr: string): string {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'Just now';
    if (mins < 60) return `${mins}m ago`;
    if (mins < 1440) return `${Math.floor(mins / 60)}h ago`;
    return `${Math.floor(mins / 1440)}d ago`;
  }

  get unreadCount() { return this.notifications.filter(n => !n.is_read).length; }
}
