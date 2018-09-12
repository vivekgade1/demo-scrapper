import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {AppHttpService} from './utils/services/app-http-service.service';
import {AsyncPipe} from '@angular/common';
import {HomeComponent} from './home/home.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'client';

  constructor( private httpService: AppHttpService) {

  }

  ngOnInit(): void {
    this.httpService.init();
  }
  ngOnDestroy(): void {
    this.httpService.deleteToken();
  }
}
