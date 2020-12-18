/// <reference path="../../globals.d.ts" />
import { Component, OnInit } from '@angular/core';
import { HttpErrorResponse, HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
const Swal = require('sweetalert2')


// CommonJS
@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent{
	  
	title = 'viewGames';
	listaJuegos:any=[];
	socket:any;

	Toast = Swal.mixin({
		toast: true,
		position: 'top-end',
		showConfirmButton: false,
		timer: 3000,
		timerProgressBar: true,
		didOpen: (toast) => {
			toast.addEventListener('mouseenter', Swal.stopTimer)
			toast.addEventListener('mouseleave', Swal.resumeTimer)
		}
	});

	constructor(
		private _http: HttpClient
	) {}

	ngOnInit() {

		this.socket = io.connect("https://young-harbor-56590.herokuapp.com");

		this.socket.on('onNewData', (data) => {
			this.listaJuegos.push(data);
			/*this.Toast.fire({
				icon: 'success',
				title: "Nuevo Juego"
			});*/
		});

		this.socket.on('end', (data) => {
			this.listaJuegos=data;
			this.Toast.fire({
				icon: 'success',
				title: "Empezando Scraping"
			});
			this.socket.emit('startAll');
		});

		this.socket.emit('startAll');
	}

	setCorreo(){

		Swal.fire({
			title: 'Enter your Gmail',
			input: 'text',
			inputAttributes: {
			  autocapitalize: 'off'
			},
			showCancelButton: true,
			confirmButtonText: 'Save',
			showLoaderOnConfirm: true,
			preConfirm: (correo) => {
				this.socket.emit('setMail',correo);
			},
			allowOutsideClick: () => !Swal.isLoading()
		  }).then((result) => {
			if (result.isConfirmed) {
			  Swal.fire({
				title: "Registered Gmail",
			  })
			}
		  })
	}
}