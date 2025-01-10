import { ApiClient } from '../api/client';
import { API_ENDPOINTS } from '../api/endpoints';
import type { TestCenter } from '../../types/center';

export class CentersService {
  constructor(private readonly api: ApiClient) {}

  async getCenters(): Promise<TestCenter[]> {
    return this.api.get<TestCenter[]>(API_ENDPOINTS.centers.list);
  }
}