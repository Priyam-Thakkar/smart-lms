import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})
export class LoginComponent {
  selectedRole: string | null = null;
  hoveredRole = '';
  email = '';
  password = '';
  loading = false;
  error = '';

  roles = [
    {
      key: 'admin',
      label: 'Administrator',
      icon: '👔',
      bg: '#EFF6FF',
      description: 'Manage parcels, hubs, routes, billing and reports'
    },
    {
      key: 'agent',
      label: 'Delivery Agent',
      icon: '🚴',
      bg: '#F0FDF4',
      description: 'View assigned parcels and update delivery status'
    },
    {
      key: 'customer',
      label: 'Customer',
      icon: '👤',
      bg: '#FFF7ED',
      description: 'Track your parcels and raise support tickets'
    }
  ];

  constructor(private authService: AuthService, private router: Router) {
    if (this.authService.isLoggedIn()) {
      this.redirectByRole(this.authService.getRole());
    }
  }

  selectRole(role: any) {
    this.selectedRole = role.key;
    this.email = '';
    this.password = '';
    this.error = '';
  }

  getSelectedRole() {
    return this.roles.find(r => r.key === this.selectedRole);
  }

  login() {
    if (!this.email || !this.password) {
      this.error = 'Please enter your email and password';
      return;
    }
    this.loading = true;
    this.error = '';
    this.authService.login({ email: this.email, password: this.password }).subscribe({
      next: (res) => {
        this.loading = false;
        // Validate returned role matches selected role
        if (res.user.role !== this.selectedRole) {
          this.authService.logout();
          this.error = `This account is not registered as ${this.getSelectedRole()?.label}. Please select the correct role.`;
          return;
        }
        this.redirectByRole(res.user.role);
      },
      error: (err) => {
        this.loading = false;
        this.error = err.error?.detail || 'Invalid email or password';
      }
    });
  }

  redirectByRole(role: string) {
    this.router.navigate([`/${role}/dashboard`]);
  }
}

