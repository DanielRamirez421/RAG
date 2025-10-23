import { Injectable } from "@angular/core";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { Observable, throwError } from "rxjs";
import { catchError } from "rxjs/operators";
import { QueryRequest, QueryResponse } from "../models/chat.models";

@Injectable({
  providedIn: "root",
})
export class RagService {
  private readonly API_BASE_URL = "http://localhost:8000";

  constructor(private http: HttpClient) {}

  queryRAG(request: QueryRequest): Observable<QueryResponse> {
    return this.http
      .post<QueryResponse>(`${this.API_BASE_URL}/query`, request)
      .pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = "An unknown error occurred!";

    if (error.error instanceof ErrorEvent) {
      // Client-side error
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Server-side error
      errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
      if (error.error && error.error.detail) {
        errorMessage += `\nDetails: ${error.error.detail}`;
      }
    }

    console.error("RAG Service Error:", errorMessage);
    return throwError(() => new Error(errorMessage));
  }
}
