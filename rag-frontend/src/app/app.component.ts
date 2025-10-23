import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatSidenavModule } from "@angular/material/sidenav";
import { MatCardModule } from "@angular/material/card";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { MatButtonModule } from "@angular/material/button";
import { MatSliderModule } from "@angular/material/slider";
import { MatSelectModule } from "@angular/material/select";
import { MatProgressSpinnerModule } from "@angular/material/progress-spinner";
import { MatIconModule } from "@angular/material/icon";
import { RagService } from "./services/rag.service";
import {
  ChatMessage,
  ChatParameters,
  QueryRequest,
} from "./models/chat.models";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatToolbarModule,
    MatSidenavModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatSliderModule,
    MatSelectModule,
    MatProgressSpinnerModule,
    MatIconModule,
  ],
  template: `
    <div class="chat-container">
      <!-- Header -->
      <mat-toolbar color="primary">
        <span>RAG Chat Assistant</span>
        <span class="spacer"></span>
        <mat-icon>chat</mat-icon>
      </mat-toolbar>

      <div class="main-content">
        <!-- Sidebar with parameters -->
        <div class="sidebar">
          <div class="parameters-section">
            <h3>Configuration</h3>

            <mat-form-field appearance="outline">
              <mat-label>Model</mat-label>
              <mat-select [(value)]="parameters.model">
                <mat-option value="gpt-4o-mini">GPT-4o Mini</mat-option>
                <mat-option value="grok-3">Grok-3</mat-option>
                <mat-option value="DeepSeek-R1">DeepSeek-R1</mat-option>
                <mat-option value="gpt-4o">GPT-4o</mat-option>
              </mat-select>
            </mat-form-field>

            <div>
              <mat-label>Temperature: {{ parameters.temperature }}</mat-label>
              <mat-slider
                min="0"
                max="2"
                step="0.1"
                [(ngModel)]="parameters.temperature"
                discrete
                showTickMarks
              >
              </mat-slider>
            </div>

            <mat-form-field appearance="outline">
              <mat-label>Context</mat-label>
              <textarea
                matInput
                [(ngModel)]="parameters.context"
                rows="4"
                placeholder="Enter additional context for the AI..."
              >
              </textarea>
            </mat-form-field>

            <button mat-raised-button color="accent" (click)="clearChat()">
              <mat-icon>clear</mat-icon>
              Clear Chat
            </button>
          </div>
        </div>

        <!-- Chat area -->
        <div class="chat-area">
          <div class="messages-container" #messagesContainer>
            <div *ngIf="messages.length === 0" class="no-messages">
              <p>
                Welcome! Ask me anything and I'll help you find information
                using RAG.
              </p>
            </div>

            <div
              *ngFor="let message of messages"
              class="message"
              [class.user-message]="message.isUser"
              [class.assistant-message]="!message.isUser"
            >
              <div [innerHTML]="message.content"></div>

              <div
                *ngIf="message.sources && message.sources.length > 0"
                class="sources"
              >
                <strong>Sources:</strong>
                <div *ngFor="let source of message.sources" class="source-item">
                  <strong>{{ source.title }}</strong> (Score:
                  {{ source.score | number : "1.2-2" }})
                  <br />
                  <small>{{ source.content }}</small>
                </div>
              </div>

              <div class="timestamp">
                {{ message.timestamp | date : "short" }}
              </div>
            </div>

            <div *ngIf="isLoading" class="loading message assistant-message">
              <mat-spinner diameter="20"></mat-spinner>
              <span>Thinking...</span>
            </div>
          </div>

          <!-- Input area -->
          <div class="input-area">
            <div style="display: flex; align-items: center;">
              <mat-form-field appearance="outline" style="flex: 1;">
                <mat-label>Type your question...</mat-label>
                <input
                  matInput
                  [(ngModel)]="currentMessage"
                  (keyup.enter)="sendMessage()"
                  [disabled]="isLoading"
                  placeholder="What would you like to know?"
                />
              </mat-form-field>

              <button
                mat-fab
                color="primary"
                class="send-button"
                (click)="sendMessage()"
                [disabled]="!currentMessage.trim() || isLoading"
              >
                <mat-icon>send</mat-icon>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [
    `
      .spacer {
        flex: 1 1 auto;
      }

      .no-messages {
        text-align: center;
        color: #666;
        padding: 40px;
        font-style: italic;
      }

      .timestamp {
        font-size: 0.8em;
        color: #666;
        margin-top: 8px;
      }

      .user-message .timestamp {
        color: #ccc;
      }
    `,
  ],
})
export class AppComponent implements OnInit {
  title = "RAG Chat Assistant";
  messages: ChatMessage[] = [];
  currentMessage = "";
  isLoading = false;

  parameters: ChatParameters = {
    model: "gpt-4o-mini",
    temperature: 0.7,
    context:
      "You are an AI Assistant. Be brief in your answers. Answer ONLY with the facts listed in the retrieved text.",
  };

  constructor(private ragService: RagService) {}

  ngOnInit() {
    // Initialize with a welcome message
    this.addMessage({
      content:
        "Hello! I'm your RAG Assistant. I can help you find information from our knowledge base. What would you like to know?",
      isUser: false,
      timestamp: new Date(),
    });
  }

  sendMessage() {
    if (!this.currentMessage.trim() || this.isLoading) {
      return;
    }

    // Add user message
    this.addMessage({
      content: this.currentMessage,
      isUser: true,
      timestamp: new Date(),
    });

    const userQuestion = this.currentMessage;
    this.currentMessage = "";
    this.isLoading = true;

    // Prepare request
    const request: QueryRequest = {
      userQuestion: userQuestion,
      model: this.parameters.model,
      temperature: this.parameters.temperature,
      context: this.parameters.context,
    };

    // Send to RAG service
    this.ragService.queryRAG(request).subscribe({
      next: (response) => {
        this.addMessage({
          content: response.answer,
          isUser: false,
          timestamp: new Date(),
          sources: response.sources,
        });
        this.isLoading = false;
      },
      error: (error) => {
        console.error("Error:", error);
        this.addMessage({
          content: `Sorry, I encountered an error: ${error.message}. Please make sure the backend server is running on http://localhost:8000`,
          isUser: false,
          timestamp: new Date(),
        });
        this.isLoading = false;
      },
    });
  }

  private addMessage(message: ChatMessage) {
    this.messages.push(message);
    // Auto-scroll to bottom
    setTimeout(() => {
      const container = document.querySelector(".messages-container");
      if (container) {
        container.scrollTop = container.scrollHeight;
      }
    }, 100);
  }

  clearChat() {
    this.messages = [];
    this.ngOnInit(); // Add welcome message again
  }
}
