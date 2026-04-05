import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';
import { AuthService } from '../../../services/auth.service';

@Component({ selector: 'app-profile', templateUrl: './profile.component.html' })
export class ProfileComponent implements OnInit {
  user: any = {};
  form: any = { name: '', phone: '' };
  pwForm: any = { current_password: '', new_password: '', confirm_password: '' };
  success = '';
  error = '';
  pwSuccess = '';
  pwError = '';
  uploading = false;
  strength = 0;

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit() {
    this.api.getProfile().subscribe((u: any) => {
      this.user = u;
      this.form = { name: u.name, phone: u.phone || '' };
    });
  }

  save() {
    this.api.updateProfile(this.form).subscribe((u: any) => {
      this.user = { ...this.user, ...u };
      this.success = '✅ Profile updated!';
      setTimeout(() => this.success = '', 3000);
    }, err => this.error = err.error?.detail || 'Error updating profile');
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    if (!file) return;
    this.uploading = true;
    const formData = new FormData();
    formData.append('file', file);
    this.api.uploadProfilePic(formData).subscribe((res: any) => {
      this.user.profile_pic = res.profile_pic;
      this.uploading = false;
      this.success = '✅ Profile picture updated!';
      setTimeout(() => this.success = '', 3000);
    }, () => { this.uploading = false; this.error = 'Upload failed'; });
  }

  changePassword() {
    const { new_password, confirm_password } = this.pwForm;
    if (new_password !== confirm_password) { this.pwError = 'Passwords do not match'; return; }
    this.api.changePassword(this.pwForm).subscribe(() => {
      this.pwSuccess = '✅ Password changed!';
      this.pwForm = { current_password: '', new_password: '', confirm_password: '' };
      setTimeout(() => this.pwSuccess = '', 3000);
    }, err => this.pwError = err.error?.detail || 'Error changing password');
  }

  onPasswordInput() {
    const pwd = this.pwForm.new_password;
    let s = 0;
    if (pwd.length >= 6) s++;
    if (pwd.length >= 10) s++;
    if (/[A-Z]/.test(pwd)) s++;
    if (/[0-9]/.test(pwd)) s++;
    if (/[^A-Za-z0-9]/.test(pwd)) s++;
    this.strength = s;
  }
}
