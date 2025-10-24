import { Component, OnInit } from "@angular/core";
import { CommonModule } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { MatToolbarModule } from "@angular/material/toolbar";
import { MatSidenavModule } from "@angular/material/sidenav";
import { MatCardModule } from "@angular/material/card";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { MatButtonModule } from "@angular/material/button";
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
    MatSelectModule,
    MatProgressSpinnerModule,
    MatIconModule,
  ],
  templateUrl: "./app.component.html",
  styleUrls: ["./app.component.scss"],
})
export class AppComponent implements OnInit {
  title = "PLA Chat Assistant";
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
      model: this.parameters.model,
      temperature: this.parameters.temperature,
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

    if (!request.context) {
      delete request.context;
    }

    // Send to RAG service
    this.ragService.queryRAG(request).subscribe({
      next: (response) => {
        this.addMessage({
          content: response.answer,
          isUser: false,
          timestamp: new Date(),
          sources: response.sources,
          model: response.selected_model,
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

  clearContext() {
    this.parameters.context = "";
  }
}
