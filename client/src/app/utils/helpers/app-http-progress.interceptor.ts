import {Injectable} from '@angular/core';
import {HttpEvent, HttpEventType, HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {AppHttpService} from '../services/app-http-service.service';
import {ProgressState} from '../Enums/progress-state.enum';

@Injectable()
export class AppHttpProgressInterceptor implements HttpInterceptor {
  constructor(private httpService: AppHttpService) {}

  intercept(
    req: HttpRequest<any>,
    next: HttpHandler
  ): Observable<HttpEvent<any>> {

    const authReq = req.clone({reportProgress: true});
    // send cloned request with header to the next handler.
    return next.handle(authReq).pipe(
      map(event => this.manageRequestProgress(event)) // return last (completed) message to caller
     );
  }

  private manageRequestProgress(event: HttpEvent<any>) {
    switch (event.type) {
      case HttpEventType.Sent:
        this.httpService.progressBar.mode = ProgressState.QUERY;
        break;
      case HttpEventType.Response:
        this.httpService.progressBar.mode = ProgressState.STOP;
        return event;
      default:
        this.httpService.progressBar.mode = ProgressState.STOP;
        break;
    }
  }
}
