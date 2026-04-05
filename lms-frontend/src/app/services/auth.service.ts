import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap } from 'rxjs';
import { AuthResponse, LoginRequest, User } from '../models/user.model';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/auth';

  constructor(private http: HttpClient, private router: Router) {}

  login(data: LoginRequest): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, data).pipe(
      tap(res => {
        localStorage.setItem('lms_token', res.access_token);
        localStorage.setItem('lms_user', JSON.stringify(res.user));
      })
    );
  }

  register(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register`, data);
  }

  logout(): void {
    localStorage.removeItem('lms_token');
    localStorage.removeItem('lms_user');
    this.router.navigate(['/login']);
  }

  getToken(): string | null {
    return localStorage.getItem('lms_token');
  }

  getUser(): User | null {
    const user = localStorage.getItem('lms_user');
    return user ? JSON.parse(user) : null;
  }

  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  getRole(): string {
    return this.getUser()?.role || '';
  }
}
