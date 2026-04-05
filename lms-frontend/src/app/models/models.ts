export interface Hub {
  id: string;
  hub_name: string;
  hub_code: string;
  city: string;
  address: string;
  contact_person: string;
  phone: string;
  capacity: number;
  created_at?: string;
}

export interface Route {
  id: string;
  route_name: string;
  origin_hub_id: string;
  destination_hub_id: string;
  waypoint_hubs?: string[];
  distance_km: number;
  estimated_days: number;
  created_at?: string;
}

export interface Dispatch {
  id: string;
  parcel_id: string;
  agent_id: string;
  hub_id: string;
  route_id: string;
  dispatch_date?: string;
  expected_delivery?: string;
  status?: string;
  notes?: string;
  created_at?: string;
}

export interface Billing {
  id: string;
  invoice_number: string;
  parcel_id: string;
  customer_name: string;
  customer_email?: string;
  amount: number;
  payment_status: 'Paid' | 'Unpaid';
  generated_at?: string;
  paid_at?: string;
}

export interface Ticket {
  id: string;
  ticket_id: string;
  customer_id: string;
  parcel_id: string;
  issue_type: string;
  description: string;
  priority: 'Low' | 'Medium' | 'High';
  status: 'Open' | 'In Progress' | 'Resolved';
  admin_notes?: string;
  created_at?: string;
  updated_at?: string;
}

export interface Notification {
  id: string;
  user_id: string;
  message: string;
  type: 'parcel' | 'ticket' | 'billing' | 'dispatch' | 'system';
  is_read: boolean;
  created_at?: string;
}
