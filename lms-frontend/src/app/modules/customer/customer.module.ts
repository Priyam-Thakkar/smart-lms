import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { CustomerLayoutComponent } from './layout/customer-layout.component';
import { CustomerTrackingComponent } from './tracking/customer-tracking.component';
import { CustomerTicketsComponent } from './tickets/customer-tickets.component';
import { ProfileComponent } from '../shared/profile/profile.component';
import { NotificationsComponent } from '../shared/notifications/notifications.component';
import { SettingsComponent } from '../shared/settings/settings.component';

const routes: Routes = [
  {
    path: '', component: CustomerLayoutComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: CustomerTrackingComponent },
      { path: 'tracking', component: CustomerTrackingComponent },
      { path: 'tickets', component: CustomerTicketsComponent },
      { path: 'profile', component: ProfileComponent },
      { path: 'notifications', component: NotificationsComponent },
      { path: 'settings', component: SettingsComponent }
    ]
  }
];

@NgModule({
  declarations: [CustomerLayoutComponent, CustomerTrackingComponent, CustomerTicketsComponent],
  imports: [CommonModule, FormsModule, RouterModule.forChild(routes)]
})
export class CustomerModule {}
