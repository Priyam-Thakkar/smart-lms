import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../../services/api.service';

@Component({ selector: 'app-settings', templateUrl: './settings.component.html' })
export class SettingsComponent implements OnInit {
  settings: any = { notifications_enabled: true, email_alerts: true, language: 'en' };
  success = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.api.getSettings().subscribe((d: any) => { this.settings = d || this.settings; });
  }

  save() {
    this.api.updateSettings(this.settings).subscribe(() => {
      this.success = '✅ Settings saved!';
      setTimeout(() => this.success = '', 3000);
    });
  }
}
