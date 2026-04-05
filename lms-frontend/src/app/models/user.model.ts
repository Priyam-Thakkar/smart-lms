export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'agent' | 'customer';
  phone?: string;
  profile_pic?: string;
  created_at?: string;
  settings?: UserSettings;
}

export interface UserSettings {
  theme: string;
  notifications_enabled: boolean;
  email_alerts: boolean;
  language: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}
