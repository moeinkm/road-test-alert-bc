import { CentersService } from './centers.service';
import { ApiClient } from '../api/client';

export const centersService = new CentersService(ApiClient.getInstance());