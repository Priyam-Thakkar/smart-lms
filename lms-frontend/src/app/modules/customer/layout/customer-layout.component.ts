import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { ApiService } from '../../../services/api.service';
import { filter } from 'rxjs/operators';

@Component({ selector: 'app-customer-layout', templateUrl: './customer-layout.component.html' })
export class CustomerLayoutComponent implements OnInit {
  user: any;
  currentRoute = '';
  unreadCount = 0;

  navItems = [
    { label: 'Track Parcel', icon: '📍', route: '/customer/tracking' },
    { label: 'Support Tickets', icon: '🎫', route: '/customer/tickets' },
    { label: 'Profile', icon: '👤', route: '/customer/profile' },
    { label: 'Settings', icon: '⚙️', route: '/customer/settings' },
  ];

  constructor(private authService: AuthService, private api: ApiService, private router: Router) {}

  ngOnInit() {
    this.user = this.authService.getUser();
    this.api.getNotifications().subscribe((d: any) => this.unreadCount = (d || []).filter((n: any) => !n.is_read).length);
    this.router.events.pipe(filter(e => e instanceof NavigationEnd)).subscribe((e: any) => this.currentRoute = e.url);
    this.currentRoute = this.router.url;
  }

  isActive(route: string): boolean { return this.currentRoute.includes(route.split('/').pop() || ''); }
  logout() { this.authService.logout(); }
  navigate(route: string) { this.router.navigate([route]); }
}
