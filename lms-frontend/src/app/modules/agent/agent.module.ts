import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';

import { AgentLayoutComponent } from './layout/agent-layout.component';
import { AgentDashboardComponent } from './dashboard/agent-dashboard.component';
import { MyParcelsComponent } from './my-parcels/my-parcels.component';
import { AgentTrackingComponent } from './tracking/agent-tracking.component';
import { ProfileComponent } from '../shared/profile/profile.component';
import { NotificationsComponent } from '../shared/notifications/notifications.component';
import { SettingsComponent } from '../shared/settings/settings.component';

const routes: Routes = [
  {
    path: '', component: AgentLayoutComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: AgentDashboardComponent },
      { path: 'my-parcels', component: MyParcelsComponent },
      { path: 'tracking', component: AgentTrackingComponent },
      { path: 'profile', component: ProfileComponent },
      { path: 'notifications', component: NotificationsComponent },
      { path: 'settings', component: SettingsComponent }
    ]
  }
];

@NgModule({
  declarations: [AgentLayoutComponent, AgentDashboardComponent, MyParcelsComponent, AgentTrackingComponent],
  imports: [CommonModule, FormsModule, RouterModule.forChild(routes)]
})
export class AgentModule {}
