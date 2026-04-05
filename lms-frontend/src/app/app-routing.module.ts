import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  {
    path: 'login',
    loadChildren: () => import('./modules/auth/auth.module').then(m => m.AuthModule)
  },
  {
    path: 'admin',
    loadChildren: () => import('./modules/admin/admin.module').then(m => m.AdminModule),
    canActivate: [AuthGuard],
    data: { role: 'admin' }
  },
  {
    path: 'agent',
    loadChildren: () => import('./modules/agent/agent.module').then(m => m.AgentModule),
    canActivate: [AuthGuard],
    data: { role: 'agent' }
  },
  {
    path: 'customer',
    loadChildren: () => import('./modules/customer/customer.module').then(m => m.CustomerModule),
    canActivate: [AuthGuard],
    data: { role: 'customer' }
  },
  { path: '**', redirectTo: '/login' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
