import { Component, OnInit } from '@angular/core';
import {FormControl, FormGroup} from '@angular/forms';
import {AppHttpService} from '../utils/services/app-http-service.service';
import {ApiPaths} from '../utils/helpers/api.paths';
import {ProgressState} from '../utils/Enums/progress-state.enum';
import {InstaVision, ResponseObj} from '../app.models';
import {MatTableDataSource} from '@angular/material';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  public formData: FormGroup;
  ProgressState =  ProgressState;
  public instaVisionTableData: InstaVision[] = null;
  public displayColumns = ['pos', 'page_url', 'max_posts', 'comments_file_name', 'images_file_name'];
  protected tableSource: MatTableDataSource<InstaVision>;
  constructor(public httpService: AppHttpService) {}

  ngOnInit() {
    this.getExistingData();
    this.formData = new FormGroup({
      page_url : new FormControl(''),
      max_posts : new FormControl(0),
      images_file : new FormControl(''),
      comments_file : new FormControl('')
    });
  }

  onSubmitInstaVisionCrawler(data) {
    this.httpService.get(ApiPaths.getInstaVisionData, data).subscribe((response: ResponseObj) => {
     if (response.success) {
        this.instaVisionTableData = response.data as InstaVision[];
      }
    });
  }

  callback() {
    console.log('call back true');
  }

  getExistingData() {
    if (this.httpService.getToken().length !== 0) {
      this.httpService.get(ApiPaths.getAllData).subscribe( (response: ResponseObj) => {
        if (response.success) {
          this.instaVisionTableData = response.data as InstaVision[];
        }
      }, err => {
        alert(err);
      });
    }
  }
}
