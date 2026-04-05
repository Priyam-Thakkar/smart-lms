import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ProfileComponent } from './profile/profile.component';
import { NotificationsComponent } from './notifications/notifications.component';
import { SettingsComponent } from './settings/settings.component';

@NgModule({
  declarations: [ProfileComponent, NotificationsComponent, SettingsComponent],
  imports: [CommonModule, FormsModule],
  exports: [ProfileComponent, NotificationsComponent, SettingsComponent]
})
export class SharedModule {}
