import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { ApiService } from '../../../services/api.service';
import { Notification } from '../../../models/models';
import { filter } from 'rxjs/operators';

@Component({
  selector: 'app-admin-layout',
  templateUrl: './admin-layout.component.html'
})
export class AdminLayoutComponent implements OnInit {
  user: any;
  currentRoute = '';
  showNotifPanel = false;
  notifications: Notification[] = [];
  unreadCount = 0;

  navItems = [
    { label: 'Dashboard', icon: '📊', route: '/admin/dashboard' },
    { label: 'Parcels', icon: '📦', route: '/admin/parcels' },
    { label: 'Hubs', icon: '🏭', route: '/admin/hubs' },
    { label: 'Routes', icon: '🗺️', route: '/admin/routes' },
    { label: 'Dispatch', icon: '🚀', route: '/admin/dispatch' },
    { label: 'Tracking', icon: '📍', route: '/admin/tracking' },
    { label: 'Billing', icon: '💳', route: '/admin/billing' },
    { label: 'Reports', icon: '📈', route: '/admin/reports' },
    { label: 'Tickets', icon: '🎫', route: '/admin/tickets' },
  ];

  bottomItems = [
    { label: 'Profile', icon: '👤', route: '/admin/profile' },
    { label: 'Settings', icon: '⚙️', route: '/admin/settings' },
  ];

  constructor(private authService: AuthService, private apiService: ApiService, private router: Router) {}

  ngOnInit() {
    this.user = this.authService.getUser();
    this.loadNotifications();
    this.router.events.pipe(filter(e => e instanceof NavigationEnd)).subscribe((e: any) => {
      this.currentRoute = e.url;
    });
    this.currentRoute = this.router.url;
  }

  loadNotifications() {
    this.apiService.getNotifications().subscribe((data: any) => {
      this.notifications = data || [];
      this.unreadCount = this.notifications.filter(n => !n.is_read).length;
    });
  }

  markAllRead() {
    this.apiService.markAllRead().subscribe(() => {
      this.notifications.forEach(n => n.is_read = true);
      this.unreadCount = 0;
    });
  }

  deleteNotif(id: string) {
    this.apiService.deleteNotification(id).subscribe(() => {
      this.notifications = this.notifications.filter(n => n.id !== id);
      this.unreadCount = this.notifications.filter(n => !n.is_read).length;
    });
  }

  getTimeAgo(dateStr: string): string {
    const diff = Date.now() - new Date(dateStr).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'Just now';
    if (mins < 60) return `${mins}m ago`;
    if (mins < 1440) return `${Math.floor(mins / 60)}h ago`;
    return `${Math.floor(mins / 1440)}d ago`;
  }

  getNotifIcon(type: string): string {
    return { parcel: '📦', ticket: '🎫', billing: '💳', dispatch: '🚀', system: '🔔' }[type] || '🔔';
  }

  logout() {
    this.authService.logout();
  }

  navigate(route: string) {
    this.showNotifPanel = false;
    this.router.navigate([route]);
  }

  isActive(route: string): boolean {
    return this.currentRoute.includes(route.split('/').pop() || '');
  }
}
