export interface StatusHistory {
  status: string;
  timestamp: string;
  updated_by: string;
}

export interface ProofOfDelivery {
  image_url: string;
  uploaded_at: string;
}

export interface Parcel {
  id: string;
  tracking_id: string;
  sender_name: string;
  sender_phone: string;
  receiver_name: string;
  receiver_phone: string;
  receiver_address: string;
  weight: number;
  dimensions?: string;
  parcel_type: string;
  description?: string;
  price: number;
  payment_status: 'Paid' | 'Unpaid';
  status: string;
  assigned_agent_id?: string;
  route_id?: string;
  hub_id?: string;
  proof_of_delivery?: ProofOfDelivery;
  status_history?: StatusHistory[];
  created_at?: string;
  updated_at?: string;
}

export interface ParcelCreate {
  sender_name: string;
  sender_phone: string;
  receiver_name: string;
  receiver_phone: string;
  receiver_address: string;
  weight: number;
  dimensions?: string;
  parcel_type: string;
  description?: string;
  price: number;
  payment_status?: string;
  assigned_agent_id?: string;
  route_id?: string;
  hub_id?: string;
}

export const PARCEL_STATUSES = [
  'Created', 'Picked Up', 'In Transit', 'At Hub', 'Out for Delivery', 'Delivered'
];
