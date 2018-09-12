import { Injectable } from '@angular/core';
import {HttpClient, HttpEvent, HttpEventType, HttpHeaders, HttpParams, HttpRequest} from '@angular/common/http';
import {ApiPaths} from '../helpers/api.paths';
import {Observable} from 'rxjs';
import {catchError, last, map, tap} from 'rxjs/operators';
import {ProgressBar} from '../models/common-models';

@Injectable({
  providedIn: 'root'
})
export class AppHttpService {
  progressBar: ProgressBar = new ProgressBar();
  headers =  new HttpHeaders().set('Content-Type', 'application/json');
  constructor(private http: HttpClient) {}

  setProgressBar(option) {
    switch (option) {
      /*case 'firstStage':
        this.progressBar.color = 'primary';
        this.progressBar.mode = 'determine';
        this.progressBar.value = 50;
        this.progressBar.bufferValue = 0;
        break;
      case 'secondStageInit':
        this.progressBar['color'] = 'primary';
        this.progressBar['mode'] = 'buffer';
        this.progressBar['value'] = 75;
        this.progressBar['bufferValue'] = 85;
      break;
      case 'secondStageCompeted':
        this.progressBar['mode'] = 'determine';
        this.progressBar['value'] = 100;
        this.progressBar['bufferValue'] = 0;
        break;
      */
      case 'query':
        this.progressBar.mode = 'query';
        break;
      case 'stop':
        this.progressBar.mode = 'determine';
        break;
    }
  }
  get(url, paramsObj?, callBack?: Function) {
/*    if (this.getToken().length > 0) {
      this.headers = this.headers.set('X-CSRFToken', this.getToken());
    }*/
    return this.http.get(url, { headers: this.headers , params : paramsObj});
  }

  getFile(url, paramsObj?, callBack?: Function) {
    const file_headers = new HttpHeaders().set('Content-Type', 'text/csv');
    return this.http.get(url, { headers: file_headers, params : paramsObj});
  }

/*  getWithProgress(url, paramsObj?) {
    const req = new HttpRequest('GET', url, {
      reportProgress: true,
      params : this.constructParams(paramsObj)
    });
    return this.http.request(req).pipe(
      map(event => this.manageRequestProgress(event)) // return last (completed) message to caller
     );
  }

  private manageRequestProgress(event: HttpEvent<any>) {
    switch (event.type) {
      case HttpEventType.Sent:
        this.setProgressBar('query');
        break;
      case HttpEventType.Response:
        this.setProgressBar('stop');
        return event.body;
    }
  }*/

  post(url, data, callBack?: Function) {
/*    if (this.getToken().length > 0) {
     this.headers = this.headers.set('X-CSRFToken', this.getToken());
    }*/
    return this.http.post(url, data, {headers: this.headers});
  }

  // contruct url params
  constructParams(obj): HttpParams {
    const params: HttpParams = new HttpParams();
    if (obj == null) { return params; }

    for (const key in Object.keys(obj)) {
      params.set(key, obj[key]);
    }
    return params;
  }

  getToken() {
    if (window.sessionStorage.getItem('token') == null) {
      return '';
    } else {
      return window.sessionStorage.getItem('token');
    }

  }

  deleteToken() {
    delete window.sessionStorage['token'];
  }

  setToken(token) {
    window.sessionStorage.setItem('token', token);
  }

  init(): void {
    if (this.getToken().length === 0) {
      this.get(ApiPaths.getAuthToken).subscribe(r => {
        if (r['success']) {
          this.setToken(r['auth_tok']);
          console.log(r);
        }
      });
    }
  }
}
