import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { SharedModule } from '../shared/shared.module';

import { AdminLayoutComponent } from './layout/admin-layout.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { ParcelsComponent } from './parcels/parcels.component';
import { HubsComponent } from './hubs/hubs.component';
import { RoutesComponent } from './routes/routes.component';
import { DispatchComponent } from './dispatch/dispatch.component';
import { BillingComponent } from './billing/billing.component';
import { TicketsComponent } from './tickets/tickets.component';
import { ReportsComponent } from './reports/reports.component';
import { TrackingComponent } from './tracking/tracking.component';
import { ProfileComponent } from '../shared/profile/profile.component';
import { NotificationsComponent } from '../shared/notifications/notifications.component';
import { SettingsComponent } from '../shared/settings/settings.component';

const routes: Routes = [
  {
    path: '', component: AdminLayoutComponent,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: DashboardComponent },
      { path: 'parcels', component: ParcelsComponent },
      { path: 'hubs', component: HubsComponent },
      { path: 'routes', component: RoutesComponent },
      { path: 'dispatch', component: DispatchComponent },
      { path: 'billing', component: BillingComponent },
      { path: 'tickets', component: TicketsComponent },
      { path: 'reports', component: ReportsComponent },
      { path: 'tracking', component: TrackingComponent },
      { path: 'profile', component: ProfileComponent },
      { path: 'notifications', component: NotificationsComponent },
      { path: 'settings', component: SettingsComponent }
    ]
  }
];

@NgModule({
  declarations: [
    AdminLayoutComponent,
    DashboardComponent,
    ParcelsComponent,
    HubsComponent,
    RoutesComponent,
    DispatchComponent,
    BillingComponent,
    TicketsComponent,
    ReportsComponent,
    TrackingComponent
  ],
  imports: [CommonModule, FormsModule, RouterModule.forChild(routes)]
})
export class AdminModule {}
