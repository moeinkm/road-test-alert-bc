export interface TestCenter {
  id: number;
  name: string;
  city: string;
  address: string;
}

export interface City {
  name: string;
  centers: TestCenter[];
}