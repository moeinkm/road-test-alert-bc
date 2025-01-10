export interface PackageFeature {
  text: string;
  important?: boolean;
  description?: string;
}

export interface Package {
  id: string;
  name: string;
  subtitle: string;
  price: number;
  discountedPrice: number;
  duration: string;
  description?: string;
  highlight?: string;
  popular?: boolean;
  features: PackageFeature[];
}