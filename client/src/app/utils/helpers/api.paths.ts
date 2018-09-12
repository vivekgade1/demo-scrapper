import {environment} from '../../../environments/environment';

export class ApiPaths {
  private static API_ROOT = environment.API_ROOT;
  static get getAuthToken(): string { return ApiPaths.API_ROOT + 'getAuthToken'; }
  static get getInstaVisionData(): string { return ApiPaths.API_ROOT + 'getInstaVisionData'; }
  static get getAllData(): string { return ApiPaths.API_ROOT + 'getAllRequests'; }
  static downloadCommentsFile(): string { return ApiPaths.API_ROOT + 'getComments?id='; }
}
