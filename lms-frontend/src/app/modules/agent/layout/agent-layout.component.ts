import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { AuthService } from '../../../services/auth.service';
import { ApiService } from '../../../services/api.service';
import { filter } from 'rxjs/operators';

@Component({ selector: 'app-agent-layout', templateUrl: './agent-layout.component.html' })
export class AgentLayoutComponent implements OnInit {
  user: any;
  currentRoute = '';
  unreadCount = 0;

  navItems = [
    { label: 'Dashboard', icon: '📊', route: '/agent/dashboard' },
    { label: 'My Parcels', icon: '📦', route: '/agent/my-parcels' },
    { label: 'Tracking', icon: '📍', route: '/agent/tracking' },
    { label: 'Profile', icon: '👤', route: '/agent/profile' },
    { label: 'Settings', icon: '⚙️', route: '/agent/settings' },
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
