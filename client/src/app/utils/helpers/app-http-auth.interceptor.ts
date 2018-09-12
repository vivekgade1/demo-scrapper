import {HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Injectable} from '@angular/core';
import {AppHttpService} from '../services/app-http-service.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private auth: AppHttpService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    // Get the auth token from the service.
    const authToken = this.auth.getToken();

    // Clone the request and replace the original headers with
    // cloned headers, updated with the authorization.
    const authReq = req.clone({
      headers: req.headers.set('X-CSRFToken', authToken)
    });

    // send cloned request with header to the next handler.
    return next.handle(authReq);
  }
}
